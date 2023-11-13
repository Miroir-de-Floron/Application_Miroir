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

fileObject2 = open("Data/image.json", "r")
jsonContent2 = fileObject2.read()
obj_python2 = json.loads(jsonContent2)

lancement_effets = False
recupération_temps = False
carte_txt1 = False
carte_txt2 = False
carte_txt3 = False

id_passe = None
id_present = None
id_futur = None
url = None
nom = None


######################################################################################################


def lire_video(type):
    global lancement_effets
    global recupération_temps
    global video_de_prediction
    global url
 
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
    
    #exception 
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
        frame_copy = frame.copy()
    
        # si un input et rentré on affiche l'image
        if afficher_image == True :
            
            #On charge l'url
            image = cv2.imread(url)
            #on redimensionne l'image
            image_resized = cv2.resize(image, (largeur_video// 2, hauteur_video // 2))
            # on centre l image
            centre_x = (largeur_video - image_resized.shape[1]) // 2
            centre_y = (hauteur_video - image_resized.shape[0]) // 2

            # on copie la vidéo defaut pour les modification
            frame_copy = frame.copy()
            frame_copy_default = frame_copy.copy()

            ####################### Application effet de blur

            # on met un effet de flou à la vidéo originale
            frame_copy_default = cv2.GaussianBlur(frame_copy_default, (0, 0), 10)

            # on superpose l'image sur la vidéo avec le blur
            frame_copy_default[centre_y:centre_y + image_resized.shape[0], centre_x:centre_x + image_resized.shape[1]] = image_resized

            #on mix les deux copie pour exlure le flou de l'image
            frame_copy = frame_copy_default

            ##################################

        # si l'effet et lancé on affiche l'image avec effet de blur
        if lancement_effets == True:
                afficher_image = True
                frame = cv2.GaussianBlur(frame, (15, 15), 0)
                video_en_sotie.write(frame)
                
                # on récupére le temps une seul fois 
                if recupération_temps == False :
                    temp_actuelle= datetime.datetime.now()

                #on bloque la récupération du temps
                recupération_temps = True

                #tant que les 4 seconde d'animation ne sont pas terminée on enléve aucun effet
                
                if (datetime.datetime.now() - temp_actuelle).total_seconds() >= 4:  
                    print("mince")
                    recupération_temps = False
                    lancement_effets = False   
                    afficher_image = False
                

         # on affiche la video
        cv2.imshow('Video', frame_copy)



        # Mettre la fenêtre en plein écran
        cv2.setWindowProperty('Video', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)


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
def lancement_voix(prediction):

    global carte_txt1
    global carte_txt2
    global carte_txt3

    robot_prediction = pyttsx3.init() 
    robot_prediction.stop()
    print("tts en cours ")
    robot_prediction.setProperty('rate', 135)
    robot_prediction.setProperty('voice', 'fr+f5')
    robot_prediction.say(prediction)
    if carte_txt1 == True:
        robot_prediction.say("vien d'étre piocher il vous reste deux carte à piocher")
    if carte_txt2 == True:
        robot_prediction.say("vien d'étre piocher il vous reste une carte à piocher")
    if carte_txt3 == True:
        robot_prediction.say("début des prédiction")
    robot_prediction.runAndWait()
    print("tts terminé")


def lectureDepuisJsonAvecInput(nbTag, temps):
    # On lance la vidéo de prédiction
    for i in range(len(obj_python)):
        if(obj_python[i]['tag'] == int(nbTag)):
            print(obj_python[i]['nom'])
            lancement_voix(obj_python[i]['prediction'][temps])

def rechercheUrlEtNom(nbTag):
    global nom
    # On lance la vidéo de prédiction
    for i in range(len(obj_python2)):
        if(obj_python2[i]['tag'] == int(nbTag)):
            nom = obj_python2[i]['nom']
            return(obj_python2[i]['url'])
            
def tts_carte(carte_tag,id):
    musique_de_fond.fadeout(1)
    voix_intro.fadeout(1)
    lancement_voix(carte_tag)
    if id != 3:
        musique_de_fond.play(-1)
        voix_intro.play(-1)

# Fonction pour la lecture des vidéos de prediction
def lanceur_video_de_prediction():
    global lancement_effets
    global id_passe
    global id_present
    global id_futur
    global url
    global nom
    global carte_txt1
    global carte_txt2
    global carte_txt3
  
    #on récupère la valeur booléenne la video de prédiction
    global video_de_prediction  

    while True:

        ### Pour Rfid
        #on récupére la méthode de l'observateur
        #import Arduino as Card
        #Card.listener_requete.get_id()

        #on récupére les donnée du tableau de l'observateur

        #si il n'y a pas d'id passé on rentre un tag
        if id_passe == None :   

            id_passe = input()
            url = rechercheUrlEtNom(id_passe)

            #on indique qu'on lance les effet de la carte et le tts
            lancement_effets = True
            carte_txt1 = True

            # on coupe le son le temps du tts d'anonce de carte
            tts_carte(nom,1)

            #on indique que le passage de la carte passé et terminer
            carte_txt1 = False

        #si il n'y a pas d'id present et que le précedent à était rentrée on rentre l'id présent
        if id_present is None and id_passe is not None and lancement_effets == False :
            
            id_present = input()
            url = rechercheUrlEtNom(id_present) 

            #on indique qu'on lance les effet de la carte et le tts
            lancement_effets = True
            carte_txt2 = True

            # on coupe le son le temps du tts d'anonce de carte
            tts_carte(nom,2)

            #on indique que le passage de la carte présent et terminer
            carte_txt2 = False

        #si il n'y a pas d'id futur et que le précedent à était rentrée on rentre l'id futur
        if id_futur is None and id_passe is not None and lancement_effets == False :

            id_futur = input()
            url = rechercheUrlEtNom(id_futur)

            #on indique qu'on lance les effet de la carte et le tts
            lancement_effets = True
            carte_txt3 = True
            
            # on coupe le son le temps du tts d'anonce de carte
            tts_carte(nom,3)

            #on indique que le passage de la carte futur et terminer
            carte_txt3 = False

        ### Pour Rfid
        #if(len(Card.listener_requete.Tab_id) == 3):

        #si le derniére id et rentrée on lance la vidéo de prediction avec le tts
        if id_futur is not None and lancement_effets == False:
            video_de_prediction = True
            lectureDepuisJsonAvecInput(id_passe, 'passe')
            lectureDepuisJsonAvecInput(id_present, 'passe')
            lectureDepuisJsonAvecInput(id_futur, 'passe')
            #une fois fini on remet tout à None pour pouvoir recommencer 
            id_passe = None
            id_present = None
            id_futur = None
            video_de_prediction = False
                                 
        ### Pour Rfid
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

        # si les carte sont joué
        if carte_txt1 == True :
            musique_de_fond.stop()
            voix_intro.stop()
            joue_son = False


        #si la video de prediction ne tourne pas on lance la vidéo d'introduction et la musique de fond
        if video_de_prediction == False and not joue_son:  
            lire_video(1)
            joue_son = True  
        
        #si la video de prédiction tourne on arrête la vidéo d'introduction et la musique de fond
        if video_de_prediction == True :
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
