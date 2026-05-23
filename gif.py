from tkinter import *
from tkvideo import tkvideo

root = Tk()
root.geometry("700x400")

video_label = Label(root)
video_label.pack()

player = tkvideo("first_1.mp4", video_label, loop=1, size=(700,400))
player.play()

root.mainloop()