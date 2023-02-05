
import time
import configuration
from cadre import Cadre
#from carte import Carte
import threading
import os
import sys


quitter     = False
changeImage = False
changeMode  = False


def _thread_intervalle_image( periode ):
    global quitter
    global changeImage

    periode = float(periode)

    while not quitter:
        time.sleep( periode )
        changeImage = True

    print( "Thread 'delaiImage' a terminé" )


class Programme:

    def __init__(self):

        self.etatActif = None
        self.cadre     = None
        self.carte     = None
        self.fconfig   = None

        self.prochaineImage = False

        self.heure_actuelle = 0
        self.diff_temps     = 0
        self.heure_reveil   = 0
        self.heure_veille   = 0
        self.intervale      = 0
        self.periode        = 0
        self.chemin_albums  = ""

        self.indexAlbum    = -1
        self.indexImage    = -1
        self.listeImages   = None
        self.listeAlbums   = None
        self.fichierActuel = ""
        self.albumActuel   = ""
        self.messageUsager = ""
        self.compteurArretFichier = 0
        self.compteurArretAlbum   = 0
        self.imageExiste = False
        self.repExiste = False

        self.imageDisponible = False
        self.repBase = None # répertoire de base
        self.listeAlbums = None

    def Initialise(self):
        global quitter

        self.fconfig = configuration.Configuration()

        data = self.fconfig.LireConfigurations()

        localtime = time.localtime( time.time() )

        # on extrait l'information retournee précédemment
        # en de valeurs numériques afin de pouvoir travailler avec
        # Les valeurs temporelles sont traduites en secondes pour un plus simple traitement
        self.heure_actuelle = (localtime.tm_hour * 60 + localtime.tm_min) * 60 + localtime.tm_sec

        heures, minutes = data[ "wakeup" ].split(":")
        self.heure_reveil = (int(heures) * 60 + int(minutes)) * 60

        heures, minutes = data[ "close" ].split(":")
        self.heure_veille = (int(heures) * 60 + int(minutes)) * 60

        heures, minutes, secondes = data[ "period" ].split(":")
        self.intervale = (int(heures) * 60 + int(minutes)) * 60 + int(secondes)

        self.chemin_albums = data[ "path" ]

        self.determinePeriode()

        threadMode = threading.Thread( target = self._thread_intervalle_mode )
        threadMode.start()

        # TO MOVE FROM HERE
        threadImage = threading.Thread( target = lambda: _thread_intervalle_image( self.intervale ) )
        threadImage.start() # starting the thread 1

        # on essaie de changer de répertoire courant
        try:
            os.chdir( self.chemin_albums )
        except:
            # répertoire inexistant
            print( "2. ATTENTION : le répertoire" + "c:\\" + self.chemin_albums + "n'existe pas" )
            self.messageUsager = "3. Le répertoire racine n'existe pas"
            print( self.messageUsager )
            quitter = True
            return
            #sys.exit()


        self.listeAlbums = os.listdir(".")
        if len( self.listeAlbums ) == 0:
            self.messageUsager = "4. Le répertoire racine est vide"
            print( self.messageUsager )
            quitter = True
            return

        # test
        #quitter = True
        #return

        self.cadre = Cadre()
        self.cadre.Initialise()

        #self.carte = Carte()
        #self.carte.Initialise()

        self.changeAlbum()

    def determinePeriode(self):
        # Ici on determine l'état (actif ou en veille)
        # en fonction de l'heure actuelle
        localtime = time.localtime( time.time() )
        self.heure_actuelle = (localtime.tm_hour * 60 + localtime.tm_min) * 60 + localtime.tm_sec

        if self.heure_actuelle < self.heure_reveil:
            self.etatActif = False
            self.periode = self.heure_reveil - self.heure_actuelle
        elif self.heure_actuelle < self.heure_veille:
            self.etatActif = True
            self.periode = self.heure_veille - self.heure_actuelle
        elif self.heure_actuelle >= self.heure_veille:
            self.etatActif = False
            self.periode = 86400 - self.heure_actuelle + self.heure_reveil

    def _thread_intervalle_mode( self ):
        global quitter
        global changeMode

        # on dort 5 secondes puis on vérifie les conditions d'abandon
        # on ne peut tout simplement dormir tout le temps car on
        # ne pourra sortir de la boucle à temps
        while not quitter:
            intervale = self.periode # temporaire
            print( "_thread_intervalle_mode intervale: ", intervale )

            # boucle intérieur
            while not quitter and intervale > 0:
                time.sleep( 5.0 )
                intervale -= 5
            changeMode = True
            self.determinePeriode()
        print( "Thread '_thread_intervalle_mode' a terminé" )


    def changeImage(self):

        #print( "self.compteurArretFichier: ", self.compteurArretFichier)

        # si on se trouve au dernier fichier, on retourne au premier
        if self.indexImage == len(self.listeImages) - 1:
            self.indexImage = 0
        else:
            self.indexImage += 1

        temp = self.listeImages[ self.indexImage ] # variable temporaire

        # on s'assure premièrement que le fichier en question est bel et bien
        # un fichier et non un répertoire et est une image par son extension
        try:
            if os.path.isfile( temp ):
                if temp[-3:].lower() in [ "png", "bmp", "jpg", "gif", "tga" ]:
                    self.fichierActuel = self.listeImages[ self.indexImage ]
                    #self.imageExiste = True
                    self.imageDisponible = True
                    self.messageUsager = "5. Images trouvées"
                    #print( "self.fichierActuel:", self.fichierActuel )
                    #print( "CWD: " + os.getcwd() )
                    asdf = self.fichierActuel
                    #print( "asdf:" , asdf )
                    self.cadre.chargeImage( asdf )
                else:
                    #self.imageExiste = False
                    self.imageDisponible = False
                    self.messageUsager = "6. Aucune image dans ce répertoire"
        except:
            # au cas où un fichier/répertoire n'est plus présent
            # la fonction s'appelle récursivement
            self.compteurArretFichier += 1 # ceci servira de condition d'arêt
            if self.compteurArretFichier < len( self.listeImages ):
                self.changeImage()

            # on affiche un message et on réinitialise le compteur
            self.messageUsager = "7. Aucune image dans ce répertoire"
            self.compteurArretFichier = 0
            #self.imageExiste = False
            self.imageDisponible = False



    def changeAlbum(self):

        #print( "self.compteurArretAlbum: ", self.compteurArretAlbum )

        # si on se trouve au dernier sous répertoire, on retourne au premier
        if self.indexAlbum == len(self.listeAlbums) - 1:
            self.indexAlbum = 0
        else:
            self.indexAlbum += 1

        # chaque fois qu'on change d'album on reinitialise l'index de l'image
        self.indexImage = -1

        temp = self.listeAlbums[ self.indexAlbum ] # variable temporaire

        # on réinitialise le répertoire actuel pour le prochain test
        os.chdir( self.chemin_albums )

        # on s'assure premièrement que le répertoire en question est bel et bien
        # un répertoire et non un fichier
        try:
            if os.path.isdir( temp ):
                self.albumActuel = self.chemin_albums + "/" + self.listeAlbums[ self.indexAlbum ]
                #print( "self.albumActuel: ", self.albumActuel )
                os.chdir( self.albumActuel )
                self.listeImages = os.listdir( self.albumActuel )
                if len( self.listeImages ) > 0:
                    self.changeImage()
                else:
                    # au cas où le rép est vide la fonction s'appelle récursivement
                    self.compteurArretAlbum += 1 # ceci servira de condition d'arêt
                    if self.compteurArretAlbum < len( self.listeAlbums ):
                        self.changeAlbum()

                    # on affiche un message et on réinitialise le compteur
                    self.messageUsager = "8. Aucune album de disponible"
                    self.compteurArretAlbum = 0
                    #self.repExiste = False
                    #self.imageDisponible = False
            else:
                if len( self.listeAlbums ) == 0:
                    self.messageUsager = "9. Aucune album de disponible"
                #self.repExiste = False
                #self.imageDisponible = False
        except:
            # au cas où un fichier/répertoire n'est plus présent
            # la fonction s'appelle récursivement
            self.compteurArretAlbum += 1 # ceci servira de condition d'arêt
            if self.compteurArretAlbum < len( self.listeAlbums ):
                self.changeAlbum()

            # on affiche un message et on réinitialise le compteur
            self.messageUsager = "10. Aucune album de disponible"
            self.compteurArretAlbum = 0
            #self.repExiste = False
            #self.imageDisponible = False


    def Roule(self):
        global quitter # très important (global)
        global changeImage
        global changeMode

        while self.cadre.pasQuitter():

            self.cadre.effacerEcran()

            if self.etatActif:
                if self.imageDisponible:
                    self.cadre.afficheImage()

                self.cadre.afficheTexte( self.messageUsager )
                if changeImage:
                    self.changeImage()

                    changeImage = False

                # C'est ici que l'on change d'album
                #if self.carte.boutonAlbum():
                    #self.changeAlbum()

            if changeMode or self.carte.boutonMode():
                if self.etatActif:
                    self.etatActif = False
                else:
                    self.etatActif = True

                changeMode = False

            self.cadre.completeAffichage()
            time.sleep( 0.033 )

        # très important pour mettre fin au threads du delai
        quitter = True


def main():

    prog = Programme()
    prog.Initialise()
    prog.Roule()


if __name__ == '__main__':
    main()
