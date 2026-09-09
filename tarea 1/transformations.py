import numpy as np


def bgr_to_rgb(img: np.ndarray) -> np.ndarray:
    b = img[:, :, 0]
    g = img[:, :, 1]
    r = img[:, :, 2]
    return np.dstack((r, g, b))



#codigo de la guia

def rgb_to_lch(img: np.ndarray) -> np.ndarray:

    lab = rgb_to_lab(img)

    L = lab[:, :, 0]
    a = lab[:, :, 1]
    b = lab[:, :, 2]

    C = np.sqrt(a ** 2 + b ** 2)
    h = np.degrees(np.arctan2(b, a))
    h = np.where(h < 0, h + 360.0, h)

    lch_img = np.stack([L, C, h], axis=-1)
    return lch_img

def rgb_to_lab(img: np.ndarray) -> np.ndarray:

  #Los parámetros X_n, Y_n, Z_n pueden variar
  _X_n = 1.0
  _Y_n = 1.0
  _Z_n = 1.0

  xyz = rgb_to_xyz(img)

  xr = xyz[:, :, 0] / _X_n
  yr = xyz[:, :, 1] / _Y_n
  zr = xyz[:, :, 2] / _Z_n

  delta = 6.0 / 29.0

  def f(t):
    return np.where(t > delta ** 3, np.cbrt(t), t / (3 * delta ** 2) + 4.0 / 29.0)

  fx, fy, fz = f(xr), f(yr), f(zr)

  L = 116.0 * fy - 16.0
  a = 500.0 * (fx - fy)
  b = 200.0 * (fy - fz)

  lab_img = np.stack([L, a, b], axis=-1)
  return lab_img

def _gamma_to_linear(c: np.ndarray, gamma: float = 2.2) -> np.ndarray:
  return c ** gamma

def rgb_to_xyz(img: np.ndarray) -> np.ndarray:

  img = img.astype(np.float64)
  img = img / 255.0

  # Matriz CIE RGB -> XYZ. Sus filas son las ecuaciones de X, Y, Z
  # en función de (R, G, B), por lo que hay que aplicarla como
  # matrix @ [R, G, B] por píxel (de ahí el matrix.T al multiplicar
  # por la imagen vista como vectores fila).
  matrix = np.array([
      [0.490, 0.310, 0.200],
      [0.177, 0.813, 0.011],
      [.000, .010, 0.990],
  ])

  rgb_linear = _gamma_to_linear(img)

  xyz = rgb_linear @ matrix.T

  return xyz


def rgb_to_hsi(img: np.ndarray) -> np.ndarray:

  # Normalizamos para evitar overflow y separamos por canal
  img = img.astype(np.float64)
  img = img / 255

  R = img[:,:, 0]
  G = img[:,:, 1]
  B = img[:,:, 2]

  # Calculamos intensidad

  I = (R + G + B) / 3.0

  # Calculamos saturación, para evitar divisiones por 0, producto
  # de que todos los canales fuesen 0 (img completamente negra) se define un
  # epsilon auxiliar

  epsilon = 1e-10

  min_rgb = np.minimum(np.minimum(R, G), B)
  max_rgb = np.maximum(np.maximum(R, G), B)
  delta = max_rgb - min_rgb
  S = 1.0 -(3.0 / (R + G + B + epsilon)) * min_rgb

  # Para calcular el tono primero se define theta

  num_theta = 0.5 * ((R - G) + (R - B))
  den_theta = np.sqrt((R -G) ** 2 + (R - B) * (G - B)) + epsilon
  theta = np.arccos(np.clip(num_theta / den_theta, -1.0, 1.0))

  H = np.degrees(theta)
  H = np.where(B > G, 360.0 - H, H)

  #Para zonas grises
  H = np.where(delta < epsilon, 0.0, H)

  hsi_img = np.stack([H, S, I], axis=-1)
  return hsi_img


def lab_to_xyz(lab_img: np.ndarray) -> np.ndarray:

    _X_n = 1.0
    _Y_n= 1.0
    _Z_n = 1.0

    L = lab_img[:, :, 0]
    a = lab_img[:, :, 1]
    b = lab_img[:, :, 2]

    fy = (L + 16.0) / 116.0
    fx = fy + a / 500.0
    fz = fy - b / 200.0

    delta = 6.0 / 29.0

    def f_inv(f):
        return np.where(f > delta, f ** 3, 3 * delta ** 2 * (f - 4.0 / 29.0))

    X = f_inv(fx) * _X_n
    Y = f_inv(fy) * _Y_n
    Z = f_inv(fz) * _Z_n

    return np.stack([X, Y, Z], axis=-1)

