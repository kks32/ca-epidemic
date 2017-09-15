from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

from epidemic.portrayal import portrayCell
from epidemic.model import Epidemic


# Make a world that is 50x50, on a 250x250 display.
canvas_element = CanvasGrid(portrayCell, 50, 50, 250, 250)

server = ModularServer(Epidemic, [canvas_element], "Planet of the Apes",
                       {"height": 50, "width": 50})
