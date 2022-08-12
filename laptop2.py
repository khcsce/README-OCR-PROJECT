import os
import threading
from multiprocessing import Process, Pipe, Queue
from queue import Empty

import paho.mqtt.client as mqtt
import pyttsx3
import speech_recognition as sr
import time
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
# TechVidvan hand Gesture Recognizer
# import UI.README_UI as ui
import README_UI as ui

# import necessary packages

import cv2
from PIL import Image
import numpy as np
# import mediapipe as mp
# import tensorflow as tf
# from tensorflow.keras.models import load_model

# import functions
import config
import speech_tts.tts1 as speechtts
# import hand_gesture_recognition_code.TechVidvan_hand_gesture_detection as pose
import hand_gesture_recognition_code.app as pose

# import Communications.gesture_control_subscriber as comms

import OCR.OCR as pytest
import pytesseract
process_text_mutex = threading.Lock()
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

client = None


def test_text_recognition(textqueue):
    sampletextfile = []
    # sampletextfile.append(open('speech_tts/testing/sampletext'))
    # sampletextfile.append(open('speech_tts/testing/sampletext1000'))
    # sampletextfile.append(open('speech_tts/testing/sampletext'))
    sampletextfile.append(open('speech_tts/testing/sampletext_short1'))
    sampletextfile.append(open('speech_tts/testing/sampletext_short2'))
    sampletextfile.append(open('speech_tts/testing/sampletext_short3'))
    while (1):
        if len(sampletextfile) > 0:
            textqueue.put(sampletextfile[0].read())
            sampletextfile.pop(0)
            # speechtts.process_text()


def image_test(textqueue):
    config.start = 1
    img = cv2.imread("image1.jpg", cv2.IMREAD_COLOR)
    config.ImagePass = "image1.jpg"
    text = pytesseract.image_to_string(img)
    config.gotImage = 1
    config.sampleText.append(text)
    textqueue.put(text)

# def image_test():
#     img = cv2.imread("image1.jpg", cv2.IMREAD_COLOR)
#     config.ImagePass = "image1.jpg"
#     process_text_mutex.acquire()
#     gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     kernel = np.ones((1, 1), np.uint8)
#     nn = cv2.dilate(gray_image, kernel, iterations=1)
#     kernel = np.ones((1, 1), np.uint8)
#     nn = cv2.erode(gray_image, kernel, iterations=1)
#     nn = cv2.morphologyEx(gray_image, cv2.MORPH_CLOSE, kernel)
#     nn = cv2.medianBlur(gray_image, 3)
#     cv2.imwrite("image1_processed.jpg", nn)
#
#     # save the processed text in 'text' to send with mqtt
#     text = pytesseract.image_to_string(nn)
#     config.gotImage = 1
#     config.sampleText = text
#     process_text_mutex.release()
#     speechtts.process_text()
#     config.gotImage = 0
# 0. define callbacks - functions that run when events happen.
# The callback for when the client receives a CONNACK response from the server.


def on_connect(client, userdata, flags, rc):
    print("Connection returned result: "+str(rc))
    # config.sampleText.append('Connected')
    #config.start = 1
    config.connect = 1
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("ece180d/text", qos=1)

# The callback of the client when it disconnects.


def on_disconnect(client, userdata, rc):
    config.connect = 0
    if rc != 0:
        print('Unexpected Disconnect')
    else:
        print('Expected Disconnect')

# The default message callback.
# (you can create separate callbacks per subscribed topic)


# def on_message(client, userdata, message):
#    print( "message received" )
#    print(str(message.payload))
#    process_text_mutex.acquire()
#    config.sampleText.append(str(message.payload))
#    process_text_mutex.release()
#    speechtts.process_text()

# with image
# def on_message(client, userdata, message):
#     img = cv2.imread("image1.jpg", cv2.IMREAD_COLOR)
#     process_text_mutex.acquire()
#     config.ImagePass = "image1.jpg"
#     # save the processed text in 'text' to send with mqtt
#     text = pytesseract.image_to_string(img)
#     config.gotImage = 1
#     config.sampleText.append(text)
#     process_text_mutex.release()
#     speechtts.process_text()


