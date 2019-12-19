# -*- coding: utf-8 -*-

'''модуль, позволяющий отображать пользователю изображение'''

from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QImage
from math import floor

class Image(QtWidgets.QLabel):
    '''дополнительный класс для отображения изображения и выбора цвета по нажатию'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.point = None

        #переменная в которую сохраняется выбранный цвет в формате BRG
        #необходима для совмещения изображений
        self.color_ = [-1,]
        self.img = [[[-1,],],]

    def mousePressEvent(self, event):
        '''при нажатии на  изображение определяет выбранного пикселя'''
        self.point = event.pos()
        if self.img[0][0][0]+1 and self.point.x()>=0 and self.point.x() < self.img.shape[1] and self.point.y()-30>=0 and (self.point.y()-30 < self.img.shape[0]):
            self.color_ = self.img[self.point.y()-30][self.point.x()]
            self.color_ = self.color_[::-1]

        # Вызов перерисовки виджета
        self.update()

    def mouseReleaseEvent(self, event):
        pass

    def show_self(self, img):
        '''метод для преобразования размеров изображения и его отображения'''
        self.img = img.copy()
        self.height_, self.width_, self.channel_ = img.shape
        x_coef = self.width_ / 640
        y_coef = self.height_ / 360
        self.img.resize((360,640,3))
        for y in range(360):
            for x in range(640):
                self.img[y][x] = img[floor(y*y_coef)][floor(x*x_coef)]
        self.height_ = 360
        self.width_ = 640
        step = self.channel_*self.width_
        qImg = QImage(self.img.data, self.width_, self.height_, step, QImage.Format_RGB888)
        self.setPixmap(QPixmap.fromImage(qImg))



if __name__ == '__main__':
    app = QApplication([])

    w = Image()
    w.show()

    app.exec()