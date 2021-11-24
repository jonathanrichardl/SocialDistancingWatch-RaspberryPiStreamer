from gdrive import Drive
from time import sleep
import datetime
from mqtt import Mqtt
import json
from picamera import PiCamera
from os import remove
    
<<<<<<< HEAD
def encode_and_upload_json(messenger, placeholder, image_id : str, drive_link):
    placeholder['link'] = image_id
    placeholder['drive_link'] = drive_link
=======
def encode_and_upload_json(messenger, placeholder, image_id : str, image_link : str):
    placeholder['link'] = image_id
    placeholder['drive_link'] = image_link
>>>>>>> 859699a8551eaf3d5a56741085f7e6c03b80d67a
    messenger.publish(json.dumps(placeholder), "119827")
    



class Camera():
    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = (1280,720)
        
    
    def take_picture(self) -> str:
        """
        take picture, save ke raspi, trus return nama filenya dan pathnya (misal 'D:/halo/kemas.jpg')
        """
        file_name = "/home/pi/Pictures/"+ str(datetime.datetime.now().strftime("%H-%M-%S-%f")) + ".png"
        self.camera.capture(file_name)
        return file_name
        


def main():
    placeholder = {"class" : 'XII IPA 2'}
    messenger = Mqtt("112234", address='broker.emqx.io', port=1883)
    drive_service = Drive() 
    drive_service.make_folder()
    camera = Camera()
    while 1:
        try:
            filename = camera.take_picture()
<<<<<<< HEAD
            photo_id,link = drive_service.upload(filename)
            encode_and_upload_json(messenger,placeholder, photo_id,link)
=======
            photo_id, photo_link = drive_service.upload(filename)
            encode_and_upload_json(messenger,placeholder, photo_id, photo_link)
>>>>>>> 859699a8551eaf3d5a56741085f7e6c03b80d67a
            remove(filename)
        except KeyboardInterrupt:
            break
    camera.camera.close()

main()