#! /usr/bin/python3.6
# -*- coding: utf-8 -*-

'''основной модуль, реализующий взаимодействие пользователя с приложением через пользовательский интерфейс'''

from PyQt5 import QtWidgets, QtGui, QtCore
from mainwindow import Ui_MainWindow
from qtimage import Image
from chroma_key_replace import *
from cv2 import cvtColor, COLOR_BGR2RGB

import os.path
import sys

class mywindow(QtWidgets.QMainWindow, Ui_MainWindow):
    '''класс, добавляющий в пользовательский интерфейс функциональность'''
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setupUi_new()

    def setupUi_new(self):
        '''дополнение виджетов пользовательского интерфейса и определение методов, которые срабатывают по нажатию'''

        #слайдеры, позволяющие выбрать точность выбора цветового ключа, заданного в формате RGB
        self.red_acc.setMinimum(0)
        self.red_acc.setMaximum(255)
        self.red_acc.setTickInterval(5)
        self.red_acc.setValue(30)
        self.green_acc.setMinimum(0)
        self.green_acc.setMaximum(255)
        self.green_acc.setTickInterval(5)
        self.green_acc.setValue(30)
        self.blue_acc.setMinimum(0)
        self.blue_acc.setMaximum(255)
        self.blue_acc.setTickInterval(5)
        self.blue_acc.setValue(30)

        #виджет, отображающий изображения и позволяющий кликом мышки выбрать цветовой ключ
        self.listWidget = Image(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(0, 0, 640, 360))
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout_3.addWidget(self.listWidget)

        #добавление функциональности кнопок для поиска картинок и папки для записи результата
        self.brws_1.clicked.connect(self.brws_img_1)
        self.brws_2.clicked.connect(self.brws_img_2)
        self.brws_s.clicked.connect(self.brws_fold_s)
        self.save_btn.clicked.connect(self.save_res)

        #добавление функциональности для кнопки совмещения изображения
        self.comb.clicked.connect(self.combine)

        #добавление функциональности для кнопки отображения исходного изображения
        self.src.clicked.connect(self.source)

        #добавление переменных, хранящих состояние приложения
        self.fileName1 = None
        self.fileName2 = None
        self.saveFolder = None
        self.img1 = None
        self.img2 = None
        self.res_im = [[[-1,],],]

    def source(self):
        '''отображает исходное изображение в случае, когда заданы имена исходного и конечного файлов'''
        if self.fileName1 and self.fileName2:
            self.img1, self.img2 = get_source_images(self.fileName1, self.fileName2)
            self.listWidget.show_self(cvtColor(self.img1, COLOR_BGR2RGB))
            self.res_im = [[[-1,],],]
 
    def combine(self):
        '''совмещает изображения, если выбраны имена файлов и задан цветовой ключ'''
        if self.fileName1 and self.fileName2:
            self.img1, self.img2 = get_source_images(self.fileName1, self.fileName2)
            if self.listWidget.color_[0] + 1:
                self.res_im = combine_images(self.img1, self.img2, chroma_key=self.listWidget.color_, acc= [ self.blue_acc.value(), self.green_acc.value(), self.red_acc.value()])
                self.listWidget.show_self(cvtColor(self.res_im, COLOR_BGR2RGB))

    def save_res(self):
        '''сохраняет результат в файл, если выбрана папка для сохранения и совмещены изображения'''
        if self.saveFolder and self.res_im[0][0][0]+1:
            name = '/res.jpg'
            counter = 0
            while os.path.exists(self.saveFolder+name):
                counter += 1
                name = '/res'+str(counter)+ '.jpg'
            write_img(self.res_im, self.saveFolder+name)

    def brws_fold_s(self):
        '''поиск папки для сохранения'''
        self.saveFolder = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите папку")

    def brws_img_1(self):
        '''поиск изображения 1'''
        self.fileName1 = QtWidgets.QFileDialog.getOpenFileName(self, "Open Image", "/home", "Image Files (*.png *.jpg *.bmp)")[0]

    def brws_img_2(self):
        '''поиск изображения 2'''
        self.fileName2 = QtWidgets.QFileDialog.getOpenFileName(self, "Open Image", "/home", "Image Files (*.png *.jpg *.bmp)")[0]

def main():
    '''отображение окна пользовательского интерфейса'''
    app = QtWidgets.QApplication(sys.argv)
    window = mywindow()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()