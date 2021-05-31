#!/usr/bin/python3    


from flask import Flask,url_for,render_template,redirect,request,session,flash
#flask est la librairie.  Flask est le nom de la classe à importer pour utiliser flask
from datetime import timedelta #librairie qui permet de gérer le temps de connexion de l'utilisateur
import os
from EcritureSQL import SQL_Ecriture

app = Flask(__name__) #crée un objet flask appelé "app".   
app.secret_key = "tatakai" #permet d'activer l'utilisation des sessions utilisateur
app.permanent_session_lifetime = timedelta(minutes=30) #détermine le temps pendant lequel l'utilisateur restera connécté
                      
dir_path = os.path.dirname(os.path.realpath(__file__))#On récupère le dossier dans lequel le code python se trouve
directory = dir_path +  '/Data.db'  # Et on ajoute au directory le nom du fichier SQL

ecriture = SQL_Ecriture(SQL_dirName= directory) # on va créer l'objet ecriture de la classe SQL_Ecriture avec le nom du fichier SQL en argument
      

etat=0 #0=remorque fermée, 1=remoque ouvertes
batterie=0 #0=aucun apport
pompe=0 #0=au repos
verin=0 #0=au repos
vitesse=0 #0=au repos
mode=0
action=0 

def sendData(Etat,Batterie,Pompe,Verin,Vitesse):
    etat=Etat
    batterie=Batterie
    pompe=Pompe
    verin=Verin
    vitesse=Vitesse
    return

def getData():
    return mode, action


@app.route('/',methods=["GET","POST"]) 
#(Une requête http c'est l'envoi d'une url au serveur. Si vous tapez "youtube.com"dans le navigateur et que vous faite enter, vous venez de créer une requête http). 
#"route" est une fonction qui va analyser les requêtes http. On peut voir ça comme un if. 
#Si l'url est "adresseduserveur/" puis rien, alors on rentre dans la fonction juste en dessous appellée "acc".
#Sinon, on passe au "if suivant".

#methods=["GET","POST"] décrit la manière d'accéder à cette url, les méthodes http. Il en existe plus que 2.
#GET correspond au cas où le serveur envoi du data (ex: je tape youtube.com, je reçois l'interface web de youtube )                 
#POST correspond au cas où le serveur recoit une information du data (ex:J'appuie sur une video youtube. Le serveur recoit l'info et agit en conséquence) 

def acc(): #On définit la fonction "acc"

  return redirect(url_for("login"))#Permet de sauter à la fonction "login"
  #url_for crée une route qui mène à la fonction appellée "login"
  #redirect redirige le programme vers la route précisée
        
@app.route('/login',methods=["GET","POST"])
#si l'adresse reçue est "adresseserveur/login", alors on rentre dans la fct "login"
def login():

     if request.method == "POST": #Vérifie si la requête http est de type POST (donc si on a appuyé sur un bouton)
         motpasse = request.form["mdp"] #récupère le texte écrit dans la zone de texte appelée "mdp" (voir dans login.html) et le stock dans "motdepasse"
         if motpasse == "ErenJaeger": #vérifie si le mot de passe est bon
            session["user"] = "logged" #créé une session "user" appellée "logged"
            session.permanent = True  #implémente le fait que l'utilisateur reste connceté (jusqu'au temps max décrit dans timedelta)
            return redirect(url_for("pgweb"))

         else:  #Si le mot de passe est mauvais
             flash("Mot de passe incorrect!") #dit "quand l'interface sera refresh, il faudra afficher le message suivant
             #à l'endroit dédié dans l'interface"
             return redirect(url_for("login")) #redirige vers login, ce qui aura pour effet d'actualiser la page et d'afficher le message flash

     else: #Si on POST pas, alors on GET, ce qui correspond voir au cas où on a tapé l'url ou on a été redirigé
            return render_template('login.html') #Envoi le fichier login.html à l'interface. Ca permet d'afficher la page codée dans le fichier html.
        



