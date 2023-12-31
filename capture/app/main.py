#Base things
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import os
from datetime import datetime
from time import sleep
# Video processing
import cv2
# Networking
import json
import requests

def process_video(source):
    print("Conect to source")
    cap = cv2.VideoCapture(source)
    ret, frame = cap.read()
    while ret:
    # Read a frame from the video
        if skip_frames:
            for i in range(skip_frames):
                cap.grab()
        ret, frame = cap.read()
        if ret:
            # Do fancy stuff to frame
            # But we just send
            req = {  "timestamp":datetime.now().isoformat()
                    ,"data":json.dumps(frame.tolist())
                    }
            resp = requests.post(url=url, json=req) 
            print(f'{req["timestamp"]}Recived answer from server: {resp.json()["message"]} on {datetime.now().isoformat()}')
    print("The video source ended")  

print("Start initialization process\nParse arguments")
parser = ArgumentParser(description="Entry point for video sender. Press 's' to stop",
                                 formatter_class=ArgumentDefaultsHelpFormatter)

parser.add_argument("-src","--source", default="", help="Source for video")
parser.add_argument("-sf", "--skip_frames", type=int, default=0, help="How many frames skip in process to increase speed")
parser.add_argument("-dst","--destination", default="", help="Destination IP address with port")

args = vars(parser.parse_args())

source = args["source"]
skip_frames=args["skip_frames"]
destination = args["destination"]

# Initialization 10.10.10.1:80/video
url = f'http://{destination}/video'

print("Connect to server")
sleep(10)
while True:
    try:
        resp = requests.get(url=f"http://{destination}/status")
        break
    except:
        print("Server not awaliable")
        sleep(1)
print("Start main working process")
process_video(source)

