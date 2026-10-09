from pregunta_1 import Gaussian_adaptative_filter
from generador_imagenes import generate_img_p1, generate_gauss_noise, show
import cv2
import matplotlib.pyplot as plt
import numpy as np
import time
import skimage as ski
from pregunta_2 import P2




if __name__ == "__main__":
    select = input("pregunta numero: ")
    if select == "1":
        data = generate_img_p1(8)
        base_img = data[0]
        img = data[4]
        g = Gaussian_adaptative_filter(img, 1.6, data)
        print("[0] Prueba de sigmas entre 0.1 y 5.5")
        print("[1] Filtrado mejor adaptativo vs mejor global")
        print("[2] Prueba de valores relacionados a 3 pixeles, uno en cada mascara")
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
            print("mejor global vs mejor adaptativo")
            g.filter()
            g.show(g.final_img)
            print(g.RMSE(g.img))
            g.adaptative_filter()
            g.show(g.final_img)
            g.show(g.sigma_map)
            print(g.RMSE(g.img))
        if sel == "2":
            filtered_img = g.adaptative_filter()
            print(f"Fondo (y=30, x=30): mu_sombrero = {filtered_img[30, 30]}, sigma asignado = {g.sigma_map[30, 30]}")
            print(f"Cuadrado (y=80, x=80): mu_sombrero = {filtered_img[80, 80]}, sigma asignado = {g.sigma_map[80, 80]}")
            print(f"Círculo (y=128, x=128): mu_sombrero = {filtered_img[128, 128]}, sigma asignado = {g.sigma_map[128, 128]}")
        
        

    elif select == "2":
        camera = ski.data.camera()
        #plt.imsave("img/original.jpg", camera)
        camera_n = camera.astype(np.float32) / 255.0
        new_camera = generate_gauss_noise(camera_n, 676767)
        #plt.imsave("img/noised.jpg", camera)
        p2 = P2(new_camera)
        print("[0] Prueba c_map para valores epsilon")
        print("[1] Prueba de efecto de variables")
        print("[2] Comparacion entre los 3")
        sel = input("Prueba seleccionada: ")
        if sel == "0":
            print("[0] TV")
            print("[1] Laplace")
            print("[2] Gauss Laplace")
            x = input("Seleccione: ")
            p2.difusion_anisotropica(x, 50, 0.1, (10)**(-3.5))
            p2.show(p2.c_map)
            p2.show(p2.final_img)
            #plt.imsave(f"img/{x}_map_10em3_5.jpg", p2.c_map)
            p2.difusion_anisotropica(x, 50, 0.1, 1e-3)
            p2.show(p2.c_map)
            p2.show(p2.final_img)
            #plt.imsave(f"img/{x}_map_10em3.jpg", p2.c_map)
            p2.difusion_anisotropica(x, 50, 0.1, (10)**(-2.5))
            p2.show(p2.c_map)
            p2.show(p2.final_img)
            #plt.imsave(f"img/{x}_map_10em2_5.jpg", p2.c_map)
            p2.difusion_anisotropica(x, 50, 0.1, (10)**(-1))
            p2.show(p2.c_map)
            p2.show(p2.final_img)
            #plt.imsave(f"img/{x}_map_0_25.jpg", p2.c_map)

        elif sel == "1": 
            print("[0] TV")
            print("[1] Laplace")
            print("[2] Gauss Laplace")
            x = input("Seleccione: ")
            
            #base
            p2.difusion_anisotropica(x, 50, 0.1, 10e-3)
            p2.show(p2.final_img)
            #plt.imsave(f"img/{x}_50_01_10e3.jpg", p2.final_img)
            
            #menos iter
            p2.difusion_anisotropica(x, 5, 0.1, 10e-3)
            p2.show(p2.final_img)
            #plt.imsave(f"img/{x}_5_01_10e3.jpg", p2.final_img)

            #mas iter
            p2.difusion_anisotropica(x, 100, 0.1, 10e-3)
            p2.show(p2.final_img)
            #plt.imsave(f"img/{x}_100_01_10e3.jpg", p2.final_img)

            #mas epsilon
            p2.difusion_anisotropica(x, 50, 0.1, 10e-2)
            p2.show(p2.final_img)
            #plt.imsave(f"img/{x}_50_01_10e2.jpg", p2.final_img)

            #menos epsilon
            p2.difusion_anisotropica(x, 50, 0.1, 10**(-3.5))
            p2.show(p2.final_img)
            #plt.imsave(f"img/{x}_50_01_10e3_5.jpg", p2.final_img)

            #mas lambda
            p2.difusion_anisotropica(x, 50, 0.25, 10e-3)
            p2.show(p2.final_img)
            #plt.imsave(f"img/{x}_50_025_10e3.jpg", p2.final_img)

            #menos lambda
            p2.difusion_anisotropica(x, 50, 0.01, 10e-3)
            p2.show(p2.final_img)
            #plt.imsave(f"img/{x}_50_001_10e3.jpg", p2.final_img)

            #para ver este descomentar proteccion
            p2.difusion_anisotropica(x, 50, 0.35, 10e-3) 
            p2.show(p2.final_img)
            #plt.imsave(f"img/{x}_50_035_10e3.jpg", p2.final_img)
        elif sel == "2":
            p2.difusion_anisotropica("0", 50, 0.1, 10e-3) 
            p2.show(p2.final_img)
            #plt.imsave(f"img/0_god.jpg", p2.final_img)

            p2.difusion_anisotropica("1", 50, 0.1, 0.1) 
            p2.show(p2.final_img)
            #plt.imsave(f"img/1_god.jpg", p2.final_img)

            p2.difusion_anisotropica("2", 50, 0.1, 0.05) 
            p2.show(p2.final_img)
            #plt.imsave(f"img/2_god.jpg", p2.final_img)
        else:
            p2.difusion_anisotropica("0", 50, 0.1, 1e-3)
            p2.show()
            p2.difusion_anisotropica("1", 50, 0.1, 1e-3)
            p2.show()
            p2.difusion_anisotropica("2", 50, 0.1, 1e-3)
            p2.show()
        
        