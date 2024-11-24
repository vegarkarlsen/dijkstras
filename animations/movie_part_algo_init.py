from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from dijkstra.dijkstra import Dijkstras
from dijkstra.grid import Grid2D
from matplotlib.animation import FuncAnimation
from matplotlib.patches import FancyArrowPatch

from .dijkstra_animation import ArtistAnimation, ArtistManager
from .draw import (
    DrawBoard,
    EdgeDistancesAnimation,
    MathBox,
    add_annotation,
    add_edge_name,
    add_text_box,
)

PROJECT_ROOT = Path(__file__).parent.parent
FRAMES_STORAGE = PROJECT_ROOT.joinpath("frames/algo_init")
NUMPY_GRID_FILE = PROJECT_ROOT.joinpath("numpy_grids/parking_lot_grid_22_28.npy")
DEBUG = False

# plt.ion()
db = DrawBoard(frames_storage=FRAMES_STORAGE)
db.show_ticks(DEBUG)
grid = Grid2D.load_from_file(NUMPY_GRID_FILE)


# Set up Start Scenario
grid.set_up_axis(db.ax)
mesh = grid.get_grid_mesh(db.ax)

# NOTE: zoom_factor needs to match movie_part_1
zoom_factor = 13
full_grid_limits = grid.get_boarders()
db.ax.set_xlim(full_grid_limits[0], full_grid_limits[1] - zoom_factor)
db.ax.set_ylim(full_grid_limits[2], full_grid_limits[3] - zoom_factor)

start_pos = (1, 4)
end_pos = (27, 21)
algo = Dijkstras(grid, start_pos, end_pos)
algo_AM = ArtistManager(db.fig, db.ax)

# init math box
math_box = MathBox(db.ax)
math_box.box.set_visible(False)

def init_algo_board():
    # Start with empty grid and curr pos
    algo_AM.active_edge_scat.set_visible(True)
    db.save_fig("start.png")

    # Draw math box
    math_box.box.set_visible(True)
    math_box.set_first_line_as_title()
    math_box.set_text("Dijkstra's Algorithm", 0)
    db.save_fig("math_box.png")

    # Set up Box title
    math_box.set_text("Distances",1)
    math_box.set_text("Queue",2)
    db.save_fig("Algorithm_init.png")

def add_current_node_distance_ani():

    # Plot active edge label
    edge_label = add_edge_name(db.ax, data.current_edge)
    db.save_fig("active_edge.png")

    # Create edge to queue animation
    target_pos = math_box.text_lines[1].get_position()
    edge_animation = EdgeDistancesAnimation(edge_label, target_pos)
    ani = edge_animation.generate_animation(db.fig)
    db.save_animation(ani, "edge_animation.mp4")
    print("edge animation finished.")

    # Plot start edge in distances
    edge_label.set_visible(False)
    math_box.set_text(f"Distances <-- {data.current_edge} = 0", 1)
    math_box.set_text((f"Queue <-- {data.current_edge, 0}"), 2)
    db.save_fig("curr_edge_in_init.png")

def add_all_nodes_distance_ani():
    frames = 30
    target_pos = math_box.text_lines[1].get_position()
    target_pos_np = np.array([ target_pos[0]+1, target_pos[1] ])
    nodes = []
    labels = []
    steps = []
    for i in range(16):
        for j in range(10):
            if i == 1 and j == 4:
                continue
            if i >9 and i < 15 and j > 5 and j < 9:
                continue
            nodes.append((i, j))
            labels.append(add_edge_name(db.ax, (i, j)))
            step = (target_pos_np - np.array([i, j])) / frames
            steps.append(step)
            # print(f"node: {i,j} has step: {step}")

    x = np.array([n[0] for n in nodes])
    y = np.array([n[1] for n in nodes])
    all_nodes_scatter = db.ax.scatter(x, y, color="grey", zorder=2)

    db.save_fig("pre_all_nodes_animation.png")

    def update(f, labels, steps):
        for i in range(len(labels)):
            curr_pos = np.array(labels[i].get_position())
            # print(f"{curr_pos} += {steps[i]}")
            new_pos = curr_pos + steps[i]
            labels[i].set_position(new_pos)
        return labels

    ani = FuncAnimation(
        db.fig, update, frames=frames - 3, fargs=(labels, steps), interval=10, blit=True
    )
    db.save_animation(ani, "all_nodes_animation.mp4")
    print("all nodes ani saved.")

    for label in labels:
        label.set_visible(False)
    math_box.set_text("Distances <-- (all other nodes) = inf", 1)
    # math_box.set_text("",2)
    all_nodes_scatter.set_visible(False)
    db.save_fig("post_all_nodes_animation.png")

def init_visited():
    math_box.set_text("Visited <-- {}", 3)
    db.save_fig("Init visited")

db.reset_frames_storage()

data = algo.iter()
algo_AM.update_artists(data)

init_algo_board()
add_current_node_distance_ani()
add_all_nodes_distance_ani()
init_visited()

plt.show()
