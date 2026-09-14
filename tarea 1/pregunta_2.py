import numpy as np
import cv2
from tkinter import filedialog
import matplotlib.pyplot as plt # uso de plt debido a incompatibilidades con ubuntu 



class Constrast():
    def __init__(self, img, reg_size = 1, reg_distance = 2):
        self.img = img
        self.reg_size = reg_size
        self.reg_distance = reg_distance
        self.final_img = img

    def more_contrast(self):
        pass

    def less_contrast(self):
        pass

    def ec_formula(self):
        self.sk_array = []
        for i in range(self.img.max() + 1):
            add = 0
            for x in range(i + 1):
                nk = np.sum(self.img == x)
                pr = nk / self.img.size
                sk = round(self.img.max() * pr)
                add += sk
            self.sk_array.append(add)
        self.sk_array = np.array(self.sk_array)
        self.final_img = self.sk_array[self.img]

    def show(self) -> None:
        plt.imshow(self.final_img, cmap = "gray")
        plt.axis("off")
        plt.show()

if __name__ == "__main__":
    my_path = filedialog.askopenfilename()
    #transformamos la imagen a escala de grises
    img = cv2.imread(my_path, cv2.IMREAD_GRAYSCALE)
    contrast = Constrast(img)
    
    contrast.ec_formula()


    contrast.show()

