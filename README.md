# Broadcasting with OpenCV and FastAPI
## Description

This project is used as basic template for CV project with separate capture and processing microservices.

Now it has descent FPS without post-processing frame (resize, etc.)

## Installing

Just `git clone https://github.com/Drakrig/opencv-fastapi-video-broadcast.git` and then `cd opencv-fastapi-video-broadcast`

## Initial setup

If you want to test it you have to change couple things in docker compose file.

**Optional**

Create network `fastapi` with command `docker network create --subnet=10.10.10.0/24 fastapi`

1. In `streamer` part change `network` to you desired (default or created). May skip if using you did optional step above.
2. In `capture` part change -` "~/Videos/:/mnt/"` to format `"{path/to/folder/with/test/video}:/mnt/"`. Be sure that video named `test.mp4` or change it in `capture/main.py` to your desired.
3. If you skip optional step, in `networks` section change network settings according to yours

## Testing

Simply `docker compose up` or `docker-compose up`. It should work out the box. In console click on `http://0.0.0.0:80` and watch your video. It might take couple seconds to load it.

## Credits

I take code for `streamer.py` and `index.html` from this great guy `https://github.com/codectl/remote-opencv-streaming-live-video/tree/master`. Also take some parts from `server.py` and `streamer.py`

## Licence 

Code and documentation released under the [MIT License](https://github.com/Drakrig/opencv-fastapi-video-broadcast/blob/master/LICENCE)
