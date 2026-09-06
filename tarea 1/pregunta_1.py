import numpy as np

class ColorSaturation():
    def __init__(self, img, pts, mode):
        self.img = img # (...)
        self.hue = pts [0] # tupla x
        self.mul = pts [1] # tupla y
        self.mode = mode # False = HS(...) True = CIE L*c*h








if __name__ == "__main__":
    colorsaturation = ColorSaturation()
