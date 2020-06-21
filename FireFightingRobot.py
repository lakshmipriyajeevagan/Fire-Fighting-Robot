import serial
import RPi.GPIO as GPIO
import os, time, sys
import spidev
import datetime
# open serial port S0
SERIAL_PORT = "/dev/ttyS0"  # Raspberry Pi 3
ser = serial.Serial(SERIAL_PORT,baudrate = 9600,timeout = 5)  
ser.write("AT + CMGF = 1\r")  # set to text mode
time.sleep(3)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
#set pins
flame1 = 5
flame2 = 6
flame3 = 13
relay = 20
buzzer = 21
servo = 18
mot1 = 4
mot2 = 17
mot3 = 27
mot4 = 22
# assigning input and output pins
GPIO.setup(flame1,GPIO.IN)
GPIO.setup(flame2,GPIO.IN)
GPIO.setup(flame3,GPIO.IN)
GPIO.setup(relay,GPIO.OUT)
GPIO.setup(buzzer,GPIO.OUT)
GPIO.setup(mot1,GPIO.OUT)
GPIO.setup(mot2,GPIO.OUT)
GPIO.setup(mot3,GPIO.OUT)
GPIO.setup(mot4,GPIO.OUT)
GPIO.setup(servo,GPIO.OUT)
GPIO.output(mot1,0)
GPIO.output(mot2,0)
GPIO.output(mot3,0)
GPIO.output(mot4,0)
spi = spidev.Spidev()
spi.open(0,0)
spi.max_speed_hz = 1000000
# function to read SPI data
def ReadChannel(channel):
    adc = spi.xfer2([1,(8 + channel) << 4,0])  # SPI transaction
    data = ((adc[1] & 3) << 8) + adc[2]  # read back into ADC
    return data
# function to convert the data to voltage level
def ConvertVolts(data,places):
    volts = (data * 3.3) / float(1023)
    volts = round(volts,places)
    return volts
# function to calculate temperature
def ConvertTemp(data,places):
    temp = ((data * 330) / float(1023))
    temp = round(temp,places)
    return temp
temp_channel = 0
delay = 5
ser.write("AT + CMGF = 1\r")
time.sleep(3)
temp_level = ReadChannel(temp_channel)  # passing ch0 to ReadChannel
temp_volts = ConvertVolts(temp_level,2)  # passing data and decimal places to ConvertVolts
temp = ConvertTemp(temp_level,2)  # passing data and decimal places to ConvertTemp
print("Temp: {} deg C", format(temp))
time.sleep(2)
# create PWM instance for servomotor
p = GPIO.PWM(servo,50)
p.start(7.5)
# loop to turn the camera
while True:
    p.ChangeDutyCycle(7.5)  # turn (the camera) towards 90 degrees
    time.sleep(3)
    p.ChangeDutyCycle(2.5)  # turn (the camera) towards 0 degrees
    time.sleep(3)
    p.ChangeDutyCycle(12.5)  # turn (the camera) towards 180 degrees
    time.sleep(3) 
# Check if the flame sensor 1 is activated   
if GPIO.input(flame1) == 1:
    GPIO.output(buzzer,1)  # activate buzzer
    print("FIRE DETECTED - FRONT")                            
    os.system('sudo python/home/pi/gsmffr.py')  # run the GSM program to send an alert SMS
    # run the robot in the forward direction
    GPIO.output(mot1,0)
    GPIO.output(mot2,1)
    GPIO.output(mot3,1)
    GPIO.output(mot4,0)
    time.sleep(2)
    # activate the pump motor
    GPIO.output(relay,1)
    time.sleep(4)
    GPIO.output(mot1,0)
    GPIO.output(mot2,0)
    GPIO.output(mot3,0)
    GPIO.output(mot4,0)
    time.sleep(3)
    GPIO.output(mot1,1)
    GPIO.output(mot2,0)
    GPIO.output(mot3,0)
    GPIO.output(mot4,1)
    time.sleep(3)
    # turn off the buzzer and pump motor if flame suffices
    if GPIO.input(flame1) == 0:
        GPIO.output(buzzer,0)
        GPIO.output(relay,0)
# Check if the flame sensor 2 is activated   
if GPIO.input(flame2) == 1:
    GPIO.output(buzzer,1)  # activate the buzzer
    print("FIRE DETECTED - LEFT")                            
    os.system('sudo python/home/pi/gsmffr.py')  # send an alert SMS
    # move the robot
    GPIO.output(mot1,0)
    GPIO.output(mot2,1)
    GPIO.output(mot3,1)
    GPIO.output(mot4,0)
    time.sleep(2)
    # activate the pump motor
    GPIO.output(relay,1)
    time.sleep(4)
    GPIO.output(mot1,1)
    GPIO.output(mot2,0)
    GPIO.output(mot3,0)
    GPIO.output(mot4,0)
    time.sleep(3)
    GPIO.output(mot1,0)
    GPIO.output(mot2,0)
    GPIO.output(mot3,0)
    GPIO.output(mot4,0)
    time.sleep(3)
    GPIO.output(mot1,1)
    GPIO.output(mot2,0)
    GPIO.output(mot3,0)
    GPIO.output(mot4,1)
    time.sleep(3)
    if GPIO.input(flame2) == 0:
        GPIO.output(buzzer,0)
        GPIO.output(relay,0)
# Check if the flame sensor 3 is activated   
if GPIO.input(flame3) == 1:
    GPIO.output(buzzer,1)  # activate the buzzer
    print("FIRE DETECTED - RIGHT")                            
    os.system('sudo python/home/pi/gsmffr.py')
    # run the robot
    GPIO.output(mot1,0)
    GPIO.output(mot2,1)
    GPIO.output(mot3,0)
    GPIO.output(mot4,1)
    time.sleep(2)
    GPIO.output(relay,1)  # activate the pump motor
    time.sleep(4)
    GPIO.output(mot1,0)
    GPIO.output(mot2,0)
    GPIO.output(mot3,1)
    GPIO.output(mot4,0)
    time.sleep(3)
    GPIO.output(mot1,0)
    GPIO.output(mot2,0)
    GPIO.output(mot3,0)
    GPIO.output(mot4,0)
    time.sleep(3)
    GPIO.output(mot1,1)
    GPIO.output(mot2,0)
    GPIO.output(mot3,1)
    GPIO.output(mot4,0)
    time.sleep(3)
    if GPIO.input(flame3) == 0:
        GPIO.output(buzzer,0)
        GPIO.output(relay,0)
else:
    GPIO.output(mot1,0)
    GPIO.output(mot2,0)
    GPIO.output(mot3,0)
    GPIO.output(mot4,0)
    print ("Safe")
    time.sleep(2)

                   

            
