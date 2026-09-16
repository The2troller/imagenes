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
            self.final_img = self.scale_img(self.img)
            self.final_img = self.scale_img(self.img)
        else:
            r = self.scale_img(self.img[:, :, 2])
            g = self.scale_img(self.img[:, :, 1])
            b = self.scale_img(self.img[:, :, 0])
            self.final_img = np.stack((r, g, b), axis = -1).astype(np.uint8)

    def scale_img(self, matrix):
        a = int(matrix.shape[0] * self.scale)
        b = int(matrix.shape[1] * self.scale)
        mod_matrix_v1 = np.zeros((matrix.shape[0], b))
        mod_matrix = np.zeros((a, b))
        for y in range(mod_matrix_v1.shape[0]):
            for x in range(mod_matrix_v1.shape[1]):
                prev_x = x / self.scale
                x_one = matrix[y, int(prev_x)] * (int(prev_x) + 1 - prev_x)
                x_two = matrix[y, min(int(prev_x) + 1, matrix.shape[1] - 1)] * (prev_x - int(prev_x))
                mod_matrix_v1[y, x] = x_one + x_two
        for x in range(mod_matrix.shape[1]):
            for y in range(mod_matrix.shape[0]):
                prev_y = y / self.scale
                y_one = mod_matrix_v1[int(prev_y), x] * (int(prev_y) + 1 - prev_y)
                y_two = mod_matrix_v1[min(int(prev_y) + 1, mod_matrix_v1.shape[0] - 1), x] * (prev_y - int(prev_y))
                mod_matrix[y, x] = y_one + y_two
        return mod_matrix

    def show(self) -> None:
        if self.mode:
            plt.imshow(self.final_img, cmap = "gray")
        else:
            plt.imshow(self.final_img)
        plt.axis("off")
        plt.show()

if __name__ == "__main__":
    my_path = filedialog.askopenfilename()
    #transformamos la imagen a escala de grises
    scalation = float(input("Selecciona multiplicador (ej: 1.5): "))
    print("0. A color")
    print("1. Blanco y negro")
    selection = input("Selecciona tipo de imagen final: ")
    if selection == "1":
        img = cv2.imread(my_path, cv2.IMREAD_GRAYSCALE)
        is_gray = True
    else:
        img = cv2.imread(my_path)
        is_gray = False
    scaling = Scaling(img, scalation, is_gray)
    scaling.process()
    scaling.show()