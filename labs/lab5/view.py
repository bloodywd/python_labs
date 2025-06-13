from model import BlockType
import tkinter as tk


class GameDrawer:
    def __init__(self, root, size):
        self.root = root
        self.cell_size = 800 // size
        self.size = size
        self.canvas = tk.Canvas(
            root,
            width=self.cell_size * size,
            height=self.cell_size * size
        )
        self.canvas.pack()

        self.timer_label = tk.Label(self.root, text="02.00",
                                    font=("Arial", 14))
        self.timer_label.pack()

        self.new_game_btn = None

    def draw_ui(self, new_game_event, apply_size_event):
        self.new_game_btn = tk.Button(
            self.root,
            text="Новая игра",
            command=new_game_event
        )
        self.new_game_btn.pack()

        size_frame = tk.Frame(self.root)
        size_frame.pack()

        tk.Label(size_frame, text="Размер поля (5-100):").pack(side=tk.LEFT)
        self.size_entry = tk.Entry(size_frame, width=5)
        self.size_entry.pack(side=tk.LEFT)
        self.size_entry.insert(0, "10")

        apply_btn = tk.Button(size_frame, text="Применить",
                              command=apply_size_event)
        apply_btn.pack(side=tk.LEFT)

    def get_size_input(self):
        try:
            value = int(self.size_entry.get())
            if 5 <= value <= 100:
                return value
        except ValueError:
            pass
        return None

    def get_cell_size(self):
        return self.cell_size

    def update_size(self, size):
        self.size = size
        self.cell_size = 800 // size
        self.canvas.config(width=self.cell_size * size,
                           height=self.cell_size * size)

    def update_timer_label(self, time):
        self.timer_label.config(text=time)

    def draw_board(self, grid, size):
        self.canvas.delete("all")
        for i in range(size):
            for j in range(size):
                self.draw_block(i, j, grid[i][j])

    def draw_block(self, i, j, block):
        x, y = j * self.cell_size, i * self.cell_size
        offset = self.cell_size // 2
        cx, cy = x + offset, y + offset
        color = "#FFFF99" if block.is_lit else "#DDDDDD"

        self.canvas.create_rectangle(
            x, y, x + self.cell_size, y + self.cell_size,
            fill=color, outline="black", width=2,
            tags=f"block_{i}_{j}"
        )

        line_width = self.cell_size // 15

        connections = block.get_connections()

        for direction in connections:
            if direction == "up":
                self.canvas.create_line(cx, cy, cx, y, width=line_width)
            if direction == "down":
                self.canvas.create_line(cx, cy, cx, y + self.cell_size,
                                        width=line_width)
            if direction == "left":
                self.canvas.create_line(cx, cy, x, cy, width=line_width)
            if direction == "right":
                self.canvas.create_line(cx, cy, x + self.cell_size, cy,
                                        width=line_width)

    def get_canvas(self):
        return self.canvas
