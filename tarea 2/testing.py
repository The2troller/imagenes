from pregunta_1 import Gaussian_adaptative_filter
from generador_imagenes import generate_img_p1
import cv2
import matplotlib.pyplot as plt

import time

if __name__ == "__main__":
    data = generate_img_p1(676767)
    base_img = data[0]
    img = data[4]
    g = Gaussian_adaptative_filter(img, 1, data)
    select = input("pregunta numero: ")
    if select == "1":
        print("[0] Prueba de sigmas entre 0.1 y 5.5")
        print("[1] Filtrado usando funcion de sigma")
        sel = input("Prueba seleccionada: ")
        if sel == "0":
            s_values = [x / 10 for x in range(0, 56)][1:]
            rmse_values_real = []
            rmse_values_background = []
            rmse_values_square = []
            rmse_values_circle = []
            background_img = img * data[1]
            square_img = img * data[2]
            circle_img = img * data[3]
            min_real = None
            min_background = None
            min_square = None
            min_circle = None
            for s in s_values: #presionar ctrl + c en consola para salir
                g.sigma = s
                g.filter()
                rmse = g.RMSE(base_img)
                rmse_values_real.append(rmse)
                if not min_real or min_real > rmse:
                    min_real = rmse
                    min_sigma_real = s
                rmse = g.RMSE(base_img, data[1])
                rmse_values_background.append(rmse)
                if not min_background or min_background > rmse:
                    min_background = rmse
                    min_sigma_background = s
                rmse = g.RMSE(base_img, data[2])
                rmse_values_square.append(rmse)
                if not min_square or min_square > rmse:
                    min_square = rmse
                    min_sigma_square = s
                rmse = g.RMSE(base_img, data[3])
                rmse_values_circle.append(rmse)
                if not min_circle or min_circle > rmse:
                    min_circle = rmse
                    min_sigma_circle = s
                #print(f"SIGMA: {s} RMSE de {rmse}")
                #g.show(g.final_img)
            print(f"min global en {min_sigma_real} con {min_real}")
            print(f"min fondo en {min_sigma_background} con {min_background}")
            print(f"min cuadrado en {min_sigma_square} con {min_square}")
            print(f"min circulo en {min_sigma_circle} con {min_circle}")
            
            plt.plot(s_values, rmse_values_real)
            plt.title("real")
            plt.show()
            plt.plot(s_values, rmse_values_background)
            plt.title("background")
            plt.show()
            plt.plot(s_values, rmse_values_square)
            plt.title("square")
            plt.show()
            plt.plot(s_values, rmse_values_circle)
            plt.title("circle")
            plt.show()
        if sel == "1":
            g.adaptative_filter()
            g.show(g.final_img)
                
        
        

    elif select == "2":
        pass