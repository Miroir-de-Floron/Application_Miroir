from gtts import gTTS
import os


# fonction(threader) pour lancer le TTS de la prédiction
def annonce_carte(prediction,carte1,carte2,carte3):
    print("tts en cours ")
    tts1 = gTTS(text= prediction, lang='fr', slow=False)
    if carte1 == True:
        text="vien d'étre piocher il vous reste deux carte à piocher"
        tts2 = gTTS(text=text, lang='fr', slow=False)
    if carte2 == True:
        text="vien d'étre piocher il vous reste une carte à piocher"
        tts2 = gTTS(text=text, lang='fr', slow=False)
    if carte3 == True:
        text="début des prédiction"
        tts2 = gTTS(text=text, lang='fr', slow=False)

    tts1.save("output1.mp3")
    tts2.save("output2.mp3")
    os.system("mpg321 output1.mp3")
    os.remove("output1.mp3")
    os.system("mpg321 output2.mp3")
    os.remove("output2.mp3")
    print("tts terminé")

# fonction(threader) pour lancer le TTS de la prédiction
def lancement_voix_de_prediction(prediction):
    tts = gTTS(text=prediction, lang='fr', slow=False)  
    tts.save("output.mp3")
    os.system("mpg321 output.mp3")
    os.remove("output.mp3")

