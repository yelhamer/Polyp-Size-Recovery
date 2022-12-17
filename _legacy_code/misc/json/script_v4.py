#!/usr/bin/python3

import re
import glob
import json
import numpy as np
from sys import argv


if len(argv) != 4:
    # Incorrect Usage
    print("Usage: {} <cases_folder> <info_file> <output_file.json>".format(argv[0]))
    exit(1)

else:
    # Correct Usage
    cases = glob.glob(argv[1]+"/*")    
    info = argv[2]

    # Json template
    case = [{"polypSize": 0, "path": [], "boxSize": [], "perimiter": [], "x": [], "y": [], "m": [], "n": []} for _ in range(len(cases))]


    for c in cases:
        # Get case number (used for indexing into the case list) and path
        c_id = int(re.match(r"^.*case(\d*).*$", c)[1])
        c_path = c

        # Get the polyp size
        with open(info, "r+") as info_file:
            content = info_file.readlines()
            c_polypSize = re.match(r"^.*\t\d*.*\t(\d+).*$", content[c_id-1])[1]

        # Parse the case annotation file
        with open(c) as case_file:
            lines = case_file.readlines()

            # Parse each image per case
            for line in lines:
                # Get coordinates of bottom left (x,y) and top right (m,n)
                x, y, m, n = map(float, line.split(" ")[1].split(",")[0:4])

                # Get height and width
                h = n-y
                w = m-x

                # Fill in json template dictionary
                case[c_id-1]["path"].append(line.split(" ")[0])
                case[c_id-1]["polypSize"] = c_polypSize
                case[c_id-1]["boxSize"].append(str(np.sqrt(h*h + w*w)))
                case[c_id-1]["perimiter"].append(str(min(h, w)))
                case[c_id-1]["x"].append(str(x))
                case[c_id-1]["y"].append(str(y))
                case[c_id-1]["m"].append(str(m))
                case[c_id-1]["n"].append(str(n))


# Save results
with open(argv[3], "w+") as save_file:
    save_file.write(json.dumps(case))

