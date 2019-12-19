# -*- coding: utf-8 -*-

'''модуль с функциями замены цветового ключа'''
import cv2
import copy


def get_source_images(filename1='images/src1.jpg', filename2='images/src2.jpg'):
    '''возвращает 2 изображения в формате ndarray
     из файлов filename1 и filename2
     по умолчанию из src1.jpg и из src2.jpg'''
    src_img_1 = cv2.imread(filename1)
    src_img_2 = cv2.imread(filename2)
    return src_img_1, src_img_2

def height(img):
    '''возвращает высоту изображения'''
    return img.shape[0]

def width(img):
    '''возвращает ширину изображения'''
    return img.shape[1]

def get_img2_coord_convers_coeffs(img1, img2):
    '''возвращает коэффициенты преобразования координат для img2 для осей y и x: 
    елси изображения имеют разные размеры, 
    то img2 необходимо растянуть или сжать перед совмещением изображений'''
    return height(img2)/height(img1), width(img2)/width(img1)

def is_pixel_chroma(pixel, chroma_key = [0, 255, 0], acc = [80, 80, 80]):
    '''сравнивает цвет пикселя с цветовым ключом'''
    [b_key, g_key, r_key ] = chroma_key
    return pixel[0] >= b_key-acc[0] and pixel[0] <= b_key+acc[0] \
            and pixel[1] >= g_key-acc[1] and pixel[1] <= g_key+acc[1]\
            and pixel[2] >= r_key-acc[2] and pixel[2] <= r_key+acc[2]

def combine_images(img1, img2, chroma_key = [0, 255, 0], acc = [100,100,100]):
    '''возвращает совмещенное изображение'''
    y_coef, x_coef = get_img2_coord_convers_coeffs(img1, img2)
    img1 = copy.deepcopy(img1)
    for i in range(height(img1)):
        for j in range(width(img1)):
            if is_pixel_chroma(img1[i][j], chroma_key, acc):
                img1[i][j][2] = img2[int(i*y_coef)][int(j*x_coef)][2]
                img1[i][j][1] = img2[int(i*y_coef)][int(j*x_coef)][1]
                img1[i][j][0] = img2[int(i*y_coef)][int(j*x_coef)][0]
    return img1

def write_img(img, filename='images/res.jpg'):
    '''записывает изображение в файл с именем filenameS
     по умолчанию res.jpg'''
    cv2.imwrite(filename, img)
