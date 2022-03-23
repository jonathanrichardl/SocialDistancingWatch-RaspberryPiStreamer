import paho.mqtt.client as mqtt
import time
import json

class Mqtt:
    def __init__(self, name : str = "python", address : str = 'localhost', port:int = 1883):
        print('connecting')
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)
        self.handlers = {}
        self.client = mqtt.Client(name)
        self.client.on_connect = on_connect
        self.client.username_pw_set('emqx', 'public')
        self.client.connect(address,port)
        self.client.loop_start()


    def on_connect(self,client, userdata, flags, rc):
        if rc==0:
            print("connected ok")
            return
        print("Error Connecting!")
        return

    def on_disconnect(self):
        print("Disconnected!")

    def publish(self,message : str, topic : str = 'default'):
        result = self.client.publish(topic, message,qos=2)
        status = result[0]
        if status != 0:
             print(f"Failed to send message to topic {topic}")

    def on_message(self,client,userdata, message : mqtt.MQTTMessage):
        self.handlers[message.topic](message.payload.decode())
        

    def subscribe(self,topic : str , handler): 
        self.client.subscribe(topic)
        self.handlers[topic] = handler


    




