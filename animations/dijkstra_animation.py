import matplotlib.pyplot as plt
import numpy as np
from animations.draw import DrawBoard
from dijkstra.dijkstra import DijekstraIterData, Dijkstras
from dijkstra.grid import Grid2D
from matplotlib.animation import ArtistAnimation, FuncAnimation
from matplotlib.collections import PathCollection
from .colors import colors
from matplotlib.axes import Axes
from matplotlib.patches import FancyArrowPatch

class ArtistManager:

    def __init__(self, fig, ax) -> None:
        self.fig = fig
        self.ax  = ax
    
        self.active_edge_scat = ax.scatter([], [], color="red", zorder=3, linewidths=3, visible=False)
        self.discovered_edges_scat = ax.scatter([], [], color="grey", zorder=2, linewidths=2, visible=False)

        self.neighbour_scat = ax.scatter([], [], color="green", zorder=2, visible=False)
        self.feasiable_edges_scat = ax.scatter([], [], color="green", zorder=2, visible=False)
        self.unfeasable_edges_scat = ax.scatter([], [], color="grey", zorder=2, visible=False)
        self.updated_edges_scat = ax.scatter([], [], color="green",zorder=2, linewidths=2, visible=False)

        self.queue_scat = ax.scatter([], [], facecolor="none", edgecolors="blue", zorder=1, linewidths=1, visible=False)

        self.empty = ax.scatter([], [], visible=False)

        # self.final_path, = ax.plot([], [], color="green", linewidth=3, zorder=4, visible=False)
        self.final_path, = ax.plot([], [], color="green", linewidth=3, zorder=4)
        self.exploration_graph = []

        self.discovered_edges = []
        self.unfeasable_edges = []
        self.new_queue = []

    
    def construct_final_graph(self, path):
        if len(path) > 0:
            x = [p[0] for p in path]
            y = [p[1] for p in path]
            
            self.final_path.set_data(x,y)

    
    def update_scat(self, artist: PathCollection, data: list[tuple]):
        # print(f"[update_scat] data: {data}, type: {type(data)}")
        # no new data
        if len(data):
            artist.set_offsets(data)
            # artists.set_visible(True)
            return
        # artists.set_visible(False)
        artist.set_offsets([100,100]) # Move out of screen (since we cannot set to empty)

    
    def update_artists(self, data: DijekstraIterData):
        # Update saved data
        self.unfeasable_edges.extend(data.unfeasable_edges)
        self.new_queue = data.current_queue

        self.active_edge_scat.set_offsets(data.current_edge)
        # print(f"[ Update Artists ] active edge {data.current_edge}: type: {type(data.current_edge)}")

        self.update_scat(self.discovered_edges_scat, self.discovered_edges)

        self.update_scat(self.neighbour_scat, data.neighbour_edges)
        self.update_scat(self.feasiable_edges_scat, data.feasiable_edges)

        self.update_scat(self.unfeasable_edges_scat, self.unfeasable_edges)

        self.update_scat(self.updated_edges_scat, data.updated_edges)
    
        # self.update_scat(self.queue_scat, self.new_queue)
        # self.new_queue = data.current_queue
        self.discovered_edges.append(data.current_edge)

        lines = self.make_graph(data.current_edge, data.updated_edges)
        self.exploration_graph.extend(lines)

        self.construct_final_graph(data.path)

    
    def update_queue(self):
        self.update_scat(self.queue_scat, self.new_queue)
        # self.new_queue
    
    def make_graph(self, current_edge: tuple[int,int], updated_edges: list[tuple[int,int]]) -> list[list]:

        arrows = []
        for e in updated_edges:
            arrow = FancyArrowPatch(
                        current_edge,
                        e,
                        arrowstyle="->",
                        connectionstyle="arc3",
                        color="grey",
                        linewidth=2,
                        zorder=2,
                        mutation_scale=10,
                    )
            # x = [current_edge[0], e[0]]
            # y = [current_edge[1], e[1]]
            # line, = self.ax.plot(x,y, color="grey", zorder=1, visible=False)
            self.ax.add_patch(arrow)
            arrows.append(arrow)
        return arrows



path_found = False
frame_iterations = 2
final_path = []

def animate_update(frame, artist_manager):
    global frame_iterations
    global path_found

    algo.grid.set_up_axis(db.ax)
    # NOTE: Frame does not behave correclty in the start?
    if frame < 3:
        # print(frame)
        return artist_manager.empty,

    # Default artists to draw
    active_artists = [
        artist_manager.active_edge_scat,
        artist_manager.unfeasable_edges_scat,
        artist_manager.discovered_edges_scat,
        artist_manager.queue_scat,
        # *artist_manager.exploration_graph
    ]
    active_artists.extend(artist_manager.exploration_graph)

    if path_found:
        print(f"Found the path after {frame+3} frames.")
        active_artists.append(artist_manager.final_path)
        return active_artists


    inside_iteration = frame % frame_iterations
    match inside_iteration:
        case 0:
            data = algo.iter()
            artist_manager.update_artists(data)
            path_found = data.path_found
        case 1:
            active_artists.extend(
                [
                    artist_manager.updated_edges_scat,
                ]
            )
            artist_manager.update_queue()

    for artist in active_artists:
        artist.set_visible(True)

    return active_artists

def init_function(f, artist_manager):
    """Choose wich frame to start from"""
    for i in range(3,f):
        animate_update(i, artist_manager)

if __name__ == "__main__":
    # Set up drawBoard
    db = DrawBoard(frames_storage=None)
    # db.show_spines(False)
    db.show_ticks(False)

    # Set up Scenario
    parking_lot_grid_file = np.load("numpy_grids/parking_lot_grid_22_28.npy")
    # cropped_grid = parking_lot_grid_file[0:20, 0:16]
    g = Grid2D(grid=parking_lot_grid_file)
    start_point = (1,4)
    end_point = (16, 21)
    algo = Dijkstras(g, start_point, end_point)

    algo.grid.set_up_axis(db.ax)
    mesh = algo.grid.get_grid_mesh(db.ax)
    artist_manager = ArtistManager(db.fig, db.ax)
    db.ax.scatter(end_point[0], end_point[1])
    
    frames = algo.grid.xEdgeRange.max() * algo.grid.yEdgeRange.max() * frame_iterations
    print(f"There are {frames} frames.")
    init_function(9, artist_manager)
    print(db.ax.get_xlim())
    db.ax.set_xlim(left=0)
    ani = FuncAnimation(db.fig, animate_update, frames=660, interval=10, blit=True, fargs=(artist_manager,))
    ani.save(f"frames/dijkstra_animation_{end_point[0]}_{end_point[1]}.mp4", writer="ffmpeg", fps=30, dpi=300)
    plt.show()
