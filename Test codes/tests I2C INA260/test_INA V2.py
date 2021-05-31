import time
import board
import busio
import adafruit_ina260
from gpiozero import LED

moteur=LED(11)
i2c = board.I2C()
ina260 = adafruit_ina260.INA260(i2c,0x43)
moteur.on()
while True :
        print (
            "Current: %.2f mA Voltage: %.2f V Power:%.2f mW"
            % (ina260.current, ina260.voltage,ina260.power)
        )
        time.sleep(1)