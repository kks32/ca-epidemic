from random import random

from mesa import Agent


class Cell(Agent):
    '''Represents a single ALIVE or DEAD cell in the simulation.'''
    
    DEAD = 0
    ALIVE = 1

    '''Represents a Cell is active during a simulation or not.'''

    INACTIVE = 0
    ACTIVE = 1

    '''Represents a Cell is mobile during a simulation or not.'''
    IMMOBILE = 0
    MOBILE = 1

    '''Represents a Cell is immutable during a simulation or not.'''
    IMMUTABLE = 0
    MUTABLE = 1

    

    def __init__(self, pos, model, \
                 init_state=DEAD, \
                 infection_level=0., \
                 activity_state=ACTIVE, \
                 mutability_status=MUTABLE, \
                 mobility_state=IMMOBILE): # Cells are immobile by default
        '''
        Create a cell, in the given state, at the given x, y position.
        '''
        super().__init__(pos, model)
        self.x, self.y = pos
        self.state = init_state
        self.infection = infection_level
        self._nextState = None
        self.time = 0
        self.infectious = False
        self.activity = activity_state
        self.mobility = mobility_state
        self.mutability = mutability_status
        # Time before a cell is fully infectious to its capacity
        self.infection_time = 50.
    
    @property
    def isInfectious(self):
        # If cell is set as infection
        if (self.infectious or \
            # Ready for infection
            (self.time > self.infection_time and \
             # Infection level is greater than 0
             self.infection > 0. and \
             # Cell is active
             self.state == self.ALIVE)):
            return True
        else:
            return False
    
    @property
    def infectionLevel(self):
        return self.infection

    @property
    def isMobile(self):
        return self.mobility == self.MOBILE
    
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

            # Set infection level to sum of all active neighbours
            infection_probability = 0.

            # Set Mobile neighbour as false
            mobile_neighbour = False
            
            sign = +1.0
            # When it is more than the infection time
            if self.time > 2 * self.infection_time:
                sign = -1.0

            # Iterate over neighbours
            for neighbour in self.neighbours:
                if neighbour.isInfectious:
                    infectious_neighbour = True
                    infection_probability += (0.9 * random() * neighbour.infectionLevel) * \
                                             1.0 / self.infection_time * sign
                if neighbour.isMobile:
                    mobile_neighbour = True
            # Assume nextState is unchanged, unless changed below.
            self._nextState = self.state
            if self.isAlive:
                # Increament time being alive
                self.time += 1
                if self.mutability == self.MUTABLE:
                    self.infection += min(0.9, infection_probability)
                # Deaths
                if self.time > 50 and random() > .5 and self.mutability == self.MUTABLE:
                    self._nextState = self.DEAD
                    self.infection = 0.
            else:
                # If there is an infected and a mobile neighbour
                if mobile_neighbour and infectious_neighbour:
                    self._nextState = self.ALIVE
                    self.mobility = self.MOBILE
                    # No infection on first coming alive
                    # self.infection = 0
        # Cell is inactive during simulation
        else:
            self.infection = 0
    def advance(self):
        '''
        Set the state to the new computed state -- computed in step().
        '''
        self.state = self._nextState