def on_message(client, userdata, message):
    textqueue = userdata['textqueue']
    f = open('temp/receive.jpg', 'wb')
    f.write(message.payload)
    f.close()
    print('image received')

    img = cv2.imread("temp/receive.jpg", cv2.IMREAD_COLOR)
    img = cv2.rotate(img, cv2.cv2.ROTATE_90_CLOCKWISE)
    cv2.imwrite("temp/receive.jpg", img)

    # New code: preprocessing if receive.jpg is the unpreprocessed image
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("temp/gray.jpg", gray_image)
    # 2 BW
    #thresh, self.bw = cv2.threshold(self.gray_image, 210, 230, cv2.THRESH_BINARY)
    thresh, bw = cv2.threshold(
        gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    cv2.imwrite("temp/bw_image.jpg", bw)

    ##########
    # 3 GRAY-> BLACK and WHITE -> DILATION
    bt = cv2.bitwise_not(bw)
    # increase 2,2 to 3,3 for stronger dilation, 5,5 is too
    kernel = np.ones((1, 1), np.uint8)
    bt = cv2.dilate(bt, kernel, iterations=1)
    bt = cv2.bitwise_not(bt)

    text = pytesseract.image_to_string(bt)

    #text = pytesseract.image_to_string(img)
    # print(text)
    process_text_mutex.acquire()
    config.ImagePass = "temp/receive.jpg"
    #config.sampleText = text
    config.start = 1
    config.sampleText.append(text)
    textqueue.put(text)

    process_text_mutex.release()

# def on_message(client, userdata, message):
#     f = open('receive.jpg', 'wb')
#     f.write(message.payload)
#     f.close()
#     #print('image received')
#     config.sampleText.append('Image Received')
#     img = cv2.imread("receive.jpg", cv2.IMREAD_COLOR)
#     text = pytesseract.image_to_string(img)
#     print(text)
#     process_text_mutex.acquire()
#     config.ImagePass = "receive.jpg"
#     #config.sampleText = text
#     config.start = 1
#     config.sampleText.append(text)

#     process_text_mutex.release()
#     speechtts.process_text()

# def on_message(client, userdata, message):
#     f = open('receive.jpg', 'wb')
#     f.write(message.payload)
#     f.close()
#     #print('image received')
#     config.sampleText.append('Image Received')
#     config.start = 1
#     img = cv2.imread("receive.jpg", cv2.IMREAD_COLOR)
#
#     process_text_mutex.acquire()
#     # Old preprocessing Midterm version
#     '''gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     kernel = np.ones((1, 1), np.uint8)
#     nn = cv2.dilate(gray_image, kernel, iterations=1)
#     kernel = np.ones((1, 1), np.uint8)
#     nn = cv2.erode(gray_image, kernel, iterations=1)
#     nn = cv2.morphologyEx(gray_image, cv2.MORPH_CLOSE, kernel)
#     nn = cv2.medianBlur(gray_image, 3)
#     cv2.imwrite("receive.jpg_processed.jpg", nn)
#     text = pytesseract.image_to_string(nn)'''
#
#     # Post midterm Feb 11, more accuracy
#     gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     thresh, bw = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
#     bt = cv2.bitwise_not(bw)
#     kernel = np.ones((1,1),np.uint8) #increase 2,2 to 3,3 for stronger dilation, 5,5 is too
#     bt = cv2.dilate(bt, kernel, iterations=1)
#     bt = cv2.bitwise_not(bt)
#     cv2.imwrite("receive.jpg_processed.jpg", bt)
#     text = pytesseract.image_to_string(bt)
#
#     process_text_mutex.acquire()
#     config.ImagePass = "receive.jpg"
#     #config.sampleText = text
#     config.start = 1
#     config.sampleText.append(text)
#
#     process_text_mutex.release()
#     speechtts.process_text()


def text_recognition(textqueue):
    # 1. create a client instance.
    client_userdata = {'textqueue': textqueue}
    client = mqtt.Client(userdata=client_userdata)
    # add additional clientoptions (security, certifications, etc.)
    # many default options should be good to start off.
    # add callbacks to client.

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    # 2. connect to a broker using one of the connect*() functions.5

    client.connect_async('test.mosquitto.org')
    # client.connect("mqtt.eclipse.org")

    # 3. call one of the loop*() functions to maintain network traffic flow with the broker.
    client.loop_start()
    # client.loop_forever()

    while True:
        pass

    # use subscribe() to subscribe to a topic and receive messages.

    # use publish() to publish messages to the broker.

    # use disconnect() to disconnect from the broker.
    client.loop_stop()
    client.disconnect()


def ui_image_test(textqueue, audioqueue):
    import config
    t1 = threading.Thread(target=ui.setup, args=(textqueue,))
    t2 = threading.Thread(target=image_test, args=(textqueue,))
    t3 = threading.Thread(target=speechtts.process_text,
                          args=(textqueue, audioqueue))

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()


def posefeed(imagequeue):
    import config
    while (1):
        try:
            config.frame = imagequeue.get()
        except Empty as e:
            pass


def ui_comms_process(textqueue, audioqueue, conn2, speechbutton1, ui_tts_conn):
    import config
    t1 = threading.Thread(target=ui.setup, args=(
        textqueue, conn2, speechbutton1, ui_tts_conn))
    t2 = threading.Thread(target=text_recognition, args=(textqueue,))
    t3 = threading.Thread(target=speechtts.process_text,
                          args=(textqueue, audioqueue))

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()


def main():
    # global config.sampleText

    # pose.setup()

    path = os.getcwd()

    textqueue = Queue()
    commandsqueue = Queue()
    audioqueue = Queue()
    conn1, conn2 = Pipe()
    speechbutton1, speechbutton2 = Pipe()
    ui_tts_conn, tts_ui_conn = Pipe()

    p2 = Process(target=speechtts.speech, args=(commandsqueue, speechbutton2))
    # send commands to tts

    p3 = Process(target=pose.main, args=(commandsqueue, path, conn1))
    # send commands to tts

    p4 = Process(target=speechtts.tts, args=(
        commandsqueue, audioqueue, tts_ui_conn))
    # read from textqueue
    # get sigs from pose and speech

    p7 = Process(target=ui_comms_process, args=(textqueue, audioqueue, conn2, speechbutton1,
                                                commandsqueue))

    p7.start()

    p2.start()
    p3.start()
    p4.start()

    p7.join()
    p2.join()
    p3.join()
    p4.join()


if __name__ == '__main__':
    main()
