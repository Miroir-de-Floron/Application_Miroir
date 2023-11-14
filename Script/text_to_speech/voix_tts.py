import pyttsx3

#Réflechir à deux vois différente pour les deux méthodes

# fonction(threader) pour lancer le TTS de la prédiction
def annonce_carte(prediction,carte1,carte2,carte3):

    robot_prediction = pyttsx3.init() 
    robot_prediction.stop()
    print("tts en cours ")
    robot_prediction.setProperty('rate', 135)
    robot_prediction.setProperty('voice', 'fr+f5')
    robot_prediction.say(prediction)
    if carte1 == True:
        robot_prediction.say("vien d'étre piocher il vous reste deux carte à piocher")
    if carte2 == True:
        robot_prediction.say("vien d'étre piocher il vous reste une carte à piocher")
    if carte3 == True:
        robot_prediction.say("début des prédiction")
    robot_prediction.runAndWait()
    print("tts terminé")

# fonction(threader) pour lancer le TTS de la prédiction
def lancement_voix_de_prediction(prediction):
    robot_prediction = pyttsx3.init() 
    robot_prediction.stop()
    robot_prediction.setProperty('rate', 105)
    robot_prediction.setProperty('voice', 'fr+f5')
    robot_prediction.say(prediction)
    robot_prediction.runAndWait()
