import serial
import subprocess


# ouverture du port série
ser = serial.Serial('/dev/ttyACM0', 9600) 
while True:
    data = ser.read()
   
    if data == b'1':
        print("on a recu 1")
        # on execute la requete avec le tag 120
        subprocess.run(['curl', '-X', 'GET', 'http://localhost:8080/recevoir?nom=120'])
    if data == b'2':
        print("on a recu 2")
        # on execute la requete avec le tag 123
        subprocess.run(['curl', '-X', 'GET', 'http://localhost:8080/recevoir?nom=123'])
