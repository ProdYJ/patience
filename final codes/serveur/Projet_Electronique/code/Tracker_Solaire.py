#!/usr/bin/python3

from EcritureSQL import SQL_Ecriture
import Serveur_Web
import os
import time

dir_path = os.path.dirname(os.path.realpath(__file__))                      #On récupère le dossier dans lequel le code python se trouve
directory = dir_path +  '/Data.db'     # Et on ajoute au directory le nom du fichier SQL

ecriture = SQL_Ecriture(SQL_dirName= directory) # on va créer l'objet ecriture de la classe SQL_Ecriture avec le nom du fichier SQL en argument



# Ci-dessous, la liste des fonction à appeler toute les 5 secondes pour enregistrer les données reçu des capteur
# il suffit de remplacer les valeurs fixe mise pour exemple par des valeur réel stocker dans des variables.
ecriture.Temperature(ambiante = 26.33,remorque=22.56, panneaux=36.8, batterie=34.5)     # Les températures sont des réels
ecriture.Courants(panneaux=2.66,batterie=1.56,verin=8.3,pompe=3)
ecriture.Tension(panneaux=3.5,batterie=1.6,verin=2.3,pompe=3.8)
ecriture.Humidite(sol=75)       #l'humidité est un chiffre entier 0 => 100
ecriture.Inclinaison(capot = 35)
ecriture.Ldr(bas = 3500, haut = 1700)
ecriture.Pluie(pluie = 10)

# Donnée à enregistrer si souhaité.
ecriture.Set_Data0(mode = 0, ouverture = 0)
# mode = 0 => off
# mode = 1 => ON
# mode = 2 => Manu ==> si mode manuelle  => ouverture = 1 => ouvrir à fond
#                                        => ouverture = 2 => fermer à fond
#                                        => ouverture = 0 => ne rien faire       
# ceux- ci sont modifié par le site web, mais peuvent être modifié par le code si c'est utile

ecriture.Set_Data1(etat = 0,batterie = 0,pompe = 0 ,verin = 0 ,vitesse = 0)
#etat 0=remorque fermée, 1=remoque ouvertes
#batterie 0=en décharge, 1= en charge
#pompe 0=au repos,1=en fonctionnement
#verin 0=au repos,1=en fonctionnement
#vitesse 0=au repos,1=en mouvement

# Pour la récupération du mode actuelle
mode, ouverture = ecriture.get_Mode()
# mode = 0 => off
# mode = 1 => ON
# mode = 2 => Manu ==> si mode manuelle  => ouverture = 1 => ouvrir à fond
#                                        => ouverture = 2 => fermer à fond
#                                        => ouverture = 0 => ne rien faire                                        


