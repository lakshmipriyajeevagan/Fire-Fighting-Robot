import serial
import time, sys
import datetime
P_BUTTON = 24
SERIAL_PORT = "/dev/ttyS0"  #Raspberry Pi 3
ser = serial.Serial(SERIAL_PORT,baudrate = 9600,timeout = 5)
ser.write("AT + CGMF = 1\r")  #set to text mode
time.sleep(3)
a=0
while True:
    ser.write("AT + CGMF = 1\r")
    time.sleep(3)
    if a == 1:
        state = "Button Released"
    else:
        state = "Button Pressed"
        ser.write ("AT + CGMS = '9889887878'\r")
        time.sleep(3)
        t = str(datetime.datetime.now())
        msg = "FIRE DETECTED at " + t +":--" + state
        print ("Sending SMS with status info: " + msg)
        ser.write(msg + chr(26)) 
        ser.write("\x1A")  #hex digits
        time.sleep(3)
