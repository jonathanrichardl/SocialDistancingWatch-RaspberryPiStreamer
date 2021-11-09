from gdrive import Drive
from time import sleep
from picamera import PiCamera
from datetime import datetime as dt
from os import remove
class Camera():
    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = (1280, 720)
    
    def take_video(self) -> str:
        filename = f"/home/pi/Pictures/{dt.now().strftime('%d-%m-%y %H:%M')}.h264"
        self.camera.start_recording(filename)
        sleep(60)
        self.camera.stop_recording()
        return filename

def main():
    drive_service = Drive() 
    drive_service.make_folder()
    cam = Camera()
    while 1:
        filename = cam.take_video()
        try:
            drive_service.upload(filename)
            remove(filename)
        except:
            pass
        


