from random import random

from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.space import Grid

from skimage import io, transform

from epidemic.cell import Cell


class Epidemic(Model):
    '''
    Represents the 2-dimensional array of cells in Conway's
    Game of Life.
    '''

    def __init__(self, height, width):
        '''
        Create a new playing area of (height, width) cells.
        '''

        map = io.imread("/home/krishna/devel/others/charlotte/ca-epidemic/image_pixel/africa.png", as_grey=True)
        map = transform.rotate(map,-90)
         
        # Set up the grid and schedule.

        # Use SimultaneousActivation which simulates all the cells
        # computing their next state simultaneously.  This needs to
        # be done because each cell's next state depends on the current
        # state of all its neighbours -- before they've changed.
        self.schedule = SimultaneousActivation(self)

        # Use a simple grid, where edges wrap around.
        self.grid = Grid(height, width, torus=True)

        # Place a cell at each location, with some initialized to
        # ALIVE and some to DEAD.
        for (contents, x, y) in self.grid.coord_iter():
            cell = Cell((x, y), self)
            # Creating a sea in the middle of the grid
            if map[x,y] == 1.0:
                if random() < 0.1:
                    cell.state = cell.ALIVE
                    cell.infection = random()
                    cell.infectious = True
            else:
                cell.state = cell.ALIVE
                cell.activity = cell.INACTIVE
            self.grid.place_agent(cell, (x, y))
            self.schedule.add(cell)
        self.running = True

    def step(self):
        '''
        Have the scheduler advance each cell by one step
        '''
        self.schedule.step()
