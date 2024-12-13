#main
import tkinter as tk
from controller.controller import Controller
#running the code through the controller
if __name__ == "__main__":
    root=tk.Tk()
    app = Controller(root)
    app.run()
