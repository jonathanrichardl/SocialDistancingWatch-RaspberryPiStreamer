from gdrive import Drive
from time import sleep
from picamera import PiCamera
from datetime import datetime as dt
from os import remove
class Camera():
    def __init__(self):
        self.camera = PiCamera()
    
    def take_picture(self) -> str:
        filename = f"/home/pi/Pictures/{dt.now().strftime('%d-%m-%y %H:%M')}.jpg"
        self.camera.capture(filename)
        return filename

def main():
    #silahkan tambah fungsi setup kameranya disini
    drive_service = Drive() 
    drive_service.make_folder()
    cam = Camera()
    while 1:
        filename = cam.take_picture()
        drive_service.upload(filename)
        remove(filename)
        sleep(7) #masukan interval pengambilan foto disini


