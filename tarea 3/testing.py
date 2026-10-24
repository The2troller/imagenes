import cv2
import matplotlib.pyplot as plt
import numpy as np
import time
import skimage as ski
from pregunta_1 import Notch_filter
from skimage import io



if __name__ == "__main__":
    select = input("pregunta numero: ")
    if select == "1":
        my_path = "img/P1.CR2"
        img = io.imread(my_path, as_gray = True)

        pos_notch = []
        for i in range(7):
        #pos de lo iluminado (141) y la separacion entre ellos (282)
            pos_notch.append(141 + 282 * i)



        n = Notch_filter(img, pos_notch)

        print("0. Mostrar espectro imagen")


        s = input("Seleccione: ")
        if s == "0":
            n.padding()
            n.show(n.f_show)
            #plt.imsave("img/transformada_base.jpg", n.f_show, cmap="gray")
            













    elif select == "2":
        pass