from matplotlib.axes import Axes
import matplotlib.pyplot as plt
from matplotlib.text import Annotation

from grid import Grid2D



# class Point:
#     def __init__(self, x, y) -> None:
#         self.x = x
#         self.y = y
#
#     def __call__(self):
#         return (self.x, self.y)
#
#     def __add__(self, other):
#         if isinstance(other, Point):
#             return Point(self.x + other.x, self.y + other.y)
#         return NotImplementedError
#
#     def __subtract__(self, other):
#         if isinstance(other, Point):
#             return Point(self.x - other.x, self.y - other.y)
#         return NotImplementedError

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



if __name__ == "__main__":
    fig, ax = plt.subplots()
    grid = Grid2D.load_from_file("numpy_grids/parking_lot_grid_22_28.npy")
    # grid.set_up_axis(ax)
    # grid.get_grid_mesh(ax)
    # test = add_annotation("test", (2.2, 2.2), (4, 4), ax)

    plt.show()
