import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
import cv2
import numpy as np

class PaintApp:
    def __init__(self, root):
        self.image_tk = None
        self.image_pil = None
        self.root = root
        self.drawing = False
        self.last_x = 0
        self.last_y = 0
        self.mode = 'draw'
        self.canvas = tk.Canvas(root, width=800, height=500)
        self.canvas.pack()
        self.image = np.ones((500, 800, 3), dtype=np.uint8) * 255
        self.temp_img = self.image.copy()
        self.color = (0, 0, 0)
        self.brush = ["circle", 12]
        self.canvas.bind('<Button-1>', self.last_position)
        self.canvas.bind('<B1-Motion>', self.draw_mode)
        self.canvas.bind('<ButtonRelease-1>', self.last_position)
        self.create_stack()

        self.button_draw_image = ImageTk.PhotoImage(Image.open('2.png').resize((50, 50)))
        self.button_line_image = ImageTk.PhotoImage(Image.open('3.png').resize((50, 50)))
        self.button_square_image = ImageTk.PhotoImage(Image.open('6.png').resize((50, 50)))
        self.button_circle_image = ImageTk.PhotoImage(Image.open('1.png').resize((50, 50)))
        self.button_erase_image = ImageTk.PhotoImage(Image.open('4.png').resize((50, 50)))

        self.button_draw = tk.Button(root, image=self.button_draw_image, command=self.set_mode_draw)
        self.button_draw.place(x=20, y=20)
        self.button_line = tk.Button(root, image=self.button_line_image, command=self.set_mode_line)
        self.button_line.place(x=20, y=80)
        self.button_square = tk.Button(root, image=self.button_square_image, command=self.set_mode_square)
        self.button_square.place(x=20, y=140)
        self.button_circle = tk.Button(root, image=self.button_circle_image, command=self.set_mode_circle)
        self.button_circle.place(x=20, y=200)
        self.button_color = tk.Button(root, image=self.button_erase_image, command=self.button_erase)
        self.button_color.place(x=20, y=260)

    def button_erase(self):
        self.mode = 'erase'

    def set_mode_circle(self):
        self.mode = 'circle'

    def set_mode_draw(self):
        self.mode = 'draw'

    def set_mode_line(self):
        self.mode = 'line'

    def set_mode_square(self):
        self.mode = 'square'

    @staticmethod
    def get_radious(x1, y1, x2, y2):
        return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def create_stack(self):
        self.image_pil = Image.fromarray(self.temp_img)
        self.image_tk = ImageTk.PhotoImage(self.image_pil)
        self.canvas.create_image(0, 0, image=self.image_tk, anchor='nw')

    def last_position(self, event):
        self.image = self.temp_img
        self.drawing = True

    def draw_mode(self, event):
        print(self.image_pil)
        x = event.x
        y = event.y

        if self.drawing:
            self.drawing = False
            self.last_x, self.last_y = x, y

        if self.mode == 'circle':
            self.temp_img = self.image.copy()
            radious = self.get_radious(self.last_x, self.last_y, x, y)
            cv2.circle(self.temp_img, (self.last_x, self.last_y), int(radious), self.color, self.brush[1],
                       lineType=cv2.LINE_AA)
            self.create_stack()
        if self.mode == 'square':
            self.temp_img = self.image.copy()
            cv2.rectangle(self.temp_img, (self.last_x, self.last_y), (x, y), self.color, self.brush[1],
                          lineType=cv2.LINE_AA)
            self.create_stack()
        if self.mode == 'draw':
            thick = 3 if self.brush[1] < 0 else self.brush[1]
            self.temp_img = self.image.copy()
            cv2.line(self.image, (self.last_x, self.last_y), (x, y), self.color, thickness=thick, lineType=cv2.LINE_AA)
            self.last_x, self.last_y = x, y
            self.create_stack()
        if self.mode == 'line':
            thick = 3 if self.brush[1] < 0 else self.brush[1]
            self.temp_img = self.image.copy()
            cv2.line(self.temp_img, (self.last_x, self.last_y), (x, y), self.color, thickness=thick,
                     lineType=cv2.LINE_AA)
            self.create_stack()
        if self.mode == 'erase':
            thick = 3 if self.brush[1] < 0 else self.brush[1]
            self.temp_img = self.image.copy()
            cv2.line(self.image, (self.last_x, self.last_y), (x, y), (255, 255, 255), thickness=thick, lineType=cv2.LINE_AA)
            self.last_x, self.last_y = x, y
            self.create_stack()


root = tk.Tk()
root.title("Paint Chido pero así bien chido")
app = PaintApp(root)
root.mainloop()
