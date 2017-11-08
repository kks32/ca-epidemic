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
        # global time
        self.globaltime = 0

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
                    cell.starttime = 0
                    cell.endtime = 5000
                    cell.mobility = cell.IMMOBILE
                    cell.infection = random()
                    cell.infectious = True
                    cell.mutability = cell.IMMUTABLE
                # Ardipithecus K
                if x > 77  and x < 81 and y > 60 and y < 64:
                    cell.state = cell.DEAD
                    cell.mobility = cell.MOBILE
                    cell.infection = 0.
                    cell.starttime = 0
                    cell.endtime = 60
                    cell.infectious = True
                if x > 50  and x < 54 and y > 67 and y < 71:
                # if y > 60 and y < 65 and x > 65 and x < 70:
                    cell.state = cell.DEAD
                    cell.mobility = cell.MOBILE
                    cell.infection = 0.
                    cell.starttime =1950
                    cell.endtime = 2050
                    cell.infectious = True
                if x > 71  and x < 75 and y > 52 and y < 56:
                # if y > 60 and y < 65 and x > 65 and x < 70:
                    cell.state = cell.DEAD
                    cell.starttime = 2050
                    cell.endtime = 2150
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
 
       # global time
       self.globaltime += 1

       if self.globaltime == 88:
            for (contents, x, y) in self.grid.coord_iter():
                cell = Cell((x, y), self)
                # Ardipithecus R
                if x > 77  and x < 81 and y > 60 and y < 64:
                    cell.state = cell.DEAD
                    cell.mobility = cell.MOBILE
                    cell.infection = 0.
                    cell.starttime = 90 #1150
                    cell.endtime = 150 #1250
                    cell.infectious = True
                    cell.globaltime = self.globaltime
                    
                    self.grid.place_agent(cell, (x, y))
                    self.schedule.add(cell)

       self.schedule.step()
