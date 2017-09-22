# Colour cells based on infection level
def colourCell(cell):
    variable = cell.infectionLevel
    colour = "white"
    if (cell.isAlive):
        if (variable == 0):
            colour = "pink"
        elif (variable > 0. and variable <= 0.25):
            colour = "yellow"
        elif (variable > 0.25 and variable <= 0.5):
            colour = "green"
        elif (variable > 0.5 and variable <= 0.75):
            colour = "red"
        elif (variable > 0.75):
            colour = "black"
        else:
            colour = "purple"
    else:
        colour = "lightyellow"
    return colour

# Colour rectangle
def colourRectange(cell):
    colour = "white"
    if (cell.isMobile):
        colour = "pink"
    if not (cell.isActive):
        colour = "blue"
    return colour

# Visualiser
def portrayCell(cell):
    '''
    This function is registered with the visualization server to be called
    each tick to indicate how to draw the cell in its current state.
    :param cell:  the cell in the simulation
    :return: the portrayal dictionary.
    '''
    assert cell is not None
    return {
        "Shape": "rect",
        "w": 1,
        "h": 1,
        "Filled": "true",
        "Layer": 0,
        "x": cell.x,
        "y": cell.y,
        #"Color": colourRectange(cell)
        "Color": colourCell(cell) if cell.isActive else "blue"
    }
