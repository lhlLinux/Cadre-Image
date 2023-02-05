import yaml


class Configuration:

    def __init__(self):
        self.nomFichier = "config.yaml"
        #self.nomFichier = "config_win.yaml"
        #self.nomFichier = "config_lin.yaml"
        self.fichier = None
        self.configurations = None

    def LireConfigurations(self):
        try:
            self.fichier = open( self.nomFichier, "r")
        except:
            print( "Le fichier " + self.nomFichier + " est introuvable" )

        try:
            self.configurations = yaml.load( self.fichier, Loader = yaml.BaseLoader ) # windows
            #self.configurations = yaml.load( self.fichier ) # pour la platforme Linux
            print( "Fichier lu" )
        except:
            print( "Misère à décoder le fichier" )

        self.fichier.close()

        return self.configurations


def main():

    objet = Configuration()
    data = objet.LireConfigurations()

if __name__ == '__main__':
    main()

