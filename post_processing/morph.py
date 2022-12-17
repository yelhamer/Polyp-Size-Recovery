#!/usr/bin/python3

import cv2
import numpy as np
from sys import argv


if len(argv) != 3:
    # Incorrect Usage
    print(f"Usage: {argv[0]} <input_image> <output_image>")
    exit(1)

else:
    # Lire l'image
    img = cv2.imread(argv[1], 0)

    # Appliquer la binarization
    _, img = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)

    # Appliquer Erosion
    kernel = np.ones((5,5), np.uint8)
    erosion = cv2.erode(img, kernel, iterations=1)

    # Sauvegarder l'output
    cv2.imwrite(argv[2], erosion)
