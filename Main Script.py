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

prediction = False
lancement_effets = False
carte_txt1 = False
carte_txt2 = False
carte_txt3 = False

id_passe = None
id_present = None
id_futur = None
url_image_carte = None


######################################################################################################

def lire_video():

    ############################################################################## Utilisation de variable commmune
    #variable booléene pour la gestion des effets
    global lancement_effets
    
    # variable contenant l'url de l'image de la carte
    global url_image_carte

    #variable booléene pour savoir si la prédiction et en cours
    global prediction



    ############################################################################## 

    ############################################################################## Déclaration

    #Chemin pour les ressources vidéo
    chemin_video = 'Ressource/Video/voyante.mp4'
    chemin_fumée = 'Ressource/Video/Fumee.mov'
    
    #variable booléene pour vérifier si c'est le moment de récupérer le temp ou non
    recupération_temps = False
   
    #on initialise les vidéo à la bibliothéque cv2
    video = cv2.VideoCapture(chemin_video)
    video_fumée = cv2.VideoCapture(chemin_fumée)
   
    # on récupere les coordonée de la video
    largeur_video = int(video.get(3))
    hauteur_video = int(video.get(4))
    
    ############################################################################## 
    
    
    #exception si l'url de la vidéo n'est pas bonne
    if not video.isOpened():
        print("La vidéo ne s'ouvre pas")
        return

    #On crée une fenêtre
    cv2.namedWindow('Video', cv2.WINDOW_NORMAL)
   
    while True:

        #on lance les frame en boucle
        ret, frame = video.read()
        ret_fumee, frame_fumée = video_fumée.read()

        # si on est en fin de vidéo on boucle la vidéo
        if not ret or not ret_fumee:
            video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            video_fumée.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
        frame_copy = frame.copy()

        cv2.imshow('Video', frame_copy)


        # si l'effet est lancé on affiche l'image avec effet de blur
        if lancement_effets == True:
            
            #On charge l'url_image_carte
            image = cv2.imread(url_image_carte, cv2.IMREAD_UNCHANGED)

            #on redimensionne l'image
            image_resized = cv2.resize(image, (largeur_video//4, hauteur_video//3))

            # on centre l image
            centre_x = (largeur_video - image_resized.shape[1]) // 2
            centre_y = (hauteur_video - image_resized.shape[0]) // 2

             # on copie la vidéo defaut pour les modification
            frame_copy_default = frame_copy.copy()

            #On applique les effets de blur
            frame_copy_default = cv2.GaussianBlur(frame_copy_default, (0, 0), 10)

            # On récuper le canal alpha de l'image PNG
            alpha_channel = image_resized[:, :, 3] / 255.0

            # On superpose l'image avec la transparence du png
            for c in range(0, 3):
                frame_copy_default[centre_y:centre_y + image_resized.shape[0], centre_x:centre_x + image_resized.shape[1], c] = \
                    (1 - alpha_channel) * frame_copy_default[centre_y:centre_y + image_resized.shape[0], centre_x:centre_x + image_resized.shape[1], c] + \
                    alpha_channel * image_resized[:, :, c]

            # On mixe les deux copies pour exclure le flou de l'image
            frame_copy = frame_copy_default
            
            ##################################
            
            # on récupére le temps une seul fois 
            if recupération_temps == False :
                temp_actuelle= datetime.datetime.now()

            #on bloque la récupération du temps
            recupération_temps = True

            #tant que les 5 seconde d'animation ne sont pas terminée on enléve aucun effet
            
            if (datetime.datetime.now() - temp_actuelle).total_seconds() >= 5:  
                recupération_temps = False
                lancement_effets = False   

            cv2.imshow('Video', frame_copy)
        
        
        if prediction == True:
            
            ###################### Application effet de blur
            # on lance les effets
            frame_copy = effets(frame_copy, frame_fumée)

            color = script.json.recherche_json.color
            couleur_opencv = getattr(cv2, f"COLOR_{color}")
            frame_color = cv2.cvtColor(frame_copy, couleur_opencv)

            # On charge l'url_image_carte
            image = cv2.imread(url_image_carte, cv2.IMREAD_UNCHANGED)

            # On redimensionne l'image
            image_resized = cv2.resize(image, (largeur_video//4, hauteur_video//3))

            # On centre l'image
            centre_x = (largeur_video - image_resized.shape[1]) // 2
            centre_y = (hauteur_video - image_resized.shape[0]) // 2

            # On copie la vidéo defaut pour les modifications
            frame_copy_default = frame_copy.copy()

            # On applique les effets de blur
            frame_copy_default = cv2.GaussianBlur(frame_copy_default, (0, 0), 10)

            # On récupère le canal alpha de l'image PNG
            alpha_channel = image_resized[:, :, 3] / 255.0

            # On superpose l'image avec la transparence du png
            for c in range(0, 3):
                frame_copy_default[centre_y:centre_y + image_resized.shape[0], centre_x:centre_x + image_resized.shape[1], c] = \
                    (1 - alpha_channel) * frame_copy_default[centre_y:centre_y + image_resized.shape[0], centre_x:centre_x + image_resized.shape[1], c] + \
                    alpha_channel * image_resized[:, :, c]

            # On utilise addWeighted pour fusionner les deux  frame donc effet de couleur et image
            frame_result = cv2.addWeighted(frame_color, 0.5, frame_copy_default, 0.5, 0)

            cv2.imshow('Video', frame_result)
                    

            ##################################
    
        
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

def tts_carte(carte_tag):
    global carte_txt1
    global carte_txt2
    global carte_txt3

    # musique_de_fond.fadeout(1)
    script.text_to_speech.voix_tts.annonce_carte(carte_tag,carte_txt1,carte_txt2,carte_txt3)
    script.json.recherche_json.fileObject.close()
  

# Fonction pour la lecture des vidéos de prediction
def gestion_des_prediction():

    ############################################################################## Utilisation de variable commmune
    #variable booléene pour la gestion des effets
    global lancement_effets

    #variables des 3 id des 3 carte scanées respectivement
    global id_passe
    global id_present
    global id_futur

    # variable qui contient l'url de l'image (contenue dans un json), de la carte rentrée
    global url_image_carte 

    #variables booléene pour savoir quel texte énoncé selon la carte rentrée
    global carte_txt1
    global carte_txt2
    global carte_txt3

    #variable booléene pour savoir si la prédiction et en cours
    global prediction 



    ##############################################################################

    ############################################################################## Déclaration

    # variable booléene permettant d'ajuster le départ de chaque condition
    declencheur_present= False
    declencheur_futur = False

    #variables booléene qui permetent de savoir si les annonces (passe,present et futur) on était réalisé
    fin_passe = False
    fin_present = False
    fin_futur = False
    ############################################################################## 

    while True:

        import Arduino as Card
        #on récupére les donnée du tableau de l'observateur
        Card.listener_requete.get_id()
        global voix_intro_flag
        voix_intro_flag = False

        #si l'id du passée n'existe pas on affecte la valeur de l'id passe au premiére id du tableau
        if id_passe is None :
            id_passe = Card.listener_requete.Tab_id[0]

        #si l'id du passée existe , que le déclencheur de l'évenement présent est activer et que le resultat renvoyé est différent de l'id affecter précedement
        #on affecte la valeur de l'id present au deuxiéme id du tableau
        if id_passe is not None and declencheur_present== True and Card.listener_requete.result != id_passe:
            id_present = Card.listener_requete.Tab_id[1]
            declencheur_present= False
        # exception
        else :
            print("le tableau n'est pas à la bonne taille car vous avez rentrez deux fois la même carte")

        #si l'id du présent existe , que le déclencheur de l'évenement futur est activer et que le resultat renvoyé est différent de l'id affecter précedement
        #on affecte la valeur de l'id futur au troisiéme id du tableau
        if id_present is not None and declencheur_futur == True and Card.listener_requete.result != id_present :

            id_futur = Card.listener_requete.Tab_id[2]
            declencheur_futur = False

        #exception
        else :
            print("le tableau n'est pas à la bonne taille car vous avez rentrez deux fois la même carte")
    


        # si l'id du passé est non null ,que l'id du présent n'a pas était encore rentré et que on est jamais rentré dans cette condition
        #on peut donc jouer les animation pour le passé
        if id_passe is not None and id_present is None and fin_passe == False :

            url_image_carte = script.json.recherche_json.rechercheUrlEtNom(id_passe)
            
            #on indique l'identité de la carte et on lance les effet
            lancement_effets = True
            carte_txt1 = True

            # on lance le tts d'annonce de carte
            tts_carte(script.json.recherche_json.nom)


            #on annonce que la prediction est en cours
            prediction = True
          

            #on lance la recherche de la prédiction puis le tts
            script.json.recherche_json.lectureDepuisJsonAvecInput(id_passe, 'passe')
            script.text_to_speech.voix_tts.lancement_voix_de_prediction(script.json.recherche_json.prediction,carte_txt1,carte_txt2,carte_txt3)
            
            #on enleve tout les précedents effets
            prediction = False
            carte_txt1 = False

            # on indique l'animation present peut etre lancée
            declencheur_present= True
            #on attend un peu
            time.sleep(1)
            #on indique que l'on peut plus passée ici tant que les trois prédiction n'ont pas était dite
            fin_passe = True

            # musique_de_fond.play(-1)

        # si l'id du présent est non null ,que l'id du futur n'a pas était encore rentré et que on est jamais rentré dans cette condition
        #on peut donc jouer les animation pour le présent
        if id_present is not None and id_futur is None and fin_present == False and fin_futur == False:


            url_image_carte = script.json.recherche_json.rechercheUrlEtNom(id_present)
            
            #on indique l'identité de la carte et on lance les effet
            lancement_effets = True
            carte_txt2 = True

            # on lance le tts d'annonce de carte
            tts_carte(script.json.recherche_json.nom)



            #on annonce que la prediction et en cours
            prediction = True


            #on lance la recherche de la prédiction puis le tts
            script.json.recherche_json.lectureDepuisJsonAvecInput(id_present, 'present')
            script.text_to_speech.voix_tts.lancement_voix_de_prediction(script.json.recherche_json.prediction,carte_txt1,carte_txt2,carte_txt3)
            
            #on enleve tout les précedent effet
            prediction = False
            carte_txt2 = False

            # on indique l'animation present peut etre lancée
            declencheur_futur= True
            #on attend un peu
            time.sleep(1)
            #on indique que l'on peut plus passée ici tant que les trois prédiction n'ont pas était dite
            fin_present = True


        #si l'id du futur n'est pas null
        #on peut donc jouer les animation pour le futur
        if id_futur is not None :

            #on attend que le processus soit bien tuer
            time.sleep(0.5)

            url_image_carte = script.json.recherche_json.rechercheUrlEtNom(id_futur)
            
            #on indique l'identité de la carte et on lance les effet
            lancement_effets = True
            carte_txt3 = True

            # on lance le tts d'annonce de carte
            tts_carte(script.json.recherche_json.nom)

           

            #on annonce que la prediction et en cours
            prediction = True

            #on lance la recherche de la prédiction puis le tts
            script.json.recherche_json.lectureDepuisJsonAvecInput(id_futur, 'futur')
            script.text_to_speech.voix_tts.lancement_voix_de_prediction(script.json.recherche_json.prediction,carte_txt1,carte_txt2,carte_txt3)
            
            #on enleve tout les précedents effets
            prediction = False
            carte_txt3 = False


            # comme les prédictions sont terminée on reset toutes les variables (id,tableau et flag de condition)
            id_passe = None
            id_present = None
            id_futur = None
        
            Card.listener_requete.Tab_id.clear()
            
            #compteur de ligne dans le serial monitor remi à zero
            Card.listener_requete.ligne_compteur = 0

            time.sleep(1)

            fin_passe = False
            fin_present = False
            fin_futur= False

            voix_intro_flag = True
            
            
            
#les voix ce chevauche mais c'est réglabe (je pense)   
def voix_intro():
    global voix_intro_flag
    voix_intro_flag = True
    chanel_d_intro = script.text_to_speech.voix_tts.voix_introduction()
    stoped = False
    while True:
        if voix_intro_flag:
            if not chanel_d_intro.get_busy():
                time.sleep(20)
                chanel_d_intro = script.text_to_speech.voix_tts.voix_introduction()
        else : 
            if not stoped:
                chanel_d_intro.stop()
                stoped = True




# Création des threads et lancement des fonctions
intro_thread = threading.Thread(target=gestion_des_prediction)
intro_thread.start()
prediction_thread = threading.Thread(target=lire_video)
prediction_thread.start()
voix_intro_thread = threading.Thread(target=voix_intro)
voix_intro_thread.start()
