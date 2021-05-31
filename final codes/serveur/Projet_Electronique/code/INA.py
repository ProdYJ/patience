import smbus as i2cINA

I2CbusINA = i2cINA.SMBus(1)

#définitions INA
INA_pump_address = 67
INA_pv_address = 65
INA_battery_address = 64
INA_current_reg = 1
INA_tension_reg = 2
INA_power_reg = 3

def getINA(address, register):
    try:
        
        data=I2CbusINA.read_i2c_block_data(address, register, 2)
        val = 256*data[0]+data[1]
        val = val * 0.00125
    except:
        print("erreur")
        
    return val