from time import sleep
import smbus
from gpiozero import LED
import math

relay = LED(11)
relay.off()

I2Cbus = smbus.SMBus(1)

print("begin config")

I2Cbus.write_byte_data(104, 107, 1) #registre de power management
I2Cbus.write_byte_data(104, 28, 0) #registre de configuration d'accélération

print("config done. Beggining")

while True :
    #I2Cbus.write_byte(67,2)
    #sleep(0.1)
    #data=I2Cbus.read_i2c_block_data(67,0x00,2)
    #data=I2Cbus.read_byte(67) #peut marcher avec write_byte!!!
    try:
        data1=I2Cbus.read_i2c_block_data(104, 63, 1)
        data2=I2Cbus.read_i2c_block_data(104, 64, 1)
        z_acc = data1[0]*256+data2[0]
        data1=I2Cbus.read_i2c_block_data(104, 61, 1)
        data2=I2Cbus.read_i2c_block_data(104, 62, 1)
        y_acc = data1[0]*256+data2[0]
        #val = 256*data[0]+data[1]
        #print(str(y_acc) + " " + str(z_acc))
        #print(y_acc)
        angle = math.atan(y_acc/z_acc)*180/3.141592
        print(angle)
        sleep(0.1)
        
    except:
        print("erreur")
        sleep(0.1)
