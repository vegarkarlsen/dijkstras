import matplotlib.pyplot as plt
import numpy as np
from animations.draw import DrawBoard
from dijkstra.dijkstra import DijekstraIterData, Dijkstras
from dijkstra.grid import Grid2D
from matplotlib.animation import ArtistAnimation, FuncAnimation
from matplotlib.collections import PathCollection
from .colors import colors
from matplotlib.axes import Axes

class ArtistManager:

    def __init__(self, fig, ax) -> None:
        self.fig = fig
        self.ax  = ax
    
        self.active_edge_scat = ax.scatter([], [], color="red", zorder=3, linewidths=3)
        self.discovered_edges_scat = ax.scatter([], [], color="grey", zorder=2, linewidths=2)

        self.neighbour_scat = ax.scatter([], [], color="green", zorder=2)
        self.feasiable_edges_scat = ax.scatter([], [], color="green", zorder=2)
        self.unfeasable_edges_scat = ax.scatter([], [], color="black", zorder=2)
        self.updated_edges_scat = ax.scatter([], [], color="green",zorder=2, linewidths=2)

        self.queue_scat = ax.scatter([], [], facecolor="none", edgecolors="blue", zorder=1, linewidths=1)

        self.empty = ax.scatter([], [])

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

    
    def update_scat(self, artists: PathCollection, data):
        if len(data):
            artists.set_offsets(data)
            artists.set_visible(True)
            return
        artists.set_visible(False)

    
    def update_artists(self, data: DijekstraIterData):
        # Update saved data
        self.unfeasable_edges.extend(data.unfeasable_edges)
        self.new_queue = data.current_queue

        self.active_edge_scat.set_offsets(data.current_edge)

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

        lines = []
        for e in updated_edges:
            x = [current_edge[0], e[0]]
            y = [current_edge[1], e[1]]
            line, = self.ax.plot(x,y, color="grey", zorder=1)
            lines.append(line)
        return lines



path_found = False
frame_iterations = 2
final_path = []

def animate_update(frame, artist_manager):
    global frame_iterations
    global path_found

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

    return active_artists

if __name__ == "__main__":
    # Set up drawBoard
    db = DrawBoard()
    # db.show_spines(False)
    db.show_ticks(False)

    # Set up Scenario
    parking_lot_grid_file = np.load("numpy_grids/parking_lot_grid_22_28.npy")
    g = Grid2D(grid=parking_lot_grid_file)
    algo = Dijkstras(g, (1, 3), (27, 21))

    algo.grid.set_up_axis(db.ax)
    mesh = algo.grid.get_grid_mesh(db.ax)
    artist_manager = ArtistManager(db.fig, db.ax)
    
    frames = algo.grid.xEdgeRange.max() * algo.grid.yEdgeRange.max() * frame_iterations
    print(f"There are {frames} frames.")
    ani = FuncAnimation(db.fig, animate_update, frames=frames, interval=10, blit=True, fargs=(artist_manager,))
    # ani.save("animation.mp4", writer="ffmpeg", fps=30, dpi=200)
    plt.show()
