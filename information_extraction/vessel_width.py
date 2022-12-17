#!/usr/bin/python3

import cv2
import width_
import argparse
import numpy as np
import matplotlib.pyplot as plt
from sys import argv
from tqdm import tqdm


def drawBorder(img, border=5, color=0):
    color = [color]*3
    top, bottom, left, right = [border]*4
    return cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)

def all_widths(img, x, y, m, n):
    w = {}
    
    for i in tqdm(range(x, m)):
        for j in range(y, n):
            vessel_width, xc, xy = width_.vessel_width(img, i, j)
            if vessel_width > 0:
                w[vessel_width] = (xc, xy)

    return w

def options():
    parser = argparse.ArgumentParser("Operations on the vessel information.")
    parser.add_argument("image_path", help="path to mask image")
    parser.add_argument("original", help="path to original image")
    parser.add_argument("--scope", nargs=4, default=False, type=int, help="coordinates of the bottom left corner and top right corner of the extraction rectangle")
    parser.add_argument("--average", action="store_true", help="get an average the blood vessels")
    parser.add_argument("--max", action="store_true", help="get max width of the blood vessels")
    parser.add_argument("--polyp-size", default=False, nargs=4, type=int, help="return the polyp size in mm")
    parser.add_argument("--plot-vessels", default=False, help="generate a plot of the blood vessels information (specify save image path if so)")

    return parser.parse_args()


if __name__ == "__main__":
    args = options()
    
    # Read image and fix cv2 axis order
    img = cv2.imread(args.image_path)
    img = img.transpose(1, 0, 2)

    # set extraction scope rectangle
    if args.scope:
        x, y = args.scope[0:2]
        m, n = args.scope[2:4]
    else:
        x, y = 0, 0 
        m, n =img.shape[0:2]


    # Get all vessel widths in the scope triangle
    w =  all_widths(img, x, y, m, n)

    if args.max:
        psize = max(w)
        print(f"Max of {args.image_path}: {psize} at {w[psize]}")
        original = cv2.imread(args.original)
#        original = original.transpose(1, 0, 2)
        xc, yc = w[psize]
        cv2.rectangle(original, (xc-psize, yc-psize), (xc+psize, yc+psize), (0, 255, 0), 2)
        cv2.imwrite(f"region_{args.original}", original)



    if args.polyp_size:
        # radius
        h, i, j, k = args.polyp_size
        pixel_size = np.sqrt((h-j)**2 + (i-k)**2)
        mm_size = pixel_size / min(w)
        print("radius")
        print(f'Polyp-Size: {mm_size}')
        print(f'Polyp-Size rounded: {round(mm_size)}')
        
        # width
        pixel_size = max(j-k, k-i)
        mm_size = pixel_size / max(w)
        print("radius")
        print(f'Polyp-Size: {mm_size}')
        print(f'Polyp-Size rounded: {round(mm_size)}')

    if args.average:
        avg = float(sum(w)) / float(len(w)) if len(w) != 0 else 0
        print(f"Average vessel width: {avg}")

    if args.plot_vessels:
        fig, ax = plt.subplots(figsize=(16,9))
        ax.set_xlabel("Width (pixels)")
        ax.set_ylabel("Occurances")
        ax.hist(w, label="Vessels")
        ax.set_title("Histogram of Vessels' width")
        ax.legend()
        fig.savefig(args.plot_vessels, dpi=400)



