#!/usr/bin/python3

from PIL import Image
import glob
from sys import argv

directory = "./"

if len(argv) == 2:
    directory = argv[1]

cpt = 4
imgs = glob.glob(directory+"*.png")
for i, img_name in enumerate(imgs):
    img = Image.open(img_name)
    pos = img.rotate(90)
    pos.save(f"{cpt:02d}_training.png")
    cpt += 1
    neg = img.rotate(270)
    neg.save(f"{cpt:02d}_manual1.png")
    cpt += 1

