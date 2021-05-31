from verin import*

def umbrella(nbre) :
    
    if nbre==1 :
        print("Présence pluie")
        verinAction("close",False)
            
        if endStop_1.is_pressed == True :
            verinAction("stop")
            print("Attent fin de la pluie")
    
    return 0