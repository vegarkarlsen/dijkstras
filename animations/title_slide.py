from pathlib import Path
import matplotlib.pyplot as plt
from .draw import PROJECT_ROOT, DrawBoard
from .colors import colors

# def add_text_box(text: str, pos: tuple, ax: Axes | None = None, **kwargs):
#     default_kwargs = {
#         "bbox": dict(
#             boxstyle="round,pad=1.9",
#             facecolor="lightblue",
#             edgecolor="black",
#         ),
#     }
#     default_kwargs.update(kwargs)
#     ax = ax or plt.gca()
#     box = ax.text(pos[0], pos[1], text, **default_kwargs)
#     return box


db = DrawBoard(PROJECT_ROOT.joinpath("frames"))
db.show_ticks(False)
db.show_spines(False)
db.set_backround_color("#f4f4f8")

db.ax.set_xlim(0, 1)
db.ax.set_ylim(0, 1)
title = "Path Planning using Dijkstra's Algorithm"
db.ax.text(
    0.5, 0.7,
    title,
    bbox=dict(boxstyle="round, pad=5", facecolor=colors["bg"], edgecolor="black"),
    va="center", ha="center",
    fontsize=20,
    color=colors["blue6"]
)

db.save_fig("title.png")
plt.show()
