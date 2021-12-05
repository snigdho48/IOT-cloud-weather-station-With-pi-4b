import sys
import RPi.GPIO as GPIO
import os
import adafruit_dht as Adafruit_DHT
import urllib.request as urllib2
import smbus
import board
import time
from ctypes import c_short
time.sleep(1)
dht_device=Adafruit_DHT.DHT11(board.D27)


#Register Address
regCall   = 0xAA
regMean   = 0xF4
regMSB    = 0xF6
regLSB    = 0xF7
regPres   = 0x34
regTemp   = 0x2e

DEBUG = 1
sample = 2
deviceAdd =0x77



i2cbus = smbus.SMBus(1) # for Pi2 uses 1
time.sleep(.5)

key="HQE1TMH8TLT7URYD"       # Enter your Write API key from ThingSpeak

GPIO.setmode(GPIO.BCM)


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)     


def convert1(data, i):   # signed 16-bit value
    return c_short((data[i]<< 8) + data[i + 1]).value
 
def convert2(data, i):   # unsigned 16-bit value
    return (data[i]<< 8) + data[i+1] 
   
def readBmp180(addr=deviceAdd):    
    value = i2cbus.read_i2c_block_data(addr, regCall, 22)  # Read calibration data
    # Convert byte data to word values
    AC1 = convert1(value, 0)
    AC2 = convert1(value, 2)
    AC3 = convert1(value, 4)
    AC4 = convert2(value, 6)
    AC5 = convert2(value, 8)
    AC6 = convert2(value, 10)
    B1  = convert1(value, 12)
    B2  = convert1(value, 14)
    MB  = convert1(value, 16)
    MC  = convert1(value, 18)
    MD  = convert1(value, 20)

    # Read temperature
    i2cbus.write_byte_data(addr, regMean, regTemp)
    time.sleep(0.005)
    (msb, lsb) = i2cbus.read_i2c_block_data(addr, regMSB, 2)
    P2 = (msb << 8) + lsb
 
    # Read pressure
    i2cbus.write_byte_data(addr, regMean, regPres + (sample << 6))
    time.sleep(0.05)
    (msb, lsb, xsb) = i2cbus.read_i2c_block_data(addr, regMSB, 3)
    P1 = ((msb << 16) + (lsb << 8) + xsb) >> (8 - sample)

    # Refine temperature
    X1 = ((P2 - AC6) * AC5) >> 15
    X2 = (MC << 11) / (X1 + MD)
    B5 = X1 + X2
    temperature = int(B5 + 8) >> 4
 
    # Refine pressure
    B6  = B5 - 4000
    B62 = round(B6 * B6) >> 12
    X1  = (B2 * B62) >> 11
    X2  = round(AC2 * B6) >> 11
    X3  = X1 + X2
    B3  = (((AC1 * 4 + X3) << sample) + 2) >> 2
 
    X1 = round(AC3 * B6) >> 13
    X2 = (B1 * B62) >> 16
    X3 = ((X1 + X2) + 2) >> 2
    B4 = (AC4 * (X3 + 32768)) >> 15
    B7 = (P1 - B3) * (50000 >> sample)
 
    P = (B7 * 2) / B4
    P=round(P)
 
    X1 = (P >> 8) * (P >> 8)
    X1 = (X1 * 3038) >> 16
    X2 = (-7357 * P) >> 16
    pressure = P + ((X1 + X2 + 3791) >> 4)
  
    return ((pressure/100.0))

def readDHT():
    #temperature and humiditry read
    temp, humi =dht_device.temperature,dht_device.humidity
    time.sleep(.05)
    return humi,temp


# main() function
def main():
    
    print ('System Ready...')
    URL = 'https://api.thingspeak.com/update?api_key=%s' % key
    print ("Wait....")
    count=1
    t=0
    h=0
    p=0
    
    while True:
        try:
            humi, temp= readDHT()
            pressure =readBmp180()
            print  (f'{count}-Humidity:{humi}% -- Temperature:{temp }c -- Pressure:{pressure}hPa')
            h=h+humi
            t=t+temp
            p=p+pressure
            
            if count==10:
                humi="{0:.2f}".format(h/10)#"%0.2f" %(h/10)
                temp="{0:.2f}".format(t/10)#"%0.2f" %(t/10)
                pressure="{0:.2f}".format(p/10)#"%0.2f" %(p/10)
                finalURL = URL +"&field1=%s&field2=%s"%(humi, temp)+"&field3=%s" %(pressure) 
                #print (finalURL)
                s=urllib2.urlopen(finalURL);
                print  (f'uploaded-- Humidity:{humi}% -- Temperature:{temp }c -- Pressure:{pressure}hPa')
                s.close()
                count=0
                t=0
                h=0
                p=0
            count=count+1
            time.sleep(30)
                
            #time.sleep(10)
        except RuntimeError as error:     # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])
        
            
       
     
if __name__=="__main__":
   main()