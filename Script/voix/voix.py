from random import *
import pygame
from waiting import wait

flag = False
robot_introduction = None
cheminParDefault = "Ressource/Son/"
# fonction(threader) pour lancer le TTS de la prédiction
def annonce_carte(urlNomCarte,carte1,carte2,carte3):
    voix_de_nom = pygame.mixer.Sound(cheminParDefault+urlNomCarte)
    chanel_de_nom = voix_de_nom.play()
    wait(lambda:audioFinished(chanel_de_nom))
    if carte1 == True:
        voix_de_nom_passe = pygame.mixer.Sound(cheminParDefault+"nom_passe.mp3")
        chanel_de_nom_passe = voix_de_nom_passe.play()
        wait(lambda:audioFinished(chanel_de_nom_passe))
    if carte2 == True:
        voix_de_nom_present = pygame.mixer.Sound(cheminParDefault+"nom_present.mp3")
        chanel_de_nom_present = voix_de_nom_present.play()
        wait(lambda:audioFinished(chanel_de_nom_present))
    if carte3 == True:
        voix_de_nom_futur = pygame.mixer.Sound(cheminParDefault+"nom_futur.mp3")
        chanel_de_nom_futur = voix_de_nom_futur.play()
        wait(lambda:audioFinished(chanel_de_nom_futur))


# fonction(threader) pour lancer le TTS de la prédiction
def lancement_voix_de_prediction(prediction,carte1,carte2,carte3):
    voix_de_prediction = pygame.mixer.Sound(cheminParDefault+prediction)
    chanel_de_prediction = voix_de_prediction.play()
    wait(lambda:audioFinished(chanel_de_prediction))
    
    if carte1 == True:
        voix_de_prediction_passe = pygame.mixer.Sound(cheminParDefault+"prediction_passe.mp3")
        chanel_de_prediction_passe = voix_de_prediction_passe.play()
        wait(lambda:audioFinished(chanel_de_prediction_passe))
    if carte2 == True:
        voix_de_prediction_present = pygame.mixer.Sound(cheminParDefault+"prediction_present.mp3")
        chanel_de_prediction_present = voix_de_prediction_present.play()
        wait(lambda:audioFinished(chanel_de_prediction_present))
    if carte3 == True:
        voix_de_prediction_futur = pygame.mixer.Sound(cheminParDefault+"prediction_futur.mp3")
        chanel_de_prediction_futur = voix_de_prediction_futur.play()
        wait(lambda:audioFinished(chanel_de_prediction_futur))


def voix_introduction():

    global robot_introduction

    texte = None
    global flag
    intro_texts = ["texte_actif.mp3", "texte_inactif_1.mp3", "texte_inactif_2.mp3", "texte_inactif_3.mp3"]

    texte = intro_texts[0]
    n = randint(0,100)

    if n < 75:
        texte = intro_texts[0]
    elif n < 85 :
        texte = intro_texts[1]
    elif n < 95 :
        texte = intro_texts[2]
    elif n > 95 :
        texte = intro_texts[3]
    else : 
        print("probleme voix d'intro")

    flag = True
    voix_d_intro = pygame.mixer.Sound(cheminParDefault+texte)
    chanel_d_intro = voix_d_intro.play()
    return chanel_d_intro
    flag = False



def audioFinished( chanel ):
    if not chanel.get_busy():
        return True
    return False