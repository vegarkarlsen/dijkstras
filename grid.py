
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from numpy._core.defchararray import lstrip
# from abc import ABC, abstractmethod

class Grid2D:

    def __init__(self, grid: np.ndarray) -> None:
        """ 2D grid"""
        self.grid: np.ndarray = grid
        self.xEdgeRange: np.ndarray = np.arange(0,grid.shape[0]+1, 1)
        self.yEdgeRange: np.ndarray = np.arange(0, grid.shape[1]+1, 1)

    @classmethod
    def get_test_grid(cls) -> "Grid2D":
        grid = np.zeros((16,16))
        grid[10, 8:12] = 1
        grid[5:10, 11] = 1
        # grid[0,:] = 1
        # grid[1,3] = 1
        return cls(grid)
    
    def set_cell(self, cell: tuple[int,int], value:int = 1):
        """Sets a cell in the grid to value.
            @param cell: tuple[row, column]"""
        self.grid[cell] = value

    def get_edges(self, cell: tuple[int,int]) -> list[tuple]:
        """Returns all edges connected to a grid cell
            @param cell: (row,colum)
            @returns edge = (x, y)
        """
        row, column = cell
        if row < 0 or column < 0:
            print(f"Grid cell {row, column} out of bounds.")
            return []
        if row > self.xEdgeRange.max() or column > self.yEdgeRange.max():
            print(f"Grid cell {row, column} out of bounds.")
            return []

        edges = [
            (column, row,),    # Bottom left
            (column, row+1,),   # top left
            (column+1, row+1,), # top right
            (column+1, row)    # bottom right
        ]

        return edges

    def get_grid_cells(self, edge: tuple[int, int]) -> list[tuple]:
        """Returns all grid cells that are connected to a edge.
            @returns list[cell] where cell = (row, column)
            -----------------
            |   |   |   |   |
            |   | x | x |   |
            --------E--------
            |   | x | x |   |
            |   |   |   |   |
            -----------------
        """
        column, row = edge
        adjunct_cells = [
            (row, column),      # Top right
            (row-1, column),    # Bottom right
            (row-1,column-1),   # Bottom left
            (row, column-1)     # Top left
        ]
        cells_in_bounds = []
        for cell in adjunct_cells:
            r, c = cell
            if r < 0 or c < 0:
                continue
            if r >= self.grid.shape[0] or c >= self.grid.shape[1]:
                continue
            cells_in_bounds.append(cell)

        return cells_in_bounds
    

    def get_neightbour_edges(self, edge: tuple[int, int]) -> list[tuple]:
        """Returns all feasialbe neighbour edges to a edge"""

        connected_cells = self.get_grid_cells(edge)

        adjunct_edges = []
        for c in connected_cells:
            adjunct_edges.extend(self.get_edges(c))

        # Remove duplicates
        adjunct_edges = list(set(adjunct_edges))
        # Remove current edge
        adjunct_edges.remove(edge)
        return adjunct_edges

    def edge_feaisable(self, edge: tuple[int,int]) -> bool:
        connected_cells = self.get_grid_cells(edge)
        for c in connected_cells:
            if self.grid[c] != 0:
                return False
        return True
 
    def plot_grid(self, ax: Axes) -> None:
        ax.pcolormesh(self.xEdgeRange, self.yEdgeRange, self.grid, cmap="Greys", zorder=0)
        ax.set_xticks(self.xEdgeRange)
        ax.set_yticks(self.yEdgeRange)
        ax.grid(True,zorder=1)
        # ax.scatter(self.edgesX, self.edgesY)


def test_grid(test_cell, test_edge):

    fig, ax = plt.subplots()
    grid = np.zeros((16,16))
    g = Grid2D(grid)

    # grid_c: row, column
    grid_c = test_cell
    g.grid[grid_c] = 1

    edges = g.get_edges(*grid_c)
    x = [e[0] for e in edges]
    y = [e[1] for e in edges]
    ax.scatter(x, y, zorder=2, color="red")

    edge = test_edge
    ax.scatter(*edge, zorder=2)
    grid_cells = g.get_grid_cells(edge)
    for cell in grid_cells:
        g.grid[cell] = 1


    # edge = (1,5)
    # ax.scatter(edge[0], edge[1])


    # edge = (5, 1)
    # ax.scatter(*edge)
    # cells = g.get_grid_cell(edge)
    # for c in cells:
    #     g.grid[c]=1

    g.plot_grid(ax)
    plt.show()


if __name__ == '__main__':
    # test_grid(test_cell=(2,6), test_edge=(16,16))
    fig, ax = plt.subplots()
    g = Grid2D.get_test_grid()

    edge = (15,15)
    neighbour_edges = g.get_neightbour_edges(edge)
    x = [ e[0] for e in neighbour_edges ]
    y = [ e[1] for e in neighbour_edges ]
    ax.scatter(x,y,color="red", zorder=2)


    ax.scatter(*edge, zorder=3)

    g.plot_grid(ax)
    plt.show()
    

