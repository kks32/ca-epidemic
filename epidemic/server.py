from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule

from skimage import io, transform

from epidemic.portrayal import portrayCell
from epidemic.model import Epidemic

map = io.imread("./image_pixel/africa.png", as_grey=True)
map = transform.rotate(map,-90)

# Make a world that is 50x50, on a 250x250 display.
canvas_element = CanvasGrid(portrayCell, map.shape[0], map.shape[1], 800, 800)

chart = ChartModule([{"Label": "Infection",
                      "Color": "Black"}],
                    data_collector_name='datacollector')

server = ModularServer(Epidemic, [canvas_element, chart], "Planet of the Apes",
                       {"height": map.shape[1], "width": map.shape[0], "map": map})
