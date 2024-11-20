# from matplotlib.lines import Line2D
# from matplotlib.text import Annotation
from genericpath import isdir
import os
from pathlib import Path

import matplotlib
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
from dijkstra.grid import Grid2D
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle

from .colors import colors
from .draw import DrawBoard, add_annotation, add_text_box
import shutil

PROJECT_ROOT = Path(__file__).parent.parent
parking_lot_image = mpimg.imread(
    PROJECT_ROOT.joinpath("figures/parking_lot_everline_cropped.jpg")
)
numpy_file = PROJECT_ROOT.joinpath("numpy_grids/add_cells_22_28.npy")
numpy_file_full_grid = PROJECT_ROOT.joinpath("numpy_grids/parking_lot_grid_22_28.npy")

frames_storage = PROJECT_ROOT.joinpath("frames")


def clean_frames_storage():
    if os.path.isdir(frames_storage):
        print("Removing Old storage")
        shutil.rmtree(frames_storage)

    os.mkdir(frames_storage)  # recreate the storage.


db = DrawBoard()
db.show_spines(False)
db.show_ticks(False)

db.ax.set_xlim(0, 1)
db.ax.set_ylim(0, 1)
# db.set_backround_color(colors['fg'])

g = np.load(numpy_file)
empty_grid = np.zeros(g.shape)
grid = Grid2D(g)
full_grid = Grid2D.load_from_file(numpy_file_full_grid)


def add_intro_text(ax):
    box_args = dict(
        boxstyle="round,pad=1.9",
        facecolor=colors["fg_dark"],
        edgecolor="black",
    )
    # x_pos = grid.xEdgeRange.max() / 2
    # y_pos = grid.yEdgeRange.max() / 2
    x_pos = 0.5
    y_pos = 0.65
    intro_text = "Shortest path using dijkstra's Algorithm"
    raw_grid_ann = ax.text(
        x_pos, y_pos, intro_text, bbox=box_args, va="center", ha="center", fontsize="16"
    )
    return raw_grid_ann


# Intro
def make_intro():
    intro_text_box = add_intro_text(db.ax)
    db.save_fig("headline.png")
    intro_text_box.set_visible(False)  # TODO: Add transition?
    # def update1(f):
    #     x_pos, y_pos = intro_text_box.get_position()
    #
    #     if f < 17:
    #         y_pos -= 0.02
    #
    #     if f > 70:
    #         x_pos += 0.02
    #
    #     intro_text_box.set_position((x_pos, y_pos))
    #     return intro_text_box,
    #
    # ani = FuncAnimation(db.fig, update1, frames=300, interval=10)


# Add map
def add_map():
    pimg = db.ax.imshow(
        parking_lot_image, zorder=0, extent=grid.get_boarders(), aspect="auto"
    )
    db.ax.set_xlim(0, 28)
    db.ax.set_ylim(0, 22)
    db.save_fig("raw_parking_lot.png")


def add_start_and_end_pos():
    start_pos = (1, 3)
    end_pos = (27, 21)

    # TODO: Consider adding start first then end
    start_pos_scat = db.ax.scatter(start_pos[0], start_pos[1], color="green", linewidths=3)
    end_pos_scat = db.ax.scatter(end_pos[0], end_pos[1], color="red", linewidths=3)

    db.save_fig("start_end_pos.png")

    start_ann = add_annotation("Start position", (1.1,3.1), (3, 5))
    end_ann = add_annotation("End position", (26.9, 20.9), (25, 19))
    db.save_fig("start_end_pos.png")

    start_ann.set_visible(False)
    end_ann.set_visible(False)
    db.save_fig("start_end_pos.png")
    start_pos_scat.set_visible(False)
    end_pos_scat.set_visible(False)


def add_grid():
    grid.set_up_axis(db.ax)
    db.ax.grid(color="black")
    db.save_fig("parking_lot_grid.png")


def add_car_grided():
    grid_mesh = grid.get_grid_mesh(db.ax)
    db.save_fig("car_gridded.png")

    grid_fill_ann = add_annotation("Obstacle", (5.1, 10.1), (7, 12), db.ax)
    db.save_fig("car_gridded.png")

    grid_fill_ann.set_visible(False)  # remove the annotation
    db.save_fig("car_gridded.png")


def add_full_grid():
    db.ax.clear()
    full_grid.set_up_axis(db.ax)
    full_grid.get_grid_mesh(db.ax)
    db.save_fig("fully_gridded.png")

def transition_to_dijkstra_lecture():

    # Scope hack
    class AniData:
        xlim = full_grid.xEdgeRange.max()
        ylim = full_grid.yEdgeRange.max()
        grid_mesh = full_grid.get_grid_mesh(db.ax)


    frames = 60
    zoom_factor = 13
    step_decrese = zoom_factor/frames
    print(f"step_decrese: {step_decrese}, xlim: {AniData.xlim}")

    def init():
        full_grid.set_up_axis(db.ax)
        AniData.xlim = full_grid.xEdgeRange.max()
        AniData.ylim = full_grid.yEdgeRange.max()
        return AniData.grid_mesh,


    def update(f):
        AniData.xlim -= step_decrese
        AniData.ylim -= step_decrese
        # print(f"limx: x {AniData.xlim} y: {AniData.ylim}")
        db.ax.set_xlim(0,AniData.xlim)
        db.ax.set_ylim(0,AniData.ylim)
        return AniData.grid_mesh,
    
    ani = FuncAnimation(db.fig, update, frames=frames, interval=10, init_func=init)
    db.save_animation(ani, "grid_zoom.mp4")
    return ani

clean_frames_storage()
make_intro()
add_map()
add_start_and_end_pos()
add_grid()
add_car_grided()
add_full_grid()
ani = transition_to_dijkstra_lecture()

plt.show()
