#!/usr/bin/python3

from PIL import Image, ImageOps
import glob
from sys import argv

directory = "./"

if len(argv) == 2:
    directory = argv[1]

cpt = 10
imgs = glob.glob(directory+"*.png")
for i, img_name in enumerate(imgs):
    img = Image.open(img_name)
    pos = ImageOps.mirror(img)
    pos.save(f"{cpt:02d}_manual1.png")
    cpt += 1
