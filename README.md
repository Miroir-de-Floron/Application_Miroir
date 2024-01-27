<h1 align="center">
  <br>
   Miroir de Floron
  <br>
</h1>

<h4 align="center">
  Projet SAE du Semestre 5, IUT AIX BUT INFO <br>
</h4>
<div align="center"> 
  <img src="https://i.pinimg.com/originals/f6/4f/53/f64f53da53b34d2479f3b3bff26fa4fc.png" width="825" height="600">
</div>

il s'agit d'un projet ayant bessoin d'un capteur RFID rc522 pour fonctionner.

Pour pouvoir faire fonctionner le projet sur linux il faut faire quelques installations :

### Modules python nécessaires 🐍 :

* opencv-python
* waiting (on test de faire sans)
* datetime
* pygame

pour la version Arduino, il faut en plus :

* pyserial

pour la version Raspberry pi, il faut en plus :

* pi-rc522
* RPi-GPIO

linux est le seul systéme que nous avons pleinnement testé mais il ne devrait pas y avoir de probléme sur les autres tant que toute les dépendances sont là.

##### en fonction de l'utilisation du projet avec une carte Arduino ou sur une Raspberry pi, il faut penser a rennomer soit le fichier listener_requete.arduino.py ou listener_requete.raspberry.py en listener_requete.py !

###### en cas d'utilisation de la carte Arduino pensez à bien changer le nom du serial sur lequel est branché votre carte Arduino.

il faut aussi penser a modifier les code des carte RFID.

* Pour plus d'information se renseigner dans le guide d'utilisation à la racine du projet

## Contributeur ✨

Personnes ayant participé à ce projet

<table >
  <td align="center">
  <a href="https://github.com/Thibault-De-Permentier">
    <img src="https://avatars.githubusercontent.com/u/91873613?v=4" width="100px;" alt="Thibault-De-Permentier"/> <br />
    <sub>
      <b>Thibault De Permentier</b>
    </sub>
  </a>
  </td>
  
  <td align="center">
  <a href="https://github.com/FabreLucas0">
    <img src="https://avatars.githubusercontent.com/u/92868641?v=4" width="100px;" alt="FabreLucas0"/> <br />
    <sub>
      <b>Lucas Fabre</b>
    </sub>
  </a>
  </td>
  
  <td align="center">
  <a href="https://github.com/Ismaiil23">
    <img src="https://avatars.githubusercontent.com/u/91462362?v=4" width="100px;" alt="Ismaiil23"/> <br />
    <sub>
      <b>Ismail Mesrouk</b>
    </sub>
  </a>
    <br />
    </a>
  </td>
  
  <td align="center">
  <a href="https://github.com/Yanis-TRIGLIA">
    <img src="https://avatars.githubusercontent.com/u/91632872?v=4" width="100px;" alt="Yanis-TRIGLIA"/> <br />
    <sub>
      <b>Triglia Yanis</b>
    </sub>
  </a>
    <br />
    </a>
  </td>
  

