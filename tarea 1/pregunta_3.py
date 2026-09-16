import numpy as np
import cv2
from tkinter import filedialog
import matplotlib.pyplot as plt # uso de plt debido a incompatibilidades con ubuntu 


class Scaling():
    def __init__(self, img, scale : float = 1.0, mode : bool = False):
        self.img = img
        self.scale = scale
        self.mode = mode #rgb = False, gray = True
        a, b = self.img.shape[0:2]
        self.a = int(a * scale)
        self.b = int(b * scale)
        self.final_img = None
        
    def process(self):
        if self.mode:
            if self.scale >= 1.0:
                pass
            else:
                self.final_img = self.downscaling(self.img)
        else:
            if self.scale >= 1.0:
                r = self.upscaling(self.img[:, :, 2])
                g = self.upscaling(self.img[:, :, 1])
                b = self.upscaling(self.img[:, :, 0])
            else:
                r = self.downscaling(self.img[:, :, 2])
                g = self.downscaling(self.img[:, :, 1])
                b = self.downscaling(self.img[:, :, 0])
                self.final_img = np.stack((r, g, b), axis = -1).astype(np.uint8)

    def upscaling(self):
        pass

    def downscaling(self, matrix):
        mod_matrix_v1 = np.zeros((matrix.shape[0], self.b))
        mod_matrix = np.zeros((self.a, self.b))

        for u in range(matrix.shape[0]):
            x = 0
            add = 0
            pixels = 0
            j = 0
            for i in range(matrix.shape[1]):
                if j >= 1:
                    mod_matrix_v1[u, x] = add / pixels
                    pixels = 0
                    j -= 1
                    add = 0
                    x += 1
                add += float(matrix[u, i])
                j += self.scale
                pixels += 1
        for i in range(self.b):
            y = 0
            add = 0
            pixels = 0
            j = 0
            for u in range(matrix.shape[0]):
                if j >= 1:
                    mod_matrix[y, i] = add / pixels
                    pixels = 0
                    j -= 1
                    add = 0
                    y += 1
                add += mod_matrix_v1[u, i]
                j += self.scale
                pixels += 1
        return mod_matrix





    def show(self) -> None:
        plt.imshow(self.final_img)
        plt.axis("off")
        plt.show()





if __name__ == "__main__":
    my_path = filedialog.askopenfilename()
    #transformamos la imagen a escala de grises
    img = cv2.imread(my_path)
    scaling = Scaling(img, 0.5)
    scaling.process()
    scaling.show()