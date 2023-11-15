import pyttsx3
from random import *

flag = False
robot_introduction = None
# fonction(threader) pour lancer le TTS de la prédiction
def annonce_carte(prediction,carte1,carte2,carte3):

    robot_annonce = pyttsx3.init() 
    robot_annonce.stop()
    print("tts en cours ")
    robot_annonce.setProperty('rate', 150)
    robot_annonce.setProperty('voice', 'fr+f5')
    robot_annonce.say(prediction)
    if carte1 == True:
        robot_annonce.say("vien d'étre piocher il vous reste deux carte à piocher")
    if carte2 == True:
        robot_annonce.say("vien d'étre piocher il vous reste une carte à piocher")
    if carte3 == True:
        robot_annonce.say("début des prédiction")
    robot_annonce.runAndWait()
    print("tts terminé")

# fonction(threader) pour lancer le TTS de la prédiction
def lancement_voix_de_prediction(prediction):
    robot_prediction = pyttsx3.init() 
    robot_prediction.stop()
    robot_prediction.setProperty('rate', 150)
    robot_prediction.setProperty('voice', 'fr+f5')
    robot_prediction.say(prediction)
    robot_prediction.runAndWait()



def voix_introduction():

    global robot_introduction

    texte = None
    global flag
    texte_actif = "Approchez, n’ayez crainte, vous êtes en présence de la voyante. Brave sont ceux qui souhaitent faire face à leurs destins... Vos réponses face à l’adversité pourraient se trouver au sein de ces cartes. Le passé, le présent et le futur 3 carte vous devrais tirer pour desceller la vérité."
    texte_inactif = ["Je suis reflet de ce qui vous est étrangé serez vous capable de venir vous présenter.","Les options sont à votre portée, 3 vous devrez en tirer.","Miroir, Miroir..."]

   
    n = randint(0,100)

    if(n <75):
        texte = texte_actif
    else :
        texte = choice(texte_inactif)

    flag = True
    robot_introduction = pyttsx3.init() 
    robot_introduction.setProperty('rate', 150)
    robot_introduction.setProperty('voice', 'fr+f5')
    robot_introduction.say(texte)
    robot_introduction.runAndWait()
    flag = False

def arreter_tts():
    global robot_introduction
    robot_introduction.stop()