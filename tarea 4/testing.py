import numpy as np
import skimage as ski
from tkinter import filedialog
import matplotlib.pyplot as plt # uso de plt debido a incompatibilidades con ubuntu 

from pregunta_1 import P1



if __name__ == "__main__":
    select = input("pregunta numero: ")
    if select == "1":
        img = ski.io.imread("archivos_t4/memorial.tif")
        p1 = P1(img)
        print("0. Capas de detalle y el residual grueso de ambas representaciones")
        print("1. Mostrar RMSE laplace")
        print("2. Mostrar RMSE starlet")
        print("3. Aplicar umbral alpha = 0.3 y 0.8")
        print("4. Multiplicador fino / grueso")
        s = input("Selecciona: ")
        p1.starlet()
        p1.piramide_laplaciana()
        if s == "0":
            p1.show_capas()
        elif s == "1":
            p1.reconst_laplaciana()
            print(p1.RMSE())
        elif s == "2":
            p1.reconst_starlet()
            print(p1.RMSE())
        elif s == "3":
            p1.umbral(0.3)
            p1.show_capas()
            p1.reconst_laplaciana()
            p1.show()
            p1.reconst_starlet()
            p1.show()
            #reset
            p1.starlet()
            p1.piramide_laplaciana()
            p1.umbral(0.8)
            p1.show_capas()
            p1.reconst_laplaciana()
            p1.show()
            p1.reconst_starlet()
            p1.show()
        elif s == "4":
            mults_grueso = [0.7, 0.9, 1.3, 1.8, 2.5]
            mults_fino = [2.5, 1.8, 1.2, 0.9, 0.8]
            p1.mult(mults_fino)
            p1.reconst_starlet()
            p1.show()
            p1.save_cut("fino", "starlet")
            p1.reconst_laplaciana()
            p1.show()
            p1.save_cut("fino", "laplaciano")
            p1.show_capas()
            #####
            p1.starlet()
            p1.piramide_laplaciana()
            p1.mult(mults_grueso)
            p1.reconst_starlet()
            p1.show()
            p1.save_cut("grueso", "starlet")
            p1.reconst_laplaciana()
            p1.show()
            p1.save_cut("grueso", "laplaciano")
            p1.show_capas()