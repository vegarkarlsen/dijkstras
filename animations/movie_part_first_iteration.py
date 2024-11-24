
from matplotlib.patches import FancyArrowPatch
from pathlib import Path
import matplotlib.pyplot as plt

from dijkstra.dijkstra import Dijkstras
from dijkstra.grid import Grid2D
from .draw import DrawBoard, add_edge_name, MathBox, EdgeDistancesAnimation

from .dijkstra_animation import ArtistManager


PROJECT_ROOT = Path(__file__).parent.parent
FRAMES_STORAGE = PROJECT_ROOT.joinpath("frames/part_second_iter")
NUMPY_GRID_FILE = PROJECT_ROOT.joinpath("numpy_grids/parking_lot_grid_22_28.npy")
DEBUG = False

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

def create_iteration_data():
    labels = []
    arrows = []
    for edge in data.updated_edges:
        label = add_edge_name(db.ax, edge)
        label.set_visible(False)
        labels.append(label)

        arrow = FancyArrowPatch(
            data.current_edge,
            edge,
            arrowstyle="->",
            connectionstyle="arc3",
            color="grey",
            linewidth=2,
            zorder=2,
            mutation_scale=10,
        )
        # print(f"arrow from {data.current_edge} to {edge}")
        arrow.set_visible(False)
        db.ax.add_patch(arrow)
        arrows.append(arrow)

    return labels, arrows

def init_math_box_algorithm(save_figs=False):

    # init Title
    math_box.box.set_visible(True)
    math_box.set_first_line_as_title()
    math_box.set_text("First iteration",0)
    if save_figs: db.save_fig("init.png")

    math_box.set_text("node, distance <-- queue",1)
    if save_figs: db.save_fig("math_box_curr_node.png")

    math_box.set_text("visited <-- node",2)
    if save_figs: db.save_fig("mat_box_curr_visited.png")

    math_box.set_text("for all neighbour_nodes:",4)
    # if save_figs: db.save_fig("for_all_init.png")

    math_box.set_text("  node_distance = distance + 1", 5)
    if save_figs: db.save_fig("claculate_distance.png")

    math_box.set_text("  if node_distance < saved_node_distance:",7)
    if save_figs: db.save_fig("if_statement.png")

    math_box.set_text("    distances <-- node_distance",8)
    if save_figs: db.save_fig("if_statement_distance.png")

    math_box.set_text("    queue <-- (neighbour_node, node_distance)", 10)
    if save_figs: db.save_fig("if_statement_enqueue.png")

    math_box.set_text(f"{data.current_edge}, 0 <-- queue",1)
    if save_figs: db.save_fig("deque.png")

    math_box.set_text(f"visited <-- {data.current_edge}",2)
    if save_figs: db.save_fig("mark_visited.png")

def add_current_node_deque_animation():

    # Add deque animation
    edge_label = add_edge_name(db.ax, data.current_edge)
    start_pos = math_box.text_lines[1].get_position()
    target_pos = edge_label.get_position()
    edge_label.set_position(start_pos)
    edge_animator = EdgeDistancesAnimation(edge_label, start_pos, target_pos, frames=30)
    ani = edge_animator.generate_animation(db.fig)
    db.save_animation(ani, "current_deque_animation.mp4")
    # print(f"label pos post animation: {edge_label.get_position()}, wanted: {target_pos}")

    algo_AM.active_edge_scat.set_visible(True)
    edge_label.set_position(target_pos)
    db.save_fig("post_current_deque.png")
    return edge_label


