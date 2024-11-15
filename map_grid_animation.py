

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np

from matplotlib.animation import ArtistAnimation
from matplotlib.animation import FuncAnimation

from grid import Grid2D
from draw import add_annotation



fig, ax = plt.subplots(figsize=(14,11))
fig.tight_layout()

img = mpimg.imread("figures/parking_lot_everline_cropped.jpg")

numpy_file = "numpy_grids/add_cells_22_28.npy"
g = np.load(numpy_file)
empty_grid = np.zeros(g.shape)
grid = Grid2D(g)
grid.set_up_axis(ax)

grid_mesh = grid.get_grid_mesh(ax)
ann = add_annotation("Add tile", (5.1,10.1), ( 7,12 ), ax)


frames = []
pimg = ax.imshow(img, zorder=0, extent=grid.get_boarders(), aspect="auto")

frames.extend([grid_mesh] for _ in range(10))

frames.extend([grid_mesh, ann] for _ in range(10))










# for row in range(g.shape[0]):
#     for col in range(g.shape[1]):
#         if g[row, col] == 3:
#             # print("added")
#             grid.grid[row, col] = 1
#             frames.append([grid.get_grid_mesh(ax), pimg]*5)

# print(frames)

# frames.extend([grid.get_grid_mesh(ax), pimg] for _ in range(10))

ani = ArtistAnimation(fig, frames, interval=100)


plt.show()



