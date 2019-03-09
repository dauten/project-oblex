import tkinter as tk
import random
from PIL import Image, ImageTk
import json
import wand
import subprocess
import shutil
import time

num_of_rows=11
num_of_cols=14
square_size=75



class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.canvas = tk.Canvas(self, width=(num_of_cols * square_size), height=(num_of_rows * square_size), borderwidth=0, highlightthickness=0)

        #add bg
        self.bgi = Image.open("images/grass.gif")
        self.bgi = self.bgi.resize((2*(num_of_cols * square_size), 2*(num_of_rows * square_size)), Image.ANTIALIAS)
        self.bgp = ImageTk.PhotoImage(self.bgi)
        self.canvas.pack(side="top", fill="both", expand="true")
        self.canvas.create_image(10,10,image=self.bgp)
        self.rows = num_of_rows
        self.columns = num_of_cols
        self.cellwidth = square_size
        self.cellheight = square_size

        self.rect = {}
        self.oval = {}
        #self.bgi = tk.PhotoImage("grass.jpg")
        #self.bgl = tk.Label(self, image=self.bgi)
        #self.bgl.place(x=0, y=0, relwidth=1, relheight=1)
        self.oldLarge = None
        self.oldBoard = None

        self.redraw(750)

    def redraw(self, delay):
        print("redrawing")
        self.canvas.itemconfig("rect")

        board = {"objects":[]}
        large = {"objects":[]}

        try:
            board = json.loads(open("board.json", "r").read())
        except Exception as e:
            print(open("board.json", 'r').read())

        try:
            large = json.loads(open("large.json", "r").read())
        except Exception as e:
            print(open("large.json", 'r').read())

        if large == None or board == None:
            print("A file was not opened.")
            sys.exit(1)
        elif large != self.oldLarge or board != self.oldBoard:
            time.sleep(2)
            try:
                board = json.loads(open("board.json", "r").read())
            except Exception as e:
                print(open("board.json", 'r').read())

            try:
                large = json.loads(open("large.json", "r").read())
            except Exception as e:
                print(open("large.json", 'r').read())


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
                            self.im.append(Image.open("images/"+each["filename"]))
                            self.im.append(self.im[-1].resize((square_size-2,square_size-2), Image.ANTIALIAS))
                            self.photo.append(ImageTk.PhotoImage(self.im[-1]))
                            self.canvas.create_image((x1-(square_size/2)-1),(y1-(square_size/2)-1), image=self.photo[-1])



            for each in large["objects"]:
                self.im.append(Image.open("images/"+each["filename"]))
                self.im.append(self.im[-1].resize((square_size*each["width"],square_size*each["height"]), Image.ANTIALIAS))
                self.photo.append(ImageTk.PhotoImage(self.im[-1]))
                self.canvas.create_image(((each["tlx"])*square_size,(each["tly"]+.5)*square_size), image=self.photo[-1])
            print("making ps")
            self.canvas.postscript(file="out.eps")
            print("done with ps")
            outfile = Image.open("out.eps")
            outfile.save("out.png", "png")
            shutil.copyfile("out.png","board.png")


            self.oldLarge = large
            self.oldBoard = board
        else:
            print("We are not rendering becuase there are no changes to render")

        self.after(delay, lambda: self.redraw(delay))

if __name__ == "__main__":
    app = App()
    app.mainloop()
