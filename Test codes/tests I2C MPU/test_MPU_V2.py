from time import sleep
import smbus
from gpiozero import LED
import math
import sys

I2Cbus = smbus.SMBus(1)

x_accel_reg = 59
y_accel_reg = 61
z_accel_reg = 63

def getReg(address):
    global x_accel
    global y_accel
    global z_accel
    
    try:
        temp1 = I2Cbus.read_i2c_block_data(104, address, 1)
        temp2 = I2Cbus.read_i2c_block_data(104, address+1, 1)
    except:
        print("error")
        
    if(address == 59):
        x_accel = temp1[0] * 256 + temp2[0]
        if(x_accel > 32768):
            x_accel = x_accel - 65536
    elif(address == 61):
        y_accel = temp1[0] * 256 + temp2[0]
        if(y_accel > 32768):
            y_accel = y_accel - 65536
    elif(address == 63):
        z_accel = temp1[0] * 256 + temp2[0]
        if(z_accel > 32768):
            z_accel = z_accel - 65536

def main(args):
    
    I2Cbus.write_byte_data(104, 107, 1) #registre de power management
    I2Cbus.write_byte_data(104, 28, 0) #registre de configuration d'accélération
    
    while True:
        getReg(x_accel_reg)
        getReg(y_accel_reg)
        getReg(z_accel_reg)
        print(str(x_accel) + " " + str(y_accel) + " " + str(z_accel))
        angle_x = (math.atan(y_accel / math.sqrt(pow(x_accel, 2) + pow(z_accel, 2))) * 180 / math.pi)
        print(angle_x)
        sleep(0.1)


if __name__ == '__main__':
     try:
        main(sys.argv)
     except KeyboardInterrupt:
        print("program was stopped manually")
     input()