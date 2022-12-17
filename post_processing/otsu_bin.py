#!/usr/bin/python3

import cv2
import numpy as np
from sys import argv


if len(argv) != 3:
    # Incorrect Usage
    print(f"Usage: {argv[0]} <input_image> <output_image>")
    exit(1)
else:
    # Correct Usage
    img = cv2.imread(argv[1], 0)
    #img = cv2.medianBlur(img, 5)
    #img = cv2.GaussianBlur(img,(5,5),0)
    ret2, th2 = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    cv2.imwrite(argv[2], th2)

