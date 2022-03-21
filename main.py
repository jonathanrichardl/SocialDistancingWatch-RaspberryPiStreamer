from mqtt import Mqtt
from firebase_service import Firebase
from io import BytesIO
from sys import path
import json
from time import sleep
class Camera():
    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = (1280,720)
        
    
    def take_picture(self) -> bytes:
        image_buffer = BytesIO()
        self.camera.capture(image_buffer, 'jpeg')
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
    camera = Camera()
    while 1:
        try:
            img_buffer = camera.take_picture()
            url = firebase_service.upload(img_buffer, f"{config['id']}/({photo_name}).jpeg")
            encode_and_upload_json(messenger, placeholder, url, mqtt_channel)
            photo_name = photo_name + 1 if photo_name <= 10 else 0
        except KeyboardInterrupt:
            break
    camera.camera.close()

def main_test():
    photo_name = 0
    with open(f'{path[0]}/gambarku.jpg', 'rb') as image:
        img_buffer = image.read()

    with open(f"{path[0]}/config.json") as config_file:
        config = json.loads(config_file.read())
    placeholder = {"class" : config['classroom']}
    mqtt_channel = config['mqtt_channel']
    mqtt_id = config['mqtt_id']
    messenger = Mqtt(mqtt_id, address='broker.emqx.io', port=1883)
    firebase_service = Firebase()
    while 1:
        try:
            url = firebase_service.upload(img_buffer, f"{config['mqtt_id']}/({photo_name}).jpeg")
            encode_and_upload_json(messenger, placeholder, url, mqtt_channel)
            photo_name = photo_name + 1 if photo_name <= 10 else 0
        except KeyboardInterrupt:
            break
    camera.camera.close()

main_test()