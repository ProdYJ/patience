#import des packages nécessaires
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

#initialisation du chrono
start_time = time.time()

#on initialise les paramère de la caméra
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 24
time.sleep(2)
#on laisse un peu de temps à la caméra pour chauffer
time.sleep(1)

#définition du seuil pour le trheshold
seuil = 50
#définition de s valeurs du filtre de kernell pour la dilation
kernel_dilation = np.ones((5,5), np.uint8)
#capture d'images et traitement

def ICU(icu_enable):
    if icu_enable == True :
        icu_value = False
        #on prend des images avec un petit lapse de temps entre les deux
        image1 = np.empty((320*240*3), dtype=np.uint8)
        camera.capture(image1,'bgr')
        image1 = image1.reshape((240,320,3))
        image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        image2 = np.empty((320*240*3), dtype=np.uint8)
        camera.capture(image2,'bgr')
        image2 = image2.reshape((240,320,3))
        image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(image1, image2)
        detection = cv2.threshold(diff, seuil, 255, cv2.THRESH_BINARY)[1]
        #on amplifie les résultats de  la détection
        detection = cv2.dilate(detection, kernel_dilation, iterations = 3)
        #on détecte les contours ressortis par le threshold
        contours, hierarchy = cv2.findContours(detection,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]
        #le [-2:]sert à ne prendre que les deux dernière valeurs du tableau d'objets
        #retourné par fincountours
        #on regarde la surface de la région sortant de la détection
        #pour ce faire on somme la surface de tous les contours trouvés
        nombre = len(contours)
        #on affiche l'image dans une fenêtre
        cv2.imshow("image1",image1)
        cv2.imshow("image2",image2)
        cv2.imshow("detection",detection)
        #on prépare la fermeture du programme
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q") :
         break
        #on propose d'adapter la sensibilité
        if key == ord("+") :
         seuil = seuil + 1
        if key == ord("-") :
         seuil = seuil - 1
        print ( "start : ",start_time,"capture : ",time.time())
        print (seuil)
        print (nombre)
        if nombre > 0  :
            icu_value = True
            
    elif icu_enable==False
        icu_value = False

return icu_value


