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
        self.max_infection_level = 0.
        self._nextState = None
        self.time = 0
        self.active_time = 0
        self.infected_time = 0
        self.globaltime = 0
        self.starttime = 0
        self.endtime = 500
        self.mobiletime = 250
        self.infectious = False
        self.activity = activity_state
        self.mobility = mobility_state
        self.mutability = mutability_status
        # Time before a cell is fully infectious to its capacity
        self.infection_time = 50.
        # Time for which it will remain infectious
        self.active_infection_time = 100.
        self.threshold_infection_level = 0.5
    
    @property
    def isInfectious(self):
        # If cell is set as infection
        if (self.infectious or \
            # Ready for infection
            (self.infected_time > self.infection_time and \
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
        # If a cell is active
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
            if self.infected_time > self.infection_time:
                # Infection level remains stable
                if self.infected_time < (self.infection_time + self.active_infection_time):
                    sign = 0.
                # Infection effect decreases to a threshold
                else:
                    sign = -1.0

            # Iterate over neighbours
            for neighbour in self.neighbours:
                if neighbour.isInfectious and neighbour.isAlive:
                    infectious_neighbour = True
                    infection_probability += (0.9 * random() * neighbour.infectionLevel) * \
                                             1.0 / self.infection_time * sign

                if neighbour.isMobile and neighbour.isAlive:
                    mobile_neighbour = True

            # When a neighbour is mobile
            if mobile_neighbour:
                self.time += 1

            # Assume nextState is unchanged, unless changed below.
            self._nextState = self.state
            if self.isAlive:
                # Increament time being alive
                self.active_time += 1
                if self.mutability == self.MUTABLE:
                    self.infection += min(0.9, infection_probability)
                    # Duration of infection
                    if self.infection > 1.E-10:
                        self.infected_time += 1

                    # Highest infection level
                    if self.infection > self.max_infection_level and sign == 1.0:
                        self.max_infection_level = self.infection

                    # Level of infection
                    if self.infection < self.threshold_infection_level and sign == -1.0:
                        if (self.max_infection_level > self.threshold_infection_level):
                            self.infection = self.threshold_infection_level
                        else:
                            self.infection = self.max_infection_level
                # Deaths
                if self.globaltime > self.endtime and self.mutability == self.MUTABLE:
                    self._nextState = self.DEAD
                    self.infection = 0.

                # After a certain time cell becomes immobile
                if self.globaltime > self.mobiletime and self.isAlive:
                    self._nextState = self.IMMOBILE

            else:
                # If there is a mobile neighbour
                if mobile_neighbour and self.time > self.infection_time and self.globaltime < self.mobiletime:
                    self._nextState = self.ALIVE
                    self.mobility = self.MOBILE
                    # No infection on first coming alive
                    # self.infection = 0

        # Cell is inactive during simulation
        else:
            self.infection = 0

        # Increament global time
        self.globaltime += 1
        
    def advance(self):
        '''
        Set the state to the new computed state -- computed in step().
        '''
        self.state = self._nextState
