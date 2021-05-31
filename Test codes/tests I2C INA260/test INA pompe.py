#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Raspberry Pi to Arduino I2C Communication
#i2cdetect -y 1

#library
import sys
import smbus2 as smbus#,smbus2
import time
import busio
import adafruit_ina260
import board
from gpiozero import LED

# Slave Addresses
I2C_SLAVE_ADDRESS = 67 #0x43 ou 67

# This function converts a string to an array of bytes.
def ConvertStringsToBytes(src):
  converted = []
  for b in src:
    converted.append(ord(b))
  return converted

def main(args):
    # Create the I2C bus
    I2Cbus = smbus.SMBus(1)
    with smbus.SMBus(1) as I2Cbus:
        #slaveSelect = input("Which Arduino (1-3): ")
        #cmd = input("Enter command: ")
        cmd="7"
        slaveAddress = I2C_SLAVE_ADDRESS

        BytesToSend = ConvertStringsToBytes(cmd)
        print("Sent " + str(slaveAddress) + " the " + str(cmd) + " command.")
        print(BytesToSend )
        
        current_int = 1
        current_byte = current_int.to_bytes(1,'big')
        print(current_byte)
        print(slaveAddress)
        i2c = board.I2C()
        #ina260 = adafruit_ina260.INA260(i2c)
       
        time.sleep(0.5)
        data2send=[4]
        moteur=LED(11)
        moteur.on()

        while True:
            #time.sleep(0.05)
            #I2Cbus.write_i2c_block_data(slaveAddress,67,data2send)
            I2Cbus.write_byte(slaveAddress, 0,42)
#             I2Cbus.write_byte(slaveAddress, 0x01,0)
            #I2Cbus.write_byte(slaveAddress, 0x01,4)
            #try:
                
            #data=I2Cbus.read_i2c_block_data(slaveAddress,0x00,16)
            #print(
            #"Current: %.2f mA Voltage: %.2f V Power:%.2f mW"
            #% (ina260.current, ina260.voltage, ina260.power)
            #)
            #time.sleep(1)
            #print(data)
            #print(data)
        #except:
            #print("remote i/o error")
            #time.sleep(0.5)
            print("steph")
    return 0

if __name__ == '__main__':
     try:
        main(sys.argv)
     except KeyboardInterrupt:
        print("program was stopped manually")
     input()
