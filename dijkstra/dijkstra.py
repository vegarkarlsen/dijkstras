import heapq
import time
from typing import NamedTuple

import matplotlib.pyplot as plt
import numpy as np

from dijkstra.grid import Grid2D


class DijekstraIterData(NamedTuple):
    current_edge: tuple[int, int]
    current_queue: list[tuple[int, int]] = []
    neighbour_edges: list[tuple[int, int]] = []
    feasiable_edges: list[tuple[int, int]]  = []
    unfeasable_edges: list[tuple[int, int]] = []
    updated_edges: list[tuple[int,int]] = []
    path: list[tuple[int, int]] = []
    path_found: bool = False


class Dijkstras:
    def __init__(
        self, grid: Grid2D, start_edge: tuple[int, int], end_edge: tuple[int, int]
    ) -> None:
        self.grid = grid
        self.start_edge = start_edge
        self.end_edge = end_edge

        self.dist_shape = (grid.xEdgeRange.max() + 1, grid.yEdgeRange.max() + 1)
        self.distances = np.full(self.dist_shape, np.inf)
        self.distances[start_edge] = 0

        # self.parents_ = {self.calcualte_pos_id(start_edge): (-1, -1)}
        self.parents_ = {start_edge: (-1, -1)}

        self.queue_ = []
        # heapq.heappush(self.queue_, (0, start_edge))
        self.queue_.append((0, start_edge))

        # Data saved for plotting
        # self.current_edge: tuple[int, int]
        # self.neighbour_edges: list[tuple[int,int]]
        # self.active_neighbour_edge: tuple[int, int]

    def iter(self) -> DijekstraIterData:
        # dist, edge = heapq.heappop(self.queue_)
        dist, edge = self.queue_.pop(0)
        # self.current_edge = edge  # Save data for plotting
        # print(f"current edge {edge}, with dist {dist}")

        if edge == self.end_edge:
            print("found destenation, reconstructing path")
            path = self.reconstructShortestPath(edge)
            return DijekstraIterData(current_edge=edge, path=path, path_found=True)

        if dist > self.distances[edge]:
            # FIXME: can we return here?
            print("Early return")
            return DijekstraIterData(current_edge=edge)

        feasiable_edges = []
        unfeasable_edges = []
        updated_edges = []

        # TODO: Consider adding distances asweell to account for non 1*1 grid
        next_edges = self.grid.get_neightbour_edges(edge)
        # print(f"current edge: {edge} next edges: {next_edges}")
        for ne in next_edges:
            # print(ne)
            if self.grid.edge_feaisable(ne):
                ne_dist = dist + 1
                # print(f"next_edge {ne} was feasialbe with dist: {ne_dist}")
                feasiable_edges.append(ne)
                if ne_dist < self.distances[ne]:
                    updated_edges.append(ne)
                    # print(
                    #     f"next edge {ne} was smaller than saved dist.\n {self.distances[ne]}"
                    # )
                    self.distances[ne] = ne_dist
                    # Current edge becomes parent to next_edge
                    # print(f"edge {edge}, becomes parent to {ne}")
                    # self.parents_[self.calcualte_pos_id(ne)] = edge
                    self.parents_[ne] = edge
                    # if self.calcualte_pos_id(ne) in list(self.parents_.keys()):
                    #     print(f"{ne} is allready in parents.")
                    if (ne_dist, ne) in self.queue_:
                        print(f"We doubled added {ne} to the queue")
                    # heapq.heappush(self.queue_, (ne_dist, ne))
                    self.queue_.append((ne_dist, ne))
            else:
                unfeasable_edges.append(ne)

        return DijekstraIterData(
            current_edge=edge,
            current_queue=[q[1] for q in self.queue_],
            neighbour_edges=next_edges,
            feasiable_edges=feasiable_edges,
            updated_edges=updated_edges,
            unfeasable_edges=unfeasable_edges
        )

    def reconstructShortestPath(self, end_edge) -> list[tuple]:
        loop_edge = end_edge
        shortestPath = []
        # print(self.parents_)
        # print("Reversing thorugh parent tree to find the path")
        while loop_edge != (-1, -1):
            # print(f"{loop_edge}, ", end="")
            # print(f"Appending edge {loop_edge}, with id: {loop_edge}")
            shortestPath.append(loop_edge)
            # print(f"next loop_edge is {self.parents_[self.calcualte_pos_id(loop_edge)]} ")
            loop_edge = self.parents_[loop_edge]
            # time.sleep(1)
        # print(f"Path created.")
        return shortestPath[::-1]


if __name__ == "__main__":
    # pass
    i = 0
    grid = Grid2D.get_test_grid()
    algo = Dijkstras(grid, (2, 2), (13, 7))
    path_found = False
    while not path_found:
        i += 1
        data = algo.iter()
        # print(data)
        path_found = data.path_found
    # print(path)
    # print(f"Distances: {algo.distances}")
    # print(i)

    fig, ax = plt.subplots()

    x = [e[0] for e in data.path]
    y = [e[1] for e in data.path]
    algo.grid.plot_grid(ax)
    ax.scatter(x, y, zorder=2)
    ax.plot(x, y)
    plt.show()
