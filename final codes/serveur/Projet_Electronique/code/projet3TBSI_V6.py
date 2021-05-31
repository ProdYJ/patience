#library
from imports import *
import sqlite3

icu_enable = False
#True pour activer la détection de mouvement 
#False pour désactiver la détection de mouvement     


def get_max_angle():
    verinAction("up", False)
    endStop_1.wait_for_press()
    verinAction("stop", False)
    angle = get_Kalman_angle()
    return angle

def get_min_angle():
    verinAction("down", False)
    endStop_2.wait_for_press()
    verinAction("stop", False)
    angle = get_Kalman_angle()
    return angle


def main(args):
    global icu_enable
    
    start = True
    global directory
    dir_path = os.path.dirname(os.path.realpath(__file__))                      #On récupère le dossier dans lequel le code python se trouve
    directory = dir_path +  '/Data.db'     # Et on ajoute au directory le nom du fichier SQL
    ecriture = SQL_Ecriture(SQL_dirName= directory) # on va créer l'objet ecriture de la classe SQL_Ecriture avec le nom du fichier SQL en argument

#Lecture de la dataBase et choix du mode de fonctionnement :
    while True :
        
        mode, ouverture = ecriture.get_Mode()
        #conn = sqlite3.connect(directory)
        #modeRemorque = get_last_db_value(conn, "DATA","MODE")
        #print('Mode détecté :', modeRemorque[0])
        
        detection = False
#         
#         while(mode==0):
#             watering(2,1)
#             if (endStop_1.is_pressed == True):
#                 verin_1.off()
#             #if (endStop_2.is_pressed == True):
#                 #verin_2.off()
#             verinAction("close", False)
#             mode, ouverture = ecriture.get_Mode()
#             start = True

        #initialisation du MPU et filtrage des donées au démarrage de l'arduino 
        if start==True :
            MPU_Init()
            Kalman_init()
            
            max_angle = 0
            min_angle = 0
            
            while(max_angle==min_angle):
                max_angle = get_max_angle();
                #print("Max angle found : " + str(max_angle))
                
                time.sleep(1)
                
                min_angle = get_min_angle();
                #print("Min angle found : " + str(min_angle))
                
                time.sleep(1)
            start = False   
        #Procédure pour fermeture de la remorque
#         while(modeRemorque[0]=="CLOSE"):
#             if (endStop_1.is_pressed == True):
#                 verin_1.off()
#             #if (endStop_2.is_pressed == True):
#                 #verin_2.off()
#             verinAction("close")
#             watering(2,1)
#             modeRemorque = get_last_db_value(conn, "DATA","MODE")
                

        #Récupération des données de l'arduino
        data = get_arduino_data(arduino_address)
        #print(data)
        if(data != None):
            if (data[4]!=255) : #condition de sécurité afin en cas d'erreur de communication avec Arduino
                
                #print(data)
                #humidity=setHumidity(data[1],data[0])
                humidityValue=data[0]
                #print(humidityValue)
                sunTrackingValue=data[1]
                averageSun = data[2]
                #print('sunTrackingValue ',sunTracking)
                rain=data[3]
                #print('rain ',rain)
                tAmbi=data[4]/5
                #print('tAmbi ',tAmbi)
                tInside=data[5]/5
                #print('tInside ',tInside)
                tBattery = data[6]/5
                tSolarPannel = data[7]/5
                tGround = data[8]/5
                #Arrosage et suntracking
                umbrella(rain)
                
                
                if mode == 0:
                    print('Dans mode off')
                    watering(2,1)
                    if (endStop_1.is_pressed == True):
                        verin_1.off()
                    #if (endStop_2.is_pressed == True):
                        #verin_2.off()
                    else :
                        verinAction("close", False)
                    
            
                elif (mode == 2) :
                    print('Dans mode manuel')
                    watering(2,1)
                    if (ouverture ==1):
                        print("Ouverture capot")
                        if(endStop_1.is_pressed==False):
                            verinAction('up',False)
                        else :
                            verin_2.off()
                        
                    elif (ouverture ==2):
                        print("Fermeture capot")
                        if(endStop_2.is_pressed==False):
                            verinAction('close',False)
                        else :
                            verin_1.off()
                        
                elif(mode ==1):
                    print('dans mode ON (auto)')
                    watering(humidityValue,sunTrackingValue)
                    sunTracking(sunTrackingValue,rain,detection)
                    
                    
            else:
                print("erreur de lecture Arduino")
            
            if (endStop_1.is_pressed == True):
                verin_1.off()
            if (endStop_2.is_pressed == True):
                verin_2.off()
            #Récupération des données des INA 
            pump_current = getINA(INA_pump_address, INA_current_reg)
            pump_tension = getINA(INA_pump_address, INA_tension_reg)
            pump_power = getINA(INA_pump_address, INA_power_reg)
            #print("Pump infos : " + str(pump_tension)[0:5] + "V " + str(pump_current)[0:5] + "A " + str(pump_power)[0:5] + "W")
            
            battery_current = getINA(INA_battery_address, INA_current_reg)
            battery_tension = getINA(INA_battery_address, INA_tension_reg)
            battery_power = getINA(INA_battery_address, INA_power_reg)
            #print("Battery infos : " + str(battery_tension)[0:5] + "V " + str(battery_current)[0:5] + "A " + str(battery_power)[0:5] + "W")
            
            pv_current = getINA(INA_pv_address, INA_current_reg)
            pv_tension = getINA(INA_pv_address, INA_tension_reg)
            pv_power = getINA(INA_pv_address, INA_power_reg)
            #print("Solar pannels info : " + str(pv_tension)[0:5] + "V " + str(pv_current)[0:5] + "A " + str(pv_power)[0:5] + "W")
            
            angle = get_Kalman_angle();
            angle = (angle - min_angle) * (40 - 0) / (max_angle - min_angle)
            #print("angle : " + str(angle))
            
            if(pump_current<80 and battery_current<80 and pv_current<80):
                #Ecriture dans la database
                test = True
                if(pv_current>pump_current):
                    batt_state = 1
                else:
                    batt_state = 0
                
                if(endStop_2.is_pressed == True):
                    rem_state = 0 # 0 = fermée
                else:
                    rem_state = 1
                
                if(sunTrackingValue == 3):
                    verin_state = 2
                else:
                    verin_state = sunTrackingValue
                    
                pump_state = humidityValue - 1;
                
                rain_state = rain
                
                try:
                    db_write_temperature(tAmbi,tInside,tSolarPannel,tBattery)
                
                #db_write_temperature(tAmbi,tInside,tSolarPannel,tBattery)
                #if test==True:
                    db_write_current(pv_current,battery_current,0,pump_current)
                    db_write_humidity(humidityValue)
                    db_write_angle(angle)
                    db_write_light(averageSun)
                    db_write_data1(rem_state, batt_state, pump_state, verin_state, 0)
                except sqlite3.Error:
                    test == False
                    print(" ")
                    print("Erreur détectée")
                    print(" ")            
            time.sleep(1)
    return 0

if __name__ == '__main__':
    try:
        main(sys.argv)
    except KeyboardInterrupt:
        print("program was stopped manually")
    input()