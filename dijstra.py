
from grid import Grid2D
import heapq
import numpy as np
import time
import matplotlib.pyplot as plt

# class Graph:
#
#     def __init__(self, grid) -> None:
#         self.grid = grid
        

# class Node:
#     def __init__(self, pos=(None,None), dist=None) -> None:
#         self.id = str(pos)
#         self.pos = pos
#         self.dist = dist


class Dikstras:

    def __init__(self, grid: Grid2D, start_edge: tuple[int,int], end_edge: tuple[int,int]) -> None:
        self.grid = grid
        self.start_edge = start_edge
        self.end_edge = end_edge

        self.dist_shape = (grid.xEdgeRange.max()+1, grid.yEdgeRange.max()+1)
        self.distances = np.full(self.dist_shape, np.inf)
        self.distances[start_edge] = 0

        self.parents_ = {
            self.calcualte_pos_id(start_edge): (-1,-1)
        }

        self.queue_ = []
        heapq.heappush(self.queue_, (0, start_edge))

        # Data saved for plotting
        # self.current_edge: tuple[int, int]
        # self.neighbour_edges: list[tuple[int,int]]
        # self.active_neighbour_edge: tuple[int, int]

    def calcualte_pos_id(self, edge: tuple)->str:
        return str( edge[0] + edge[1] * self.dist_shape[1] )

    def iter(self) -> tuple[bool, list]:

        dist, edge = heapq.heappop(self.queue_)
        self.current_edge = edge # Save data for plotting
        print(f"current edge {edge}, with dist {dist}")

        if edge == self.end_edge:
            # print("found path")
            return True, self.reconstructShortestPath(edge)

        if dist > self.distances[edge]:
            # FIXME: can we return here?
            print("Early return")
            return False, []

        next_edges = self.grid.get_neightbour_edges(edge)
        self.neighbour_edges = next_edges
        print(f"next edges: {next_edges}")
        for ne in next_edges:
            if self.grid.edge_feaisable(ne):
                ne_dist = dist + 1
                # print(f"next_edge {ne} was feasialbe with dist: {ne_dist}")

                if ne_dist < self.distances[ne]:
                    self.neighbour_edges.append(ne)
                    print(f"next edge {ne} was smaller than saved dist.\n {self.distances[ne]}")
                    self.distances[ne] = ne_dist
                    # Current edge becomes parent to next_edge
                    self.parents_[self.calcualte_pos_id(ne)] = edge
                    heapq.heappush(self.queue_, (ne_dist, ne))

        return False, []

    def reconstructShortestPath(self, end_edge) -> list[tuple]:
        loop_edge = end_edge
        shortestPath = []
        # print(self.parents_)
        # print("Reversing thorugh parent tree to find the path")
        while loop_edge != (-1, -1):
            # print(f"{loop_edge}, ", end="")
            # print(f"Appending edge {loop_edge}, with id: {self.calcualte_pos_id(loop_edge)}")
            shortestPath.append(loop_edge)
            # print(f"next loop_edge is {self.parents_[self.calcualte_pos_id(loop_edge)]} ")
            loop_edge = self.parents_[self.calcualte_pos_id(loop_edge)]
            # time.sleep(1)
        return shortestPath[::-1]


if __name__ == '__main__':
    # pass
    i = 0
    grid = Grid2D.get_test_grid()
    algo = Dikstras(grid, (9,8), (13,7))
    path_found = False
    while not path_found:
        i += 1
        path_found, path = algo.iter()
    # print(path)
    # print(f"Distances: {algo.distances}")
    print(i)

    fig, ax = plt.subplots()
    
    x = [e[0] for e in path]
    y = [e[1] for e in path]
    algo.grid.plot_grid(ax)
    ax.scatter(x, y, zorder=2)
    ax.plot(x,y)
    plt.show()
    


