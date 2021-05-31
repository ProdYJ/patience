
from gpiozero import LED, Button
from time import sleep

enable=LED(22)
sens1=LED(17)
sens2=LED(27)

enable.on()

signal_pico = Button(5)


while True :
    if signal_pico.is_pressed:
        print("sens1")
        sens1.on()
        
    else :
        sens1.off()
    

