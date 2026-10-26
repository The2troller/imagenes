import cv2
import matplotlib.pyplot as plt
import numpy as np
import time
import skimage as ski
from pregunta_1 import Notch_filter
from skimage import io
def normalize(image):
                        img_float = image.astype(float)
                        return (img_float - np.min(img_float)) / (np.max(img_float) - np.min(img_float) + 1e-8)



if __name__ == "__main__":
    select = input("pregunta numero: ")
    if select == "1":
        my_path = "img/P1.CR2"
        img = io.imread(my_path, as_gray = True)

        pos_notch = []
        for i in range(7):
        #pos de lo iluminado (141) y la separacion entre ellos (282)
            pos_notch.append(141 + 282 * i)




        print("0. Mostrar espectro imagen")
        print("1. Casos notch 1, 5, 15, 60 para Ideal y despues Gaussiano")
        print("2. Tamaños de padding nulo, (50,50) y (h/2, l/2)")

        s = input("Seleccione: ")
        if s == "0":
            n = Notch_filter(img, pos_notch)
            n.padding()
            n.show(n.f_show)
            #plt.imsave("img/transformada_base.jpg", n.f_show, cmap="gray")
            print(n.f_show.min(), n.f_show.max(), np.percentile(n.f_show, [1, 50, 99]))
        if s == "1":
            values = [1, 5, 15, 60]
            pos = [True, False]
            cand = ["perfecta", "gauss"]
            for i in range(2):
                for val in values:
                    n = Notch_filter(img, pos_notch, perfect = pos[i], d0 = val)
                    n.padding()
                    pre_f_show = n.f_show
                    n.filter_img()
                    n.show(n.final_img)
                    #plt.imsave(f"img/img_filtrada_{cand[i]}_{val}.jpg", n.final_img, cmap="gray")
                    n.show(pre_f_show)
                    n.show(n.f_show)
                    #plt.imsave(f"img/transformada_filtrada_{cand[i]}_{val}.jpg", n.f_show, cmap="gray")
                    res = np.abs(img.astype(float) - n.final_img.astype(float))
                    res = normalize(res)
                    plt.imshow(res, cmap = "gray", vmin = 0, vmax = 1)
                    plt.axis("off")
                    plt.show()
                    #plt.imsave(f"img/resta_img_og_y_{cand[i]}_{val}.jpg", res, cmap="gray")
        if s == "2":
            values = [(0,0), (50,50), None]
            pos = [True, False]
            cand = ["perfecta", "gauss"]
            for i in range(2):
                for val in values:
                    n = Notch_filter(img, pos_notch, perfect= pos[i], size = val)
                    n.filter_img()
                    zoomed = n.final_img[500:650, 500:650]
                    n.show(zoomed)
                    #plt.imsave(f"img/zoomed_img_filtrada_{cand[i]}_{val}.jpg", zoomed, cmap="gray")



                

            













    elif select == "2":
        pass