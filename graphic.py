from grid import Grid
from case import Case
from case_default import Case_Default
from case_bomb import Case_Bomb
import tkinter as tk
from tkinter import RAISED, SUNKEN, PhotoImage, ttk
from copy import deepcopy
from functools import partial
import numpy as np

class MineSweeper():

    def __init__(self, width, height, mines_nb) -> None:

        self.model = Grid(width, height, mines_nb)
        self.create_view()
        self.place_components()
        self.create_controller()

    def create_view(self):
        self.root = tk.Tk()
        self.root.title("Démineur")
        self.root.config(bg="white")
        self.main_frame = ttk.Frame(self.root, padding="10 10 10 10")
        self.main_frame.grid(column=0, row=0, sticky="nsew")
        self.canvas = tk.Canvas(self.main_frame, bg="white", width=300, height=300)
        self.canvas.grid(row=0, column=1, sticky="nsew")
        self.solve_button = ttk.Button(self.main_frame, text="Résoudre", command=self.resolve)
        self.solve_button.grid(row=0, column=0, sticky="nsew")
        
        self.buttons = np.array([[None for _ in range(self.model.getWidth())] for _ in range(self.model.getHeight())], dtype=object)
        for i in range(self.model.getWidth()):
            for j in range(self.model.getHeight()):
                self.buttons[j, i] = tk.Button(self.canvas, text="", command=partial(self.click, j,i), bg="white", fg ="black", width=5, height=2)
                self.buttons[j, i].config()
                self.buttons[j, i].grid(column=i, row=j, sticky="nwes",)


    def place_components(self):
        self.canvas.create_rectangle(0, 0, 500, 500, fill="white", outline="black", width=2)
        self.canvas.grid(row=self.model.getWidth(), column=self.model.getHeight(), sticky="nsew")
        self.main_frame.pack(fill="both", expand=True)
    

    def create_controller(self):
        self.root.mainloop()

    def click(self, x, y):
        self.model.playAMove(y, x)
        self.update_buttons_text()
    
    def update_buttons_text(self):
        for i in range(0,self.model.getWidth()):
            for j in range(0,self.model.getHeight()):
                button = self.buttons[j,i]
                if self.model.getCase(i,j).isHidden():
                    if self.model.getCase(i,j).isMarked():
                        button.config(text="?", fg="red")
                    else :
                        button.config(text=" ")
                elif isinstance(self.model.getCase(i,j),Case_Default):
                    nbOfBombs = self.model.getCase(i,j).getNumberOfBombs()
                    colors = ["blue", "green", "red", "purple", "brown", "cyan", "gray", "yellow", "black"]
                    if nbOfBombs > 0:
                        button.config(text=str(nbOfBombs), bg="white", fg=colors[nbOfBombs-1])
                    else:
                        button.config(text=" ", bg="gray87")
                    button.config(relief=SUNKEN)
                else:
                    button.config(text="*", bg="red")
                    button.config(relief=SUNKEN)

    def mark_mines(self):
        current_grid = self.model.getCaseArray()
        for i in range(0,self.model.getWidth()):
            for j in range(0,self.model.getHeight()):
                if isinstance(current_grid[i,j], Case_Default) and current_grid[i,j].getNumberOfBombs() > 0:
                    kernel = np.array([[self.model.getCase(i + k, j + p) if i + k >= 0 and i + k < self.model.getWidth() and j + p >= 0 and j + p < self.model.getHeight() else Case() for k in range(-1, 2)] for p in range(-1, 2)], dtype=Case)
                    count = 0
                    for k in kernel:
                        for p in k:
                            if p.isHidden():
                                count += 1
                    if count == current_grid[i,j].getNumberOfBombs():
                        for k in range(0,3):
                            for p in range(0,3):
                                if kernel[k,p].isHidden() and i + k - 1 >= 0 and i + k - 1 < self.model.getWidth() and j + p - 1 >= 0 and j + p - 1 < self.model.getHeight():
                                    kernel[k,p].mark()
        self.update_buttons_text()

    def click_safe_case(self):
        current_grid = self.model.getCaseArray()
        for i in range(0,self.model.getWidth()):
            for j in range(0,self.model.getHeight()):
                if isinstance(current_grid[i,j], Case_Default) and current_grid[i,j].getNumberOfBombs() > 0 and not current_grid[i,j].isHidden():
                    count = 0
                    for k in range(-1, 2):
                        for p in range(-1, 2):
                            if i + k >= 0 and i + k < self.model.getWidth() and j + p >= 0 and j + p < self.model.getHeight() and current_grid[i + k, j + p].isMarked():
                                count += 1
                    if count == current_grid[i,j].getNumberOfBombs() and count > 0:
                        for k in range(-1, 2):
                            for p in range(-1, 2):
                                if i + k >= 0 and i + k < self.model.getWidth() and j + p >= 0 and j + p < self.model.getHeight():
                                    if current_grid[i + k, j + p].isHidden() and not current_grid[i + k, j + p].isMarked():
                                        self.click(j + p, i + k)

    def resolve(self):
        for _ in range(0, 1):
            self.mark_mines()
            self.click_safe_case()
        self.update_buttons_text()

if __name__ == "__main__":
    MineSweeper(20, 20, 50)
