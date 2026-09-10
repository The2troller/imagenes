from pregunta_1 import ColorSaturation
import cv2
from transformations import bgr_to_rgb


if __name__ == "__main__":
    select = input("pregunta numero: ")
    if select == "1":
        print("0. imagen 1")
        print("1. imagen 2")
        if input("seleccione el numero: "):
            my_path = "tarea 1/test_imgs/betis.jpg"
        else:
            my_path = "tarea 1/test_imgs/benzema.jpg"
        img = cv2.imread(my_path) #saves in bgr

        gray = ((0,0), (120, 0), (240, 0))
        yes_red = ((0, 4), (30, 1), (120, 1), (240, 1), (330, 1), (350, 1), (10, 3), (355, 1))
        no_green = ((0, 1), (90, 1), (120, 0), (150, 0.3), (240, 1), (170, 0.6))
        no_blue = ((120, 4), (150, 2.8),
                   (0, 1), (240, 0), (270, 0), (220, 0), (240, 0), (250, 0))
        only_red = ((30, 0), (120, 0), (240, 0), (330, 0), (350, 0), (355, 0),
                    (0, 1),(10, 1), (15, 1))
        selections = [gray, yes_red, no_green, no_blue, only_red]
        print("1. gray")
        print("2. yes_red")
        print("3. no_green")
        print("4. yes_green / no_blue")
        print("5. only_red")
        pts = selections[int(input("prueba :")) - 1]
        print("0. HSI")
        print("1. Lch")
        space = int(input("espacio:"))
        colorsaturation = ColorSaturation(bgr_to_rgb(img), pts, space)
        colorsaturation.modify()
        colorsaturation.show()
    else:
        pass
