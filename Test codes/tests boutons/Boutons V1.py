from gpiozero import Button
from time import sleep

FDC1 = Button(6, None, True)

while True :
    if FDC1.is_pressed:
        print("pressed")
    else:
        print("released")
    
    sleep(0.5)