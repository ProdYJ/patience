from gpiozero import LED

pump = LED(11)

nightWatering = False
    #False = pas d'arrosagela nuit
    #true = arrosage la nuit
    
def watering (humidityValue,lumi):
    if (nightWatering ==True) :
        if (lumi==3):
            pumpAction(humidityValue)
    else :
        pumpAction(humidityValue)
        
def pumpAction (humidityValue) :
    if humidityValue == 1:
        pump.on()
        print('Pump on')
    elif humidityValue==2 :
        pump.off()
        print("Pump off")