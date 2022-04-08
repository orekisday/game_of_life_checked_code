import tkinter as tk
from tkinter import Canvas
import random
import math


class GameOfLife(tk.Tk):

    def __init__(self, canvas_size, cell_size):
        # giving access to methods and properties of a parent or sibling class
        super().__init__()

        self.title("Game of life ヅ")

        # the height and width
        self.canvas_size = canvas_size
        self.cell_size = cell_size
        self.size_factor = self.canvas_size / self.cell_size

        # the size of the canvas
        self.geometry(str(self.canvas_size) + "x" + str(self.canvas_size))

        # creating the canvas and adding to tkinter
        self.canvas = Canvas(
            self, width=self.canvas_size, height=self.canvas_size, bg='#FFFACD'
        )
        self.canvas.pack()

        # Set a click event on the canvas.
        self.canvas.bind('<Button-1>', self.click_event)
        self.canvas.bind('<Button1-Motion>', self.click_event)

        # Set up an empty game grid.
        self.grid = [
            [0 for x in range(self.cell_size)] for x in range(self.cell_size)
        ]

        # Fill the game grid with random data.
        for x in range(0, self.cell_size):
            for y in range(0, self.cell_size):
                self.grid[x][y] = random.randint(0, 1)

        # generating the board
        self.generate_board()

        self.after(100, self.board_updating)

    def board_updating(self):
        # updating the canvas
        self.canvas.delete("all")
        # running the next generation and updating the grid
        self.grid = self.run_generation()
        # generating the game board with the current population
        self.generate_board()
        # the next tick in the timer
        self.after(150, self.board_updating)

    def generate_board(self):
        # Draw a square on the game board for every live cell in the grid.
        for x in range(0, self.cell_size):
            for y in range(0, self.cell_size):
                real_x = x * self.size_factor
                real_y = y * self.size_factor
                if self.grid[x][y] == 1:
                    self.draw_square_like_shape(
                        real_x, real_y, self.size_factor
                    )
                    self.draw_square(real_x, real_y, self.size_factor)

        for a in range(1, self.cell_size):
            for b in range(1, self.cell_size):
                real_a = a * self.size_factor
                real_b = b * self.size_factor
                if self.grid[a][b] == 1:
                    self.draw_square_like_shape(
                        real_a, real_b, self.size_factor
                    )
                    self.draw_square(
                        real_a, real_b, self.size_factor
                    )

    # creating two type of shapes in our canvas.
    # I had problems with the shapes overlapping
    # so, don't judge me for that :p
    def draw_square_like_shape(self, y, x, size):
        self.canvas.create_rectangle(
            x, y, x + size / 2, y + size, fill='#9999ff', outline='#9999ff'
        )

    def draw_square(self, a, b, size):
        self.canvas.create_rectangle(
            a, b, a + size, b + size, fill='#99d6ff', outline='#99d6ff'
        )

    def run_generation(self):
        # Generate new empty grid to populate with result of generation.
        return_grid = [
            [0 for x in range(self.cell_size)] for x in range(self.cell_size)
        ]

        # Iterate over the grid.
        for x in range(0, self.cell_size):
            for y in range(0, self.cell_size):
                neighbours = self.number_neighbours(x, y)
                if self.grid[x][y] == 1:
                    # current cell is alive
                    if neighbours < 2:
                        # cell dies
                        return_grid[x][y] = 0
                    elif neighbours == 2 or neighbours == 3:
                        # cell lives
                        return_grid[x][y] = 1
                    elif neighbours > 3:
                        # cell dies
                        return_grid[x][y] = 0
                else:
                    # current cell is dead
                    if neighbours == 3:
                        # making cell live
                        return_grid[x][y] = 1
        return return_grid

    def number_neighbours(self, x, y):
        count = 0
        x_range = [x - 1, x, x + 1]
        y_range = [y - 1, y, y + 1]

        for x1 in x_range:
            for y1 in y_range:
                if x1 == x and y1 == y:
                    # Don't count this cell.
                    continue
                try:
                    if self.grid[x1][y1] == 1:
                        count += 1
                except IndexError:
                    continue
        return count

    def click_event(self, event):
        # finding out where the mouse is in relation to the grid.
        grid_x = math.floor((event.y / self.canvas_size) * self.cell_size)
        grid_y = math.floor((event.x / self.canvas_size) * self.cell_size)

        # making that cell alive
        self.grid[grid_x][grid_y] = 1


try:
    if __name__ == "__main__":
        # creating the class and kick off the Tkinter loop
        tkinter_canvas = GameOfLife(
            canvas_size=int(input(
                'Size of your canvas: ')), cell_size=int(
                input("Size of your cell: "))
        )
        tkinter_canvas.mainloop()
except ValueError:
    print("You might have entered a wrong value.")
