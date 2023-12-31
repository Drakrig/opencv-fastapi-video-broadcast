#Base
from datetime import datetime
import numpy as np
from queue import Queue
# Video processing
import cv2
#Networking
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
import json
import uvicorn

# Functions

# Models 
class Img(BaseModel):
    timestamp: str
    data: str

frame_buffer = Queue()
placeholder = cv2.imread("placeholder.jpg")

width, height= 1280, 720

templates = Jinja2Templates(directory="templates")
 
app = FastAPI()

# FastAPI
@app.get('/')
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws")
async def stream_video(websocket: WebSocket):
    await websocket.accept()
    global frame_buffer
    try:
        await websocket.send_text("Frame")
        if frame_buffer.empty():
            await websocket.send_bytes(placeholder.tobytes())
        else:
            await websocket.send_bytes(frame_buffer.get())
    except WebSocketDisconnect:
        print("Client disconnected")   

@app.post("/video")
async def video_feed(payload: Img):

    if type(payload) is not Img:
        print("Wrong requrst")
        return {"message": "Fail"}

    data = np.array(json.loads(payload.data), dtype='uint8')

    # Do fancy stuff with frame
    # But we only resize it and encode to jpg 

    resized_frame = cv2.resize(data, (width, height), interpolation = cv2.INTER_AREA)

    status, frame = cv2.imencode(".jpg", resized_frame)

    if status:
        frame_buffer.put(frame.tobytes())
       
    else:
        print("Image encoding failed")
    
    return {"message": "OK" if status else "Fail"} 
 
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=80)