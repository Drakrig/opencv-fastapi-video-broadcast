#Base things
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import os
from time import sleep
import struct
from io import BytesIO
# Video processing
import numpy as np
import cv2
# Networking
import socket

def process_video(source, client_socket):
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
            #Taken from https://github.com/codectl/remote-opencv-streaming-live-video/blob/master/client.py
            memfile = BytesIO()
            np.save(memfile, frame)
            memfile.seek(0)
            data = memfile.read()
            client_socket.sendall(struct.pack("L", len(data)) + data)
            
    print("The video source ended")  

print("Start initialization process\nParse arguments")
parser = ArgumentParser(description="Entry point for video sender. Press 's' to stop",
                                 formatter_class=ArgumentDefaultsHelpFormatter)

parser.add_argument("-src","--source", default="", help="Source for video")
parser.add_argument("-sf", "--skip_frames", type=int, default=0, help="How many frames skip in process to increase speed")
parser.add_argument("-dst","--destination", default="", help="Destination IP address with port like address:port")


args = vars(parser.parse_args())

source = args["source"]
skip_frames=args["skip_frames"]
destination, port = args["destination"].split(":")
port = int(port) 

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("Connect to server")
sleep(5)
while True:
    try:
        client_socket.connect((destination, port))
        break
    except:
        print("Server not awaliable")
        sleep(1)
print("Start main working process")
#asyncio.run(process_video(source))
process_video(source, client_socket)

