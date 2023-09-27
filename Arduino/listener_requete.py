import serial
import subprocess


# ouverture du port série
ser = serial.Serial('COM3', 9600) 
while True:
    data = ser.read()
    print(data)
    if data == b'1':
        print("1 reçu !")
        # on exe qu'on on recoi 1
        subprocess.run(['curl', '-X', 'GET', 'http://localhost:8080/recevoir?nom=123'])

