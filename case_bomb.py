from case import Case

class Case_Bomb(Case):
    # Constructeur
    def __init__(self):
        super().__init__()
        self.__isExploded = False

    # Requêtes

    def isExploded(self):
        '''Retourne true si la bombe a explosé sinon false'''
        return self.__isExploded

    # Commandes

    def explode(self):
        '''Explose la bombe'''
        self.__isExploded = True