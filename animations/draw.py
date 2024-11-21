import os
import shutil
from typing import Match
import matplotlib
from matplotlib.axes import Axes
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
from matplotlib.text import Annotation, Text

from dijkstra.grid import Grid2D
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
# FRAMES_STORAGE = PROJECT_ROOT.joinpath("frames")

class DrawBoard:

    def __init__(self, frames_storage: Path|None=None) -> None:
        matplotlib.rcParams["toolbar"] = "none"
        self.fig, self.ax = plt.subplots(figsize=(16,9))
        self.fig.tight_layout()
        self.frames_storage = frames_storage
        self._frame_id = 0

        # Init the drawboard empty
        # self.show_spines(False)
        # self.show_ticks(False)
        self.dpi = 500

    def _frame_id_to_string(self):
        return str(self._frame_id).zfill(3)


    def save_fig(self, filename):
        if not self.frames_storage:
            return
        self._frame_id += 1
        name_with_id = f"{ self._frame_id_to_string() }_{ filename }"
        self.fig.savefig(self.frames_storage.joinpath(name_with_id), dpi=self.dpi)

    def save_animation(self, ani, filename):
        if not self.frames_storage:
            return
        self._frame_id += 1
        name_with_id = f"{self._frame_id_to_string()}_{filename}"
        ani.save(self.frames_storage.joinpath(name_with_id), writer="ffmpeg", fps=30, dpi=self.dpi)

    def reset_frames_storage(self):
        if not self.frames_storage:
            return
        if os.path.isdir(self.frames_storage):
            print("Removing Old storage")
            shutil.rmtree(self.frames_storage)

        os.mkdir(self.frames_storage)  # recreate the storage.


    def show_spines(self, visable=True):
        for spine in self.ax.spines.values():
            spine.set_visible(visable)

    def show_ticks(self, visable):
        self.ax.tick_params(left=visable, bottom=visable, labelleft=visable, labelbottom=visable)

    def set_backround_color(self, color):
        self.fig.set_facecolor(color)
        self.ax.set_facecolor(color)

 

class MathBox:
    def __init__(self, ax:Axes) -> None:
        self.ax = ax

        self.xlim = ax.get_xlim()
        self.ylim = ax.get_ylim()
        self.size = 3
        self.width = self.xlim[1]/self.size
        self.height = self.ylim[1]/self.size

        self.x_padding = self.xlim[1]/(self.xlim[1] - 1)
        self.y_padding = self.ylim[1]/(self.ylim[1] - 1)
 
        self.text_lines = []
        self.max_text_lines = 6
        
        self.box = self._init_box()

    def _init_box(self):
        print(f"x: {self.xlim}, y: {self.ylim}")

        pos = (self.width * (self.size - self.x_padding), self.height * (self.size - self.y_padding))

        box = Rectangle(pos, self.width, self.height, edgecolor="black", facecolor="lightblue", zorder=3)
        self.ax.add_patch(box)

        # Add the empty text lines:
        self._add_text_lines()

        return box

    def _add_text_lines(self):
        x_pos = self.xlim[1] - self.x_padding - self.width/2
        y_pos = self.ylim[1] - self.y_padding/2
        # y_pos = self.ylim[1]
        line_spacing = self.height/self.max_text_lines
        print(f"[_add_text_lines]: x: {x_pos}, y: {y_pos}, line_spacing: {line_spacing}, using padding (x,y): {self.x_padding, self.y_padding}")
        for _ in range(self.max_text_lines):
            self.text_lines.append(self.ax.text(x_pos, y_pos, "", va="center"))
            y_pos -= line_spacing
         
    def set_text(self, text, line):
        self.text_lines[line].set_text(text)

def add_edge_name(ax: Axes, edge: tuple)->Text:
    offset = 0.1
    x = edge[0] + offset
    y = edge[1] + offset

    text = ax.text(x,y,str(edge), zorder=3)
    return text


# Wrapper for Axes.annotation with default style
def add_annotation(text: str, xy=None, xytext=None, ax=None, **kwargs) -> Annotation:
    default_kwargs = {
        "arrowprops": dict(
            facecolor="black", arrowstyle="->", connectionstyle="arc3,rad=.3"
        ),
        "bbox": dict(
            boxstyle="round,pad=0.9",
            facecolor="lightblue",
            edgecolor="black",
        ),
    }
    default_kwargs.update(kwargs)

    ax = ax or plt.gca()
    ann = ax.annotate(text=text, xy=xy, xytext=xytext, **default_kwargs)  # pyright: ignore
    return ann

def add_text_box(text: str, pos: tuple, ax:Axes|None=None, **kwargs):

    default_kwargs = {
        "bbox": dict(
            boxstyle="round,pad=1.9",
            facecolor="lightblue",
            edgecolor="black",
        ),
    }
    default_kwargs.update(kwargs)
    ax = ax or plt.gca()
    box = ax.text(pos[0], pos[1], text, **default_kwargs)
    return box


if __name__ == "__main__":
    db = DrawBoard(frames_storage=None)
    # fig, ax = plt.subplots()
    grid = Grid2D.load_from_file("numpy_grids/parking_lot_grid_22_28.npy")
    grid.set_up_axis(db.ax)
    # # grid.get_grid_mesh(ax)
    # test = add_annotation("test", (2.2, 2.2), (4, 4), ax)
    # box = add_text_box("this is a box", (5,5), ax)
    mb = MathBox(db.ax)

    for i in range(6):
        mb.set_text(str(i),i)

    plt.show()
