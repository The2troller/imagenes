import numpy as np

def rgb_to_hsi(img):
    rgb_img = normalize_rgb(img)
    r = rgb_img[:, :, 0]
    g = rgb_img[:, :, 1]
    b = rgb_img[:, :, 2]
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
     
def rgb_to_xyz(img, custom_matrix):
    rgb = normalize_rgb(img)
    #xyz
    matrix = np.array([
        [0.490, 0.310, 0.200],
        [0.177, 0.813, 0.011],
        [0.000, 0.010, 0.990]
    ]).T
    if custom_matrix is not None:
        matrix = custom_matrix
    return np.dot(rgb, matrix)

def xyz_to_lab(img, x_n = 1.0, y_n = 1.0, z_n = 1.0, delta = 6/29):
    def f(t):
        result = np.where(
            t > (delta**3),
            t**(1/3),
            (t / (3.0 * (delta ** 2))) + (4 / 29)
        )
        return result
    x = img[:, :, 0]
    y = img[:, :, 1]
    z = img[:, :, 2]

    f_x = f(x/ x_n)
    f_y = f(y/ y_n)
    f_z = f(z/ z_n)
    l = 116 * f_y - 16
    a = 500 * (f_x - f_y)
    b = 200 * (f_y - f_z)
    lab_img = np.dstack((l, a, b))
    return lab_img

def rgb_to_lab(img, custom_matrix = None, x_n = 1.0, y_n = 1.0, z_n = 1.0, delta = 6/29):
    xyz_img = rgb_to_xyz(img, custom_matrix)
    lab_img = xyz_to_lab(xyz_img, x_n, y_n, z_n, delta)
    return lab_img

def xyz_to_lch(img, x_n = 1.0, y_n = 1.0, z_n = 1.0, delta = 6/29):
    lab_img = xyz_to_lab(img,x_n, y_n, z_n, delta)
    lch_img = lab_to_lch(lab_img)
    return lch_img

def lab_to_lch(img):
    l = img[:, :, 0]
    a = img[:, :, 1]
    b = img[:, :, 2]

    c = (a ** 2 + b ** 2) ** 0.5
    h = np.arctan2( b / a)

    lch_img = np.dstack((l, c, h))
    return lch_img

def rgb_to_lch(img, custom_matrix = None, x_n = 1.0, y_n = 1.0, z_n = 1.0, delta = 6/29):
    xyz_img = rgb_to_xyz(img, custom_matrix)
    lch_img = xyz_to_lch(xyz_img, x_n, y_n, z_n, delta)
    return lch_img

def normalize_rgb(img):
    pre_r = img[:, :, 2]
    pre_g = img[:, :, 1]
    pre_b = img[:, :, 0]
    r = pre_r / 255.0
    g = pre_g / 255.0
    b = pre_b / 255.0
    rgb_img = np.dstack((r, g, b))
    return rgb_img