@app.route('/interface',methods=["GET","POST"])
def pgweb():
    if "user" in session: #vérifie si l'utilisateur est bel et bien connecté. Seul l'interface nécessite d'être connecté.
     #Les fonctions menant à l'affichage des graphs ne nécessitent pas de protection.
        
        if request.method == "POST":#si oui, lance interface
            bouton = request.form["btn"]
            
            if bouton=="ON": #si utilisateur appuie sur ON, alors on défini le mode à 1
                mod,ouv = ecriture.get_Mode() #Seul "mod" change, mais il faut récupérer l'etat de l'ouverture "ouv" et la renvoyer
                ecriture.Set_Data0(mode = 1,ouverture =  ouv)
                return redirect(url_for("pgweb"))
            elif bouton=="Manual":
                mod,ouv = ecriture.get_Mode()
                ecriture.Set_Data0(mode = 2,ouverture =  ouv)
                return redirect(url_for("pgweb"))
            elif bouton=="OFF":
                mod,ouv = ecriture.get_Mode()
                ecriture.Set_Data0(mode = 0,ouverture =  ouv)
                return redirect(url_for("pgweb"))
            elif bouton=="OPEN":
                mod,ouv = ecriture.get_Mode()
                ecriture.Set_Data0(mode = mod,ouverture =  1)
                return redirect(url_for("pgweb"))
            elif bouton=="CLOSE":
                mod,ouv = ecriture.get_Mode()
                ecriture.Set_Data0(mode = mod,ouverture =  2)
                return redirect(url_for("pgweb"))

        else:
            lastPluie = ecriture.ReadLast(table ="PLUIE", index="PLUIE")

            lastLDRBAS = ecriture.ReadLast(table ="LDR", index = "BAS")
            lastLDRHAUT = ecriture.ReadLast(table ="LDR", index = "HAUT")
            lastHumidite = ecriture.ReadLast(table = "HUMIDITE", index="SOL")
            lastInclinaison = ecriture.ReadLast(table ="INCLINAISON", index = "CAPOT")

            lastTAmbiante = ecriture.ReadLast(table ="TEMPERATURE", index = "AMBIANTE")
            lastTRemorque = ecriture.ReadLast(table ="TEMPERATURE", index = "REMORQUE")
            lastTPanneaux = ecriture.ReadLast(table ="TEMPERATURE", index = "PANNEAUX")
            lastTBatterie = ecriture.ReadLast(table ="TEMPERATURE", index = "BATTERIE")

            lastIPanneaux = ecriture.ReadLast(table ="COURANTS", index = "PANNEAUX")
            lastIBatterie = ecriture.ReadLast(table ="COURANTS", index = "BATTERIE")
            lastIVerin = ecriture.ReadLast(table ="COURANTS", index = "VERIN")
            lastIPompe = ecriture.ReadLast(table ="COURANTS", index = "POMPE")

            lastUPanneaux = ecriture.ReadLast(table ="TENSION", index = "PANNEAUX")
            lastUBatterie = ecriture.ReadLast(table ="TENSION", index = "BATTERIE")
            lastUVerin = ecriture.ReadLast(table ="TENSION", index = "VERIN")
            lastUPompe = ecriture.ReadLast(table ="TENSION", index = "POMPE")

            etat=ecriture.ReadLast(table="DATA1",index="ETAT")
            batterie=ecriture.ReadLast(table="DATA1",index="BATTERIE")
            pompe=ecriture.ReadLast(table="DATA1",index="POMPE")
            verin=ecriture.ReadLast(table="DATA1",index="VERIN")
            vitesse=ecriture.ReadLast(table="DATA1",index="VITESSE")

            #lancement de l'interface et envoie des arguments nécessaires. Les noms oranges ICI correspondent aux noms des variables dans l'html. Les noms en blancs sont les variables à envoyer. 
            return render_template("index.html",pluie=lastPluie,etat=etat,batterie=batterie,pompe=pompe,verin=verin,vitesse=vitesse,
                                    t_ext=lastTAmbiante,t_int=lastTRemorque,t_panneaux=lastTPanneaux,t_batterie=lastTBatterie,
                                    i1=lastIPompe,i2=lastIVerin,i3=lastIPanneaux,i4=lastIBatterie,
                                    u1=lastUPompe,u2=lastUVerin,u3=lastUPanneaux,u4=lastUBatterie,
                                    ldr_b=lastLDRBAS,ldr_h=lastLDRHAUT,incli=lastInclinaison,humi=lastHumidite)  
    else:
        return redirect(url_for("login")) #sinon, reviens à la page de connexion

