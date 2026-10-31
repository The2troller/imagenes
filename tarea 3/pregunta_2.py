import cv2
import matplotlib.pyplot as plt # uso de plt debido a incompatibilidades con ubuntu 
import numpy as np
from scipy import fft as sfft


fft2 = lambda x: sfft.fft2(x, workers=-1)
ifft2 = lambda X: sfft.ifft2(X, workers=-1)


class Filters():
    def __init__(self, img, psf, seed = 1234):
        self.img = self.normalize(img)
        self.bad_img = None
        self.psf = self.normalize_psf(psf)
        self.seed = seed
        self.h = None
        self.final_img = None

    def wiener(self, K):
        Y = fft2(self.bad_img)
        W = np.conj(self.h) / (np.abs(self.h)**2 + K)
        
        final_img = np.real(ifft2(Y * W))
        self.final_img = np.clip(final_img, 0, 1)

    def tikhonov(self, lam, tau, max_iter=100, tol=1e-4):
        x = self.bad_img.copy() 
        y = self.bad_img
        
        costos = []
        rmses = []
        
        for k in range(max_iter):
            Hx = np.real(ifft2(fft2(x) * self.h))
            diff = Hx - y
            Ht_diff = np.real(ifft2(fft2(diff) * np.conj(self.h)))
            grad = Ht_diff + lam * x
            x_next = x - tau * grad
            costo = 0.5 * np.sum(diff**2) + 0.5 * lam * np.sum(x**2)
            rmse = np.sqrt(np.mean((x_next - self.img)**2)) 
            
            costos.append(costo)
            rmses.append(rmse)
            
            cambio = np.linalg.norm(x_next - x) / (np.linalg.norm(x) + 1e-8)
            if cambio < tol:
                print(f"Tikhonov convergió en la iteración {k}")
                x = x_next
                break
            x = x_next            
        x = np.clip(x, 0, 1)
        return x, costos, rmses

    ###################### ARRUINAR IMAGEN ######################################
    def normalize(self, img):
        img_float = img.astype(float)
        return (img_float - np.min(img_float)) / (np.max(img_float) - np.min(img_float) + 1e-8)

    def normalize_psf(self, img):
        float_img = img.astype(float)
        suma = np.sum(float_img)
        if suma > 0:
            return float_img / suma
        return float_img

    def noise(self):
        self.bad_img = self.conv()
        self.bad_img = self.generate_gauss_noise()
        self.bad_img = np.clip(self.bad_img, 0, 1)

    def generate_psf(self):
        shape = self.img.shape
        kh, kw = self.psf.shape
        hp = np.zeros(shape)
        hp[:kh, :kw] = self.psf
        self.h = fft2(np.roll(hp, (-(kh // 2), -(kw // 2)), axis=(0, 1)))

    def conv(self):
        if self.h is None:
            self.generate_psf()
        img_borrosa = np.real(ifft2(fft2(self.img) * self.h))
        return img_borrosa

    #de T2
    def generate_gauss_noise(self):
        np.random.seed(self.seed)
        ruido = np.random.normal(0, 0.05, self.img.shape)
        imagen_ruidosa = self.bad_img + ruido
        return imagen_ruidosa

    def show(self, img) -> None:
        plt.imshow(img, cmap="gray", vmin=0, vmax=1)
        plt.axis("off")
        plt.show()


if __name__ == "__main__":
    cameraman = cv2.imread("img/cameraman.jpg", cv2.IMREAD_GRAYSCALE)
    psf = cv2.imread("img/psf.png", cv2.IMREAD_GRAYSCALE)
    filter = Filters(cameraman, psf)
    filter.noise()
    filter.show(filter.img)
    filter.show(filter.bad_img)
    filter.wiener(0.01)
    filter.show(filter.final_img)
    filter.tikhonov(0.01, 1.0, 200)
    filter.show(filter.final_img)