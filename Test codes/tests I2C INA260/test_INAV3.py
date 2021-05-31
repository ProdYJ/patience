from time import sleep
import smbus
from gpiozero import LED

relay = LED(11)
relay.on()

tension = 0
current = 0

I2Cbus = smbus.SMBus(1)

while True :
    #I2Cbus.write_byte(67,2)
    #sleep(0.1)
    #data=I2Cbus.read_i2c_block_data(67,0x00,2)
    #data=I2Cbus.read_byte(67) #peut marcher avec write_byte!!!
    try:
        data=I2Cbus.read_i2c_block_data(67, 2, 2)
        val = 256*data[0]+data[1]
        tension = str(val * 0.00125)
        tension = tension[0:5]
        sleep(0.1)
    except:
        print("erreur")
        
    try:
        data=I2Cbus.read_i2c_block_data(67, 1, 2)
        val = 256*data[0]+data[1]
        courant = str(val * 0.00125)
        courant = courant[0:5]
        sleep(0.1)
    except:
        print("erreur")
        
    print("Tension : " + tension + "V. Current : " + courant + "A")
