import paho.mqtt.client as mqtt
import base64

# open and read the image
with open("cropped_plate.jpg", "rb") as image:
    img_str = base64.b64encode(image.read())

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")

        # encode and publish the image
        client.publish("camera/1", img_str)
    else:
        print("Connection failed")

# create a new MQTT client and connect to the broker
client = mqtt.Client()
client.on_connect = on_connect
client.connect("localhost", 1883)

client.loop_forever()
