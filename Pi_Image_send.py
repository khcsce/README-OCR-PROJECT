import paho.mqtt.publish as publish
import os

os.system('fswebcam -r 1280x720 --no-banner saved_img.jpg')

f = open("saved_img.jpg", "rb")
filecontent = f.read()
byteArr = bytearray(filecontent)

publish.single("ece180d/text", byteArr, hostname="test.mosquitto.org")
