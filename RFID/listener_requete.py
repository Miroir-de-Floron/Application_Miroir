from pirc522 import RFID
import RPi.GPIO as GPIO
import time
Tab_id = []
ligne_compteur = 0
exception_tableau = False
result = None
ligne = 0
rdr = RFID()
util = rdr.util()

def get_id():
    global Tab_id
    global ligne_compteur
    global exception_tableau
    global ligne
    global rdr
    global util


    time.sleep(1)
    while True:
            rdr.wait_for_tag()
            (error, data) = rdr.request()
            if not error:
               (error, uid) = rdr.anticoll()
               ligne = str(uid)
               ligne_compteur+= 1
               util.set_tag(uid)
               util.auth(rdr.auth_a, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF,0xFF])
               util.deauth()

            #on vérifie toute les possibilité à l'aide d'un switch case des carte qui peuvent etre utilisée
            def switch_case(ligne):
                global result
                switch_dict = {
                    b"83156130233000000\r\n": 0,        #le fou
                    "[179, 138, 21, 233, 197]": 1,        #le magicien
                    b"311362233000000\r\n": 2,          #la papesse
                    "[179, 31, 132, 233, 193]": 3,        #l'imperatrice
                    b"5117195232000000\r\n": 4,         #l'empereur
                    b"516739233000000\r\n": 5,          #le pape
                    "[35, 140, 232, 232, 175]": 6,        #les amoureux
                    b"839337233000000\r\n": 7,          #le chariot
                    "[195, 50, 23, 233, 15]": 8,         #la justice
                    "[66, 187, 184, 137, 200]": 9,        #l'ermite
                    "[163, 246, 62, 233, 130]": 10,       #la rou de fortune
                    "[195, 6, 191, 232, 146]": 11,        #la force
                    b"11515648233000000\r\n": 12,       #le pendu
                    "[83, 14, 24, 233, 172]": 13,         #la mort
                    "[163, 172, 63, 233, 217]": 14,       #la tempairence
                    "[131, 245, 219, 232, 69]": 15,      #le diable
                    "[179, 176, 80, 233, 186]": 16,       #maison dieu
                    b"518093233000000\r\n": 17,         #l'etoile
                    "[51, 50, 23, 233, 255]": 18,         #la lune
                    "[83, 80, 250, 232, 17]": 19,        #le soleil
                    "[83, 158, 81, 233, 117]": 20,        #la renaissance
                    "[163, 69, 245, 232, 251]": 21         #le monde
                
                }
            
                if ligne in switch_dict:
                    result = switch_dict[ligne]
                    #on vérifie si l'élement n'est pas dans le tableau
                    if result not in Tab_id :
                        Tab_id.append(result)


            switch_case(ligne)
        
            
            #on sort si le tableau d'id et égale à 3
            if(len(Tab_id) >= 1):
                print("Sortie de boucle",Tab_id)
                break