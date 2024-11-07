
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

from grid import Grid2D
from dijstra import Dikstras


fig, ax = plt.subplots()

grid = Grid2D.get_test_grid()
algo = Dikstras(grid, (9,8), (13,7))
algo.grid.plot_grid(ax)

discovered_scat = ax.scatter([],[])
neighbour_scat = ax.scatter([],[], color="green")
queue_scat = ax.scatter([],[], facecolor="none", edgecolors="blue")

line, = ax.plot([], [], color="green")

edges = []
path = []

path_found = False
def animate_update(frame):
    global path_found
    global path
    if path_found:
        x = [p[0] for p in path]
        y = [p[1] for p in path]
        line.set_data(x,y)
        return discovered_scat, line

    path_found, path = algo.iter()
    edges.append(algo.current_edge)

    neighbour_scat.set_offsets(algo.neighbour_edges)
    discovered_scat.set_offsets(edges)

    queue = [q[1] for q in algo.queue_]
    queue_scat.set_offsets(queue)
    return discovered_scat, neighbour_scat, queue_scat

frames = algo.grid.xEdgeRange.max() * algo.grid.yEdgeRange.max()
ani = FuncAnimation(fig, animate_update, frames=frames, interval=100, blit=True)
plt.show()
