import paho.mqtt.client as mqtt
import base64
from plate_detection import detect_license_plate, ocr_license_plate
import cv2

import numpy as np


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        # subscribe to the image topic
        for id in range(2):
            client.subscribe(f"camera/{id}")

    else:
        print("Connection failed")


def on_message(client, userdata, msg):
    if msg.topic.startswith("camera/"):
        id = msg.topic.split("/")[1]

        print("Image received from camera", id, "processing...")
        # decode the image and load it into opencv
        img = base64.b64decode(msg.payload)
        cv2_img = cv2.imdecode(np.frombuffer(img, np.uint8), -1)
        # licence_plate = detect_license_plate(cv2_img)
        licence_plate = ocr_license_plate(cv2_img)

        client.publish(f"camera/{id}/result", licence_plate)
        print(licence_plate)

# create a new MQTT client and connect to the broker
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883)

client.loop_forever()
