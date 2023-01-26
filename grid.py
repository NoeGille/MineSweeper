import numpy as np
from case import Case
from case_default import Case_Default
from case_bomb import Case_Bomb

class Grid():
    #Constructeur
    def __init__(self, width, height, nbBombs):
        assert width > 0
        assert height > 0
        assert nbBombs <= width * height

        self.__width = width
        self.__height = height
        self.__nbBombs = nbBombs
        self.__caseArray = np.ndarray(width * height,dtype=Case)
        self.__hasLost = False
        self.__nbHiddenCases = width * height
        bomb_placed = 0
        for i in range(0,width * height):
            if bomb_placed < self.__nbBombs:
                self.__caseArray[i] = Case_Bomb()
                bomb_placed += 1
            else:
                self.__caseArray[i] = Case_Default()
        np.random.shuffle(self.__caseArray)
        self.__caseArray = self.__caseArray.reshape((width,height))
        for i in range(0,width):
            for j in range(0,height):
                if isinstance(self.__caseArray[i][j],Case_Default):
                    self.__caseArray[i][j].setNumberOfBombs(self.__countbombs(i,j))
    # Méthodes spéciales

    def __repr__(self):
        s = ""
        for i in range(0,self.getWidth()):
            for j in range(0,self.getHeight()):
                if self.getCase(i,j).isHidden():
                    s += "+"
                elif isinstance(self.getCase(i,j),Case_Default):
                    s += str(self.getCase(i,j).getNumberOfBombs())
                else:
                    s += "*"
                s += " "
            s += "\n"
        return s
    
    # Requêtes

    #Renvoie la largeur de la grille
    def getWidth(self):
        return self.__width

    #Renvoie la hauteur de la grille
    def getHeight(self):
        return self.__height

    #Renvoie le nombre de bombes contenues dans la grille
    def getNbBombs(self):
        return self.__nbBombs

    #Renvoie le nombre de cases voilées contenues  dans la grille
    def getNbHiddenCases(self):
        return self.__nbHiddenCases

    #Renvoie True si le joueur a perdu
    def hasLost(self):
        return self.__hasLost

    #Renvoie un ndarray 2d contenant l'emplacement des cases
    def getCaseArray(self):
        return self.__caseArray

    #Renvoie l'objet représentant la case (x, y)
    def getCase(self, x, y):
        assert x >= 0 and x < self.getWidth()
        assert y >= 0 and y < self.getHeight()

        return self.__caseArray[x][y]

    def isGameWon(self):
        return self.getNbHiddenCases() == self.getNbBombs()
    # Commandes

    #Simule un tour de jeu où le joueur clique sur la case (x, y) 
    #   si le joueur clique sur une bombe il perd et dévoile la grille
    #   sinon dévoile les cases "sures" cliquer par le joueur
    def playAMove(self, x, y):
        assert x >= 0 and x < self.getWidth()
        assert y >= 0 and y < self.getHeight()

        if isinstance(self.getCase(x,y), Case_Bomb):
            self.__hasLost = True
            self.__showGrid()
        else:
            self.__recShowSafeCase(x, y)
        if self.__hasWon():
            print("Bravo vous avez gagné")
        if self.hasLost():
            print("Bouh ! Vous avez perdu")

    #Relance la partie avec la même grille
    def replay(self):
        self.__hasLost = False
        self.__hideGrid()

    # Outils

    #Dévoile la case (x, y)
    def __showCase(self, x, y):
        self.getCase(x, y).show()
    
    #Dévoile la grille entière
    def __showGrid(self):
        for i in range(0,self.getWidth()):
            for j in range(0,self.getHeight()):
                self.__showCase(i, j)

    #Cache la grille entière
    def __hideGrid(self):
        for i in range(0,self.getWidth()):
            for j in range(0,self.getHeight()):
                self.getCase(i, j).hide()

    #Renvoie le nombre de bombes adjacentes à la case (x,y)
    def __countbombs(self, x, y):
        count = 0
        for i in range(-1,2):
            for j in range(-1,2):
                try:
                    if isinstance(self.getCase(x + i, y + j),Case_Bomb):
                        count += 1
                except:
                    pass
        return count

    #Renvoie True si le joueur a gagné la partie (dévoilé toutes les cases
    #        qui ne sont pas des bombes)
    def __hasWon(self):
        if self.__nbBombs == self.__nbHiddenCases:
            return True
        return False

    #Fonction récursive dévoilant les cases ayant 0 bombes adjacentes (pas recursive terminale)
    def __recShowSafeCase(self, x, y):
        if self.getCase(x , y).isHidden():
            self.__showCase(x , y)
            self.__nbHiddenCases -= 1
        if self.getCase(x, y).getNumberOfBombs() == 0:
            for i in range(-1,2):
                for j in range(-1,2):
                    try:
                        if self.getCase(x + i, y + j).isHidden():
                            self.__recShowSafeCase(x + i, y + j)
                    except:
                        pass