@app.route('/logout')
def logout():
        session.pop("user", None) #pour quitter la session si on ne veut pas attendre que le temps max passe pour être déconnecté (voir timedelta(minutes=30))
        flash("Déconnecté avec succès")
        return redirect(url_for("login"))


@app.route('/temperature.html')  
def gtemp(): #
        label,data1 = ecriture.Read15Min(table ="TEMPERATURE", index = "AMBIANTE") #va dans la table "température", dans l'index "AMBIANTE" et renvoit deux tableau (label contient le texte d'abscisses et data contient les valeurs d'ordonnées)
        label,data2 = ecriture.Read15Min(table ="TEMPERATURE", index = "REMORQUE")
        label,data3 = ecriture.Read15Min(table ="TEMPERATURE", index = "PANNEAUX")
        label,data4 = ecriture.Read15Min(table ="TEMPERATURE", index = "BATTERIE")
        return render_template("temperature.html",datas1=data1,datas2=data2,datas3=data3,datas4=data4 ,labels=label,titre="Temperature journee") #permet d'envoyer des arguments au fichier html

@app.route('/temperature15min.html')  
def gtemp15():
        label,data1 = ecriture.Read5Sec(table ="TEMPERATURE", index = "AMBIANTE")
        label,data2 = ecriture.Read5Sec(table ="TEMPERATURE", index = "REMORQUE")
        label,data3 = ecriture.Read5Sec(table ="TEMPERATURE", index = "PANNEAUX")
        label,data4 = ecriture.Read5Sec(table ="TEMPERATURE", index = "BATTERIE")
        return render_template("temperature.html",datas1=data1,datas2=data2,datas3=data3,datas4=data4 ,labels=label,titre="Temperature 15min")

@app.route('/temperature1h.html')  
def gtemp1():
        label,data1 = ecriture.Read15Sec(table ="TEMPERATURE", index = "AMBIANTE")
        label,data2 = ecriture.Read15Sec(table ="TEMPERATURE", index = "REMORQUE")
        label,data3 = ecriture.Read15Sec(table ="TEMPERATURE", index = "PANNEAUX")
        label,data4 = ecriture.Read15Sec(table ="TEMPERATURE", index = "BATTERIE")
        return render_template("temperature.html",datas1=data1,datas2=data2,datas3=data3,datas4=data4 ,labels=label,titre="Temperature 1h")
@app.route('/temperature8h.html')  
def gtemp8():
        label,data1 = ecriture.Read1Min(table ="TEMPERATURE", index = "AMBIANTE")
        label,data2 = ecriture.Read1Min(table ="TEMPERATURE", index = "REMORQUE")
        label,data3 = ecriture.Read1Min(table ="TEMPERATURE", index = "PANNEAUX")
        label,data4 = ecriture.Read1Min(table ="TEMPERATURE", index = "BATTERIE")
        return render_template("temperature.html",datas1=data1,datas2=data2,datas3=data3,datas4=data4 ,labels=label,titre="Temperature 8h")

@app.route('/temperatureSem.html')  
def gtempSem():
        label,data1 = ecriture.Read1H(table ="TEMPERATURE", index = "AMBIANTE")
        label,data2 = ecriture.Read1H(table ="TEMPERATURE", index = "REMORQUE")
        label,data3 = ecriture.Read1H(table ="TEMPERATURE", index = "PANNEAUX")
        label,data4 = ecriture.Read1H(table ="TEMPERATURE", index = "BATTERIE")
        return render_template("temperature.html",datas1=data1,datas2=data2,datas3=data3,datas4=data4 ,labels=label,titre="Temperature semaine")




        
@app.route('/precipitation.html')  
def gprec():
        label,data = ecriture.Read15Min(table ="PLUIE", index = "PLUIE")
        return render_template("precipitation.html",labels=label,datas=data)
   
@app.route('/precipitation15min.html')  
def gprec15():
        label,data = ecriture.Read5Sec(table ="PLUIE", index = "PLUIE")
        return render_template("precipitation.html",labels=label,datas=data)

@app.route('/precipitation1h.html')  
def gprec1():
        label,data = ecriture.Read15Sec(table ="PLUIE", index = "PLUIE")
        return render_template("precipitation.html",labels=label,datas=data)

