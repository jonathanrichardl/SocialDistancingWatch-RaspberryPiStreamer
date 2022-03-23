import os
from mqtt import Mqtt
from firebase_service import Firebase
from io import BytesIO
from sys import path
import json
from time import sleep
import sys
class Camera():
    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = (1280,720)
        
    
    def take_picture(self) -> bytes:
        image_buffer = BytesIO()
        self.camera.capture(image_buffer, 'jpeg')
        image_buffer.seek(0)
        return image_buffer.read()
        

def encode_and_upload_json(messenger : Mqtt, placeholder : dict, image_link : str, channel : str):
    placeholder['link'] = image_link
    messenger.publish(json.dumps(placeholder), channel)

def main():
    photo_name = 0
    with open(f"{path[0]}/config.json") as config_file:
        config = json.loads(config_file.read())
    placeholder = {"class" : config['classroom']}
    mqtt_channel = config['mqtt_channel']
    mqtt_id = config['mqtt_id']
    messenger = Mqtt(mqtt_id, address='broker.emqx.io', port=1883)
    firebase_service = Firebase()
    for img in os.listdir(f"{sys.path[0]}/test"):
        try:
            with open(f'{sys.path[0]}/test/{img}', 'rb') as file:
                img_buffer = file.read()
                file.close()
            url = firebase_service.upload(img_buffer, f"{config['id']}/({photo_name}).jpeg")
            encode_and_upload_json(messenger, placeholder, url, mqtt_channel)
            photo_name = photo_name + 1 if photo_name <= 10 else 0
            sleep(2)
        except KeyboardInterrupt:
            break


if __name__ == '__main__':
    main()