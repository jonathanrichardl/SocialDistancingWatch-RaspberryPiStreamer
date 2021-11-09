from gdrive import Drive
from time import sleep
from picamera import PiCamera
from datetime import datetime as dt
from os import remove
class Camera():
    def __init__(self):
        self.camera = PiCamera()
    
    def take_video(self) -> str:
        filename = f"/home/pi/Pictures/{dt.now().strftime('%d-%m-%y %H:%M')}.jpg"
        self.camera.start_recording(filename)
        sleep(60)
        self.camera.stop_recording()
        return filename

def main():
    #silahkan tambah fungsi setup kameranya disini
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
        


