import matplotlib
from matplotlib.axes import Axes
import matplotlib.pyplot as plt
from matplotlib.text import Annotation

from dijkstra.grid import Grid2D
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
frames_storage = PROJECT_ROOT.joinpath("frames")

class DrawBoard:

    def __init__(self) -> None:
        matplotlib.rcParams["toolbar"] = "none"
        self.fig, self.ax = plt.subplots(figsize=(16,9))
        self.fig.tight_layout()
        self.frames_storage = frames_storage
        self._frame_id = 0

        # Init the drawboard empty
        # self.show_spines(False)
        # self.show_ticks(False)

    def _frame_id_to_string(self):
        return str(self._frame_id).zfill(3)


    def save_fig(self, filename):
        name_with_id = f"{ self._frame_id_to_string() }_{ filename }"
        self.fig.savefig(self.frames_storage.joinpath(name_with_id))
        self._frame_id += 1

    def save_animation(self, ani, filename):
        name_with_id = f"{self._frame_id_to_string()}_{filename}"
        ani.save(self.frames_storage.joinpath(name_with_id), writer="ffmpeg", fps=30, dpi=200)
        self._frame_id += 1


    def show_spines(self, visable=True):
        for spine in self.ax.spines.values():
            spine.set_visible(visable)

    def show_ticks(self, visable):
        self.ax.tick_params(left=visable, bottom=visable, labelleft=visable, labelbottom=visable)

    def set_backround_color(self, color):
        self.fig.set_facecolor(color)
        self.ax.set_facecolor(color)

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
    fig, ax = plt.subplots()
    grid = Grid2D.load_from_file("numpy_grids/parking_lot_grid_22_28.npy")
    grid.set_up_axis(ax)
    # grid.get_grid_mesh(ax)
    test = add_annotation("test", (2.2, 2.2), (4, 4), ax)
    box = add_text_box("this is a box", (5,5), ax)

    plt.show()
