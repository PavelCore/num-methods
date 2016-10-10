#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, 
    QGridLayout, QApplication, QPushButton)


class Window(QWidget):

    p_edit_a = None
    p_edit_b = None
    s_edit = None
    z_edit = None
    x_0_edit = None
    y_0_edit = None
    beta_edit = None
    T_edit = None


    def __init__(self, click_function):
        super().__init__()

        self.click_function = click_function
        self.initUI()


    def initUI(self):

        z_descr = QLabel('Enter c parameter for z function: c * t - cos(t))')
        z_par_descr = QLabel('c: ')
        s_descr = QLabel('Enter d parameter for s function: d * t + sin(t)')
        s_par_descr = QLabel('d: ')
        p_descr = QLabel('Enter a and b parameters for p function: aw(b - w)')
        p_par_descr_a = QLabel('a: ')
        p_par_descr_b = QLabel('b: ')
        other_par_descr = QLabel("Enter initial parameters")
        x_0_descr = QLabel("x0: ")
        y_0_descr = QLabel("y0: ")
        beta_descr = QLabel("beta: ")
        T_descr = QLabel("T: ")

        self.p_edit_a = QLineEdit()
        self.p_edit_b = QLineEdit()
        self.s_edit = QLineEdit()
        self.z_edit = QLineEdit()
        self.x_0_edit = QLineEdit()
        self.y_0_edit = QLineEdit()
        self.beta_edit = QLineEdit()
        self.T_edit = QLineEdit()

        submit_btn = QPushButton("submit", self)

        grid = QGridLayout()

        grid.addWidget(z_descr, 1, 0)
        grid.addWidget(z_par_descr, 2, 0)
        grid.addWidget(self.z_edit, 2, 1)

        grid.addWidget(s_descr, 3, 0)
        grid.addWidget(s_par_descr, 4, 0)
        grid.addWidget(self.s_edit, 4, 1)

        grid.addWidget(p_descr, 5, 0)
        grid.addWidget(p_par_descr_a, 6, 0)
        grid.addWidget(p_par_descr_b, 7, 0)
        grid.addWidget(self.p_edit_a, 6, 1)
        grid.addWidget(self.p_edit_b, 7, 1)

        grid.addWidget(other_par_descr, 8, 0)
        grid.addWidget(x_0_descr, 9, 0)
        grid.addWidget(y_0_descr, 10, 0)
        grid.addWidget(beta_descr, 11, 0)
        grid.addWidget(T_descr, 12, 0)
        grid.addWidget(self.x_0_edit, 9, 1)
        grid.addWidget(self.y_0_edit, 10, 1)
        grid.addWidget(self.beta_edit, 11, 1)
        grid.addWidget(self.T_edit, 12, 1)

        grid.addWidget(submit_btn, 13, 0)
        submit_btn.clicked.connect(self.on_button_click)

        self.setLayout(grid)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('NumMethods')
        self.show()

    def on_button_click(self):
        a = float(self.p_edit_a.text())
        b = float(self.p_edit_b.text())
        c = float(self.s_edit.text())
        d = float(self.z_edit.text())
        x_0 = float(self.x_0_edit.text())
        y_0 = float(self.y_0_edit.text())
        beta = float(self.beta_edit.text())
        T = float(self.T_edit.text())
        self.click_function(a, b, c, d, x_0, y_0, beta, T)


def draw_graphics():
    plt.figure(1)

    # initialize plots data and add them as subplot
    t_x, x = [], []
    with open("x_answer.txt", 'r') as f:
        for line in f:
            data = line.split(' ')
            t_x.append(float(data[0]))
            x.append(float(data[1]))
    plt.subplot(231)
    plt.plot(t_x, x)
    plt.title('X(t)')

    t_s, s = [], []
    with open("tabulated_functions/s_func_tabulated", 'r') as f:
        for line in f:
            data = line.split(' ')
            t_s.append(float(data[0]))
            s.append(float(data[1]))
    plt.subplot(232)
    plt.plot(t_s, s)
    plt.title('S(t)')

    t_p, p = [], []
    with open("tabulated_functions/p_func_tabulated", 'r') as f:
        for line in f:
            data = line.split(' ')
            t_p.append(float(data[0]))
            p.append(float(data[1]))
    plt.subplot(233)
    plt.plot(t_p, p)
    plt.title('p(w)')

    t_z, z = [], []
    with open("tabulated_functions/z_func_tabulated", 'r') as f:
        for line in f:
            data = line.split(' ')
            t_z.append(float(data[0]))
            z.append(float(data[1]))
    plt.subplot(234)
    plt.plot(t_z, z)
    plt.title('Z(t)')

    x_s = [x[i] - s[i] for i in range(0, len(t_x))]
    plt.subplot(235)
    plt.plot(t_x, x_s)
    plt.title('X(t) - S(t)')

    t_y, y = [], []
    with open("y_answer.txt", 'r') as f:
        for line in f:
            data = line.split(' ')
            t_y.append(float(data[0]))
            y.append(float(data[1]))
    plt.subplot(236)
    plt.plot(t_y, y)
    plt.title('Y(t)')

    plt.show()
