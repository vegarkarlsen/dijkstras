
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

FRAMES_STORAGE = PROJECT_ROOT.joinpath("frames/part3")


db = DrawBoard(frames_storage=FRAMES_STORAGE)
db.show_spines(False)
db.show_ticks(False)

db.ax.set_xlim(0, 1)
db.ax.set_ylim(0, 1)
# db.set_backround_color(colors['fg'])

g = np.load(numpy_file)
empty_grid = np.zeros(g.shape)
grid = Grid2D(g)
full_grid = Grid2D.load_from_file(numpy_file_full_grid)

def zoom(direction=-1):

    # Scope hack
    class AniData:
        xlim = full_grid.xEdgeRange.max()
        ylim = full_grid.yEdgeRange.max()
        grid_mesh = full_grid.get_grid_mesh(db.ax)


    # NOTE: zoom_factor needs to match movie_part_2
    frames = 30
    zoom_factor = 13
    step_decrese = zoom_factor/frames
    print(f"step_decrese: {step_decrese}, xlim: {AniData.xlim}")

    def init():
        full_grid.set_up_axis(db.ax)
        AniData.xlim = full_grid.xEdgeRange.max()
        AniData.ylim = full_grid.yEdgeRange.max()
        return AniData.grid_mesh,


    def update(f):
        AniData.xlim += step_decrese * direction
        AniData.ylim += step_decrese * direction
        # print(f"limx: x {AniData.xlim} y: {AniData.ylim}")
        db.ax.set_xlim(0,AniData.xlim)
        db.ax.set_ylim(0,AniData.ylim)
        return AniData.grid_mesh,
    
    ani = FuncAnimation(db.fig, update, frames=frames, interval=10, init_func=init)
    db.save_animation(ani, "grid_zoom.mp4")
    return ani

db.reset_frames_storage()
zoom()
