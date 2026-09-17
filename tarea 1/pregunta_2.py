import numpy as np
import cv2
from tkinter import filedialog
import matplotlib.pyplot as plt # uso de plt debido a incompatibilidades con ubuntu 



class Constrast():
    def __init__(self, img, reg_size = (450, 450), reg_distance = 15, mult = 255):
        self.img = img
        self.reg_size = reg_size #tamaño de las regiones (vertical, horizontal)
        self.reg_distance = reg_distance #distancia entre centros de regiones
        self.final_img = np.zeros(self.img.shape)
        self.area = mult
        self.offset = (255.0 - mult) / 2.0

    def more_contrast(self):
        h, w = self.img.shape
        mod_matrix = np.zeros(self.img.shape)
        for a in range(0, h, self.reg_distance): #vertical
            m = slice(a, a + self.reg_size[0])
            for b in range(0, w, self.reg_distance): #horizontal
                n = slice(b, b + self.reg_size[1])
                mod_matrix[m, n] += 1
                self.final_img[m, n] += self.contrast(self.img[m, n])
        self.final_img = np.round(self.final_img / mod_matrix).astype(np.uint8)

    def full_image(self):
        self.final_img = self.contrast(self.img)

    def contrast(self, img):
        sk_array = np.round(
            self.offset + (self.area * np.cumsum(
                np.bincount(img.ravel(), minlength = 256) / img.size
                )),
                0
                )
        return sk_array[img]

    def show(self) -> None:
        plt.imshow(self.final_img, cmap = "gray", vmin = 0, vmax = 255)
        plt.axis("off")
        plt.show()

if __name__ == "__main__":
    my_path = filedialog.askopenfilename()
    #transformamos la imagen a escala de grises
    img = cv2.imread(my_path, cv2.IMREAD_GRAYSCALE)
    print("0. Total")
    print("1. Regiones")
    if input("Que desea ocupar?: ") == "1":
        size_reg = [int(a) for a in input("Seleccione tamaño de regiones (ej: 450,450) [enteros] (en pixeles): ").split(",")]
        distance_reg = int(input("Seleccione distancia entre regiones (ej: 15) [entero] (en pixeles): "))
        contrast = Constrast(img, size_reg, distance_reg)
        contrast.more_contrast()
    else:
        contrast = Constrast(img)
        contrast.full_image()
    contrast.show()

