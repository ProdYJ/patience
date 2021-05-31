from gpiozero import LED, Button
#from picam import *

icu_enable = True
#True = activation de la détection de mouvement
#False = désactivation de la détection de mouvement

#detection = ICU(icu_enable)

verin_1=LED(17)
verin_2=LED(27)
verin_EN=LED(22)

endStop_1 = Button(5, None, True)
endStop_2 = Button(6, None, True)

def verinAction(mot, detection):
    if detection == False :
        if mot=="up" :
            #testSecuPres()
            if(endStop_1.is_pressed == False):
                print("v UP")
                verin_EN.on()
                verin_1.on()
                verin_2.off()
        elif mot=="down" :
            #testSecuPres()
            if(endStop_2.is_pressed == False):
                print("v DOWN")
                verin_EN.on()
                verin_1.off()
                verin_2.on()
        elif mot=="stop" :
            print("v STOP")
            verin_EN.off()
            verin_1.off()
            verin_2.off()
        elif mot=="close" :
            print("v CLOSE")
            verinAction("down",detection)
            endStop_2.wait_for_press()
            verinAction("stop",False)
            
    elif detection==True :
        print("Vérin stoppé car mouvement détecté")
        verin_EN.off()
        verin_1.off()
        verin_2.off()
    return 0


def sunTracking(nbre_sun,nbre_rain,detection):
    global icu_enable
    #Rappel : 0 = STOP
    # 1 = monter
    # 2 = descendre
    if nbre_rain == 0 :
        if nbre_sun ==0 :
            verinAction("stop", detection)
        elif nbre_sun ==1 :
            verinAction("up", detection)
        elif nbre_sun == 2 :
            verinAction("down", detection)
        elif nbre_sun == 3 :
            verinAction("close", detection)
            print("KID CUDY DAN AND NIGHT")
            
    return 0