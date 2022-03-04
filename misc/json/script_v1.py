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

    case = {"id": "0", "path": "", "polypSize": "", "boxSize": "", "perimiter": ""}
    
    for c in cases:
        # get case number and path
        case["id"] = re.match(r"^.*case(\d*).*$", c)[1]

        # get the polyp size
        with open(info, "r+") as info_file:
            content = info_file.readlines()
            case["polypSize"] = re.match(r"^.*\t\d*.*\t(\d+).*$", content[int(case["id"])-1])[1]

        # parse the case annotation file
        with open(c) as case_file, open(argv[3], "a+") as save_file:
            lines = case_file.readlines()

            # parse each image per case
            for line in lines:
                # get coordinates of bottom left (x,y) and top right (m,n)
                x, y, m, n = map(int, line.split(" ")[1].split(",")[0:4])
                case["path"] = line.split(" ")[0]

                # get height and width
                h = n-y
                w = m-x

                # fill in boxSize and perimiter
                case["boxSize"] = str(np.sqrt(h*h + w*w))
                case["perimiter"] = str(max(h, w))

                # save results
                save_file.write(json.dumps(case)+"\n")
