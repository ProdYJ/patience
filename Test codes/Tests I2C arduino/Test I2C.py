#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Raspberry Pi to Arduino I2C Communication
#i2cdetect -y 1

#library
import sys
import smbus2 as smbus#,smbus2
import time

# Slave Addresses
I2C_SLAVE_ADDRESS = 11 #0x0b ou 11

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
        #I2Cbus.write_i2c_block_data(slaveAddress, 0x00, BytesToSend)
        #I2Cbus.write_i2c_block_data(slaveAddress, 0x00, BytesToSend)
        time.sleep(0.5)

        while True:
            time.sleep(0.1)
            try:
                data=I2Cbus.read_i2c_block_data(slaveAddress,0x00,16)
                print("recieve from slave:")
                #print(data)
                print(data)
            except:
                print("remote i/o error")
                time.sleep(0.5)
    return 0

if __name__ == '__main__':
     try:
        main(sys.argv)
     except KeyboardInterrupt:
        print("program was stopped manually")
     input()
