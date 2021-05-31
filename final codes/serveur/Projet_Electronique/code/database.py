from EcritureSQL import SQL_Ecriture
import os


#def db_init():
dir_path = os.path.dirname(os.path.realpath(__file__))                      #On récupère le dossier dans lequel le code python se trouve
directory = dir_path +  '/Data.db'     # Et on ajoute au directory le nom du fichier SQL
ecriture = SQL_Ecriture(SQL_dirName= directory) # on va créer l'objet ecriture de la classe SQL_Ecriture avec le nom du fichier SQL en argument

def db_write_temperature(amb, rem, pv,batt):
    ecriture.Temperature(ambiante = amb,remorque=rem, panneaux=pv, batterie=batt)     # Les températures sont des réel

def db_write_current(pv, batt, ver, pump):
    ecriture.Courants(panneaux=pv,batterie=batt,verin=ver,pompe=pump)

def db_write_humidity(hum):
    ecriture.Humidite(sol=hum)       #l'humidité est un chiffre entier 0 => 100
    
def db_write_angle(angle):
    ecriture.Inclinaison(capot = angle)
    
def db_write_light(ldr):
    ecriture.Ldr(bas = ldr,haut = 0)
    
def db_write_mode(auto_man):
    ecriture.Data(mode = auto_man)    #le mode est une chaîne de caractère
    
def db_write_data1(etat_remorque, batterie, pompe, verin, vitesse):
    ecriture.Set_Data1(etat_remorque, batterie, pompe, verin, vitesse)
    
def get_last_db_value(conn, table, row, index = -1):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    command = "SELECT " + row + " FROM " + table
    cur = conn.cursor()
    cur.execute(command)

    rows = cur.fetchall()

    #for row in rows:
     #   print(row)
    if(index == -1):
        data = rows[len(rows)-1]
    elif(index<len(rows)):
        data = rows[index]
    else:
        data = "ERROR"
    
    print(data)
    return data