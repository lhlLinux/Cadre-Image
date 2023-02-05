## Cadre d'Images

Ce projet est un programme qui affiche des images dans une fen�tre. C'est une simple reproduction d'un d�fileur d'images (picture slideshow) ou un cadre d'images (picture frame), d�velopp� pour un projet scolaire.

Le programme est roul� sur un Raspberry Pi auquel une carte GPIO est connect�e, et sur laquelle deux boutons poussoir sont mont�s; un permettant de passer en mode veille ou de se r�veill� de ce mode, et l'autre pour changer d'album.

**Note**: la version originale tenait compte de l'orientation de l'image (en lisant les infos EXIF) afin de la redresser.

Technologies utilis�es:
- Raspberry Pi 4 avec Raspbian OS
- GPIO : simple montage de deux boutons (en rappel haut) sur plaquette
- tkinter : pour interface graphique
- yaml : pour le fichier de configuration