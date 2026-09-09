import numpy as np
import skimage
import cv2
from tkinter import filedialog
# uso de plt debido a incompatibilidades con ubuntu 
import matplotlib.pyplot as plt
from transformations import (
    rgb_to_hsi, rgb_to_lch, hsi_to_rgb, lch_to_rgb, bgr_to_rgb
)


class ColorSaturation():
    def __init__(self, img, pts, mode: bool):
        self.img = img
        self.pts = pts # tupla pts
        self.mode = mode # Bool; False = HSI True = CIE L*c*h
        self.trans_img = None
        self.mod_img = None
        self.mh = None

    def modify(self) -> None:
        if self.mode:
            #CIE L*c*h
            self.lch_mod()
        else:
            #HSI
            self.hsi_mod()

    def lch_mod(self) -> None:
        self.trans_img = rgb_to_lch(self.img)

    def hsi_mod(self) -> None:
        self.trans_img = rgb_to_hsi(self.img)
        self.map_mh()


    def map_mh(self):
        self.mh = np.interp(self.trans_img[:, :, 0],
                                 self.pts[:, 0],  self.pts[:, 1], period = 360.0)

    def show(self) -> None:
        plt.imshow(self.img)
        plt.axis("off")
        plt.show()






if __name__ == "__main__":
    my_path = filedialog.askopenfilename()
    img = cv2.imread(my_path) #saves in bgr
    if input("Alternar a CIE L*c*h? (Y) Default = HSI : ") == "Y":
        mode = True
    else:
        mode = False

    points = list()
    while True:
        print("Si no deseas colocar mas puntos, dejalo vacio")
        point = input("Puntos (escribe 'x,y'): ")
        if point:
            points.append([float(p) for p in point.split(",")])
        if not points:
            print("Minimo de un punto")
        else:
            if not point:
                break
    points.sort(key = lambda x: x[0])
    colorsaturation = ColorSaturation(bgr_to_rgb(img), np.array(points), mode)
    colorsaturation.modify()

    colorsaturation.show()
