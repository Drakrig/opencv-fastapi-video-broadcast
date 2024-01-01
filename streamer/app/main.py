# Video processing
import cv2
#Networking
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse
from streamer import Streamer
import socket
import uvicorn

width, height= 1280, 720

templates = Jinja2Templates(directory="templates")

streamer = Streamer('', 8080)
streamer.start()

app = FastAPI()

# FastAPI
@app.get('/')
def index(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})
    #return StreamingResponse(stream_video(), media_type="multipart/x-mixed-replace;boundary=frame")


def recive_video():
    global streamer
    try:
        while True:
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + streamer.get_jpeg() + b'\r\n\r\n')
    except GeneratorExit:
        print("cancelled")

@app.get("/stream_video")
def stream_video():
    return StreamingResponse(recive_video(), media_type='multipart/x-mixed-replace; boundary=frame')
 
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=80)