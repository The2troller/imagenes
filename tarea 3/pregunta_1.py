from skimage import io
import matplotlib.pyplot as plt # uso de plt debido a incompatibilidades con ubuntu 
import numpy as np 

class Notch_filter:
    def __init__(self, img, size = None, pad_mode = "constant", perfect = True, d0 = 15, pos_notch = None):
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
        if pos_notch == None:
            self.pos_notch = []
            for i in range(7):
                self.pos_notch.append(141 + 282 * i)
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


    def show(self) -> None:
        plt.imshow(self.final_img, cmap = "gray")
        plt.axis("off")
        plt.show()
        plt.imshow(self.f_show, cmap = "gray")
        plt.show()



if __name__ == "__main__":
    my_path = "img/P1.CR2"
    img = io.imread(my_path, as_gray = True)
    #plt.imsave("img/img_original_para_comparar.jpg", img, cmap="gray")
    notch = Notch_filter(img, perfect=False)
    notch.filter_img()
    notch.show()
    #plt.imsave("img/img_filtrada_gauss_const.jpg", notch.final_img, cmap="gray")
    #plt.imsave("img/transformada_filtrada_gauss_const.jpg", notch.f_show, cmap="gray")
        