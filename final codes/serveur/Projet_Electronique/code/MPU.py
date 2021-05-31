import smbus as i2cINA
import math

#définitions MPU6050
MPU_x_accel_reg = 59
MPU_y_accel_reg = 61
MPU_z_accel_reg = 63

I2CbusINA = i2cINA.SMBus(1)


def MPU_config():
    I2CbusINA.write_byte_data(104, 107, 1) #registre de power management
    I2CbusINA.write_byte_data(104, 28, 0) #registre de configuration d'accélération

def get_MPU_accel(register):
    try:
        temp1 = I2CbusINA.read_i2c_block_data(104, register, 1)
        temp2 = I2CbusINA.read_i2c_block_data(104, register+1, 1)
        val = 256 * temp1[0] + temp2[0]
        if(val>32768):
            val = val-65536
        return val
    except:
        print("MPU read fail")
        return 0

def getAngle():
    x_accel = get_MPU_accel(MPU_x_accel_reg)
    y_accel = get_MPU_accel(MPU_y_accel_reg)
    z_accel = get_MPU_accel(MPU_z_accel_reg)
    
    angle_x = (math.atan(y_accel / math.sqrt(pow(x_accel, 2) + pow(z_accel, 2))) * 180 / math.pi)
    
    return angle_x