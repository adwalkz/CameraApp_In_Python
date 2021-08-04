from tkinter import *
import cv2
import time
from PIL import Image, ImageTk


class AdCam:
    def __init__(self, src=0):
        self.src = src
        self.cam = cv2.VideoCapture(src)
        self.width = int(str(self.cam.get(cv2.CAP_PROP_FRAME_WIDTH)).partition('.')[0].partition('x')[0])
        self.height = int(str(self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT)).partition('.')[0].partition('x')[0]) + 50

        self.pic = None

        self.window = Tk()
        self.window.title("AdCam: Camera")
        self.window.resizable(0, 0)
        self.window.geometry(f"{self.width}x{self.height}")
        self.window['bg'] = 'black'

        self.menuBar = Menu(self.window)
        self.window.config(menu=self.menuBar)

        self.mi_File = Menu(self.menuBar, tearoff=0)
        self.menuBar.add_cascade(label="File", menu=self.mi_File)
        self.mi_File.add_command(label="Open Recent")
        self.mi_File.add_separator()
        self.mi_File.add_command(label="Exit", command=self.exit_AdCam, accelerator="Alt+X")

        self.mi_Filters = Menu(self.menuBar, tearoff=0)
        self.menuBar.add_cascade(label="Filters", menu=self.mi_Filters)
        self.mi_Filters.add_command(label="Black and White")
        self.mi_Filters.add_command(label="Coloured")

        self.canvas = Canvas(self.window, width=self.width, height=self.height, bg="black")
        self.canvas.pack()

        self.click = Button(self.window, text="CLICK", bg="yellow", width=20, command=self.AdClick)
        self.click.place(x=self.width//2-80, y=self.height-45)
        self.click.focus_force()

        self.update()
        self.active_thread()
        self.window.mainloop()

    def AdClick(self):
        check, frame = self.getFrame()
        if check:
            image = "AdCam-IMG-" + time.strftime("%H-%M-%S-%d-%m") + ".jpeg"
            cv2.imwrite(image, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            # view = Frame(self.window, height=45, width=30, bg="white")
            # view.place(x=5, y=self.height-50)
            # view.config(frame)
            # msg = Label(self.window, text="image saved as: "+image, bg="black", fg="green")
            # msg.place(x=self.width//2-100, y=self.height-25)

    def update(self):
        check, frame = self.getFrame()

        if check:
            self.pic = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.pic, anchor=NW)

        self.window.after(1, self.update)

    def exit_AdCam(self, e=None):
        self.window.destroy()

    def active_thread(self):
        self.window.bind('<Alt-x>', self.exit_AdCam)

    def getFrame(self):
        check, frame = self.cam.read()

        if check:
            return check, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        else:
            return check, None

    def __del__(self):
        if self.cam.isOpened():
            self.cam.release()


if __name__ == "__main__":
    AdCam()
