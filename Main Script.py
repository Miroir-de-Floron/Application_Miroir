import vlc
import threading
import time
import pyttsx3
import pygame
import json
import cv2

############################################################################################### Déclaration
# booléen pour savoir si une vidéo de prédiction est en cours de lecture ou non
video_de_prediction = False

# Création de l'instance VLC
lanceur = vlc.Instance()

pygame.init()

# on charge les fichiers audio de musique 
musique_de_fond = pygame.mixer.Sound("Ressource/Son/Musique_de_fond.mp3")
voix_intro = pygame.mixer.Sound("Ressource/Son/voix_intro.mp3")

fileObject = open("Data/data.json", "r")
jsonContent = fileObject.read()
obj_python = json.loads(jsonContent)


######################################################################################################


def lire_video(type):
    global video_de_prediction

    if type == 1:
        musique_de_fond.play(-1)
        voix_intro.play(-1)
        chemin_video = 'Ressource/Video/Fond.mp4'
    elif type == 2:
        chemin_video = 'Ressource/Video/Carte.mp4'
    else:
        print("le Type ne correspond pa")
        return

    video = cv2.VideoCapture(chemin_video)
    

    if not video.isOpened():
        print("La vidéo ne s'ouvre pas")
        return
    
    #on met en grand écran
    cv2.namedWindow('La Video', cv2.WINDOW_NORMAL)  
    cv2.setWindowProperty('La Video', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    
    while True:
        #on lance les frame en boucle
        ret, frame = video.read()

        # si on et en fin de vidéo on boucle la vidéo
        if not ret:
            video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        # on affiche la video
        cv2.imshow('La Video', frame)

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
  
    #on récupère la valeur booléenne la video de prédiction
    global video_de_prediction  


    while True:
        
        #on récupére la méthode de l'observateur
        #import Arduino as Card
        #Card.listener_requete.get_id()

        #on récupére les donnée du tableau de l'observateur
        id_passe = input()
        id_present = input()
        id_futur = input()
        print(id_futur)
   
        #if(len(Card.listener_requete.Tab_id) == 3):
        if id_futur !=None:
            video_de_prediction = True
            lectureDepuisJsonAvecInput(id_passe, 'passe')
            lectureDepuisJsonAvecInput(id_present, 'passe')
            lectureDepuisJsonAvecInput(id_futur, 'passe')
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
