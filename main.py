from gdrive import Drive
from time import sleep
import datetime
from mqtt import Mqtt
import json
from picamera import PiCamera
from os import remove

class Messenger():
    def __init__(self, classroom):
        self.messenger = Mqtt("server", address='broker.emqx.io', port=1883)
        self.placeholder = {
            "class" : classroom

        }
    
    def encode_and_upload_json(self, image_id : str):
        self.placeholder['link'] = image_id
        self.messenger.publish(json.dumps(self.placeholder), "59288f20-4e6d-4423-938a-84b9dcfc7be4")
        



class Camera():
    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = (1280,720)
        
    
    def take_picture(self) -> str:
        """
        take picture, save ke raspi, trus return nama filenya dan pathnya (misal 'D:/halo/kemas.jpg')
        """
        file_name = "/home/pi/Tes/"+ str(datetime.datetime.now().strftime("%H-%M-%S-%f")) + ".png"
        self.camera.capture(file_name)
        return file_name
        


def main():
    messenger = Messenger()
    drive_service = Drive() 
    drive_service.make_folder()
    camera = Camera()
    while 1:
        try:
            filename = camera.take_picture() 
            try:
                file_id = drive_service.upload(filename)
                messenger.encode_and_upload_json(file_id)
                remove(filename)
                
                
            except :
                pass
        except KeyboardInterrupt:
            break
    camera.camera.close()

main()
