
from PIL import Image, ExifTags
from PIL.ExifTags import TAGS
import pygame
from time import sleep


# différentes couleurs
BLEU  = ( 80, 140, 245)
BLANC = (245, 245, 245)
ROUGE = (200,  80,  80)
NOIR  = ( 32,  32,  32)

ecranX = 500
ecranY = 500

class Cadre:

    def __init__(self):
        # initialisation des variables
        self.listePolices = None
        self.police       = None
        self.policeDefaut = None
        self.taillePolice = 32
        #self.pasQuitter   = True
        self.fenetre      = None
        self.imageFinale  = None
        self.rectangleImg = None


    def Initialise(self):

        print( pygame.init() ) # il est nécessaire de premièrement initialiser pyGame

        # preparation d'un police de caractères pour les messages
        self.listePolices = pygame.font.get_fonts()
        self.policeDefaut = pygame.font.get_default_font()
        self.police       = pygame.font.SysFont( None, self.taillePolice )

        # Création de la fenêtre du cadre
        self.fenetre = pygame.display.set_mode([ ecranX, ecranY ])

    def pasQuitter(self):
        # on parcour la liste d'événements potentiels
        # afin de détérminer si on quite ou non
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                # le programme est terminé
                pygame.quit()
                return False
        return True


    def afficheTexte( self, message ):
        impression = self.police.render( message, True, BLEU )
        self.fenetre.blit( impression, (20, 20) )

    def effacerEcran(self):        # on peinture l'écran en blanc
        self.fenetre.fill( NOIR )

    def chargeImage( self, fichier ):

        original_image = pygame.image.load( fichier )
        original_image.convert()

        if fichier[-3:].lower() == "png":
            # convert à jpg et sauvegarder
            fichier = fichier[0:-3] + "jpg"
            pygame.image.save( original_image, fichier )

        # on réoriente l'image au besoin
        pilIMG = Image.open( fichier )
        angle = 0

        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[ orientation ]=='Orientation':
                break

        # reload converted image
        img = pygame.image.load( fichier )
        img.convert()
        img = pygame.transform.rotate( img, angle )
        recimg = img.get_rect()

        # on redimensionne l'image au besoin
        if recimg.width > recimg.height:
            facteur = float(ecranX) / float(recimg.width)
        else:
            facteur = float(ecranY) / float(recimg.height)

        imageW = int( float(recimg.width ) * facteur )
        imageH = int( float(recimg.height) * facteur )

        result = pygame.transform.scale( img, ( imageW, imageH) )
        recres = result.get_rect()
        recres.center = ( ecranX//2, ecranY//2 )

        self.imageFinale  = result
        self.rectangleImg = recres


    def afficheImage(self):
        pass
        self.fenetre.blit( self.imageFinale, self.rectangleImg )

    def completeAffichage(self): # compléter l'Affichage
        # on affiche l'image produite
        pygame.display.flip()
        sleep( 120.0 / 1000.0 )

    def Roule(self):
        while self.pasQuitter():
            self.effacerEcran()

            self.afficheTexte( "Bonjour" )

            self.completeAffichage()

def main():

    objet = Cadre()
    objet.Initialise()
    objet.Roule()


if __name__ == '__main__':
    main()