#!/usr/bin/python3

import os
import cv2
import argparse

parser = argparse.ArgumentParser("Get polyp size (px)")
parser.add_argument("image", help="path to image")

if __name__ == "__main__":
    # holds polyp size
    size = 0

    # get args
    args = parser.parse_args()
    image = args.image

    # read image
    image = cv2.imread(image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, image = cv2.threshold(image, 60, 255, cv2.THRESH_BINARY)

    # get image center
    xc, yc = image.shape[0] // 2, image.shape[1] // 2

    # get size (do 180 rotations and grab max(width, height) of each corresponding contour
    for i in range(0, 180):
        # rotate
        M = cv2.getRotationMatrix2D((xc, yc), i, 1.0)
        rotated = cv2.warpAffine(image, M, image.shape)
        # get contour
        contours = cv2.findContours(rotated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = contours[0] if len(contours) == 2 else contours[1]
        for contour in contours:
            _, _, h, w = cv2.boundingRect(contour)
            size = max(size, h, w)

    # return size
    print(size)


