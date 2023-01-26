from case import Case

class Case_Default(Case):
    # Constructeur
    def __init__(self):
        super().__init__()
        self.__bombs = 0
    
    # Requêtes

    def getNumberOfBombs(self):
        '''Retourne le nombre de bombes autour de la case'''
        return self.__bombs

    # Commandes

    def setNumberOfBombs(self, n):
        '''Définit le nombre de bombes autour de la case'''
        self.__bombs = n
