import tkinter as tk
import os, sys
import random
import threading as th
import time

class App:
    """
    Main blokudooku app class
    """
    def __init__(self) -> None:
        
        # init constants
        self.HEIGHT = 800
        self.WIDTH = 1100
        self.TEXTURES_PATH = os.path.join(sys.path[0], "assets\\textures")
        self.BLOCK_ICON_DISTANCE = lambda x: 280+200*x
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
        self.blocks_to_choose = [-1, -1, -1]
        self.current_block = -1
        self.coords = [0, 0]
        self.flag_working = True
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
            f"Blocks\\{i}")) for i in sorted(os.listdir(os.path.join(self.TEXTURES_PATH, "Blocks")), key=lambda x: int(x.split(".png")[0]))],
            [tk.PhotoImage(file=os.path.join(self.TEXTURES_PATH,
            f"Blocks_icons\\{i}")) for i in sorted(os.listdir(os.path.join(self.TEXTURES_PATH, "Blocks_icons")), key=lambda x: int(x.split(".png")[0]))]]
        self.BG_TEXTURE = tk.PhotoImage(file=os.path.join(self.TEXTURES_PATH, "bg.png"))
        self.CELL_TEXTURE = tk.PhotoImage(file=os.path.join(self.TEXTURES_PATH, "cell.png"))
        self.CHOOSE_TEXTURE = tk.PhotoImage(file=os.path.join(self.TEXTURES_PATH, "choose_bg.png"))
        self.POINTS_TEXTURE = tk.PhotoImage(file=os.path.join(self.TEXTURES_PATH, "points_bg.png"))
        self.BUTTON_TEXTURE = tk.PhotoImage(file=os.path.join(self.TEXTURES_PATH, "button.png"))
        self.LOSE_TEXTURE = tk.PhotoImage(file=os.path.join(self.TEXTURES_PATH, "lose_bg.png"))
        self.LOSE_POINTS_TEXTURE = tk.PhotoImage(file=os.path.join(self.TEXTURES_PATH, "lose_points_bg.png"))
        # create app widgets
        self.canvas.create_image(self.WIDTH//2, self.HEIGHT//2, image=self.BG_TEXTURE, tags=("bg"))
        self.canvas.create_image(self.WIDTH-40, 40, anchor="ne", image=self.POINTS_TEXTURE)
        self.canvas.create_image(self.WIDTH-40, self.HEIGHT-40, anchor='se', image=self.CHOOSE_TEXTURE)
        # create cells and bind them to method
        self.master.bind("<ButtonRelease-1>", lambda event: self.release_button())
        self.master.bind("<B1-Motion>", self.mouse_motion)
        for i in range(9):
            for j in range(9):
                self.canvas.create_image(80+80*j, 80+80*i, image=self.CELL_TEXTURE,
                                         tags=(f"cell{i}_{j}"))
        
        self.generate_blocks()
        self.master.mainloop()

    def release_button(self) -> None:
        # (I tried to do it with tag binds, but background bind was blocking cell ones)
        """
        Method connected to releasing left button, checks if button is released over the gridcell,
        and if block can be placed, puts block in board matrix and over the gridcell
        """
        if self.current_block!=-1:
            # delete block moved with mouse
            self.canvas.delete(f"block_moving{self.current_block}")
            # check if release was in grid area
            if 40 <= self.coords[0] <= 760 and 40 <= self.coords[1] <= 760:
                y, x = (self.coords[0]-40)//80, (self.coords[1]-40)//80
                flag = True
                # check for all cells of block if both coords of them
                # are in range [0, 8] and points to empty cell in board matrix
                for i in self.BLOCKS_DATA[self.blocks_to_choose[self.current_block]]:
                    if (x+i[0]<0 or x+i[0]>8 or y+i[1]<0 or y+i[1]>8 or 
                        self.board[x+i[0]][y+i[1]]!=0):
                        flag = False
                        break
                # put block in board matrix and on gridcell if 
                # previous conditions are true
                if flag:
                    for i in self.BLOCKS_DATA[self.blocks_to_choose[self.current_block]]:
                        self.board[x+i[0]][y+i[1]] = 1
                        self.canvas.create_image(80+80*(y+i[1]), 80+80*(x+i[0]), 
                                                 image=self.BLOCKS_IMG_LIST[0][0],
                                                 tags=(f"block{x+i[0]}_{y+i[1]}"))
                    self.blocks_to_choose[self.current_block] = -1
                    if self.blocks_to_choose.count(-1)==3: self.generate_blocks()
                    l = []
                    for i in range(9):
                        if self.board[i].count(1)==9:
                            l.extend([[i, j] for j in range(9)])
                        if [self.board[k][i] for k in range(9)].count(1)==9:
                            l.extend([j, i] for j in range(9))
                    l1 = []
                    for i in l:
                        self.board[i[0]][i[1]]=0
                        if i not in l1: l1.append(i)
                    th.Thread(target=self.rows_cols_falling_animation, args=(l1, )).start()
                    self.current_block = -1
                    return
            # put block icon back in panel if block wasn't put on board previously
            link = lambda x: (lambda p: self.block_input(x))
            self.canvas.create_image(self.WIDTH-160, 310+150*self.current_block, anchor='center',
                                    image=self.BLOCKS_IMG_LIST[1][self.blocks_to_choose[self.current_block]], 
                                    tags=(f"block_icon{self.current_block}"))
            self.canvas.tag_bind(f"block_icon{self.current_block}", "<Button-1>", link(self.current_block))
            self.current_block = -1

    def rows_cols_falling_animation(self, blocks: list) -> None:
        """
        Thread function to load falling animation for all cells in given list
        """
        for i in blocks:
            self.canvas.delete(f"block{i[0]}_{i[1]}")
            self.canvas.update()
            time.sleep(0.02)

    def block_input(self, idx: int) -> None:
        """
        Method connected to blocks icons
        """
        self.canvas.delete(f"block_icon{idx}")
        self.canvas.create_image(self.WIDTH-160, self.BLOCK_ICON_DISTANCE(idx), 
                                 image=self.BLOCKS_IMG_LIST[0][self.blocks_to_choose[idx]], 
                                 tags=(f"block_moving{idx}"))
        self.current_block = idx

    def mouse_motion(self, event) -> None:
        """
        Method connected to mouse motion with left button event
        """
        self.coords[0], self.coords[1] = event.x, event.y
        if self.current_block!=-1:
            self.canvas.coords(f"block_moving{self.current_block}", self.coords[0], self.coords[1])

    def generate_blocks(self, mode: int = 3, block: int = -1) -> None:
        """
        Generate three blocks on right if mode == 3 
        or specific one given by block if 0 <= mode <= 2
        """
        link = lambda x: (lambda event: self.block_input(x))
        if mode==3:
            l = random.sample(range(23), 3)
            for i in range(3):
                self.blocks_to_choose[i] = l[i]
                self.canvas.create_image(self.WIDTH-160, self.BLOCK_ICON_DISTANCE(i), anchor='center',
                                         image=self.BLOCKS_IMG_LIST[1][l[i]], 
                                         tags=(f"block_icon{i}"))
                self.canvas.tag_bind(f"block_icon{i}", "<Button-1>", link(i))
        else:
            self.blocks_to_choose[mode] = block
            self.canvas.create_image(self.WIDTH-160, self.BLOCK_ICON_DISTANCE(mode), anchor='center',
                                         image=self.BLOCKS_IMG_LIST[1][block], 
                                         tags=(f"block_icon{mode}"))
            self.canvas.tag_bind(f"block_icon{mode}", "<Button-1>", link(mode))


if __name__ == "__main__":
    app = App()