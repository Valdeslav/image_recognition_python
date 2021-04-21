import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Combobox
from PIL import ImageGrab, Image, ImageTk
import numpy as np
from neural_network.expert_vectors import ExpertVector
from matplotlib import pyplot as plt
from neural_network.algorithm import predict


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.cur_numb = 1
        self.exp_v = ExpertVector()
        self.x = self.y = 0

        # Создание элементов
        self.canvas = tk.Canvas(self, width=300, height=300, bg="white", cursor="cross")
        self.label = tk.Label(self, text="Думаю..", font=("Helvetica", 24))
        self.classify_btn = tk.Button(self, text="Распознать", command=self.classify_handwriting)
        self.button_clear = tk.Button(self, text="Очистить", command=self.clear_all)
        self.add_exp_vector_btn = tk.Button(self, text="Добавить к экспертным", command=self.add_expert_vector)
        self.chose_number_combo = Combobox(self)
        self.chose_number_combo['values'] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.chose_number_combo.current(1)

        # Сетка окна
        self.canvas.grid(row=0, column=0, pady=2, sticky=tk.W, columnspan=2, rowspan=2)
        self.label.grid(row=1, column=2, pady=2, padx=2, sticky=tk.N)
        self.classify_btn.grid(row=2, column=1, padx=2)
        self.button_clear.grid(row=2, column=0, padx=2)
        self.add_exp_vector_btn.grid(row=2, column=2)
        self.chose_number_combo.grid(row=0, column=2, pady=4, sticky=tk.N)

        # self.canvas.bind("<Motion>", self.start_pos)
        self.canvas.bind("<B1-Motion>", self.draw_lines)
        self.chose_number_combo.bind("<<ComboboxSelected>>", self.change_num)
        self.add_exp_vector_btn.bind()

    def clear_all(self):
        self.canvas.delete("all")

    def _canvas(self):
        cv = self.canvas
        x1 = cv.winfo_rootx() + cv.winfo_x()
        y1 = cv.winfo_rooty() + cv.winfo_y()
        x2 = x1 + cv.winfo_width()
        y2 = y1 + cv.winfo_height()
        rect = (x1, y1, x2, y2)
        return rect

    def classify_handwriting(self):
        im = ImageGrab.grab(bbox=self._canvas())
        im = im.resize((100, 100))
        if predict(self.exp_v.simplify_vector(im), self.cur_numb):
            self.label.configure(text=f'Число является {self.cur_numb}')
        else:
            self.label.configure(text=f'Число не является {self.cur_numb}')
        #plt.imshow(iar)

        #plt.imshow(part)
        #plt.show()

    def add_expert_vector(self):
        res = messagebox.askyesno('предупреждение', f'Вы действительно хотите добавить экспертный вектор для цифры {self.cur_numb}')
        if res:
            im = ImageGrab.grab(bbox=self._canvas())
            im = im.resize((100, 100))
            self.exp_v.add_expert_vector(im, f'vectors/{self.cur_numb}.bin')

    def draw_lines(self, event):
        self.x = event.x
        self.y = event.y
        r = 8
        self.canvas.create_oval(self.x - r, self.y - r, self.x + r, self.y + r, fill='black')

    def change_num(self, event):
        self.cur_numb = self.chose_number_combo.get()
