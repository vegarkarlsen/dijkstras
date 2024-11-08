
import numpy as np
from grid import Grid2D
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
# from matplotlib.animation import ArtistAnimation
from matplotlib.animation import FuncAnimation
import re

plt.ion()
fig, ax = plt.subplots(figsize=(14,11))
fig.tight_layout()

img = mpimg.imread("figures/parking_lot_everline_cropped.jpg")

# g = np.zeros((20,30))
g = np.load("parking_lot_grid_20_30.npy")

walking_grid = Grid2D(g)
walking_grid.grid[np.where(walking_grid.grid == 1)] = 3
# keep_grid = Grid2D(g)
walking_grid.set_up_axis(ax)
pimg = ax.imshow(img, zorder=0, extent=walking_grid.get_boarders(), aspect="auto")

# keep_row = False
# row_added = True

# keep_grid = np.zeros(g.shape)
keep_grid = np.array(g)

running = True
cell = 0,0

walking_grid.grid[0,0] = 1
message = []

while running:
    print("\033c", end="")
    # print(walking_grid.grid)
    print("".join(message))
    if len(message) > 0:
        message.clear()

    if walking_grid.grid[cell] == 3:
        walking_grid.grid[cell] = 2
    else:
        walking_grid.grid[cell] = 1

    walk_mesh = walking_grid.get_grid_mesh(ax)
    walk_mesh.set_alpha(0.5)
    plt.draw()

    if walking_grid.grid[cell] == 2:
        walking_grid.grid[cell] = 3
    else:
        walking_grid.grid[cell] = 0


    command = input("-> ")
    match command:
        case "a":
            keep_grid[cell] = 1
            walking_grid.grid[cell] = 3
            message.append(f"{cell} = {keep_grid[cell]}")

        case "d":
            keep_grid[cell] = 0
            walking_grid.grid[cell] = 0
            message.append(f"{ cell } = {keep_grid[cell]}")

        case "ra":
            keep_grid[cell[0], :] = 1
            walking_grid.grid[cell[0], :] = 3
            message.append("keep current row")
        case "rd":
            keep_grid[cell[0], :] = 0
            walking_grid.grid[cell[0], :] = 0
            message.append("remove current row")

        case "ca":
            keep_grid[:, cell[1]] = 1
            walking_grid.grid[:, cell[1]] = 3
            message.append("keep current col")
        case "cd":
            keep_grid[:, cell[1]] = 0
            walking_grid.grid[:, cell[1]] = 0
            message.append("remove current col")

        case command if re.match(r'^k', command): # Up
            step = 1
            if len(command) > 1:
                try:
                    step = int( command[1:] )
                except ValueError:
                    step = 1
            if cell[0] + step > g.shape[0]:
                continue
            cell = (cell[0] + step, cell[1])
        case command if re.match(r'^j', command): # down
            step = 1
            if len(command) >1:
                try:
                    step = int( command[1:] )
                except ValueError:
                    step = 1
            if cell[0] - step < 0:
                continue
            cell = (cell[0] - step, cell[1])
        case command if re.match(r'^h', command): # left
            step = 1
            if len(command) >1:
                try:
                    step = int( command[1:] )
                except ValueError:
                    step = 1
            if cell[1] - step < 0:
                continue
            cell = (cell[0], cell[1] - step)
        case command if re.match(r'^l', command): # right
            step = 1
            if len(command) > 1:
                try:
                    step = int( command[1:] )
                except ValueError:
                    step = 1
            if cell[1] + step > g.shape[1]:
                continue
            cell = (cell[0], cell[1] + step)
        case "q":
            running = False
            break


    walk_mesh.remove()
    # keep_mesh.remove()

np.save("parking_lot_grid_20_30.npy", keep_grid)


# fig.tight_layout()
# plt.show()


