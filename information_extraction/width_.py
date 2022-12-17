#!/usr/bin/python3
#
# This script retrieves the width if a line which contains the pixel (x,y) given in params
#

from sys import argv
import numpy as np
import cv2


### Functions ###

# Checks if a point (BGR) is Black (below thresh)
def isBlack(img, x, y , thresh):
    if (x < 0 or x >= img.shape[0]) or  (y < 0 or y >= img.shape[1]):
        return True
    else:
        return ((img[x, y] < [thresh, thresh, thresh]).all())

# Per-element sum of two arrays
def elemSum(arr1, arr2):
    return (x+y for x, y in zip(arr1, arr2))

# Returns the width of a white line at pixel img[x, y]
def vessel_width(img, x, y, thresh=127, steps=20):
    radius = 1  # Half the line's thickness (diameter)
    angles = np.linspace(0, 2*np.pi, steps)   # Generate rotation angles
    ret = 1000  #assums a line is never of width 1000 (which true in our particular use-case)
    shifted = False # Has the center been shifted, if so, reiterate throught previous angles

    # Check if in black void
    if isBlack(img, x, y, thresh):
        return (0, 0, 0)

    # Pixel is white
    else:
        i_id = 0
        # Find the Vessel thickness at pixel (x, y) by drawing multiple circles of incrementally-increasing radius, until a black pixel falls on the perimiter
        while(True):
            # Check new perimiter
            for angle in angles:
                # Get perimiter pixel to check
                x_comp, y_comp = map(lambda val: int(np.round(radius * val)), (np.cos(angle), np.sin(angle)))

                if isBlack(img, x+x_comp, y+y_comp, thresh):
                    if isBlack(img, x-x_comp, y-y_comp, thresh):
                        ret = min(ret, (radius-1)*2+1)

                    else:
                        x_peek, y_peek = map(lambda val: int(np.round(val)), (np.cos(angle), np.sin(angle)))
                        if not isBlack(img, x-(x_comp+x_peek), y-(y_comp+y_peek), thresh):
                            #print(f"{x}, {y}")
                            # Shift the circle's center in the opposite direction
                            #radius += 1
                            #shifted = True
                            x, y = elemSum((x, y), (-x_peek, -y_peek))

                        else:
                            # return 
                            ret = min(ret, (radius-1)*2+1+1)

                else:
                    #print("pixel is white, pass to outer ring")
                    continue

            if (ret != 1000):
                return (ret, x, y)
                    
            else:
                i_id += 1
                # Move on to next circle only if the center hasn't been shifted, otherwise, re-iterate over angles with new center
                if shifted:
                    x, y = elemSum((x, y), (-x_peek, -y_peek))
                    #print(f"({-x_peek},{-y_peek})")
                    shifted = False
                    
                else:
                    # Move on to upper ring
                    radius = radius + 1


### Main ###
if __name__ == "__main__":
    # Check Usage
    if len(argv) != 4:
        # Incorrect usage
        print(f"Usage: {argv[0]} <image_path> <x> <y>")

    else:
        # Correct Usage
        img = cv2.imread(argv[1])

        # cv2 (unlike PIL) transposes image's axis for some reason... *shrugs*
        img = img.transpose(1, 0, 2)
        
        # Get pixel coordinates
        x, y = map(int, (argv[2], argv[3]))

        # Get and return width
        width = vessel_width(img, x, y)
        print(f"The vessel width at ({x}, {y}) is: {width[0]}")


