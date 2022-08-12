# https://pypi.org/project/pygatt/

import pygatt
from binascii import hexlify

import time 
import RPi.GPIO as GPIO
import pigpio

import paho.mqtt.publish as publish 
import os 

adapter = pygatt.GATTToolBackend()

servo = 17 
servo2 = 18

pwm = pigpio.pi()
pwm.set_mode(servo, pigpio.OUTPUT)
pwm.set_PWM_frequency( servo, 50 )

pwm.set_mode(servo2, pigpio.OUTPUT) 
pwm.set_PWM_frequency( servo2, 50 )

def toggle_action(data):
    print(data)
    BYTE = '0x00'
    ba = bytearray([int(BYTE, 16)])
    if(data != ba):
        print("run")
        for x in reversed(range(900, 1900, 10)): 
            pwm.set_servo_pulsewidth( servo, x )
            time.sleep(0.1)
 
        time.sleep(0.5) 
        
        pwm.set_servo_pulsewidth( servo2, 1500 )
        time.sleep(1)
    
        pwm.set_servo_pulsewidth( servo, 1900 )
        time.sleep(1)

        pwm.set_servo_pulsewidth( servo2, 2500 ) 
        time.sleep(1)

        pwm.set_servo_pulsewidth( servo2, 500 ) 
        time.sleep(1)

        os.system('fswebcam -r 1280x720 --no-banner saved_img.jpg')
        #time.sleep(1)
        f = open("saved_img.jpg", "rb")
        filecontent = f.read()
        byteArr = bytearray(filecontent)

        publish.single("ece180d/text", byteArr, hostname="test.mosquitto.org")



def handle_data(handle, value):
        
        print("Received data: %s" % hexlify(value))
        toggle_action(value)


def main():
    #os.system('sudo pigpiod')
    adapter.start()
    while(1):
        try:
            device = adapter.connect('91:2a:70:0e:41:e3')
            device.subscribe("84dfdb6a-8a51-8afd-5425-17c7f94d8199",callback=handle_data)
        except:
            print("Cannnot subscribe")

    time.sleep(0.5)

if __name__=="__main__":
    main()
