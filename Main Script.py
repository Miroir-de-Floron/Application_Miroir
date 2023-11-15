import threading
import datetime
import time
import pygame
import cv2
import Script as script
############################################################################################### Déclaration
# booléen pour savoir si une vidéo de prédiction est en cours de lecture ou non
video_de_prediction = False

pygame.init()

# on charge les fichiers audio de musique 
musique_de_fond = pygame.mixer.Sound("Ressource/Son/Musique_de_fond.mp3")
pygame.mixer.music.set_volume(0.2)

prediction = False
lancement_effets = False
recupération_temps = False
carte_txt1 = False
carte_txt2 = False
carte_txt3 = False

id_passe = None
id_present = None
id_futur = None
url = None

nom_passe = None
nom_present = None

nom1 = False
nom2 = False

stop = False
######################################################################################################

def lire_video():
    global lancement_effets
    global recupération_temps
    global url
    global prediction
    global nom_passe
    global nom_present
    global nom1
    global nom2
 
    chemin_video = 'Ressource/Video/Fond.mp4'
    chemin_fumée = 'Ressource/Video/Fumee.mov'

    musique_de_fond.play(-1)
   
    video = cv2.VideoCapture(chemin_video)
    video_fumée = cv2.VideoCapture(chemin_fumée)
    
    #exception 
    if not video.isOpened():
        print("La vidéo ne s'ouvre pas")
        return
    
    # fréquence d'images par seconde
    fps = video.get(cv2.CAP_PROP_FPS)

    # on récupere kes coordonée de la video
    largeur_video = int(video.get(3))
    hauteur_video = int(video.get(4))

    
    # Créer une fenêtre
    cv2.namedWindow('Video', cv2.WINDOW_NORMAL)
   
    while True:

        #on lance les frame en boucle
        ret, frame = video.read()
        ret_fumee, frame_fumée = video_fumée.read()

        # si on et en fin de vidéo on boucle la vidéo
        if not ret or not ret_fumee:
            video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            video_fumée.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
        frame_copy = frame.copy()


        # si l'effet et lancé on affiche l'image avec effet de blur
        if lancement_effets == True:
                
            #On charge l'url
            image = cv2.imread(url)
            #on redimensionne l'image
            image_resized = cv2.resize(image, (largeur_video// 4, hauteur_video // 3))
            # on centre l image
            centre_x = (largeur_video - image_resized.shape[1]) // 2
            centre_y = (hauteur_video - image_resized.shape[0]) // 2

            # on copie la vidéo defaut pour les modification
            frame_copy_default = frame_copy.copy()

            ####################### Application effet de blur

            # on met un effet de flou à la vidéo originale
            frame_copy_default = cv2.GaussianBlur(frame_copy_default, (0, 0), 10)

            # on superpose l'image sur la vidéo avec le blur
            frame_copy_default[centre_y:centre_y + image_resized.shape[0], centre_x:centre_x + image_resized.shape[1]] = image_resized

            #on mix les deux copie pour exlure le flou de l'image
            frame_copy = frame_copy_default
            
            ##################################
            
            # on récupére le temps une seul fois 
            if recupération_temps == False :
                temp_actuelle= datetime.datetime.now()

            #on bloque la récupération du temps
            recupération_temps = True

            #tant que les 5 seconde d'animation ne sont pas terminée on enléve aucun effet
            
            if (datetime.datetime.now() - temp_actuelle).total_seconds() >= 5:  
                print("mince")
                recupération_temps = False
                lancement_effets = False   
        
        
        if prediction == True:
            
            ####################### Application effet de blur
                # on lance les effets
            frame_copy = effets(frame_copy,frame_fumée)


            # Définir les propriétés du texte
            police = cv2.FONT_HERSHEY_SIMPLEX
            position = (800, 500)
            taille_police = 2
            couleur_police = (255, 255, 255)
            espacement = 2

            if nom1 :
                text = nom_passe
            elif nom2 :
                text = nom_present
            else :    
                text = script.json.recherche_json.nom

            text = text.encode('utf-8').decode('utf-8')   

            cv2.putText(frame_copy, text, position, police, taille_police, couleur_police, espacement)

        
            ##################################



    
         # on affiche la video
        cv2.imshow('Video', frame_copy)

        # Mettre la fenêtre en plein écran
        cv2.setWindowProperty('Video', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    # on libére les frame et on ferme la video
    video.release()
    video_fumée.release()
    cv2.destroyAllWindows()

def effets(frame_copy,frame_fumée):
    global prediction
    if prediction == True :
        frame_fumée_resized = cv2.resize(frame_fumée, (frame_copy.shape[1], frame_copy.shape[0]))
        return cv2.addWeighted(frame_copy, 0.5, frame_fumée_resized, 0.5, 0)
    return frame_copy

def tts_carte(carte_tag,id):
    global carte_txt1
    global carte_txt2
    global carte_txt3
    global stop

    musique_de_fond.fadeout(1)
    stop = True
    script.text_to_speech.voix_tts.annonce_carte(carte_tag,carte_txt1,carte_txt2,carte_txt3)
    script.json.recherche_json.fileObject2.close()
    if id != 3:
        musique_de_fond.play(-1)

# Fonction pour la lecture des vidéos de prediction
def gestion_des_prediction():
    global lancement_effets
    global id_passe
    global id_present
    global id_futur
    global url 
    global carte_txt1
    global carte_txt2
    global carte_txt3
    global nom1
    global nom2
  
    #on récupère la valeur booléenne de la prédiction
    global prediction  
    global nom_passe
    global nom_present

    while True:

        ### Pour Rfid
        #on récupére la méthode de l'observateur
        #import Arduino as Card
        #Card.listener_requete.get_id()

        #on récupére les donnée du tableau de l'observateur

        #si il n'y a pas d'id passé on rentre un tag
        if id_passe == None :   

            id_passe = input()
            url = script.json.recherche_json.rechercheUrlEtNom(id_passe)

            #on indique qu'on lance les effet de la carte et le tts
            lancement_effets = True
            carte_txt1 = True

            # on coupe le son le temps du tts d'anonce de carte
            tts_carte(script.json.recherche_json.nom,1)
            nom_passe = script.json.recherche_json.nom

            #on indique que le passage de la carte passé et terminer
            carte_txt1 = False

        #si il n'y a pas d'id present et que le précedent à était rentrée on rentre l'id présent
        if id_present is None and id_passe is not None and lancement_effets == False :
            
            id_present = input()
            url = script.json.recherche_json.rechercheUrlEtNom(id_present) 

            #on indique qu'on lance les effet de la carte et le tts
            lancement_effets = True
            carte_txt2 = True

            # on coupe le son le temps du tts d'anonce de carte
            tts_carte(script.json.recherche_json.nom,2)
            nom_present = script.json.recherche_json.nom

            #on indique que le passage de la carte présent et terminer
            carte_txt2 = False

        #si il n'y a pas d'id futur et que le précedent à était rentrée on rentre l'id futur
        if id_futur is None and id_passe is not None and lancement_effets == False :

            id_futur = input()
            url = script.json.recherche_json.rechercheUrlEtNom(id_futur)

            #on indique qu'on lance les effet de la carte et le tts
            lancement_effets = True
            carte_txt3 = True
            
            # on coupe le son le temps du tts d'anonce de carte
            tts_carte(script.json.recherche_json.nom,3)

            #on indique que le passage de la carte futur et terminer
            carte_txt3 = False

        ### Pour Rfid
        #if(len(Card.listener_requete.Tab_id) == 3):

        #si le derniére id et rentrée on lance la vidéo de prediction avec le tts
        if id_futur is not None and lancement_effets == False:
            prediction = True
            nom1 = True
            script.json.recherche_json.lectureDepuisJsonAvecInput(id_passe, 'passe')
            script.text_to_speech.voix_tts.lancement_voix_de_prediction(script.json.recherche_json.prediction)
            nom1 = False
            nom2 = True
            script.json.recherche_json.lectureDepuisJsonAvecInput(id_present, 'present')
            script.text_to_speech.voix_tts.lancement_voix_de_prediction(script.json.recherche_json.prediction)
            nom2 = False
            script.json.recherche_json.lectureDepuisJsonAvecInput(id_futur, 'futur')
            script.text_to_speech.voix_tts.lancement_voix_de_prediction(script.json.recherche_json.prediction)
            script.json.recherche_json.fileObject.close()
            prediction = False
            musique_de_fond.play(-1)
            #voix_intro.play(-1)
            #une fois fini on remet tout à None pour pouvoir recommencer 
            id_passe = None
            id_present = None
            id_futur = None
                                 
        ### Pour Rfid
        #Card.listener_requete.Tab_id.clear()
        #Card.listener_requete.ligne_compteur = 0

def musique():
     while True:
        if script.text_to_speech.voix_tts.flag == False :
            script.text_to_speech.voix_tts.voix_introduction()
            time.sleep(25)


     
# Création des threads et lancement des fonctions
intro_thread = threading.Thread(target=gestion_des_prediction)
intro_thread.start()
prediction_thread = threading.Thread(target=lire_video)
prediction_thread.start()
musique_thread = threading.Thread(target=musique)
musique_thread.start() 
