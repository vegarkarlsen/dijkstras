import matplotlib.pyplot as plt
from .dijkstra_animation import ArtistManager
from dijkstra.dijkstra import Dijkstras
from dijkstra.grid import Grid2D
from .draw import DrawBoard

import numpy as np

# Set up drawBoard
db = DrawBoard(frames_storage=None)
# db.show_spines(False)
db.show_ticks(False)

# Set up Scenario
parking_lot_grid_file = np.load("numpy_grids/parking_lot_grid_22_28.npy")
# cropped_grid = parking_lot_grid_file[0:20, 0:16]
g = Grid2D(grid=parking_lot_grid_file)
start_point = (1,4)
end_point = (16, 21)
algo = Dijkstras(g, start_point, end_point)

algo.grid.set_up_axis(db.ax)
mesh = algo.grid.get_grid_mesh(db.ax)
artist_manager = ArtistManager(db.fig, db.ax)
db.ax.set_xlim(left=0)


path_found = False

while not path_found:
    data = algo.iter()
    path_found = data.path_found
    artist_manager.update_artists(data)

db.ax.scatter(end_point[0], end_point[1], color="Orange", linewidths=2, zorder=100)
db.ax.scatter(start_point[0], start_point[1], color="red", linewidths=2, zorder=100)
db.fig.savefig("frames/Final_image.png")
plt.show()
