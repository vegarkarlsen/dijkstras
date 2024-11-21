import numpy as np
from pathlib import Path
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt

from dijkstra.dijkstra import Dijkstras
from dijkstra.grid import Grid2D
from .draw import DrawBoard, add_annotation, add_edge_name, add_text_box, MathBox

from .dijkstra_animation import ArtistAnimation, ArtistManager


PROJECT_ROOT = Path(__file__).parent.parent
FRAMES_STORAGE = PROJECT_ROOT.joinpath("frames/part2")
NUMPY_GRID_FILE = PROJECT_ROOT.joinpath("numpy_grids/parking_lot_grid_22_28.npy")
DEBUG = True

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
# math_box.set_text("0", 0)
# math_box.set_text("Distances = []", 1)
# math_box.set_text("Distances[test] = []", 2)
# math_box.set_text("Parents = []", 2)
# math_box.set_text("3",3)
# math_box.set_text("4",4)
# math_box.set_text("5",5)

class EdgeDistancesAnimation:

    def __init__(self, edge_label, target_pos, frames=40) -> None:
        self.edge_label = edge_label
        self.pos = np.array(edge_label.get_position())
        self.target_pos = np.array(target_pos)
        self.frames = frames
        self.step = (self.target_pos-self.pos)/self.frames
        # self.x_step = abs(self.target_x-self.x)/(self.frames)
        # self.y_step = abs(self.target_y-self.y)/(self.frames)
        print(f"start_pos: {self.pos}, target: {self.target_pos}, step: {self.step}")

    def update(self, f, edge_label):
        # print(self.pos, len(self.pos))
        # print(self.step)
        self.edge_label.set_position(self.pos)
        self.pos += self.step
        return edge_label,
        
    def generate_animation(self):
        ani = FuncAnimation(db.fig, self.update, frames=self.frames-3, blit=True, interval=10, fargs=(self.edge_label,))
        return ani
        # db.save_animation(ani, "edge_animation.mp4")
        


def add_algo_intro():

    db.save_fig("start.png")

    math_box.box.set_visible(True)
    math_box.set_text("Algorithm", 0)
    db.save_fig("math_box.png")

    algo_AM.active_edge_scat.set_visible(True)
    db.save_fig("active_edge.png")
    
    edge_label = add_edge_name(db.ax, data.current_edge)
    db.save_fig("active_edge.png")

    # math_box.set_text(f"Distances <-- {data.current_edge} = 0", 1)
    math_box.set_text("Distances", 1)

    edge_animation = EdgeDistancesAnimation(edge_label, math_box.text_lines[1].get_position())
    ani = edge_animation.generate_animation()
    db.save_animation(ani, "edge_animation.mp4")
    print("edge animation finished.")
    edge_label.set_visible(False)

    math_box.set_text(f"Distances <-- {data.current_edge} = 0", 1)
    db.save_fig("after_edge_animation.png")

def add_all_nodes_distance_ani():

    frames = 40
    target_pos = np.array(math_box.text_lines[1].get_position())
    nodes = []
    labels = []
    steps = []
    for i in range(16):
        for j in range(10):
            if i == 1 and j == 4:
                continue
            nodes.append((i,j))
            labels.append(add_edge_name(db.ax, (i,j)))
            step = ( target_pos - np.array([i,j]) )/frames
            steps.append(step)
            print(f"node: {i,j} has step: {step}")

    x = np.array([n[0] for n in nodes])
    y = np.array([n[1] for n in nodes])
    all_nodes_scatter = db.ax.scatter(x,y,color="grey",zorder=2)

    db.save_fig("pre_all_nodes_animation.png")

    def update(f, labels, steps):
        for i in range(len(labels)):
            curr_pos = np.array(labels[i].get_position())
            print(f"{curr_pos} += {steps[i]}")
            new_pos = curr_pos + steps[i]
            labels[i].set_position(new_pos)
        return labels

    ani = FuncAnimation(db.fig, update, frames=frames-3,fargs=(labels, steps), interval=10, blit=True)
    db.save_animation(ani, "all_nodes_animation.mp4")
    print("all nodes ani saved.")

    math_box.set_text("Distances <-- (all other nodes) = inf", 1)
    all_nodes_scatter.set_visible(False)
    db.save_fig("post_all_nodes_animation.png")

def add_neigbour_edges():
    algo_AM.active_edge_scat.set_visible(True)
    algo_AM.neighbour_scat.set_visible(True)
    db.save_fig("neighbour.png")

    labels = []
    for edge in data.neighbour_edges:
        labels.append(add_edge_name(db.ax, edge))



# def add_active_edge():
#     data = algo.iter()
#     algo_AM.update_artists(data)
#     algo_AM.active_edge_scat.set_visible(True)
#     db.save_fig("active_edge.png")

# def add_neigbour_edges():
#     text = "Neighbour nodes"
#
#     algo_AM.neighbour_scat.set_visible(True)
#     db.save_fig("neighbour.png")
#
#     neighbour_text = add_annotation(text, (2.1, 5.1), (3, 6), db.ax)
#     db.save_fig("neighbour_text.png")
#
#     neighbour_text.set_visible(False)
#     db.save_fig("neighbour.png")

# def add_exploration_graph():
#
#     text = "Neightbour nodes becomes parent to current node"
#
#     for line in algo_AM.exploration_graph:
#         line.set_visible(True)
#     db.save_fig("exploration_graph.png")
#
#     graph_creation_text = add_annotation(
#         text, (1.5, 3.5), (2, 5)
#     )
#     db.save_fig("exploration_graph_text.png")
#
#     graph_creation_text.set_visible(False)
#     db.save_fig("exploration_graph_text.png")

# def add_neigbour_edges_to_queue():
#
#     text = "Put neighbour nodes in queue"
#
#     algo_AM.neighbour_scat.set_visible(False)
#     algo_AM.queue_scat.set_visible(True)
#     algo_AM.update_queue()
#     db.save_fig("queue.png")
#
#     add_to_queue_text = add_text_box(text,( 2,5 ))
#     db.save_fig("queue_text.png")
#
#     add_to_queue_text.set_visible(False)
#     db.save_fig("queue_text.png")

# def second_iteration():
#     data = algo.iter()
#     algo_AM.update_artists(data)
#     algo_AM.updated_edges_scat.set_visible(True)
#     algo_AM.unfeasable_edges_scat.set_visible(True)
#     db.save_fig("second_iteration.png")


db.reset_frames_storage()

data = algo.iter()
algo_AM.update_artists(data)
# add_algo_intro()
# add_all_nodes_distance_ani()
add_neigbour_edges()

# add_neigbour_edges()
# add_exploration_graph()
# add_neigbour_edges_to_queue()
# second_iteration()


# algo_AM.update_artists(algo.iter())
# algo_AM.update_artists(algo.iter())
#
plt.show()
