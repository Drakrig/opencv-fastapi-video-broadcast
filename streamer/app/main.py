#Base
import numpy as np
from queue import Queue
# Video processing
import cv2
#Networking
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
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

frame_buffer.put(placeholder)
 
app = FastAPI()

# FastAPI
@app.get('/')
def index(request: Request):
    return StreamingResponse(stream_video(), media_type="multipart/x-mixed-replace;boundary=frame")

def stream_video():
    try:
        while frame_buffer:
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                   bytearray(frame_buffer.get()) + b'\r\n')
    except GeneratorExit:
        print("cancelled")



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