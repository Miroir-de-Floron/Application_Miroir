import json
import pyttsx3

fileObject = open("data.json", "r")
jsonContent = fileObject.read()
obj_python = json.loads(jsonContent)
#obj_python = obj_python['objet']

def readingFromJsonAndInput(nbTag, temps):
    for i in range(len(obj_python)):
        if(obj_python[i]['tag'] == int(nbTag)):
            tts = pyttsx3.init() 
            tts.stop()
            print("tts en cours ")
            print(obj_python[i]['nom'])
            tts.setProperty('rate', 135)
            tts.setProperty('voice', 'fr+f5')
            tts.say(obj_python[i]['prediction'][temps])
            tts.runAndWait()
            print("tts terminé")

# print(obj_python)

# input1 = input()

# while(input1 != 'q'):
#     readingFromJsonAndInput(input1, 'present')
#     input1 = input()


input1 = input()
input2 = input()
input3 = input()
readingFromJsonAndInput(input1, 'passe')
readingFromJsonAndInput(input2, 'present')
readingFromJsonAndInput(input3, 'futur')


fileObject.close()