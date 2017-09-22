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

    def __init__(self, height, width, map):
        '''
        Create a new playing area of (height, width) cells and map.
        '''
        # Greyscale image
        self.map = map 
         
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
            if self.map[x,y] == 1.0:
                if y > 37.5 and y < 55 and x > 37.5 and x < 62.5:
                    cell.state = cell.ALIVE
                    cell.mobility = cell.IMMOBILE
                    cell.infection = random()
                    cell.infectious = True
                    cell.mutability = cell.IMMUTABLE
                if y > 56 and y < 69 and x > 59 and x < 71:
                # if y > 60 and y < 65 and x > 65 and x < 70:
                    cell.state = cell.ALIVE
                    cell.mobility = cell.MOBILE
                    cell.infection = 0.
                    cell.infectious = True
            else:
                cell.mobility = cell.IMMOBILE
                cell.activity = cell.INACTIVE
            self.grid.place_agent(cell, (x, y))
            self.schedule.add(cell)
        self.running = True

    def step(self):
        '''
        Have the scheduler advance each cell by one step
        '''
        self.schedule.step()
