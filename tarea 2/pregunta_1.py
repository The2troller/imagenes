import numpy as np
import cv2
import matplotlib.pyplot as plt # uso de plt debido a incompatibilidades con ubuntu 

from generador_imagenes import generate_img_p1

class Gaussian_adaptative_filter():
    def __init__(self, img, sigma, data:None):
        self.img = img
        self.data = data
        self.sigma = sigma
        self.kernel = None
        self.final_img = None

    def filter(self):
        self.gaussian_kernel(self.sigma)
        self.final_img = self.apply_gaussian_filter(self.img, self.kernel)

    def adaptative_filter(self): #podemos añadir el test de testing para calcular la mejor sola
        min_data = self.get_min()
        self.filter()
        filtered_img = self.final_img.copy()
        background_mask = filtered_img < 0.30
        square_mask = (filtered_img >= 0.30) & (filtered_img < 0.60)
        circle_mask = (filtered_img >= 0.60)
        self.sigma_map = np.zeros((256,256))
        self.sigma_map[background_mask] = min_data[1]
        self.sigma_map[square_mask] = min_data[2]
        self.sigma_map[circle_mask] = min_data[3]
        background_kernel = self.gaussian_kernel(min_data[1]) 
        background = self.apply_gaussian_filter(self.img, background_kernel)
        background *= background_mask
        square_kernel = self.gaussian_kernel(min_data[2])
        square = self.apply_gaussian_filter(self.img, square_kernel)
        square *= square_mask
        circle_kernel = self.gaussian_kernel(min_data[3])
        circle = self.apply_gaussian_filter(self.img, circle_kernel)
        circle *= circle_mask
        self.final_img = background + square + circle
        return filtered_img

    def RMSE(self, base_img, mask = None):
        dif = 0
        count = 0
        if mask is not None:
            for y in range(256):
                for x in range(256):
                    if mask[x, y] != 0:
                        dif += np.square(base_img[x, y] - self.final_img[x, y])
                        count += 1 
            dif = dif / count
            return np.sqrt(dif) 
        else:
            for y in range(256):
                for x in range(256):
                    dif += np.square(base_img[x, y] - self.final_img[x, y])
                    count += 1 
            dif = dif / count
            return np.sqrt(dif)


    def show(self, img) -> None:
        plt.imshow(img)
        plt.axis("off")
        plt.title(self.sigma)
        plt.show()

    def get_min(self):
        rmse_values_real = []
        rmse_values_background = []
        rmse_values_square = []
        rmse_values_circle = []
        min_real = None
        min_background = None
        min_square = None
        min_circle = None
        s_values = [x / 10 for x in range(0, 56)][1:]
        for s in s_values: #presionar ctrl + c en consola para salir
            self.sigma = s
            self.filter()
            rmse = self.RMSE(self.data[0])
            rmse_values_real.append(rmse)
            if not min_real or min_real > rmse:
                min_real = rmse
                min_sigma_real = s
            rmse = self.RMSE(self.data[0], self.data[1])
            rmse_values_background.append(rmse)
            if not min_background or min_background > rmse:
                min_background = rmse
                min_sigma_background = s
            rmse = self.RMSE(self.data[0], self.data[2])
            rmse_values_square.append(rmse)
            if not min_square or min_square > rmse:
                min_square = rmse
                min_sigma_square = s
            rmse = self.RMSE(self.data[0], self.data[3])
            rmse_values_circle.append(rmse)
            if not min_circle or min_circle > rmse:
                min_circle = rmse
                min_sigma_circle = s
        return (min_sigma_real, min_sigma_background, min_sigma_square, min_sigma_circle)




    
    #funcion obtenida de la ayudantia para un kernel gaussiano isotropico base normalizado
    #pero usando la formula simple vista en clases
    def gaussian_kernel(self, sigma):
        size = int(np.ceil(sigma * 2))* 2 + 1
        if size % 2 == 0:
            raise ValueError("El tamaño del kernel debe ser impar.")

        center = size // 2
        x, y = np.mgrid[-center:center+1, -center:center+1]

        self.kernel = np.exp(-(x**2 + y**2) / (2 * sigma**2))
        self.kernel /= self.kernel.sum()
        return self.kernel

    def apply_gaussian_filter(self, img, kernel):
        #libreria externa usada para las convoluciones
        return cv2.filter2D(img, -1, kernel)

if __name__ == "__main__":
    print("Escribe la seed para el ruido Poisson (entero (EJ: 3)):")
    seed = int(input())
    data = generate_img_p1(seed)
    img = data[4]
    print("Escribe el sigma a utilizar en la gaussiana (float con punto (EJ: 3.5))")
    print("se recomienda 1.6")
    sigma = float(input())
    g = Gaussian_adaptative_filter(img, sigma, data)
    print("[0] Global")
    print("[1] Local, usando bordes de global")
    if input("Seleccione el modo: ") == "1":
        g.adaptative_filter()
        print(g.RMSE(data[0]))
    else:
        g.filter()
        print(g.RMSE(data[0]))
    g.show(g.img)
    g.show(g.final_img)