import tkinter as tk
import os, sys



class App:

    def __init__(self) -> None:
        """
        Main blokudooku app class
        """
        # init constants
        self.HEIGHT = 800
        self.WIDTH = 1100
        self.TEXTURES_PATH = os.path.join(sys.path[0], "assets\\textures")
        self.BLOCKS_DATA = [[[0, 0]], [[-1, 0], [0, 0]], [[0, 0], [0, 1]], 
                            [[-1, -1], [0, -1], [0, 0], [0, 1]], [[-1, 0], [0, 0], [1, -1], [1, 0]],
                            [[0, -1], [0, 0], [0, 1], [1, 1]], [[-1, 0], [-1, 1], [0, 0], [1, 0]],
                            [[-1, 1], [0, -1], [0, 0], [0, 1]], [[-1, -1], [-1, 0], [0, 0], [1, 0]],
                            [[0, -1], [0, 0], [0, 1], [1, -1]], [[-1, 0], [0, 0], [1, 0], [1, 1]],
                            [[-1, 0], [0, -1], [0, 0], [0, 1]], [[-1, 0], [0, -1], [0, 0], [1, 0]],
                            [[0, -1], [0, 0], [0, 1], [1, 0]], [[-1, 0], [0, 0], [0, 1], [1, 0]],
                            [[0, -2], [0, -1], [0, 0], [0, 1], [0, 2]], [[-2, 0], [-1, 0], [0, 0], [1, 0]],
                            [[0, -1], [0, 0], [0, 1]], [[-1, 0], [0, 0], [1, 0]],
                            [[-1, 0], [-1, 1], [0, 0], [0, 1]],
                            [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 0], [0, 1], [1, -1], [1, 0], [1, 1]],
                            [[-1, -1], [-1, 0], [-1, 1], [0, -1], [1, -1]],
                            [[-1, -1], [-1, 0], [-1, 1], [0, 1], [1, 1]]]
        # init variables
        self.board = [[0 for i in range(9)] for j in range(9)]
        # init app master and main canvas
        self.master = tk.Tk()
        self.master.title("Blokudooku")
        self.master.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.canvas = tk.Canvas(self.master, height=self.HEIGHT, width=self.WIDTH,
                                bd=0, highlightthickness=0)
        self.canvas.place(x=0, y=0)
        # init textures constants
        self.BLOCKS_IMG_LIST = [
            [tk.PhotoImage(file=os.path.join(self.TEXTURES_PATH,
            f"Blocks\\{i}")) for i in os.listdir(
            os.path.join(self.TEXTURES_PATH, "Blocks"))],
            [tk.PhotoImage(file=os.path.join(self.TEXTURES_PATH,
            f"Blocks_icons\\{i}")) for i in os.listdir(
            os.path.join(self.TEXTURES_PATH, "Blocks_icons"))]]
        self.BG_TEXTURE = tk.PhotoImage(file=os.path.join(self.TEXTURES_PATH, "bg.png"))
        self.CELL_TEXTURE = tk.PhotoImage(file=os.path.join(self.TEXTURES_PATH, "cell.png"))
        self.CHOOSE_TEXTURE = tk.PhotoImage(file=os.path.join(self.TEXTURES_PATH, "choose_bg.png"))
        self.POINTS_TEXTURE = tk.PhotoImage(file=os.path.join(self.TEXTURES_PATH, "points_bg.png"))
        self.BUTTON_TEXTURE = tk.PhotoImage(file=os.path.join(self.TEXTURES_PATH, "button.png"))
        self.LOSE_TEXTURE = tk.PhotoImage(file=os.path.join(self.TEXTURES_PATH, "lose_bg.png"))
        self.LOSE_POINTS_TEXTURE = tk.PhotoImage(file=os.path.join(self.TEXTURES_PATH, "lose_points_bg.png"))
        # create app widgets
        self.canvas.create_image(self.WIDTH//2, self.HEIGHT//2, image=self.BG_TEXTURE)
        self.canvas.create_image(self.WIDTH-40, 40, anchor="ne", image=self.POINTS_TEXTURE)
        self.canvas.create_image(self.WIDTH-40, self.HEIGHT-40, anchor='se', image=self.CHOOSE_TEXTURE)
        # create cells and bind them to method
        link = lambda x, y: (lambda event: self.cell_input(x, y))
        for i in range(9):
            for j in range(9):
                self.canvas.create_image(80+80*j, 80+80*i, image=self.CELL_TEXTURE,
                                         tags=(f"cell{i}_{j}"))
                self.canvas.tag_bind(f"cell{i}_{j}", "<ButtonRelease-1>", link(i, j))

        
        self.master.mainloop()

    def cell_input(self, h: int, w: int) -> None:
        """
        Method connected to all cells
        """
        print(h, w)

    def block_input(self, idx: int) -> None:
        """
        Method connected to blocks icons
        """
        print(idx)


if __name__ == "__main__":
    app = App()