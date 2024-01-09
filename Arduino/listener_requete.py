import serial
import time
Tab_id = []
ligne_compteur = 0
exception_tableau = False
result = None
arduino_brancher = True
ligne = 0


def get_id():
    global Tab_id
    global ligne_compteur
    global exception_tableau
    global ligne

    try:
        ser = serial.Serial('/dev/ttyACM0', 9600)
    except:
        arduino_brancher = False

    time.sleep(1)
    while True:
        # si la arduino est branché nous executons le code si dessous 
        if arduino_brancher:
            #on lit une ligne du serial qui correpons à l'id uniquement
            ligne = ser.readline()
            ligne_compteur+= 1
        # sinon nous demandons des entrées au clavier
        else:
            print("veillez entré un nombre entre 0 et 21")
            result = int(input()) 
            ligne_compteur+= 1
            if result not in Tab_id :
                    Tab_id.append(result)
                    print(result)

    
        #on vérifie toute les possibilité à l'aide d'un switch case des carte qui peuvent etre utilisée
        def switch_case(ligne):
            global result
            switch_dict = {
                b"83156130233000000\r\n": 0,
                b"17913821233000000\r\n": 1,
                b"311362233000000\r\n": 2,
                b"17931132233000000\r\n": 3,  
                b"5117195232000000\r\n": 4,
                b"516739233000000\r\n": 5,
                b"35140232232000000\r\n": 6,
                b"839337233000000\r\n": 7,
                b"1955023233000000\r\n": 8,
                b"66187184137000000\r\n": 9,
                b"16324662233000000\r\n": 10,
                b"1956191232000000\r\n": 11,
                b"11515648233000000\r\n": 12,
                b"831424233000000\r\n": 13,
                b"16317263233000000\r\n": 14,
                b"131245219232000000\r\n": 15,
                b"17917680233000000\r\n": 16,
                b"518093233000000\r\n": 17,
                b"515023233000000\r\n": 18,
                b"8380250232000000\r\n": 19,
                b"8315881233000000\r\n": 20,
                b"1636924523200000\r\n": 21
                
            }
            
            if ligne in switch_dict and arduino_brancher:
                result = switch_dict[ligne]
                #on vérifie si l'élement n'est pas dans le tableau
                if result not in Tab_id :
                    Tab_id.append(result)
                    print(result)

            else:
                print("ligne n'a pas de valeur")

        switch_case(ligne)
        
            
        #on sort si le tableau d'id et égale à 3
        if(len(Tab_id) >= 1):
            print("Sortie de boucle",Tab_id)
            break