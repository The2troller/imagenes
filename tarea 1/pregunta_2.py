import numpy as np
import cv2
from tkinter import filedialog
import matplotlib.pyplot as plt # uso de plt debido a incompatibilidades con ubuntu 



class Constrast():
    def __init__(self, img, reg_size = (200, 200), reg_distance = 10):
        self.img = img
        self.reg_size = reg_size #tamaño de las regiones (vertical, horizontal)
        self.reg_distance = reg_distance #distancia entre centros de regiones
        self.final_img = np.zeros(self.img.shape, dtype = np.float32)

    def more_contrast(self):
        h, w = self.img.shape
        mod_matrix = np.zeros(self.img.shape, dtype = np.uint8)
        for a in range(0, h, self.reg_distance): #vertical
            m = slice(a, a + self.reg_size[0])
            for b in range(0, w, self.reg_distance): #horizontal
                n = slice(b, b + self.reg_size[1])
                sk_array = np.zeros(256, dtype = np.uint8)
                for i in range(256):
                    add = 0
                    for x in range(i + 1):
                        nk = np.sum(self.img[m, n] == x)
                        pr = nk / self.img[m, n].size
                        add += pr
                    sk_array[i] = round(255 * add)
                mod_matrix[m, n] += 1
                self.final_img[m, n] += sk_array[self.img[m, n]]
        self.final_img = np.round(self.final_img / mod_matrix).astype(np.uint8)
 

    def less_contrast(self):
        pass

    def full_image(self):
        sk_array = np.zeros(256, dtype = np.uint8)
        for i in range(256):
            add = 0
            for x in range(i + 1):
                nk = np.sum(self.img == x)
                pr = nk / self.img.size
                add += pr
            sk_array[i] = round(255 * add)
        self.final_img = sk_array[self.img]

    def show(self) -> None:
        plt.imshow(self.final_img, cmap = "gray")
        plt.axis("off")
        plt.show()

if __name__ == "__main__":
    my_path = filedialog.askopenfilename()
    #transformamos la imagen a escala de grises
    #img = cv2.imread(my_path, cv2.IMREAD_GRAYSCALE)
    #contrast = Constrast(img)
    #contrast.full_image()
    #contrast.show()
    #contrast = Constrast(img)
    #contrast.more_contrast()
    #contrast.show()

