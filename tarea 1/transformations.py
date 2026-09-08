import numpy as np

def rgb_to_hsi(img):
    pre_r = img[:, :, 2]
    pre_g = img[:, :, 1]
    pre_b = img[:, :, 0]
    r = pre_r / 255.0
    g = pre_g / 255.0
    b = pre_b / 255.0
    #hsi
    angle = np.where((r - g) ** 2 + (r - b) * (g - b) != 0, 
                    np.degrees(np.arccos(
                    (0.5 * ((r - g) + (r - b))) /
                    ((r - g) ** 2 + (r - b) * (g - b)) ** 0.5
                )), 0)
    h = np.where(b <= g, angle, 360.0 - angle)
    s = np.where(r + g + b != 0,
                1 - (3 / (r + g + b)) * np.minimum(np.minimum(r, g), b),
                0)
    i = (1 / 3) * (r + g + b)

    hsi_img = np.dstack((h, s, i))
    return hsi_img