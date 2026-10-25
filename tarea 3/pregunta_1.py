from skimage import io
import matplotlib.pyplot as plt # uso de plt debido a incompatibilidades con ubuntu 
import numpy as np 

class Notch_filter:
    def __init__(self, img, pos_notch, size = None, pad_mode = "symmetric", perfect = True, d0 = 15):
        self.img = img
        self.final_img = img
        if size == None:
            rows, cols = img.shape
            self.size_r = rows // 2
            self.size_c = cols // 2
        else:
            self.size_r, self.size_c = size
        self.perfect = perfect
        self.pad_mode = pad_mode
        self.d0 = d0
        self.pos_notch = pos_notch
        self.img_pad = None
        self.pad_cols = None
        self.pad_rows = None

    def filter_img(self):
        self.padding()
        mask = 1
        center = self.pad_cols // 2
        for pos in self.pos_notch:
            if self.perfect:
                m = self.create_notch_ideal(0, center - pos, self.d0)
            else:
                m = self.create_notch_gaussian(0, center - pos, self.d0)
            mask *= m
        self.apply_filter(mask)
        self.transform(self.final_img)

    def padding(self):   
        self.img_pad = np.pad(self.img,
                            ((self.size_r, self.size_r), (self.size_c, self.size_c)), 
                            mode=self.pad_mode)
        self.pad_rows, self.pad_cols = self.img_pad.shape
        self.transform(self.img_pad)
        crow, ccol = self.pad_rows // 2, self.pad_cols // 2
        self.y, self.x = np.ogrid[-crow:self.pad_rows-crow, -ccol:self.pad_cols-ccol]

    def apply_filter(self, mask):
        f_filtered = self.f_shift * mask
        f_ishift = np.fft.ifftshift(f_filtered)
    
        img_back = np.fft.ifft2(f_ishift)
        img_back = np.real(img_back)
        
        rows, cols = self.img.shape
        self.final_img = img_back[self.size_r : self.size_r + rows, 
                                  self.size_c : self.size_c + cols]



    def transform(self, img):
        f_transform = np.fft.fft2(img)
        self.f_shift = np.fft.fftshift(f_transform)
        self.f_show = np.log10(np.abs(self.f_shift) + 1e-20)


    def create_notch_ideal(self, u0, v0, d0):
        d1 = np.sqrt((self.x - v0)**2 + (self.y - u0)**2)
        d2 = np.sqrt((self.x + v0)**2 + (self.y + u0)**2)
        mask = np.ones((self.pad_rows, self.pad_cols))
        mask[(d1 <= d0) | (d2 <= d0)] = 0
        return mask
    
    def create_notch_gaussian(self, u0, v0, d0):
        d1_sq = (self.x - v0)**2 + (self.y - u0)**2
        d2_sq = (self.x + v0)**2 + (self.y + u0)**2

        h1 = 1.0 - np.exp(-d1_sq / (2 * d0**2))
        h2 = 1.0 - np.exp(-d2_sq / (2 * d0**2))
        return h1 * h2


    def show(self, img) -> None:
        plt.imshow(img, cmap = "gray")
        plt.axis("off")
        plt.show()



if __name__ == "__main__":
    my_path = "img/P1.CR2"
    img = io.imread(my_path, as_gray = True)
    #plt.imsave("img/img_original_para_comparar.jpg", img, cmap="gray")
    print("0. Ideal")
    print("1. Gaussiano")
    if input("Seleccione el tipo de notch reject: ") == "0":
        perfect = True
    else:
        perfect = False
    print("Dejar vacio para tamaño estandar")
    s = input("Seleccione el tamaño del padding (EJ: 5,5 o 8,19): ").split(",")
    print(s)
    if s == [""]:
        size = None
    else:
        size = [int(a) for a in s]
    print("0. constant")
    print("1. edge")
    print("2. linear_ramp")
    print("3. maximum")
    print("4. mean")
    print("5. median")
    print("6. minimum")
    print("7. reflect")
    print("8. symmetric")
    print("9. wrap")
    pad_modes = ["constant", "edge", "linear_ramp", "maximum",
                "mean", "median", "minimum", "reflect", "symmetric", "wrap"]
    pad_mode = pad_modes[int(input("Seleccione el tipo de padding: "))]

    if perfect:
        d0 = int(input("Ancho del radio ideal: "))
    else:
        d0 = int(input("Escala de la campana gaussiana: "))

    #basados en la imagen
    pos_notch = []
    for i in range(7):
    #pos de lo iluminado (141) y la separacion entre ellos (282)
        pos_notch.append(141 + 282 * i)
    notch = Notch_filter(img, pos_notch, size, pad_mode, perfect, d0)
    notch.filter_img()
    notch.show(notch.final_img)
    #zoomed = notch.final_img[500:650, 500:650]
    
    #plt.imsave("img/img_filtrada_perfect_NOSIMETRICA.jpg", zoomed, cmap="gray")
    #plt.imsave("img/transformada_filtrada_gauss_const.jpg", notch.f_show, cmap="gray")
        