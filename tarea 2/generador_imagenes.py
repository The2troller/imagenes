import numpy as np
import matplotlib.pyplot as plt

def generate_synthetic_image():
    base_matrix = np.full((256, 256), 0.15)
    base_mask = np.full((256, 256), 1.0)
    base_matrix[64:193, 64:193] = 0.45
    base_square_mask = np.zeros((256, 256))
    base_circle_mask = base_square_mask.copy()
    base_square_mask[64:193, 64:193] = 1.0
    base_mask -= base_square_mask
    for y in range(-32, 33):
        for x in range(-32, 33):
            if (x)**2 + (y)**2 <= 32**2:
                base_matrix[128 + x, 128 + y] = 0.80
                base_circle_mask[128 + x, 128 + y] = 1.0
    base_square_mask -= base_circle_mask
    return [base_matrix, base_mask, base_square_mask, base_circle_mask]
    

def generate_poisson_noise(matrix, seed):
    np.random.seed(seed)
    noised_matrix = np.random.poisson(40 * matrix) / 40
    return noised_matrix

def show(img) -> None:
    plt.imshow(img)
    plt.axis("off")
    plt.show()

def generate_img_p1(seed: 676767):
    a = generate_synthetic_image()
    return a + [generate_poisson_noise(a[0], seed)]

if __name__ == "__main__":
    img_list = generate_img_p1()
    show(img_list[0])
    show(img_list[1])
    show(img_list[2])
    show(img_list[3])
    show(img_list[4])
