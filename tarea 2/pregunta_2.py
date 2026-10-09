import numpy as np
import cv2
from tkinter import filedialog
import matplotlib.pyplot as plt # uso de plt debido a incompatibilidades con ubuntu 
from generador_imagenes import generate_gauss_noise
import skimage as ski
from scipy.ndimage import map_coordinates

class P2():
    def __init__(self, img):
        self.img = img
        self.final_img = None

    def difusion_anisotropica(self):
        img = self.img.copy()
        for _ in range():
            nabla_N = np.roll(img, 1, axis=0) - img
            nabla_S = np.roll(img, -1, axis=0) - img
            nabla_E = np.roll(img, -1, axis=1) - img
            nabla_W = np.roll(img, 1, axis=1) - img

    def variacion_total(self, grad_mag_sq, epsilon):
        c_tv= 1 / np.sqrt(grad_mag_sq + np.square(epsilon))

    def show(self) -> None:
        plt.imshow(self.final_img)
        plt.axis("off")
        plt.show()

if __name__ == "__main__":
    my_path = filedialog.askopenfilename()
    camera = ski.data.camera()
    camera_n = camera.astype(np.float32) / 255.0
