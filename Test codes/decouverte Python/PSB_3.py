from gpiozero import LED, Button
from time import sleep

enable=LED(22)
sens1=LED(17)
sens2=LED(27)

enable.on()

signal_pico = Button(5)
sens1.on()
signal_pico.wait_for_press()

while True :
    
    if signal_pico.is_pressed:
        sens1.toggle()
        sleep(0.5)
        sens2.toggle()
        sleep(0.5)
        while signal_pico.is_pressed:
            pass
    
#     else if signal_pico.is_released
#         sens2.toggle()
#         sleep(0.5)
#         sens2.toggle()
#         sleep(0.5)w<