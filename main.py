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
        self.current_points = 0
        self.coords = [0, 0]
        self.flag_working = True
        self.flag_pause = False
        # init app master and main canvas
        self.master = tk.Tk()
        self.master.title("Blokudooku")
        self.master.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.master.resizable(False, False)
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
        self.canvas.create_text(self.WIDTH-160, 80, justify='center', anchor='center',
                                 font=('Courier', '30', 'bold'), fill="#E29C49", 
                                 text=str(self.current_points), tags=("points"))
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
            block_put = False
            if 40 <= self.coords[0] <= 760 and 40 <= self.coords[1] <= 760:
                y, x = (self.coords[0]-40)//80, (self.coords[1]-40)//80
                # put block in board matrix and on gridcell if 
                # previous conditions are true
                if self.check_correctness(self.blocks_to_choose[self.current_block], x, y):
                    for i in self.BLOCKS_DATA[self.blocks_to_choose[self.current_block]]:
                        self.board[x+i[0]][y+i[1]] = 1
                        self.canvas.create_image(80+80*(y+i[1]), 80+80*(x+i[0]), 
                                                 image=self.BLOCKS_IMG_LIST[0][0],
                                                 tags=(f"block{x+i[0]}_{y+i[1]}"))
                    self.blocks_to_choose[self.current_block] = -1
                    # generates new three blocks if previous three are gone
                    if self.blocks_to_choose.count(-1)==3: self.generate_blocks()
                    # makes a list with cells from filled cols and rows
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
                    if len(l1)>0:
                        th.Thread(target=self.rows_cols_break_animation, args=(l1, )).start()
                    self.current_block = -1
                    # checks if there's at least one cell to place at least one block
                    block_put = True
                    flag = False
                    for i in [self.blocks_to_choose[x] for x in range(3) if self.blocks_to_choose[x]!=-1]:
                        if flag: break
                        for j in range(9):
                            if flag: break
                            for k in range(9):
                                flag = self.check_correctness(i, j, k)
                                if flag: break
                    # if previous condition is false, make game over screen
                    if not flag:
                        self.flag_pause = True
                        self.canvas.create_image(self.WIDTH//2, self.HEIGHT//2,
                                                 image=self.LOSE_TEXTURE,
                                                 tags=("lose_panel"))
                        self.canvas.create_image(self.WIDTH//2, self.HEIGHT//2-20,
                                                 image=self.LOSE_POINTS_TEXTURE,
                                                 tags=("lose_panel"))
                        self.canvas.create_text(self.WIDTH//2, self.HEIGHT//2-120,
                                                text="Game over!", justify='center', anchor='center',
                                                font=('Courier', '30', 'bold'), fill="#E29C49",
                                                tags=("lose_panel"))
                        self.canvas.create_image(self.WIDTH//2, self.HEIGHT//2+100,
                                                 image=self.BUTTON_TEXTURE,
                                                 tags=("lose_panel", "lose_resume_btn"))
                        self.canvas.create_text(self.WIDTH//2, self.HEIGHT//2+100,
                                                text="Play again", justify='center', anchor='center',
                                                state='disabled', fill="#000000",
                                                font=('Courier', '30', 'bold'),
                                                tags=("lose_panel"))
                        self.canvas.create_text(self.WIDTH//2, self.HEIGHT//2-20,
                                                text="0", justify='center', anchor='center',
                                                font=('Courier', '30', 'bold'), fill="#E29C49",
                                                tags=("lose_panel", "lose_points_counter"))
                        self.points_animation(0, self.current_points, "lose_points_counter")
                        self.canvas.tag_bind("lose_resume_btn", "<Button-1>", lambda event: self.new_game())
            # put block icon back in panel if block wasn't put on board previously
            if not block_put:
                link = lambda x: (lambda p: self.block_input(x))
                self.canvas.create_image(self.WIDTH-160, self.BLOCK_ICON_DISTANCE(self.current_block), anchor='center',
                                        image=self.BLOCKS_IMG_LIST[1][self.blocks_to_choose[self.current_block]], 
                                        tags=(f"block_icon{self.current_block}"))
                self.canvas.tag_bind(f"block_icon{self.current_block}", "<Button-1>", link(self.current_block))
                self.current_block = -1

    def new_game(self) -> None:
        """
        Creates a new game
        """
        for i in range(3):
            self.blocks_to_choose[i]=-1
            self.canvas.delete(f"block_icon{i}")
        for i in range(9):
            for j in range(9):
                self.board[i][j] = 0
                self.canvas.delete(f"block{i}_{j}")
        self.canvas.itemconfig("points", text="0")
        self.current_points = 0
        self.generate_blocks()
        self.canvas.delete("lose_panel")
        self.flag_pause = False
        
    def points_animation(self, a: int, b: int, tag: str) -> None:
        """
        Create a smooth transition between two numbers in text widget
        """
        if b-a>0:
            steps = int((b-a)//4)
            for i in range(steps+1):
                self.canvas.itemconfig(tag, text=str(int(a+(b-a)*i/steps)))
                time.sleep(0.4/steps)
                self.canvas.update()

    def check_correctness(self, block: int, x: int, y: int) -> bool:
        """
        Checks if given block can fit on board in given (x, y) cell
        """
        for i in self.BLOCKS_DATA[block]:
            if (x+i[0]<0 or x+i[0]>8 or y+i[1]<0 or y+i[1]>8 or 
                self.board[x+i[0]][y+i[1]]!=0):
                return False
        return True

    def rows_cols_break_animation(self, blocks: list) -> None:
        """
        Thread function to load falling animation for all cells in given list
        """
        for i in blocks:
            self.current_points += 1
            self.canvas.itemconfig("points", text=str(self.current_points))
            self.canvas.delete(f"block{i[0]}_{i[1]}")
            self.canvas.update()
            time.sleep(0.02)

    def block_input(self, idx: int) -> None:
        """
        Method connected to blocks icons
        """
        if not self.flag_pause:
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