import numpy as np
from tkinter import filedialog
import matplotlib.pyplot as plt # uso de plt debido a incompatibilidades con ubuntu 
import skimage as ski
from generador_imagenes import generate_gauss_noise

class P2():
    def __init__(self, img):
        self.img = img
        self.final_img = None
        self.c_map = None

    def difusion_anisotropica(self, mode, num_iterations, lam, epsilon):
        if lam > 0.25:
            print(f"Advertencia: lam={lam} inestable. Se ajustó a 0.25 por seguridad.")
            lam = 0.25
        img = self.img.copy()
        for i in range(num_iterations):
            up = np.roll(img, 1, axis=0) - img
            down = np.roll(img, -1, axis=0) - img
            right = np.roll(img, -1, axis=1) - img
            left = np.roll(img, 1, axis=1) - img

            if mode == "0": #TV
                grad_x = (right - left) / 2.0
                grad_y = (down - up) / 2.0
                grad_mag_sq = np.square(grad_x) + np.square(grad_y)

                c = 1 / np.sqrt(grad_mag_sq + np.square(epsilon))
                c =  c / np.max(c)

            if mode == "1": #LP
                laplaciano = up + down + right + left

                c = np.exp(-np.square(laplaciano / epsilon))
                c = c / np.max(c)

            if mode == "2": #gauss + LP
                grad_x = (right - left) / 2.0
                grad_y = (down - up) / 2.0
                grad_mag_sq = np.square(grad_x) + np.square(grad_y)
                laplaciano = up + down + right + left
                ep = epsilon + laplaciano + 1e-6
                c = np.exp(-grad_mag_sq / (2 * np.square(ep)))
                c =  c / np.max(c)

            c_up = (c + np.roll(c, 1, axis=0)) / 2.0
            c_down = (c + np.roll(c, -1, axis=0)) / 2.0
            c_right = (c + np.roll(c, -1, axis=1)) / 2.0
            c_left = (c + np.roll(c, 1, axis=1)) / 2.0
            img = img + lam * (c_up * up + c_down * down + c_right * right + c_left * left)
            if i == num_iterations - 1:
                self.c_map = c

        self.final_img = img


    def show(self, img) -> None:
        plt.imshow(img)
        plt.axis("off")
        plt.show()

if __name__ == "__main__":
    camera = ski.data.camera()
    seed = int(input("semilla a usar: "))
    camera_n = camera.astype(np.float32) / 255.0
    camera_n = generate_gauss_noise(camera_n, seed)
    print("[0] TV")
    print("[1] LP")
    print("[2] G + LP")
    mode = input("modo: ")
    num_iter = int(input("cantidad de iteraciones (int): "))
    lam = float(input("lambda (float): "))
    eps = float(input("epsilon (float): "))
    p2 = P2(camera_n)
    p2.difusion_anisotropica(mode, num_iter, lam, eps)
    p2.show(camera_n)
    p2.show(p2.final_img)
    p2.show(p2.c_map)
