import vlc
import threading
import time
import sqlite3
import pyttsx3
import pygame

# booléen pour savoir si une vidéo de prédiction est en cours de lecture ou non
video_de_prediction = False

# Création de l'instance VLC
lanceur = vlc.Instance()

pygame.init()

# on charge les fichiers audio de musique 
musique_de_fond = pygame.mixer.Sound("Ressource/Son/Musique_de_fond.mp3")
voix_intro = pygame.mixer.Sound("Ressource/Son/voix_intro.mp3")

######################################################################################################



# fonction(threader) pour lancer le TTS de la prédiction
def lancement_voix_prediction(prediction):
    robot_prediction = pyttsx3.init() 
    robot_prediction.stop()
    print("tts en cours ")
    robot_prediction.say(prediction)
    robot_prediction.setProperty('rate', 115)
    robot_prediction.runAndWait()
    print("tts terminé")



# Fonction pour la lecture des vidéos de prediction
def lanceur_video_de_prediction():
    #on se connecte à la base de données
    baseDeDonnees = sqlite3.connect('instance/Tag.db')
    #on crée un curseur pour pouvoir executer des requêtes
    curseur1 = baseDeDonnees.cursor()
    curseur2 = baseDeDonnees.cursor()
    curseur1.execute("SELECT etat FROM tag WHERE nom = 120")
    curseur2.execute("SELECT etat FROM tag WHERE nom = 123")
    #on récupère les valeurs des tags
    Tag1 = curseur1.fetchone()
    Tag2 = curseur2.fetchone()

    #on récupère la valeur booléenne la video de prédiction
    global video_de_prediction  

    #on configure la video de prédiction
    prediction = lanceur.media_list_new()
    prediction.add_media(lanceur.media_new('Ressource/Video/Carte.mp4'))
    media_prediction = lanceur.media_list_player_new()
    media_prediction.set_media_list(prediction)
    media_prediction.get_media_player().set_fullscreen(True)

    while True:
        # On met à jour les valeurs des tagsà chaque tour de boucle
        curseur1.execute("SELECT etat FROM tag WHERE nom = 120")
        curseur2.execute("SELECT etat FROM tag WHERE nom = 123")
        Tag1 = curseur1.fetchone()
        Tag2 = curseur2.fetchone()

        # On vérifie si le tag 120 a été scanné
        if Tag1[0] == True:
            # On lance la vidéo de prédiction
            media_prediction.play()
            video_de_prediction = True
            # On met à jour l'état du tag pour pouvoir le rescaner après
            curseur1.execute("UPDATE tag SET etat = 0 WHERE nom = 120")
            baseDeDonnees.commit()

            # On lance le thread TTS
            tts_thread = threading.Thread(target=lancement_voix_prediction, args=("Vous avez tirez la carte Lune, synonyme d'un grand avenir dans l'astronomie foudroyante.",))
            tts_thread.start()
            tts_thread.join()
            
            #une fois le thread TTS terminé, on arrête la vidéo de prédiction
            video_de_prediction = False
            media_prediction.stop()

        # On vérifie si le tag 123 a été scanné
        if Tag2[0] == True:
            # On lance la vidéo de prédiction
            media_prediction.play()
            video_de_prediction = True
             # On met à jour l'état du tag pour pouvoir le rescaner après
            curseur2.execute("UPDATE tag SET etat = 0 WHERE nom = 123")
            baseDeDonnees.commit()

            # On lance le thread TTS
            tts_thread = threading.Thread(target=lancement_voix_prediction, args=("Vous avez tiré la carte soleil, bohneur sur vous , plein de chance et de reichesses",))
            tts_thread.start()
            tts_thread.join()

            #une fois le thread TTS terminé, on arrête la vidéo de prédiction
            video_de_prediction = False
            media_prediction.stop()




# Fonction pour la lecture de la vidéo d'introduction
def lanceur_video_intro():

    #on configure la vidéo d'introduction
    default = lanceur.media_list_new()
    default.add_media(lanceur.media_new('Ressource/Video/Fond.mp4'))
    media_intro = lanceur.media_list_player_new()
    media_intro.set_media_list(default)
    media_intro.get_media_player().set_fullscreen(True)
    media_intro.set_playback_mode(vlc.PlaybackMode.loop)
    media_intro.play()
    #on configure la musique de fond
    musique_de_fond.play(-1)
    #on configure la voix d'introduction
    voix_intro.play(-1)
    
    #on récupère la valeur booléenne de la video de prédiction
    global video_de_prediction
    #on crée un boolén pour savoir si la musique de fond est en cours de lecture ou non
    joue_son = False 
    while True:
        #si la video de prediction ne tourne pas on lance la vidéo d'introduction et la musique de fond
        if video_de_prediction == False and not joue_son:  
            media_intro.play()
            musique_de_fond.play(-1)
            voix_intro.play(-1)
            joue_son = True  
        
              
        #si la video de prédiction tourne on arrête la vidéo d'introduction et la musique de fond
        if video_de_prediction == True:
            voix_intro.stop()
            media_intro.stop()
            musique_de_fond.stop()
            joue_son = False

        #on attend 0.2 secondes avant de relancer la boucle
        time.sleep(0.2)  

# Création des threads et lancement des fonctions
intro_thread = threading.Thread(target=lanceur_video_de_prediction)
intro_thread.start()
prediction_thread = threading.Thread(target=lanceur_video_intro)
prediction_thread.start()
