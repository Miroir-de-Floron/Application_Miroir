import threading
import datetime
import time
import pygame
import cv2
import Script as script
from waiting import wait

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ déclaration ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

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

fin_passe = False
fin_present = False

effet = 'Ressource/Video/Fumee.mov'


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ fonction de lecture des vidéos ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def lire_video():

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ utilisation des variables global ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    #variable booléene pour la gestion des effets
    global lancement_effets
    
    # variable contenant l'url de l'image de la carte
    global url_image_carte

    #variable booléene pour savoir si la prédiction et en cours
    global prediction
    
    global effet


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ déclaration ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

    #Chemin pour les ressources vidéo
    chemin_video = 'Ressource/Video/voyante.mp4'
    
    #variable booléene pour vérifier si c'est le moment de récupérer le temp ou non
    recupération_temps = False
   
    #on initialise les vidéo à la bibliothéque cv2
    video = cv2.VideoCapture(chemin_video)
   
    # on récupere les coordonée de la video
    largeur_video = int(video.get(3))
    hauteur_video = int(video.get(4))
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    
    #exception si l'url de la vidéo n'est pas bonne
    if not video.isOpened():
        print("La vidéo ne s'ouvre pas")
        return

    #On crée une fenêtre
    cv2.namedWindow('Video', cv2.WINDOW_NORMAL)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ boucle de lecture des video ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    while True:

        video_fumée = cv2.VideoCapture(effet)
        #on lance les frames en boucle
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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ effet de flou ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

            #On applique les effets de flou
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
            
            
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
            
            # on récupére le temps une seul fois 
            if recupération_temps == False :
                temp_actuelle= datetime.datetime.now()

            #on bloque la récupération du temps
            recupération_temps = True

            #tant que les 5 secondes d'animation ne sont pas terminée on enléve aucun effet
            
            if (datetime.datetime.now() - temp_actuelle).total_seconds() >= 5:  
                recupération_temps = False
                lancement_effets = False   

            cv2.imshow('Video', frame_copy)
        
        
        if prediction == True:
            
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ application de l'effet de flou ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
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

            # On applique les effets de flou
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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    
        
        # Mettre la fenêtre en plein écran
        cv2.setWindowProperty('Video', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ liberation des frames plus fermeture de la video ~~~~~~~~~~~~~~~~~~~~#
    video.release()
    video_fumée.release()
    cv2.destroyAllWindows()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ fonction des effets des vidéos de prediction ~~~~~~~~~~~~~~~~~~~~~~~~#
def effets(frame_copy,frame_fumée):
    global prediction
    if prediction :
        frame_fumée_resized = cv2.resize(frame_fumée, (frame_copy.shape[1], frame_copy.shape[0]))
        return cv2.addWeighted(frame_copy, 0.5, frame_fumée_resized, 0.5, 0)
    return frame_copy

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ fonction de lecture des voix tts des predictions ~~~~~~~~~~~~~~~~~~~~#
def tts_carte(carte_tag):
    global carte_txt1
    global carte_txt2
    global carte_txt3
    script.voix.voix.annonce_carte(carte_tag,carte_txt1,carte_txt2,carte_txt3)
    script.json.recherche_json.fileObject.close()
  
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ fonction de lecture des vidéos de prediction ~~~~~~~~~~~~~~~~~~~~~~~~#
# Fonction pour la lecture des vidéos de prediction

stop_prediction_thread = threading.Event()
def gestion_des_prediction():
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ utilisation de varibles globale ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

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
    
    #variables booléene qui permetent de savoir si les annonces (passe,present et futur) on était réalisé
    global fin_passe 
    global fin_present 
    
    #effet de video
    global effet

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ debut boucle ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

    while True:

        import Arduino as Card
        #on récupére les donnée du tableau de l'observateur
        Card.listener_requete.get_id()
        global voix_intro_flag
        voix_intro_flag = False
        

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Affectation Passé ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

        #si l'id du passée n'existe pas on affecte la valeur de l'id passe au premiére id du tableau
        if id_passe is None :
            id_passe = Card.listener_requete.Tab_id[0]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Affectation Present ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

        #si l'évenement passé est fini et qu'un resultat a etait envoyé
        #on affecte la valeur du deuxiéme element du tableau a l'id du present 
        if fin_passe and len(Card.listener_requete.Tab_id) == 2:
            id_present = Card.listener_requete.Tab_id[1]
        
        # exceptions
        #si l'evenement passe est terminé mais qu'il n'y a pas d'id pour le prensent on ingique que que la carte present est la même que celle du passé
        elif fin_passe and len(Card.listener_requete.Tab_id) == 1:
            print("id carte present est le même que celle du passe")
        #sinon on indique que la carte present n'a pas encore était passé
        elif fin_present == False:
            print("la carte du present n'a pas encore était passé ")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Affectation futur ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

        #si l'évenement present est terminé et qu'un resultat a été renvoyé
        #on affecte la valeur du troisiéme id du tableau a l'id futur 
        if fin_present and fin_present and len(Card.listener_requete.Tab_id) == 3 :
            id_futur = Card.listener_requete.Tab_id[2]
        
        #exception
        #si l'evenement present est terminé et qu'aucun nouvelle id est la on indique que la carte a deja etait passé
        elif fin_present and len(Card.listener_requete.Tab_id) == 2:
            print("la carte est deja passé choisissez-en un autre")
        #sinon on indique que la carte du futur n'a pas encore était passé
        else:
            print("la carte du futur n'a pas encore était passé")
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ lecture video passé ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

        # si l'id du passé est non null et que on est jamais rentré dans cette condition
        #on peut donc jouer les animation pour le passé
        if id_passe is not None and fin_passe == False :
            voix_intro_flag = False
            
            url_image_carte = script.json.recherche_json.rechercheUrlEtNom(id_passe)
            effet = script.json.recherche_json.effet
            
            #on indique l'identité de la carte et on lance les effet
            lancement_effets = True
            carte_txt1 = True

            # on lance le tts d'annonce de carte
            tts_carte(script.json.recherche_json.nom)

        
            #on annonce que la prediction est en cours
            prediction = True
          

            #on lance la recherche de la prédiction puis le tts
            script.json.recherche_json.lectureDepuisJsonAvecInput(id_passe, 'passe')
            script.voix.voix.lancement_voix_de_prediction(script.json.recherche_json.prediction,carte_txt1,carte_txt2,carte_txt3)
            
            #on enleve tout les précedents effets
            prediction = False
            carte_txt1 = False

            #on attend un peu
            time.sleep(1)
            #on indique que l'on peut plus passée ici tant que les trois prédiction n'ont pas était dite
            fin_passe = True
            
            timer = threading.Timer(120, timer_call)
            timer.start()
            voix_intro_flag = True
            


            # musique_de_fond.play(-1)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ lecture video present ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

        # si l'id du présent est non null et que on est jamais rentré dans cette condition
        #on peut donc jouer les animation pour le présent

        if id_present is not None and fin_present == False :
            voix_intro_flag = False
           
            timer.cancel()

            url_image_carte = script.json.recherche_json.rechercheUrlEtNom(id_present)
            effet = script.json.recherche_json.effet
            
            #on indique l'identité de la carte et on lance les effet
            lancement_effets = True
            carte_txt2 = True

            # on lance le tts d'annonce de carte
            tts_carte(script.json.recherche_json.nom)
            
            

            #on annonce que la prediction et en cours
            prediction = True


            #on lance la recherche de la prédiction puis le tts
            script.json.recherche_json.lectureDepuisJsonAvecInput(id_present, 'present')
            script.voix.voix.lancement_voix_de_prediction(script.json.recherche_json.prediction,carte_txt1,carte_txt2,carte_txt3)
            
            #on enleve tout les précedent effet
            prediction = False
            carte_txt2 = False

            #on attend un peu
            time.sleep(1)
            #on indique que l'on peut plus passée ici tant que les trois prédiction n'ont pas était dite
            fin_present = True
            
            timer2 = threading.Timer(120, timer_call)
            timer2.start()
            voix_intro_flag = True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ lecture video futur ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

        #si l'id du futur n'est pas null
        #on peut donc jouer les animation pour le futur
        if id_futur is not None :
            voix_intro_flag = False
            timer2.cancel()

            #on attend que le processus soit bien tuer
            time.sleep(0.5)

            url_image_carte = script.json.recherche_json.rechercheUrlEtNom(id_futur)
            effet = script.json.recherche_json.effet
            
            #on indique l'identité de la carte et on lance les effet
            lancement_effets = True
            carte_txt3 = True

            # on lance le tts d'annonce de carte
            tts_carte(script.json.recherche_json.nom)

           

            #on annonce que la prediction et en cours
            prediction = True

            #on lance la recherche de la prédiction puis le tts
            script.json.recherche_json.lectureDepuisJsonAvecInput(id_futur, 'futur')
            script.voix.voix.lancement_voix_de_prediction(script.json.recherche_json.prediction,carte_txt1,carte_txt2,carte_txt3)
            
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
            voix_intro_flag = True
                      
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ lecture des voix ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#gestion voix introduction 
def voix_intro():
    global voix_intro_flag
    voix_intro_flag = True
    chanel_d_intro = script.voix.voix.voix_introduction()
    stoped = False
    while True:
        if voix_intro_flag:
            if not chanel_d_intro.get_busy():
                time.sleep(20)
                if voix_intro_flag:
                    chanel_d_intro = script.voix.voix.voix_introduction()
        else : 
            if not stoped:
                chanel_d_intro.stop()
                stoped = True

def timer_call():

    import Arduino as Card

    #variables des 3 id des 3 carte scanées respectivement
    global id_passe
    global id_present
    global id_futur

    global voix_intro_flag

    global prediction_thread
    
    # comme les prédictions sont terminée on reset toutes les variables (id,tableau et flag de condition)
    id_passe = None
    id_present = None
    id_futur = None

    #variables booléene qui permettent de savoir si les annonces (passe,present et futur) on était réalisé
    global fin_passe 
    global fin_present 
    global fin_futur 

    Card.listener_requete.Tab_id.clear()
    print("tableau suprimée",Card.listener_requete.Tab_id)

    #compteur de ligne dans le serial monitor remi à zero
    Card.listener_requete.ligne_compteur = 0

    fin_passe = False
    fin_present = False
    fin_futur= False

    voix_intro_flag = True
    
    # Attendre que le thread existant se termine proprement (facultatif)
    prediction_thread.join()

    # Créer et démarrer un nouveau thread de lecture vidéo
    prediction_thread = threading.Thread(target=lire_video)
    prediction_thread.start()

    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ création des thread ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# Création des threads et lancement des fonctions
intro_thread = threading.Thread(target=gestion_des_prediction)
intro_thread.start()
prediction_thread = threading.Thread(target=lire_video)
prediction_thread.start()
voix_intro_thread = threading.Thread(target=voix_intro)
voix_intro_thread.start()
