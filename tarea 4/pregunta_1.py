import numpy as np
import skimage as ski
from tkinter import filedialog
import matplotlib.pyplot as plt # uso de plt debido a incompatibilidades con ubuntu 
from scipy.ndimage import convolve1d



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

    def reconst_laplaciana(self):
        last_level = self.piramide[-1]
        for c in reversed(self.piramide[:-1]):
            expanded_last = ski.transform.resize(last_level, c.shape, order = 1)
            last_level = c + expanded_last
        self.l_out = last_level

    def starlet(self):
        self.piramide_starlet = list()
        h_base = np.array([1, 4, 6, 4, 1], dtype=np.float64) / 16.0

        img_aprox_nxt_lvl_0 = convolve1d(self.l_norm, h_base, 0)
        img_aprox_nxt_lvl = convolve1d(img_aprox_nxt_lvl_0, h_base, 1)
        capa_de_detalle = self.l_norm - img_aprox_nxt_lvl
        self.piramide_starlet.append(capa_de_detalle)
        img_aprox_nxt_lvl_og = img_aprox_nxt_lvl
        for i in range(4):
            paso = 2 ** (i + 1)
            h_i = np.zeros(4 * paso + 1, dtype=np.float64)
            h_i[0::paso] = h_base

            img_aprox_nxt_lvl_0 = convolve1d(img_aprox_nxt_lvl_og, h_i, 0)
            img_aprox_nxt_lvl = convolve1d(img_aprox_nxt_lvl_0, h_i, 1)
            capa_de_detalle = img_aprox_nxt_lvl_og - img_aprox_nxt_lvl
            self.piramide_starlet.append(capa_de_detalle)
            img_aprox_nxt_lvl_og = img_aprox_nxt_lvl
        last_level = img_aprox_nxt_lvl_og
        self.piramide_starlet.append(last_level)

    def reconst_starlet(self):
        self.l_out = np.sum(self.piramide_starlet, axis=0)

    def show(self) -> None:
        rgb_l = self.recolorear(self.img, self.l, self.l_out)
        plt.imshow(rgb_l)
        plt.axis("off")
        plt.show()

    def RMSE(self):
        return np.sqrt(np.mean((self.l_norm - self.l_out) ** 2))

    def umbral(self, a):
        for i in range(5):
            t_j_l = a * np.max(np.abs(self.piramide[i]))
            t_j_s = a * np.max(np.abs(self.piramide_starlet[i]))
            self.piramide[i] = np.where(np.abs(self.piramide[i]) >= t_j_l, self.piramide[i], 0.0)
            lp_safe = 100.0 * np.count_nonzero(self.piramide[i]) / self.piramide[i].size
            self.piramide_starlet[i] = np.where(np.abs(self.piramide_starlet[i]) >= t_j_s, self.piramide_starlet[i], 0.0)
            starlet_safe = 100.0 * np.count_nonzero(self.piramide_starlet[i]) / self.piramide_starlet[i].size
            print(f"Capa {i}, laplace: {lp_safe}, starlet: {starlet_safe}")
            
    def mult(self, mults):
        for i in range(5):
            self.piramide[i] = self.piramide[i] * mults[i]
            self.piramide_starlet[i] = self.piramide_starlet[i] * mults[i]

    def save_cut(self, mult, tipo):
        img = self.recolorear(self.img, self.l, self.l_out)
        y0 = 120
        y1 = 320
        x0 = 140
        x1 = 360
        img = img[y0:y1, x0:x1]
        plt.imsave(f"imgs/recorte_{mult}_{tipo}.png", img)
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

    #fusionada
    def show_capas(self):
        vmax = max(np.max(np.abs(d)) for d in self.piramide[:-1] + self.piramide_starlet[:-1])
        axes = plt.subplots(2, 6, figsize=(16, 6))[1]
        for j in range(5):
            axes[0, j].imshow(self.piramide[j], cmap="RdBu_r", vmin=-vmax, vmax=vmax)
            axes[0, j].set_title(f"Laplace piso: {j+1} {self.piramide[j].shape}", fontsize=8)
            axes[0, j].axis("off")
            axes[1, j].imshow(self.piramide_starlet[j], cmap="RdBu_r", vmin=-vmax, vmax=vmax)
            axes[1, j].set_title(f"Starlet piso: {j+1} {self.piramide_starlet[j].shape}", fontsize=8)
            axes[1, j].axis("off")
        axes[0, 5].imshow(self.piramide[-1], cmap="gray", vmin=0, vmax=1)
        axes[0, 5].set_title(f"Laplace aproximacion a sgnte nivel {self.piramide[-1].shape}", fontsize=8)
        axes[0, 5].axis("off")
        axes[1, 5].imshow(self.piramide_starlet[-1], cmap="gray", vmin=0, vmax=1)
        axes[1, 5].set_title(f"Starlet aproximacion a sgnte nivel {self.piramide_starlet[-1].shape}", fontsize=8)
        axes[1, 5].axis("off")
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    img = ski.io.imread("archivos_t4/memorial.tif")
    p1 = P1(img)
    p1.piramide_laplaciana()
    p1.reconst_laplaciana()
    print(p1.RMSE())
    p1.show()
    p1.starlet()
    p1.reconst_starlet()
    print(p1.RMSE())
    p1.show()
    p1.show_capas()