import json

fileObject = open("Data/data.json", "r", encoding="utf-8")
jsonContent = fileObject.read()
obj_python = json.loads(jsonContent)

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
    # On lance la vidéo de prédiction
    for i in range(len(obj_python)):
        if(obj_python[i]['tag'] == int(nbTag)):
            nom = obj_python[i]['nom']
            color = obj_python[i]['color']
            return(obj_python[i]['url'])
