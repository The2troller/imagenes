import numpy as np
import skimage
import cv2
from tkinter import filedialog
# uso de plt debido a incompatibilidades con ubuntu 
import matplotlib.pyplot as plt
from transformations import rgb_to_hsi


class ColorSaturation():
    def __init__(self, img, pts, mode):
        self.img = img
        self.hue = pts [0] # tupla color seleccionado
        self.mul = pts [1] # tupla saturacion seleccionada
        self.mode = mode # Bool; False = HSI True = CIE L*c*h
        self.mod_img = None

    def modify(self) -> None:
        if mode:
            #CIE L*c*h
            self.cie_mod()
        else:
            #HSI
            self.hsi_mod()

    def cie_mod(self) -> None:
        pass

    def hsi_mod(self) -> None:
        pass

    def show(self) -> None:
        plt.imshow(img)
        plt.axis("off")
        plt.show()






if __name__ == "__main__":
    my_path = filedialog.askopenfilename()
    img = cv2.imread(my_path) #saves in bgr
    pts_x = int(input("Color a modificar: "))
    pts_y = int(input("Saturacion deseada: "))
    if input("Switch to CIE L*c*h? (Y) Default = HSI : ") == "Y":
        mode = True
    else:
        mode = False
    colorsaturation = ColorSaturation(img, (pts_x, pts_y), mode)
    colorsaturation.modify()
    colorsaturation.show()