def add_neigbour_iteration(save_all_slides):
    
    # Draw neighbour edges
    algo_AM.active_edge_scat.set_visible(True)
    algo_AM.updated_edges_scat.set_visible(True)
    algo_AM.queue_scat.set_visible(True)
    algo_AM.unfeasable_edges_scat.set_visible(True)
    algo_AM.discovered_edges_scat.set_visible(True)
    db.save_fig("neighbour_edges_draw.png")
    algo_AM.update_queue()

    labels, arrows = create_iteration_data()
 
    curr_dist = int( algo.distances[data.current_edge] )
    frames = 30
    n_neigbbour = len(labels)
    first_iteration = True and save_all_slides
    for i in range(n_neigbbour):
        # Draw label and arrow
        labels[i].set_visible(True)
        arrows[i].set_visible(True)
        db.save_fig("draw_label_and_arrow.png")
        
        # TODO: add distance animation

        # neighbour in math box animation
        start_pos = labels[i].get_position()
        target_pos = math_box.text_lines[6].get_position()
        # target_pos = ( target_pos[0] + 0.5, target_pos[1] - 0.1) # Small correction for offsets
        edge_animator = EdgeDistancesAnimation(labels[i],start_pos, target_pos,frames=frames)
        animation = edge_animator.generate_animation(db.fig)
        db.save_animation(animation, "for_edge_animation.mp4")

        # remove label
        labels[i].set_visible(False)

        node_name = labels[i].get_text()
        neighbour_node_name = data.neighbour_edges[i]
        neighbour_dist = int( algo.distances[neighbour_node_name] )

        math_box.set_text(f"for all neighbour_nodes:  ({neighbour_node_name})", 4)
        if first_iteration: db.save_fig("post_neighbour_ani.png")

        math_box.set_text(f"  node_distance = {curr_dist} + 1",5)
        if first_iteration: db.save_fig("post_neighbour_slide1.png")

        math_box.set_text(f"  if {neighbour_dist} < inf",7)
        if first_iteration: db.save_fig("post_neighbour_slide2.png")

        math_box.set_text(f"    distances <-- {neighbour_dist}",8)
        if first_iteration: db.save_fig("post_neighbour_slide3.png")

        math_box.set_text(f"    queue <- ({neighbour_node_name}, {neighbour_dist})", 10)
        db.save_fig("post_neighbour_slide4.png")

        # Remove neighbour edge in scat
        neighbour_scat_data = algo_AM.updated_edges_scat.get_offsets()
        algo_AM.updated_edges_scat.set_offsets(neighbour_scat_data[1:])

        first_iteration = False
        frames = 10
    


def add_neigbour_edges(use_long_start_frame=False):
    algo_AM.active_edge_scat.set_visible(True)
    algo_AM.updated_edges_scat.set_visible(True)
    algo_AM.queue_scat.set_visible(True)
    algo_AM.unfeasable_edges_scat.set_visible(True)
    algo_AM.discovered_edges_scat.set_visible(True)
    db.save_fig("neighbour.png")
    algo_AM.update_queue()

    labels = []
    arrows = []
    for edge in data.updated_edges:
        label = add_edge_name(db.ax, edge)
        label.set_visible(False)
        labels.append(label)

        arrow = FancyArrowPatch(
            data.current_edge,
            edge,
            arrowstyle="->",
            connectionstyle="arc3",
            color="grey",
            linewidth=2,
            zorder=2,
            mutation_scale=10,
        )
        # print(f"arrow from {data.current_edge} to {edge}")
        arrow.set_visible(False)
        db.ax.add_patch(arrow)
        arrows.append(arrow)

    # frames = 10

    curr_dist = int( algo.distances[data.current_edge] )

    n_nodes = len(data.updated_edges)
    for i in range(n_nodes):

        if i < 2 and use_long_start_frame:
            frames = 30
        else:
            frames = 10

        labels[i].set_visible(True)
        arrows[i].set_visible(True)
        db.save_fig("pre_neighbour_ani.png")
        
        start_pos = labels[i].get_position()
        target_pos = math_box.text_lines[1].get_position()
        target_pos = ( target_pos[0] + 0.5, target_pos[1] - 0.1) # Small correction for offsets
        edge_animator = EdgeDistancesAnimation(labels[i],start_pos, target_pos,frames=frames)
        animation = edge_animator.generate_animation(db.fig)
        db.save_animation(animation, "neighbour_ani.mp4")
        
        neighbour_scat_data = algo_AM.updated_edges_scat.get_offsets()
        algo_AM.updated_edges_scat.set_offsets(neighbour_scat_data[1:])

        # print(neighbour_scat_data, type(neighbour_scat_data))

        labels[i].set_visible(False)
        # node_name = labels[i].get_text()
        neighbour_node_name = data.updated_edges[i]

        neighbour_dist = int( algo.distances[neighbour_node_name] )

        math_box.set_text(f"Distances <-- {neighbour_node_name} = {curr_dist} + 1",1)
        math_box.set_text(f"Queue <-- ({neighbour_node_name}, {neighbour_dist})",2)
        # math_box.set_text(f"Parents[{node_name}]=")
        db.save_fig("post_neighbour_ani.png")
        # if i > 1 and use_long_start_frame:
        #     frames = 10


db.reset_frames_storage()
db.save_to_file_disabled = True

data = algo.iter()
algo_AM.update_artists(data)
current_node_label = add_current_node_deque_animation()
add_neigbour_iteration(False)
current_node_label.set_visible(False)

data = algo.iter()
algo_AM.update_artists(data)
db.save_to_file_disabled = False
algo_AM.updated_edges_scat.set_visible(False)
algo_AM.active_edge_scat.set_visible(False)

init_math_box_algorithm(False)
math_box.set_text("Second iteration",0)
db.save_fig("Init_math_second_iteration.png")

add_current_node_deque_animation()
add_neigbour_iteration(False)

plt.show()
