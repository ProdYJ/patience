from gpiozero import LED
from time import sleep

enable = LED(22)
sens1 = LED(17)
sens2 = LED(27)

enable.on()

while True:
    sens1.on()
    print("sens1 on")
    sleep(1)
    sens1.off()
    print("sens1 off")
    sleep(1)
    sens2.on()
    print("sens2 on")
    sleep(1)
    sens2.off()
    print("sens2 off")
    sleep(1)
    