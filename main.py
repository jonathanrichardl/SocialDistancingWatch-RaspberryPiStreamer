from mqtt import Mqtt
from firebase_service import Firebase
from io import BytesIO
from sys import path
import json



class Camera():
    def __init__(self):
        self.camera = Camera()
        self.camera.resolution = (1280,720)
        
    
    def take_picture(self) -> bytes:
        image_buffer = BytesIO()
        self.camera.capture(image_buffer, 'jpeg')
        return image_buffer.read()
        

def encode_and_upload_json(messenger, placeholder, image_link):
    placeholder['link'] = image_link
    messenger.publish(json.dumps(placeholder), "119827")

def main():
    i = 0
    with open(f"{path[0]}/config.json") as config_file:
        config = json.loads(config_file.read())
    placeholder = {"class" : config['classroom']}
    messenger = Mqtt("112234", address='broker.emqx.io', port=1883)
    firebase_service = Firebase()
    camera = Camera()
    while 1:
        try:
            img_buffer = camera.take_picture()
            firebase_service.upload(img_buffer, f"{config['id']}/({i}).jpeg")
            encode_and_upload_json(messenger,placeholder, f"{config['id']}/({i}).jpeg")
            i += 1
            i = max(i,10)
        except KeyboardInterrupt:
            break
    camera.camera.close()

main()