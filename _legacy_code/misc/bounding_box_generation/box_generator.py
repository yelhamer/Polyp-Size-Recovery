#!/usr/bin/python3


import cv2
import json
import os
from sys import argv


if len(argv) != 3:
    print("Usage {} <input_data.json> <images_directory>")

else:
    cases_log = [] # For logging
    json_file = argv[1]
    
    # Read images' annotations from json file
    with open(json_file, "r+") as f:
        input_data = json.loads(f.read())

    # Draw bounding box for each image
    for i in range(0, len(input_data["id"])):
        # Log to standard output
        if input_data["id"][i] not in cases_log:
            cases_log.append(input_data["id"][i])
            print("Generating Bounding-Box for Images of Case {} ({}/100)...".format(input_data["id"][i], len(cases_log)))

        # Generate respective image path and read it
        img_path = "{}/case{}/{}".format(argv[2], input_data["id"][i], input_data["path"][i])
        img = cv2.imread(img_path)

        # Read corners' coordinates
        x, y, m, n = map(int, (input_data["x"][i], input_data["y"][i], input_data["m"][i], input_data["n"][i]))

        # Draw bounding-box
        cv2.rectangle(img, (x, y), (m, n), (0, 255, 0), 2)

        # Generate respective save_path and save image to it
        try:
            fname, extension = os.path.splitext(input_data["path"][i])
            os.mkdir("case{}".format(input_data["id"][i]))
        except:
            pass 
        finally:
            save_path = "case{}/{}_box{}".format(input_data["id"][i], fname, extension)
            cv2.imwrite(save_path, img)
