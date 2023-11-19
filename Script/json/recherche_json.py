import json

fileObject = open("Data/data.json", "r", encoding="utf-8")
jsonContent = fileObject.read()
obj_python = json.loads(jsonContent)

fileObject2 = open("Data/image.json", "r", encoding="utf-8")
jsonContent2 = fileObject2.read()
obj_python2 = json.loads(jsonContent2)

nom = None
color = None
prediction = None


def lectureDepuisJsonAvecInput(nbTag, temps):
    global prediction
    # On lance la vidéo de prédiction
    for i in range(len(obj_python)):
        if(obj_python[i]['tag'] == int(nbTag)):
            prediction = obj_python[i]['prediction'][temps]
            return(obj_python[i]['prediction'][temps])

def rechercheUrlEtNom(nbTag):
    global nom
    global color
    print("le tag et",nbTag)
    # On lance la vidéo de prédiction
    for i in range(len(obj_python2)):
        if(obj_python2[i]['tag'] == int(nbTag)):
            nom = obj_python2[i]['nom']
            color = obj_python2[i]['color']
            return(obj_python2[i]['url'])
