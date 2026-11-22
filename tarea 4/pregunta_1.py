import numpy as np
import skimage as ski
from tkinter import filedialog
import matplotlib.pyplot as plt # uso de plt debido a incompatibilidades con ubuntu 



class P1():
    def __init__(self, img):
        self.img = img[:, :, :3]
        self.normalizar_l()

    def normalizar_l(self):
        self.l = self.luminancia(self.img)
        self.l_norm = self.a_pantalla(self.reescalar(self.l))

    def piramide_laplaciana(self):
        self.piramide = list()
        img_aprox_nxt_lvl = ski.filters.gaussian(self.l_norm, sigma = 1.0, preserve_range = True)
        img_aprox_nxt_lvl = ski.transform.resize(img_aprox_nxt_lvl, [x // 2 for x in self.l_norm.shape], order = 1)
        capa_de_detalle = self.l_norm - ski.transform.resize(img_aprox_nxt_lvl, self.l_norm.shape, order = 1)
        self.piramide.append(capa_de_detalle)
        img_aprox_nxt_lvl_og = img_aprox_nxt_lvl
        for i in range(4):
            img_aprox_nxt_lvl = ski.filters.gaussian(img_aprox_nxt_lvl_og, sigma = 1.0, preserve_range = True)
            img_aprox_nxt_lvl = ski.transform.resize(img_aprox_nxt_lvl, [x // 2 for x in img_aprox_nxt_lvl_og.shape], order = 1)
            capa_de_detalle = img_aprox_nxt_lvl_og - ski.transform.resize(img_aprox_nxt_lvl, img_aprox_nxt_lvl_og.shape, order = 1)
            self.piramide.append(capa_de_detalle)
            img_aprox_nxt_lvl_og = img_aprox_nxt_lvl
        last_level = img_aprox_nxt_lvl_og
        self.piramide.append(last_level)
        #recontruccion

        for c in reversed(self.piramide):
            expanded_last = ski.transform.resize(last_level, c.shape, order = 1)
            last_level = c + expanded_last
        self.l_out = last_level

    def scarlet(self):
        pass
        
    def show(self) -> None:
        rgb_l = self.recolorear(self.img, self.l, self.l_out)
        plt.imshow(rgb_l)
        plt.axis("off")
        plt.show()


    #Ayudantia
    def luminancia(self, E):
        # Fila Y de la matriz RGB -> XYZ usada en la cápsula de espacios de color
        return 0.177 * E[..., 0] + 0.813 * E[..., 1] + 0.011 * E[..., 2]

    def a_pantalla(self, x, gamma=2.2):
        # Corrección gamma para desplegar una imagen lineal en [0, 1]
        return np.clip(x, 0.0, 1.0) ** (1.0 / gamma)


    def recolorear(self, E, L_in, L_out, s=0.6):
        # C_out = (C_in / L_in)^s · L_out, para cada canal C = R, G, B
        return np.clip((E / (L_in[..., None] + 1e-12)) ** s * L_out[..., None], 0.0, 1.0)


    def reescalar(self, g, p_bajo=0.5, p_alto=99.5):
        # Lleva los percentiles p_bajo y p_alto a 0 y 1, recortando los extremos
        lo, hi = np.percentile(g, [p_bajo, p_alto])
        return np.clip((g - lo) / (hi - lo), 0.0, 1.0)


    
if __name__ == "__main__":
    img = ski.io.imread("archivos_t4/memorial.tif")
    p1 = P1(img)
    p1.piramide_laplaciana()
    p1.show()
