#!/usr/bin/python3

import cv2
import os
from sys import argv


# path dimensions
patch_height, patch_width = 250, 250


# enumerate images in directory
content = os.listdir(argv[1])
content.sort()

def main():
    # patch images
    image_number = 1    # used to keep track of patch filenames
    for original in content:
        if original == "s.py" or original == "patches":
            continue
        img = cv2.imread(f"{argv[1]}/{original}")
        for i in range(int(img.shape[0]/patch_height)):
            for j in range(int(img.shape[1]/patch_width)):
                patch = img[i*patch_height:(i+1)*patch_height, j*patch_width:(j+1)*patch_width]
                print(patch.shape)
                cv2.imwrite(f"{image_number}.png", patch)
                image_number += 1

if __name__ == "__main__":
    if len(argv) != 2:
        print(f"Usage: {argv[0]} dataset_directory")
        exit(1)
    else:
        main()
