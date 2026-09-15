import numpy as np
import cv2
from tkinter import filedialog
import matplotlib.pyplot as plt # uso de plt debido a incompatibilidades con ubuntu 


class Scaling():
    def __init__(self, img, scale : float = 1.0, mode : bool = False):
        self.img = img
        self.scale = scale
        self.mode = mode #rgb = False, gray = True
        self.final_img = np.zeros([int(length * scale) for length in self.img.shape],
                                dtype = np.uint8)

    def process(self):
        if self.mode:
            pass
        else:
            if self.scale >= 1.0:
                r = self.upscaling(self.img[:, :, 2])
                g = self.upscaling(self.img[:, :, 1])
                b = self.upscaling(self.img[:, :, 0])
            else:
                r = self.downscaling(self.img[:, :, 2])
                g = self.downscaling(self.img[:, :, 1])
                b = self.downscaling(self.img[:, :, 0])
                self.final_img = np.clip((r, g, b))

    def upscaling(self):
        pass

    def downscaling(self, matrix):
        mod_img = np.zeros(self.final_img.shape, dtype = np.uint8)
        a, b = matrix.shape
        x = self.scale
        y = 0
        l = 0
        n = 0
        for i in range(a):
            for m in range(b):
                if x > 1:
                    mod_img[i, y] = int(n / l)
                    y += 1
                    n = 0
                    x = 0
                n += matrix[i, m]
                x += self.scale
                l += 1
        return mod_img

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