import threading
import datetime
import time
import pyttsx3
import pygame
import json
import cv2

############################################################################################### Déclaration
# booléen pour savoir si une vidéo de prédiction est en cours de lecture ou non
video_de_prediction = False

pygame.init()

# on charge les fichiers audio de musique 
musique_de_fond = pygame.mixer.Sound("Ressource/Son/Musique_de_fond.mp3")
voix_intro = pygame.mixer.Sound("Ressource/Son/voix_intro.mp3")

fileObject = open("Data/data.json", "r")
jsonContent = fileObject.read()
obj_python = json.loads(jsonContent)

lancement_effets = False
recupération_temps = False

id_passe = None
id_present = None
id_futur = None


######################################################################################################


def lire_video(type):
    global lancement_effets
    global recupération_temps
    global video_de_prediction

    image = cv2.imread("Ressource/image/image.jpg")
    
    if type == 1:
        musique_de_fond.play(-1)
        voix_intro.play(-1)
        chemin_video = 'Ressource/Video/Fond.mp4'

    elif type == 2:
        chemin_video = 'Ressource/Video/Carte.mp4'
    else:
        print("le Type ne correspond pas")
        return

    video = cv2.VideoCapture(chemin_video)
    

    if not video.isOpened():
        print("La vidéo ne s'ouvre pas")
        return
    
    # fréquence d'images par seconde
    fps = video.get(cv2.CAP_PROP_FPS)

    # on récupere kes coordonée de la video
    largeur_video = int(video.get(3))
    hauteur_video = int(video.get(4))

    # on crée une video modfiée
    type_video = cv2.VideoWriter_fourcc(*'mp4v')  
    video_en_sotie = cv2.VideoWriter('Carte.mp4', type_video, fps, (int(video.get(3)), int(video.get(4))))
    

    image_resized = cv2.resize(image, (largeur_video// 2, hauteur_video // 2))

    # Créer une fenêtre
    cv2.namedWindow('Video', cv2.WINDOW_NORMAL)

    # Variable pour contrôler l'affichage de l'image
    afficher_image = False

   
  
    while True:
        #on lance les frame en boucle
        ret, frame = video.read()

        # si on et en fin de vidéo on boucle la vidéo
        if not ret:
            video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        # on fait une copie de la frame (c'est la video qui tourne)
        frame_copy = frame.copy()

        # si un input et rentré on affiche l'image
        if afficher_image == True :
            # on centre l image
            centre_x = (largeur_video - image_resized.shape[1]) // 2
            centre_y = (hauteur_video - image_resized.shape[0]) // 2

            # on superpose l'image
            frame_copy[centre_y:centre_y + image_resized.shape[0], centre_x:centre_x + image_resized.shape[1]] = image_resized

        # on affiche la video
        cv2.imshow('Video', frame_copy)

        # Mettre la fenêtre en plein écran
        cv2.setWindowProperty('Video', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        
        # si l'effet et lancé on met un effet de flou
        if lancement_effets == True:
                afficher_image = True
                frame = cv2.GaussianBlur(frame, (15, 15), 0)
                video_en_sotie.write(frame)
                
                # on récupére le temps une seul fois 
                if recupération_temps == False :
                    temp_actuelle= datetime.datetime.now()

                #on bloque la récupération du temps
                recupération_temps = True

                #tant que les 6 seconde d'animation ne sont pas terminée
                if (datetime.datetime.now() - temp_actuelle).total_seconds() >= 6:  
                    print("mince")
                    recupération_temps = False
                    lancement_effets = False   
                    afficher_image = False

        
        if type == 1 and video_de_prediction == True:
            break
        elif type == 2 and video_de_prediction == False:
            break


        elif cv2.waitKey(25) & 0xFF == ord('q'):
            break

    # on libére les frame et on ferme la video
    video.release()
    cv2.destroyAllWindows()


# fonction(threader) pour lancer le TTS de la prédiction
def lancement_voix_prediction(prediction):
    robot_prediction = pyttsx3.init() 
    robot_prediction.stop()
    print("tts en cours ")
    robot_prediction.setProperty('rate', 135)
    robot_prediction.setProperty('voice', 'fr+f5')
    robot_prediction.say(prediction)
    robot_prediction.runAndWait()
    print("tts terminé")


def lectureDepuisJsonAvecInput(nbTag, temps):
    # On lance la vidéo de prédiction
    for i in range(len(obj_python)):
        if(obj_python[i]['tag'] == int(nbTag)):
            print(obj_python[i]['nom'])
            lancement_voix_prediction(obj_python[i]['prediction'][temps])


# Fonction pour la lecture des vidéos de prediction
def lanceur_video_de_prediction():
    global lancement_effets
    global id_passe
    global id_present
    global id_futur
  
    #on récupère la valeur booléenne la video de prédiction
    global video_de_prediction  

    while True:
        
        
        #on récupére la méthode de l'observateur
        #import Arduino as Card
        #Card.listener_requete.get_id()

        #on récupére les donnée du tableau de l'observateur
   
        if id_passe == None :   
            id_passe = input()
            print("passse",id_passe)
            lancement_effets = True
        
        if id_present is None and id_passe is not None and lancement_effets == False :
            id_present = input()
            print("present",id_present)
            lancement_effets = True

        if id_futur is None and id_passe is not None and lancement_effets == False :
            id_futur = input()
            print("futur",id_futur)
            

        #if(len(Card.listener_requete.Tab_id) == 3):
        if id_futur is not None:
            video_de_prediction = True
            lectureDepuisJsonAvecInput(id_passe, 'passe')
            lectureDepuisJsonAvecInput(id_present, 'passe')
            lectureDepuisJsonAvecInput(id_futur, 'passe')
            id_passe = None
            id_present = None
            id_futur = None
            video_de_prediction = False
                                 

        #Card.listener_requete.Tab_id.clear()
        #Card.listener_requete.ligne_compteur = 0


# Fonction pour la lecture de la vidéo d'introduction
def lanceur_video_intro():
    
    #on lance la video d'introduction
    lire_video(1) 
  
    #on récupère la valeur booléenne de la video de prédiction
    global video_de_prediction

    #on crée un boolén pour savoir si la musique de fond est en cours de lecture ou non
    joue_son = False 

    while True:
        #si la video de prediction ne tourne pas on lance la vidéo d'introduction et la musique de fond
        if video_de_prediction == False and not joue_son:  
            lire_video(1)
            joue_son = True  
        
        #si la video de prédiction tourne on arrête la vidéo d'introduction et la musique de fond
        if video_de_prediction == True:
            musique_de_fond.stop()
            voix_intro.stop()
            joue_son = False
            lire_video(2)
            
        #on attend 0.2 secondes avant de relancer la boucle
        time.sleep(0.2)  

# Création des threads et lancement des fonctions
intro_thread = threading.Thread(target=lanceur_video_de_prediction)
intro_thread.start()
prediction_thread = threading.Thread(target=lanceur_video_intro)
prediction_thread.start()
