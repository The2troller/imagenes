import numpy as np
import skimage
import cv2
from tkinter import filedialog
# uso de plt debido a incompatibilidades con ubuntu 
import matplotlib.pyplot as plt   

class ColorSaturation():
    def __init__(self, img, pts, mode):
        self.img = img # string
        self.hue = pts [0] # tupla x
        self.mul = pts [1] # tupla y
        self.mode = mode # Bool; False = HS(...) True = CIE L*c*h

    def show(self) -> None:
        plt.imshow(img)
        plt.axis("off")
        plt.show()






if __name__ == "__main__":
    my_path = filedialog.askopenfilename()
    img = cv2.imread(my_path)
    pts_x = int(input("x: "))
    pts_y = int(input("y: "))
    if input("Switch to CIE L*c*h? (Y) Default = HS... : ") == "Y":
        mode = True
    else:
        mode = False
    colorsaturation = ColorSaturation(img, (pts_x, pts_y), mode)
    colorsaturation.show()
