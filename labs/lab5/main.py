import tkinter as tk
from tkinter import messagebox
from view import GameDrawer
from model import GameBoardModel

GAME_TIME = 120

class GameController:
    def __init__(self, root, size=5):
        self.root = root
        self.model = GameBoardModel(size)
        self.is_playing = True
        self.grid_size = size
        self.time_left = GAME_TIME
        self.timer_id = None

        self.drawer = GameDrawer(root, self.grid_size)

        self.canvas = self.drawer.get_canvas()
        self.canvas.bind("<Button-1>", self.on_grid_click)

        self.drawer.draw_ui(self.new_game_event, self.apply_size_event)
        self.start_timer()

        self.update_view()


    def on_grid_click(self, event):
        cell_size = self.drawer.get_cell_size()
        j = event.x // cell_size
        i = event.y // cell_size
        if self.is_playing:
            if 0 <= i < self.model.size and 0 <= j < self.model.size:
                win = self.model.rotate_block(i, j)
                self.update_view()
                if win:
                    self.is_playing = False
                    messagebox.showinfo("Победа!", "Вы выиграли!")

    def new_game_event(self):
        self.is_playing = True
        self.model = GameBoardModel(self.grid_size)

        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.start_timer()
        self.update_view()

    def apply_size_event(self):
        new_size = self.drawer.get_size_input()
        if new_size:
            self.grid_size = new_size
            self.model = GameBoardModel(self.grid_size)
            self.drawer.update_size(self.grid_size)

            self.new_game_event()
        else:
            messagebox.showwarning("Ошибка", "Введите число от 5 до 100")

    def update_view(self):
        board = self.model.get_board()
        self.drawer.draw_board(board, self.grid_size)

    def start_timer(self):
        self.time_left = GAME_TIME
        self.update_timer()

    def update_timer(self):
        if self.is_playing:
            minutes = self.time_left // 60
            seconds = self.time_left % 60
            self.drawer.update_timer_label(f"{minutes:02} {seconds:02}")
            if self.time_left > 0:
                self.time_left -= 1
                self.timer_id = self.root.after(1000, self.update_timer)
            elif self.time_left == 0:
                self.is_playing = False
                messagebox.showinfo("Поражение", "Время вышло!")
                self.model.set_board_to_solved()
                self.update_view()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Подсвети!")
    game = GameController(root, size=10)
    root.mainloop()
