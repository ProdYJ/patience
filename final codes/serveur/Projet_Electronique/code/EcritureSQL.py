#!/usr/bin/python3

import sqlite3
import os
from datetime import datetime,timedelta
class SQL_Ecriture():

    def __init__(self, SQL_dirName):
        self.dirName = SQL_dirName
    
    def Temperature(self, ambiante,remorque, panneaux, batterie):
        conn = sqlite3.connect(self.dirName)     
        cursor = conn.cursor() 
        cursor.execute("insert into TEMPERATURE(AMBIANTE,REMORQUE,PANNEAUX,BATTERIE) values(?,?,?,?)", (ambiante,remorque,panneaux,batterie))  
        conn.commit()                                                              
        conn.close()     

    def Courants(self, panneaux, batterie, verin, pompe):
        conn = sqlite3.connect(self.dirName)     
        cursor = conn.cursor() 
        cursor.execute("INSERT INTO COURANTS(PANNEAUX,BATTERIE,VERIN,POMPE) VALUES(?,?,?,?)",(panneaux, batterie, verin, pompe))  
        conn.commit()                                                               
        conn.close()   

    def Humidite(self,sol) :
        conn = sqlite3.connect(self.dirName)     
        cursor = conn.cursor() 
        cursor.execute("INSERT INTO HUMIDITE(SOL) VALUES(?)",(sol,)) 
        conn.commit()                                                               
        conn.close()   

    def Inclinaison(self,capot) :
        conn = sqlite3.connect(self.dirName)     
        cursor = conn.cursor() 
        cursor.execute("INSERT INTO INCLINAISON(CAPOT) VALUES(?)",(capot,))  
        conn.commit()                                                               
        conn.close()   

    def Ldr(self,bas,haut):
        conn = sqlite3.connect(self.dirName)     
        cursor = conn.cursor() 
        cursor.execute("INSERT INTO LDR(BAS,HAUT) VALUES(?,?)",(bas,haut))  
        conn.commit()                                                               
        conn.close() 

    def Set_Data0(self,mode, ouverture):
        conn = sqlite3.connect(self.dirName)    
        cursor = conn.cursor() 
        cursor.execute("DELETE FROM DATA0")
        cursor.execute("INSERT INTO DATA0(MODE,OUVERTURE) VALUES(?,?)",(int(mode),int(ouverture))) 
        conn.commit()     
        conn.close() 

    def Set_Data1(self,etat, batterie,pompe,verin,vitesse):
        conn = sqlite3.connect(self.dirName)    
        cursor = conn.cursor() 
        cursor.execute("DELETE FROM DATA1")
        cursor.execute("INSERT INTO DATA1(ETAT,BATTERIE,POMPE,VERIN,VITESSE) VALUES(?,?,?,?,?)",(etat,batterie,pompe,verin,vitesse)) 
        conn.commit()     
        conn.close() 

    def get_Mode(self) :
        mod = self.ReadLast(table = "DATA0",index="MODE")
        ouv = self.ReadLast(table="DATA0", index="OUVERTURE")

        return int(mod),int(ouv)
    
    def Tension(self,panneaux,batterie,verin,pompe):
        conn = sqlite3.connect(self.dirName)    
        cursor = conn.cursor() 
        cursor.execute("INSERT INTO TENSION(PANNEAUX,BATTERIE,VERIN,POMPE) VALUES(?,?,?,?)",(panneaux,batterie,verin,pompe)) 
        conn.commit()     
        conn.close()

    def Pluie(self,pluie):
        conn = sqlite3.connect(self.dirName)    
        cursor = conn.cursor() 
        cursor.execute("INSERT INTO PLUIE(PLUIE) VALUES(?)",(pluie,)) 
        conn.commit()     
        conn.close() 
    

    def Read5Sec (self,table,index) :
        return self.tableDeTemps(5,180), self.ReadElement(table=table,index=index,nombre = 1,limit=180)
    def Read15Sec (self,table,index) :
        return self.tableDeTemps(15,240), self.ReadElement(table=table,index=index,nombre = 3,limit=240)
    def Read1Min (self,table,index) :
        return self.tableDeTemps(60,480), self.ReadElement(table=table,index=index,nombre = 12,limit=480)
    def Read15Min (self,table,index) :
        return self.tableDeTemps(900,96), self.ReadElement(table=table,index=index,nombre = 180,limit=96)
    def Read1H (self,table,index) :
        return self.tableDeTemps(3600,168), self.ReadElement(table=table,index=index,nombre = 720,limit=168)

    def tableDeTemps(self,delaiEnSec, nombre ):
        array = []
        i = 0
        temps = datetime.now()
        while i< nombre:
            if (delaiEnSec <60) : formatDetemps = str(temps.hour)+"h"+str(temps.minute)+":"+str(temps.second)
            elif (delaiEnSec <3600) : formatDetemps = str(temps.hour)+"h"+str(temps.minute)
            elif (delaiEnSec >=3600) : formatDetemps = str(temps.day)+"/"+str(temps.month)+"/"+str(temps.year)+" "+str(temps.hour) + "h"
            
            array.append(formatDetemps)
            temps = temps - timedelta(seconds=delaiEnSec)
            i+= 1
        return array


    def ReadElement (self,table,index, nombre, limit) :
        array = self.ReadAll(table=table,index=index)
        array.reverse()
        arrayMoyenne = [0]*nombre
        tableau = []
        i=0
        for value in array:
            arrayMoyenne[i] = value
            i +=1
            if(i== len(arrayMoyenne)) :
                tableau.append(self.CalculMoyenne(arrayMoyenne))
            i = i % len(arrayMoyenne)
            if len(tableau) >= limit : break
        return tableau
                
    def CalculMoyenne (self, arrayMoyenne):
        sum = 0
        for save in arrayMoyenne :
            sum += save
        mean = sum / len(arrayMoyenne) 
        return float("{:.2f}".format(mean))

    def ReadLast (self,table,index) :
        conn = sqlite3.connect(self.dirName)    
        curs = conn.cursor()
        text ="select " + index + " from " + table                                                        #On crée le cursor curs qui va nous permtre d'intéragir avec la DB
        recup = curs.execute(text)
        rec  = curs.fetchall()
        if (len(rec)>0):
            value = rec[- 1]
        else : value = [0]
        conn.commit()                                                               #Sauvegarde
        conn.close()                     
        return value[0]

    def ReadAll(self,table,index):
        conn = sqlite3.connect(self.dirName)    
        curs = conn.cursor()
        text ="select " + index + " from " + table                                                        #On crée le cursor curs qui va nous permtre d'intéragir avec la DB
        recup = curs.execute(text)
        rec  = curs.fetchall()
        array = []
        for row in rec:
            array.append(row[0])
        conn.commit()                                                               #Sauvegarde
        conn.close()                     
        return array

