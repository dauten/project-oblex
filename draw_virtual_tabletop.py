import tkinter as tk
import random
from PIL import Image, ImageTk
import json

num_of_rows=9
num_of_cols=16
square_size=25

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.canvas = tk.Canvas(self, width=(num_of_cols * square_size), height=(num_of_rows * square_size), borderwidth=0, highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand="true")
        self.rows = num_of_rows
        self.columns = num_of_cols
        self.cellwidth = square_size
        self.cellheight = square_size

        self.rect = {}
        self.oval = {}
        board = json.loads(open("board.json", "r").read())
        print(board['objects'])
        self.im = []
        self.photo = []
        for column in range(num_of_cols):
            for row in range(num_of_rows):
                x1 = column*self.cellwidth
                y1 = row * self.cellheight
                x2 = x1 + self.cellwidth
                y2 = y1 + self.cellheight

                self.rect[row,column] = self.canvas.create_rectangle(x1,y1,x2,y2, tags="rect")
                for each in board["objects"]:
                    if column is each["column"] and row is each["row"]:
                        print("drawing man")
                        self.im.append(Image.open(each["file"]))
                        self.im.append(self.im[-1].resize((square_size-2,square_size-2), Image.ANTIALIAS))
                        self.photo.append(ImageTk.PhotoImage(self.im[-1]))
                        self.canvas.create_image((x1-(square_size/2)-1),(y1-(square_size/2)-1), image=self.photo[-1])

        self.redraw(200)

    def redraw(self, delay):
        self.canvas.itemconfig("rect", fill="green")
        board = json.loads(open("board.json", "r").read())
        print(board['objects'])
        self.im = []
        self.photo = []
        for column in range(num_of_cols):
            for row in range(num_of_rows):
                x1 = column*self.cellwidth
                y1 = row * self.cellheight
                x2 = x1 + self.cellwidth
                y2 = y1 + self.cellheight

                self.rect[row,column] = self.canvas.create_rectangle(x1,y1,x2,y2, tags="rect")
                for each in board["objects"]:
                    if column is each["column"] and row is each["row"]:
                        print("drawing man")
                        self.im.append(Image.open(each["file"]))
                        self.im.append(self.im[-1].resize((square_size-2,square_size-2), Image.ANTIALIAS))
                        self.photo.append(ImageTk.PhotoImage(self.im[-1]))
                        self.canvas.create_image((x1-(square_size/2)-1),(y1-(square_size/2)-1), image=self.photo[-1])

        self.after(delay, lambda: self.redraw(delay))

if __name__ == "__main__":
    app = App()
    app.mainloop()