
#------------------------------------------------------------------------------
# Auteur: Linus Levi
# Cours: Programmation embarquée
# Description: ce fichier contient le code pour le GPIO
#------------------------------------------------------------------------------

import RPi.GPIO as GPIO
from time import sleep


class Carte:

    def __init__(self):
        # Constantes du GPIO
        self.boutonALBUM = 17
        self.boutonMODE  = 18


    def Initialise(self):
        print( "Initialisation de la carte GPIO" )

        GPIO.setmode( GPIO.BCM )
        GPIO.setwarnings(False)

        # les deux boutons sont initialés en rappel heut
        GPIO.setup( self.boutonALBUM, GPIO.IN, pull_up_down = GPIO.PUD_UP )
        GPIO.setup( self.boutonMODE , GPIO.IN, pull_up_down = GPIO.PUD_UP )


    def boutonAlbum(self):
        #sleep( 250 / 1000.0 ) # bref délai entre les opérations du bouton
        if GPIO.input( self.boutonALBUM ) == GPIO.LOW:
            return True
        return False


    def boutonMode(self):
        #sleep( 250 / 1000.0 ) # bref délai entre les opérations du bouton
        if GPIO.input( self.boutonMODE ) == GPIO.LOW:
            return True
        return False


def main():

    objet = Carte()
    objet.Initialise()
    
    for i in range(0, 5):
        print( objet.boutonAlbum() )
        print( objet.boutonMode() )
        sleep(1)
        


if __name__ == '__main__':
    main()