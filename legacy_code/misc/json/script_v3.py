#!/usr/bin/python3

import re
import glob
import json
import numpy as np
from sys import argv


if len(argv) != 4:
    # Incorrect Usage
    print("Usage: {} <cases_folder> <info_file> <output_file.json>".format(argv[1]))
    exit(1)

else:
    # Correct Usage
    cases = glob.glob(argv[1]+"/*")
    
    info = argv[2]

    # Json template
    case = {"id": [], "path": [], "polypSize": [], "boxSize": [], "perimiter": [], "x": [], "y": [], "m": [], "n": []}
    
    for c in cases[1:2]:
        # Get case number and path
        c_id = re.match(r"^.*case(\d*).*$", c)[1]
        c_path = c

        # Get the polyp size
        with open(info, "r+") as info_file:
            content = info_file.readlines()
            c_polypSize = re.match(r"^.*\t\d*.*\t(\d+).*$", content[int(c_id)-1])[1]

        # Parse the case annotation file
        with open(c) as case_file:
            lines = case_file.readlines()

            # Parse each image per case
            for line in lines:
                # Get coordinates of bottom left (x,y) and top right (m,n)
                x, y, m, n = map(int, line.split(" ")[1].split(",")[0:4])

                # Get height and width
                h = n-y
                w = m-x

                # Fill in json template dictionary
                case["id"].append(c_id)
                case["path"].append(line.split(" ")[0])
                case["polypSize"].append(c_polypSize)
                case["boxSize"].append(str(np.sqrt(h*h + w*w)))
                case["perimiter"].append(str(max(h, w)))
                case["x"].append(str(x))
                case["y"].append(str(y))
                case["m"].append(str(m))
                case["n"].append(str(n))

# Save results
with open(argv[3], "w+") as save_file:
    save_file.write(json.dumps(case))

