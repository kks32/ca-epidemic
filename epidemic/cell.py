from random import random

from mesa import Agent


class Cell(Agent):
    '''Represents a single ALIVE or DEAD cell in the simulation.'''
    
    DEAD = 0
    ALIVE = 1

    '''Represents a single is active during a simulation or not.'''

    INACTIVE = 0
    ACTIVE = 1

    def __init__(self, pos, model, init_state=DEAD, infection_level=0., activity_state=ACTIVE):
        '''
        Create a cell, in the given state, at the given x, y position.
        '''
        super().__init__(pos, model)
        self.x, self.y = pos
        self.state = init_state
        self.infection = infection_level
        self._nextState = None
        self.time = 0
        # Time before a cell is fully infectious to its capacity
        self.infection_time = 50.
        self.infectious = False
        self.activity = activity_state
    
    @property
    def isInfectious(self):
        if (self.infectious or (self.time > self.infection_time and self.state == self.ALIVE)):
            return True
        else:
            return False
    
    @property
    def infectionLevel(self):
        return self.infection

    @property
    def isActive(self):
        return self.activity == self.ACTIVE

    @property
    def isAlive(self):
        return self.state == self.ALIVE

    @property
    def neighbours(self):
        return self.model.grid.neighbor_iter((self.x, self.y), True)

    def step(self):
        if self.activity == self.ACTIVE:
            '''
            Compute if the cell will be dead or alive at the next tick.  Th#is is
            based on the number of alive or dead neighbours.  The state is not
            changed here, but is just computed and stored in self._nextState,
            because our current state may still be necessary for our neighbours
            to calculate their next state.
            '''
            # Get the neighbours and apply the rules on whether to be alive or dead
            # at the next tick.
            live_neighbours = sum(neighbour.isAlive for neighbour in self.neighbours)

            # Check if at least one active neighbour is infectious
            infectious_neighbour = False
            for neighbour in self.neighbours:
                if neighbour.isInfectious:
                    infectious_neighbour = True
                    
            # Assume nextState is unchanged, unless changed below.
            self._nextSstate = self.state
            if self.isAlive:
                # Increament time being alive
                self.time += 1
                # Set infection level to sum of all active neighbours
                infection_probability = 0.
                for neighbour in self.neighbours:
                    if neighbour.isInfectious:
                        infection_probability += neighbour.infectionLevel * 1.0 / self.infection_time

                self.infection += min(0.9, infection_probability)
                # Deaths
                if self.time > 30 and live_neighbours <=2 and random() > .75:
                    self._nextState = self.DEAD
            else:
                # If there is an infected neighbour
                if infectious_neighbour:
                    self._nextState = self.ALIVE
                    # No infection on first coming alive
                    self.infection = 0
        # Cell is inactive during simulation
        else:
            self.infection = 0
    def advance(self):
        '''
        Set the state to the new computed state -- computed in step().
        '''
        self.state = self._nextState
