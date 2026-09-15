import numpy as np
import cv2
from tkinter import filedialog
import matplotlib.pyplot as plt # uso de plt debido a incompatibilidades con ubuntu 



class Constrast():
    def __init__(self, img, reg_size = (450, 450), reg_distance = 15):
        self.img = img
        self.reg_size = reg_size #tamaño de las regiones (vertical, horizontal)
        self.reg_distance = reg_distance #distancia entre centros de regiones
        self.final_img = np.zeros(self.img.shape)

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
 

    def less_contrast(self):
        pass

    def full_image(self):
        self.final_img = self.contrast(self.img)

    def contrast(self, img):
        sk_array = np.round(
            255 * np.cumsum(
                np.bincount(img.ravel(), minlength = 256) / img.size
                ),
                0
                )
        return sk_array[img]

    def show(self) -> None:
        plt.imshow(self.final_img, cmap = "gray")
        plt.axis("off")
        plt.show()

if __name__ == "__main__":
    my_path = filedialog.askopenfilename()
    #transformamos la imagen a escala de grises
    img = cv2.imread(my_path, cv2.IMREAD_GRAYSCALE)
    contrast = Constrast(img)
    if input("Desea ocupar regiones? (Y) : ") == ("Y" or "y"):
            contrast.more_contrast()
    else:
        contrast.full_image()
    contrast.show()

