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
        # init app master and main canvas
        self.master = tk.Tk()
        self.master.title("Blokudooku")
        self.master.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.canvas = tk.Canvas(self.master, height=self.HEIGHT, width=self.WIDTH,
                                bd=0, highlightthickness=0)
        self.canvas.place(x=0, y=0)
        # init textures constants
        self.BLOCKS_IMG_LISTS = [
            [tk.PhotoImage(file=os.path.join(self.TEXTURES_PATH,
            f"Blocks\\{i}")) for i in os.listdir(
            os.path.join(self.TEXTURES_PATH, "Blocks"))],
            [tk.PhotoImage(file=os.path.join(self.TEXTURES_PATH,
            f"Blocks_icons\\{i}")) for i in os.listdir(
            os.path.join(self.TEXTURES_PATH, "Blocks_icons"))]]
        

        
        self.master.mainloop()

if __name__ == "__main__":
    app = App()