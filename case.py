
class Case:

    # Constructeur

    def __init__(self):
        self.__isHidden = True
        self.__isMarked = False

    # Requêtes

    
    def isHidden(self):
        '''Retourne true si la case est visible sinon false'''
        return self.__isHidden

    def isMarked(self):
        return self.__isMarked
    
    #Commandes

    
    def show(self):
        '''Dévoile la case'''
        self.__isHidden = False
        self.__isMarked = False

    def hide(self):
        '''Cache la case'''
        self.__isHidden = True

    def mark(self):
        '''Mets un drapeau sur la case'''
        assert self.isHidden()

        self.__isMarked = True

    def unmark(self):
        '''Retire le drapeau de la case'''
        assert self.isMarked()

        self.__isMarked = False