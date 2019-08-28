 #!/usr/bin/env python3
 
# first call sudo pigpiod
import sys
import time
import struct
import serial
import pigpio
import threading
import csv

import tkinter as tk

def exit_prog():
    sys.exit("User exited program")
    
def read_counts():
    prev = 0
    curr = 0 
    global cps
    while True:
        time.sleep(1.0)
        curr = cb.tally()
        cps.set(curr - prev)
        prev = curr

def read_gps():
    global utc, lat, lon, mtype, filename
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
                    utc.set(gps_message[1])
                    lat.set(gps_message[3])
                    lon.set(gps_message[5])
                    data = [utc, lat, lon, cps]
                    #print(data)
                    writer.writerow(data)


# declare global variables
cps = None
utc = None
lat = None
lon = None
mtype = 'test'
                  
ser = serial.Serial("/dev/ttyS0")  # open serial port
ser.baudrate = 9600
ser.timeout = 1

pi = pigpio.pi()
cb = pi.callback(17)
cb.reset_tally()


filename = time.strftime("%Y%m%d-%H%M%S") + '.csv'

ser.reset_input_buffer()      


# Create the main window
root = tk.Tk()
root.title("Temperature Converter")
root.attributes('-fullscreen', True)

# Variables
cps = tk.DoubleVar()
utc = tk.DoubleVar()
lat = tk.DoubleVar()
lon = tk.DoubleVar()

# Create the main container
frame = tk.Frame(root)

# Lay out the main container, specify that we want it to grow with window size
frame.pack(fill=tk.BOTH, expand=True)

# Allow middle cell of grid to grow when window is resized
#frame.columnconfigure(1, weight=1)
#frame.rowconfigure(1, weight=1)

# Create widgets
label_filen = tk.Label(frame, text='Filename:', font=("Courier", 20))
label_file = tk.Label(frame, text=filename, font=("Courier", 20))

label_timen = tk.Label(frame, text='UTC:', font=("Courier", 20))
label_time = tk.Label(frame, textvariable=utc, font=("Courier", 20))

label_latn = tk.Label(frame, text='Lat:', font=("Courier", 20))
label_lat = tk.Label(frame, textvariable=lat, font=("Courier", 20))

label_lonn = tk.Label(frame, text='Lon:', font=("Courier", 20))
label_lon = tk.Label(frame, textvariable=lon, font=("Courier", 20))

label_cpsn = tk.Label(frame, text='Cps:', font=("Courier", 20))
label_cps = tk.Label(frame, textvariable=cps, font=("Courier", 20))

button_convert = tk.Button(frame, text="Exit",command = exit_prog, font=("Courier", 20))

# Lay out widgets
label_filen.grid(row=0, column=0, padx=5, pady=5)
label_file.grid(row=0, column=1, padx=5, pady=5)

label_timen.grid(row=1, column=0, padx=5, pady=5)
label_time.grid(row=1, column=1, padx=5, pady=5)

label_latn.grid(row=2, column=0, padx=5, pady=5)
label_lat.grid(row=2, column=1, padx=5, pady=5)

label_lonn.grid(row=3, column=0, padx=5, pady=5)
label_lon.grid(row=3, column=1, padx=5, pady=5)

label_cpsn.grid(row=4, column=0, padx=5, pady=5)
label_cps.grid(row=4, column=1, padx=5, pady=5)
button_convert.grid(row=5, column=1, padx=5, pady=5)

thread_cps = threading.Thread(target=read_counts)
thread_cps.start()

thread_gps = threading.Thread(target=read_gps)
thread_gps.start()


# Run forever!
root.mainloop()

