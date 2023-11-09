import tkinter as tk
import tkinter.font as tkFont

class App:
    def __init__(self, root):
        #setting title
        root.title("")
        #setting window size
        width=600
        height=300
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        GButton_416=tk.Button(root)
        GButton_416["activebackground"] = "#528181"
        GButton_416["bg"] = "#90ee90"
        ft = tkFont.Font(family='Times',size=16)
        GButton_416["font"] = ft
        GButton_416["fg"] = "#000000"
        GButton_416["justify"] = "center"
        GButton_416["text"] = "Start Game"
        GButton_416["relief"] = "flat"
        GButton_416.place(x=200,y=0,width=200,height=300)
        GButton_416["command"] = self.GButton_416_command

        GLabel_825=tk.Label(root)
        ft = tkFont.Font(family='Times',size=18)
        GLabel_825["font"] = ft
        GLabel_825["fg"] = "#333333"
        GLabel_825["justify"] = "center"
        GLabel_825["text"] = "Score"
        GLabel_825["relief"] = "flat"
        GLabel_825.place(x=400,y=30,width=200,height=50)

        GLabel_191=tk.Label(root)
        ft = tkFont.Font(family='Times',size=13)
        GLabel_191["font"] = ft
        GLabel_191["fg"] = "#333333"
        GLabel_191["justify"] = "center"
        GLabel_191["text"] = "Player"
        GLabel_191.place(x=400,y=100,width=200,height=50)

        GLabel_917=tk.Label(root)
        ft = tkFont.Font(family='Times',size=13)
        GLabel_917["font"] = ft
        GLabel_917["fg"] = "#333333"
        GLabel_917["justify"] = "center"
        GLabel_917["text"] = "Computer"
        GLabel_917.place(x=400,y=200,width=200,height=50)

        GLabel_975=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_975["font"] = ft
        GLabel_975["fg"] = "#333333"
        GLabel_975["justify"] = "center"
        GLabel_975["text"] = "playerscore"
        GLabel_975.place(x=400,y=140,width=200,height=25)

        GLabel_677=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_677["font"] = ft
        GLabel_677["fg"] = "#333333"
        GLabel_677["justify"] = "center"
        GLabel_677["text"] = "computerscore"
        GLabel_677.place(x=400,y=190,width=200,height=25)

        GLabel_631=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_631["font"] = ft
        GLabel_631["fg"] = "#333333"
        GLabel_631["justify"] = "right"
        GLabel_631["text"] = "Rounds played: "
        GLabel_631.place(x=420,y=80,width=90,height=30)

        GLabel_644=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_644["font"] = ft
        GLabel_644["fg"] = "#333333"
        GLabel_644["justify"] = "left"
        GLabel_644["text"] = "roundsplayed"
        GLabel_644.place(x=510,y=80,width=90,height=30)

        GLabel_805=tk.Label(root)
        ft = tkFont.Font(family='Times',size=13)
        GLabel_805["font"] = ft
        GLabel_805["fg"] = "#333333"
        GLabel_805["justify"] = "center"
        GLabel_805["text"] = "VS"
        GLabel_805.place(x=400,y=170,width=200,height=25)

    def GButton_416_command(self):
        print("command")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
