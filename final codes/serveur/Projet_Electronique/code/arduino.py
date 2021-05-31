import smbus#2 as smbus

I2Cbus = smbus.SMBus(1)

arduino_address = 11

def get_arduino_data(address):
    
    try:
        data=I2Cbus.read_i2c_block_data(address,0x00,16)
        return data
    except:
        print("remote i/o error")