@app.route('/precipitation8h.html')  
def gprec8():
        label,data = ecriture.Read1Min(table ="PLUIE", index = "PLUIE")
        return render_template("precipitation.html",labels=label,datas=data)

@app.route('/precipitationSem.html')  
def gprecSem():
        label,data = ecriture.Read1H(table ="PLUIE", index = "PLUIE")
        return render_template("precipitation.html",labels=label,datas=data)




@app.route('/electrique.html')  
def elec():
        label,C1 = ecriture.Read15Min(table ="COURANTS", index = "POMPE")
        label,C2 = ecriture.Read15Min(table ="COURANTS", index = "VERIN")
        label,C3 = ecriture.Read15Min(table ="COURANTS", index = "PANNEAUX")
        label,C4 = ecriture.Read15Min(table ="COURANTS", index = "BATTERIE")

        label,T1 = ecriture.Read15Min(table ="TENSION", index = "POMPE")
        label,T2 = ecriture.Read15Min(table ="TENSION", index = "VERIN")
        label,T3 = ecriture.Read15Min(table ="TENSION", index = "PANNEAUX")
        label,T4 = ecriture.Read15Min(table ="TENSION", index = "BATTERIE")

        P1=[] #crée des tableaux qui contiendront les valeurs de puissance
        P2=[]
        P3=[]
        P4=[]
               
        for i in range(0, len(C1)): #sert à muliplier les matrice tension et courant pour obtenir la puissance
        #Remplacez Tn[i] par 12  si vous n'avez pas de capteurs de tension
            P1.append(C1[i]*T1[i])
            P2.append(C2[i]*T2[i])
            P3.append(C3[i]*T3[i])
            P4.append(C4[i]*T4[i])

        return render_template("electrique.html",datas1=P1,datas2=P2,datas3=P3,datas4=P4 ,labels=label,titre="Temperature journee")

@app.route('/electrique15min.html')  
def elec15():
        label,C1 = ecriture.Read5Sec(table ="COURANTS", index = "POMPE")
        label,C2 = ecriture.Read5Sec(table ="COURANTS", index = "VERIN")
        label,C3 = ecriture.Read5Sec(table ="COURANTS", index = "PANNEAUX")
        label,C4 = ecriture.Read5Sec(table ="COURANTS", index = "BATTERIE")

        label,T1 = ecriture.Read5Sec(table ="TENSION", index = "POMPE")
        label,T2 = ecriture.Read5Sec(table ="TENSION", index = "VERIN")
        label,T3 = ecriture.Read5Sec(table ="TENSION", index = "PANNEAUX")
        label,T4 = ecriture.Read5Sec(table ="TENSION", index = "BATTERIE")

        P1=[]
        P2=[]
        P3=[]
        P4=[]
               
        for i in range(0, len(C1)): #boucle for qui parcourt les tableaux (ils ont tous la même taille)
        #Remplacez Tn[i] par 12  si vous n'avez pas de capteurs de tension
            P1.append(C1[i]*T1[i]) #sert à muliplier les matrice tension et puissance pour obtenir la puissance
            P2.append(C2[i]*T2[i])
            P3.append(C3[i]*T3[i])
            P4.append(C4[i]*T4[i])

        return render_template("electrique.html",datas1=P1,datas2=P2,datas3=P3,datas4=P4 ,labels=label,titre="Temperature journee")

@app.route('/electrique1h.html')  
def elec1():
        label,C1 = ecriture.Read15Sec(table ="COURANTS", index = "POMPE")
        label,C2 = ecriture.Read15Sec(table ="COURANTS", index = "VERIN")
        label,C3 = ecriture.Read15Sec(table ="COURANTS", index = "PANNEAUX")
        label,C4 = ecriture.Read15Sec(table ="COURANTS", index = "BATTERIE")

        label,T1 = ecriture.Read15Sec(table ="TENSION", index = "POMPE")
        label,T2 = ecriture.Read15Sec(table ="TENSION", index = "VERIN")
        label,T3 = ecriture.Read15Sec(table ="TENSION", index = "PANNEAUX")
        label,T4 = ecriture.Read15Sec(table ="TENSION", index = "BATTERIE")

        P1=[]
        P2=[]
        P3=[]
        P4=[]
               
        for i in range(0, len(C1)): #sert à muliplier les matrice tension et puissance pour obtenir la puissance
            P1.append(C1[i]*T1[i])
            P2.append(C2[i]*T2[i])
            P3.append(C3[i]*T3[i])
            P4.append(C4[i]*T4[i])

        return render_template("electrique.html",datas1=P1,datas2=P2,datas3=P3,datas4=P4 ,labels=label,titre="Temperature journee")