def lab_to_rgb(lab_img: np.ndarray) -> np.ndarray:
    return xyz_to_rgb(lab_to_xyz(lab_img))

def xyz_to_rgb(xyz_img: np.ndarray) -> np.ndarray:

    matrix = np.array([
        [0.490, 0.310, 0.200],
        [0.177, 0.813, 0.011],
        [.000, .010, 0.990],
    ])

    inv = np.linalg.inv(matrix)

    rgb_linear = xyz_img @ inv.T
    rgb_linear = np.clip(rgb_linear, 0.0, 1.0)

    #Aplicar corrección gamma
    rgb = rgb_linear ** (1.0 / 2.2)

def xyz_to_rgb(xyz_img: np.ndarray) -> np.ndarray:

    matrix = np.array([
        [0.490, 0.310, 0.200],
        [0.177, 0.813, 0.011],
        [.000, .010, 0.990],
    ])

    inv = np.linalg.inv(matrix)

    rgb_linear = xyz_img @ inv.T
    rgb_linear = np.clip(rgb_linear, 0.0, 1.0)

    #Aplicar corrección gamma
    rgb = rgb_linear ** (1.0 / 2.2)

    return np.clip(rgb, 0.0, 1.0)

def lab_to_xyz(lab_img: np.ndarray) -> np.ndarray:

    _X_n = 1.0
    _Y_n= 1.0
    _Z_n = 1.0

    L = lab_img[:, :, 0]
    a = lab_img[:, :, 1]
    b = lab_img[:, :, 2]

    fy = (L + 16.0) / 116.0
    fx = fy + a / 500.0
    fz = fy - b / 200.0

    delta = 6.0 / 29.0

    def f_inv(f):
        return np.where(f > delta, f ** 3, 3 * delta ** 2 * (f - 4.0 / 29.0))

    X = f_inv(fx) * _X_n
    Y = f_inv(fy) * _Y_n
    Z = f_inv(fz) * _Z_n

    return np.stack([X, Y, Z], axis=-1)

def lab_to_rgb(lab_img: np.ndarray) -> np.ndarray:
  return xyz_to_rgb(lab_to_xyz(lab_img))


def lch_to_lab(lch_img: np.ndarray) -> np.ndarray:
  """Inversa de rgb_to_lch: vuelve de coordenadas polares (C, h)
  a cartesianas (a, b)."""

  L = lch_img[:, :, 0]
  C = lch_img[:, :, 1]
  h = np.radians(lch_img[:, :, 2])

  a = C * np.cos(h)
  b = C * np.sin(h)

  return np.stack([L, a, b], axis=-1)


def lch_to_rgb(lch_img: np.ndarray) -> np.ndarray:
  return lab_to_rgb(lch_to_lab(lch_img))


def hsi_to_rgb(hsi_img: np.ndarray) -> np.ndarray:

  H = hsi_img[:, :, 0] % 360.0
  S = np.clip(hsi_img[:, :, 1], 0.0, 1.0)
  I = np.clip(hsi_img[:, :, 2], 0.0, 1.0)

  epsilon = 1e-10
  Hr = np.radians(H)

  R = np.zeros_like(I)
  G = np.zeros_like(I)
  B = np.zeros_like(I)

  # Sector RG: 0 <= H < 120
  m = (H >= 0) & (H < 120)
  B[m] = I[m] * (1 - S[m])
  R[m] = I[m] * (1 + (S[m] * np.cos(Hr[m])) / (np.cos(np.radians(60) - Hr[m]) + epsilon))
  G[m] = 3 * I[m] - (R[m] + B[m])

  # Sector GB: 120 <= H < 240
  m = (H >= 120) & (H < 240)
  Hp = Hr[m] - np.radians(120)
  R[m] = I[m] * (1 - S[m])
  G[m] = I[m] * (1 + (S[m] * np.cos(Hp)) / (np.cos(np.radians(60) - Hp) + epsilon))
  B[m] = 3 * I[m] - (R[m] + G[m])

  # Sector BR: 240 <= H <= 360
  m = (H >= 240) & (H <= 360)
  Hp = Hr[m] - np.radians(240)
  G[m] = I[m] * (1 - S[m])
  B[m] = I[m] * (1 + (S[m] * np.cos(Hp)) / (np.cos(np.radians(60) - Hp) + epsilon))
  R[m] = 3 * I[m] - (G[m] + B[m])

  rgb_img = np.clip(np.stack([R, G, B], axis=-1), 0.0, 1.0)
  return rgb_img