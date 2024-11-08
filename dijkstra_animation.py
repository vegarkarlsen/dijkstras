from matplotlib.collections import PathCollection
import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation, FuncAnimation
import numpy as np

from grid import Grid2D
from dijstra import DijekstraIterData, Dikstras
from parking_lot_grid import parking_lot
fig, ax = plt.subplots(figsize=(16,9))

# grid = Grid2D.get_test_grid()

# grid[10,15:20] = 1
# grid[20:30, 10:15] = 1
# g = Grid2D.get_test_grid()
g = Grid2D(grid=parking_lot[::-1])

algo = Dikstras(g, (3, 1), (28, 22))
algo.grid.plot_grid(ax)


class ArtistManager:
    active_edge_scat = ax.scatter([], [], color="red", zorder=3, linewidths=3)
    discovered_edges_scat = ax.scatter([], [], color="grey", zorder=2, linewidths=2)

    neighbour_scat = ax.scatter([], [], color="green", zorder=2)
    feasiable_edges_scat = ax.scatter([], [], color="green", zorder=2)
    unfeasable_edges_scat = ax.scatter([], [], color="black", zorder=2)
    updated_edges_scat = ax.scatter([], [], color="green",zorder=2, linewidths=2)

    queue_scat = ax.scatter([], [], facecolor="none", edgecolors="blue", zorder=1, linewidths=1)

    empty = ax.scatter([], [])

    final_path, = ax.plot([], [], color="green", linewidth=3, zorder=4)
    exploration_graph = []

    discovered_edges = []
    unfeasable_edges = []
    new_queue = []

    @classmethod
    def construct_final_graph(cls, path):
        if len(path) > 0:
            x = [p[0] for p in path]
            y = [p[1] for p in path]
            
            cls.final_path.set_data(x,y)

    @classmethod
    def update_scat(cls, artists: PathCollection, data):
        if len(data):
            artists.set_offsets(data)
            artists.set_visible(True)
            return
        artists.set_visible(False)

    @classmethod
    def update_artists(cls, data: DijekstraIterData):
        # Update saved data
        cls.unfeasable_edges.extend(data.unfeasable_edges)
        cls.new_queue = data.current_queue

        cls.active_edge_scat.set_offsets(data.current_edge)

        cls.update_scat(cls.discovered_edges_scat, cls.discovered_edges)

        cls.update_scat(cls.neighbour_scat, data.neighbour_edges)
        cls.update_scat(cls.feasiable_edges_scat, data.feasiable_edges)

        cls.update_scat(cls.unfeasable_edges_scat, cls.unfeasable_edges)

        cls.update_scat(cls.updated_edges_scat, data.updated_edges)
    
        # cls.update_scat(cls.queue_scat, cls.new_queue)
        # cls.new_queue = data.current_queue
        cls.discovered_edges.append(data.current_edge)

        lines = cls.make_graph(data.current_edge, data.updated_edges)
        cls.exploration_graph.extend(lines)

        cls.construct_final_graph(data.path)

    @classmethod
    def update_queue(cls):
        cls.update_scat(cls.queue_scat, cls.new_queue)
        # cls.new_queue
    
    @classmethod
    def make_graph(cls, current_edge: tuple[int,int], updated_edges: list[tuple[int,int]]) -> list[list]:

        lines = []
        for e in updated_edges:
            x = [current_edge[0], e[0]]
            y = [current_edge[1], e[1]]
            line, = ax.plot(x,y, color="grey", zorder=1)
            lines.append(line)
        return lines



path_found = False
frame_iterations = 2
final_path = []

def animate_update(frame):
    global frame_iterations
    global path_found

    # NOTE: Frame does not behave correclty in the start?
    if frame < 3:
        # print(frame)
        return ArtistManager.empty,

    # Default artists to draw
    active_artists = [
        ArtistManager.active_edge_scat,
        ArtistManager.unfeasable_edges_scat,
        ArtistManager.discovered_edges_scat,
        ArtistManager.queue_scat,
        # *ArtistManager.exploration_graph
    ]
    active_artists.extend(ArtistManager.exploration_graph)

    if path_found:
        active_artists.append(ArtistManager.final_path)
        return active_artists


    inside_iteration = frame % frame_iterations
    match inside_iteration:
        case 0:
            data = algo.iter()
            ArtistManager.update_artists(data)
            path_found = data.path_found
        case 1:
            active_artists.extend(
                [
                    ArtistManager.updated_edges_scat,
                ]
            )
            ArtistManager.update_queue()

    return active_artists


frames = algo.grid.xEdgeRange.max() * algo.grid.yEdgeRange.max() * frame_iterations
print(f"There are {frames} frames.")
ani = FuncAnimation(fig, animate_update, frames=frames, interval=1, blit=True)
# ani.save("animation.mp4", writer="ffmpeg", fps=30, dpi=200)
plt.show()
