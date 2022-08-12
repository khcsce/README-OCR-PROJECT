#!/bin/bash 

# update raspberryPi

sudo apt-get update 

# GPIO control  

sudo apt-get install python3-pigpio
#sudo pigpiod 

# Bluetooth control 

sudo pip install pygatt 

# Wireless MQTT comms 

sudo pip install paho-mqtt 
