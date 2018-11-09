import Tkinter as tk
from copy import deepcopy
from random import randrange

def random_fields(width):#Prasanna
    """
    Returns a list of list of random integers, eg: setA [[23,4], [16,19]].
    These lists inside fields are meant as each coordiante.
    The parameter width is the maximum value of x and y.
    """
    fields_alive = width * width/4#say just to start with a few number of alive cells or else screen would be full of living cells(it gives number of points in matrix)
    fields = []      #to make an empty list 
    for i in range(fields_alive):
        x = randrange(width)#to take a random x co-ordinate
        y = randrange(width)#to take a random y co-ordinate
        fields.append((x,y))#to append all co-ordinates in the above created list
    return fields#returns a list of co-ordinates 

class Field(object):#done
    """ Represents a field in Game of Life. Not matrix"""
    def __init__(self, x, y):
        """ Constructs a "dead" field at co-ordinates x and y """
        self.x = x
        self.y = y
        self.is_alive = False

    def __str__(self):
    #It prints the given things in format in place of curley bracket which is later changed to its colour version while executing the program
        return "Field: \n   x: {0}; y: {1}; is_alive: {2}\n".format(self.x, self.y, self.is_alive)#check out??????????????????? why printing it
    
    def change(self):
        """ Changes from dead to alive and vice-versa. """
        if self.is_alive:
            self.is_alive = False
        else:
            self.is_alive = True


class GameOfLifeMatrix(object):#Apurva
    """
    Represents a matrix of Game of Life and contains its logic.
    """
   
    def __init__(self, width = 25, start_fields = "random"):
        """ 
        Constructs a new square matrix for Game Of Life. 
        parameters:
        width: integer, the width and height of the matrix
                - a set of tuples containing specified "alive" coordinates
        """
        if start_fields=="random":
            self.start_fields=random_fields(width)#a set of 25 random co-ordinates
        else:
            self.start_fields=start_fields
        self.width=width
        self.generation = 0
        self.matrix = []#genrating matrix using list
        for x in range(width):
            row=[]
            self.matrix.append(row)
            for y in range(width):
                field = Field(x, y)
                if (x,y) in self.start_fields:
                    field.change() #changing dead to alive
                row.append(field)

    def _should_change(self, field):
        """ Determines if a given field should be changed according to the rules of the game"""
        if (field.x==0 or field.y==0 or field.x == self.width - 1 or field.y == self.width - 1):
            # i.e.: field is at the border should not change?
            return False
        alive_neighbours = 0
        for x in range(field.x -1, field.x +2):
            for y in range(field.y -1, field.y +2):
                if x == field.x and y == field.y:
                    # field is not neighbour of itself
                    continue
                if self.matrix[x][y].is_alive:
                    alive_neighbours += 1

            if (not field.is_alive) and alive_neighbours == 3:#dead->alive
                return True
            elif field.is_alive and (alive_neighbours < 2 or alive_neighbours > 3):
                return True
            else:
                return False 

    def next_generation(self):
        """ Evolves the matrix to the next generation. """
        self.generation += 1
        new_matrix = deepcopy(self.matrix)
        for field in self.fields():
            if self._should_change(field):
                new_matrix[field.x][field.y].change()
        self.matrix = new_matrix


    def fields(self):
        """ Generator, yields all fields of the matrix. """
        for row in self.matrix:
            for field in row:  
                yield field#a type of return which does not destroy previous variable's value




class GameOfLifeApp(tk.Frame):#Sumanth
    """ Represents the TkInter-Version of the game """
    def __init__(self, game, generation_interval_ms = 3000, color_alive = "green", color_dead = "black"):#3000 is time in which screen changes 
        """
        Constructs the TkInter app.
        parameters:
        game: an object of type GameOfLifeMatrix
        generation_interval_ms: integer time in milliseconds to display the next genereation
        color_alive and color_dead: TkInter-color-strings for alive and dead fields
            black for dead and green for alive
        """
        self.game=game
        self.generation_interval_ms=generation_interval_ms
        self.color_alive=color_alive
        self.color_dead=color_dead
        self.widgets = {}#initializing dictionary
        self.root = tk.Tk()#making screen
        tk.Frame.__init__(self, self.root)
        self.grid()#understand its use

        for field in self.game.fields():
            widget = tk.Label(height = 1, width = 2, bg = self.color_dead, relief = "ridge")#relief is for 3-D ridge is a type, making boxes
            widget.grid(column = field.x, row = field.y)
            if field.is_alive:
                widget.configure(bg = self.color_alive)
            self.widgets[(field.x, field.y)] = widget

        self.root.after(self.generation_interval_ms, self.draw)#showing next genertion


    def draw(self):#to show dead or alive cell
        """ Draws the new generation. """
        for field in self.game.fields():
            if field.is_alive:
                self.widgets[(field.x, field.y)].configure(bg = self.color_alive)
            else:
                self.widgets[(field.x, field.y)].configure(bg = self.color_dead)
        self.game.next_generation()
        self.root.after(self.generation_interval_ms, self.draw)

if __name__ == "__main__":#final execution
    game = GameOfLifeMatrix()
    app = GameOfLifeApp(game)
    app.mainloop()
'''Group members
IMT2016010 Apurva Bhatt
IMT2016044 Prasanna Kumar
IMT2016041 Lakshmi Sai Sumanth
'''
