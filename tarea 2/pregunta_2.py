import numpy as np
import cv2
from tkinter import filedialog
import matplotlib.pyplot as plt # uso de plt debido a incompatibilidades con ubuntu 


class P2():
    def show(self) -> None:
        plt.imshow(self.final_img)
        plt.axis("off")
        plt.show()

if __name__ == "__main__":
    my_path = filedialog.askopenfilename()
    img = cv2.imread(my_path) #saves in bgr