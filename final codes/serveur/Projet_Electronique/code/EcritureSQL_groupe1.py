import sqlite3
import os

class SQL_Ecriture():

    def __init__(self, SQL_dirName):
        self.dirName = SQL_dirName
    
    def Temperature(self, ambiante,remorque, panneaux, batterie ):
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

    def Ldr(self,moyenne):
        conn = sqlite3.connect(self.dirName)     
        cursor = conn.cursor() 
        cursor.execute("INSERT INTO LDR(MOYENNE) VALUES(?)",(moyenne,))  
        conn.commit()                                                               
        conn.close() 

    def Data(self,mode):
        conn = sqlite3.connect(self.dirName)    
        cursor = conn.cursor() 
        cursor.execute("INSERT INTO DATA(MODE) VALUES(?)",(mode,)) 
        conn.commit()     
        conn.close() 
    



