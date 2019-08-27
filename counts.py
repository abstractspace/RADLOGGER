# first call sudo pigpiod
import sys
import time
import struct
import serial
import pigpio
import threading
import csv


GPIO=17

cps = 100


ser = serial.Serial("/dev/ttyS0")  # open serial port
ser.baudrate = 9600
ser.timeout = 1

    

pi = pigpio.pi()
cb = pi.callback(17)
cb.reset_tally()

filename = time.strftime("%Y%m%d-%H%M%S")

def read_counts():
    prev = 0
    curr = 0 
    global cps
    while True:
        time.sleep(1.0)
        curr = cb.tally()
        #print(curr-prev)
        cps = curr - prev
        prev = curr
    
thread = threading.Thread(target=read_counts)
thread.start()
mtype = 'test'
ser.reset_input_buffer()

with open(filename, "w") as file:
    writer = csv.writer(file)
    while True:
            
            try:
                gps_message = ser.readline()
                #print(gps_message)
                gps_message = str(gps_message)
                gps_message = gps_message.split(",")
                mtype = gps_message[0].split("$")[1]
            except:
                time.sleep(1)  # wait 1 second before trying again
            
            if mtype == "GPRMC":
                #print(gps_message)
                utc = gps_message[1]
                lat = gps_message[3]
                lon = gps_message[5]
                data = [utc, lat, lon, cps]
                print(data)
                writer.writerow(data)