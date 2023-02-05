## Cadre d'Images

Ce projet est un programme qui affiche des images dans une fenêtre. C'est une simple reproduction d'un défileur d'images (picture slideshow) ou un cadre d'images (picture frame), développé pour un projet scolaire.

Le programme est roulé sur un Raspberry Pi auquel une carte GPIO est connectée, et sur laquelle deux boutons poussoir sont montés; un permettant de passer en mode veille ou de se réveillé de ce mode, et l'autre pour changer d'album.

**Note**: la version originale tenait compte de l'orientation de l'image (en lisant les infos EXIF) afin de la redresser.

Technologies utilisées:
- Raspberry Pi 4 avec Raspbian OS
- GPIO : simple montage de deux boutons (en rappel haut) sur plaquette
- tkinter : pour interface graphique
- yaml : pour le fichier de configuration