@app.route('/electrique8h.html')  
def elec8():
        label,C1 = ecriture.Read1Min(table ="COURANTS", index = "POMPE")
        label,C2 = ecriture.Read1Min(table ="COURANTS", index = "VERIN")
        label,C3 = ecriture.Read1Min(table ="COURANTS", index = "PANNEAUX")
        label,C4 = ecriture.Read1Min(table ="COURANTS", index = "BATTERIE")

        label,T1 = ecriture.Read1Min(table ="TENSION", index = "POMPE")
        label,T2 = ecriture.Read1Min(table ="TENSION", index = "VERIN")
        label,T3 = ecriture.Read1Min(table ="TENSION", index = "PANNEAUX")
        label,T4 = ecriture.Read1Min(table ="TENSION", index = "BATTERIE")

        P1=[]
        P2=[]
        P3=[]
        P4=[]
               
        for i in range(0, len(C1)): #sert à muliplier les matrice tension et puissance pour obtenir la puissance
            P1.append(C1[i]*T1[i])
            P2.append(C2[i]*T2[i])
            P3.append(C3[i]*T3[i])
            P4.append(C4[i]*T4[i])

        return render_template("electrique.html",datas1=P1,datas2=P2,datas3=P3,datas4=P4 ,labels=label,titre="Temperature journee")

@app.route('/electriqueSem.html')  
def elecSem():
        label,C1 = ecriture.Read1H(table ="COURANTS", index = "POMPE")
        label,C2 = ecriture.Read1H(table ="COURANTS", index = "VERIN")
        label,C3 = ecriture.Read1H(table ="COURANTS", index = "PANNEAUX")
        label,C4 = ecriture.Read1H(table ="COURANTS", index = "BATTERIE")

        label,T1 = ecriture.Read1H(table ="TENSION", index = "POMPE")
        label,T2 = ecriture.Read1H(table ="TENSION", index = "VERIN")
        label,T3 = ecriture.Read1H(table ="TENSION", index = "PANNEAUX")
        label,T4 = ecriture.Read1H(table ="TENSION", index = "BATTERIE")

        P1=[]
        P2=[]
        P3=[]
        P4=[]
               
        for i in range(0, len(C1)): #sert à muliplier les matrice tension et puissance pour obtenir la puissance
            P1.append(C1[i]*T1[i])
            P2.append(C2[i]*T2[i])
            P3.append(C3[i]*T3[i])
            P4.append(C4[i]*T4[i])

        return render_template("electrique.html",datas1=P1,datas2=P2,datas3=P3,datas4=P4 ,labels=label,titre="Temperature journee")




@app.route('/ouverture.html')  
def ouv():
        label,data = ecriture.Read15Min(table ="INCLINAISON", index = "CAPOT")
        return render_template("ouverture.html",labels=label,datas=data)

@app.route('/ouverture15min.html')  
def ouv15():
        label,data = ecriture.Read5Sec(table ="INCLINAISON", index = "CAPOT")
        return render_template("ouverture.html",labels=label,datas=data)

@app.route('/ouverture1h.html')  
def ouv1():
        label,data = ecriture.Read15Sec(table ="INCLINAISON", index = "CAPOT")
        return render_template("ouverture.html",labels=label,datas=data)

@app.route('/ouverture8h.html')  
def ouv8():
        label,data = ecriture.Read1Min(table ="INCLINAISON", index = "CAPOT")
        return render_template("ouverture.html",labels=label,datas=data)

@app.route('/ouvertureSem.html')  
def ouvSem():
        label,data = ecriture.Read1H(table ="INCLINAISON", index = "CAPOT")
        return render_template("ouverture.html",labels=label,datas=data)






if __name__ == "__main__": #protection qui autorise le lancement du serveur uniquement si le fichier python est lancé (si ce fichier python est run via un import, le serveur ne sera pas démarré)
       app.run(debug=True, host='0.0.0.0') #Lance le serveur. Host définit l'adresse du serveur et port le port où il sera hébergé.


    
  


