#!/usr/bin/python3


import os
import json
from sys import argv
import numpy as np
import matplotlib.pyplot as plt


if len(argv) != 3:
    print("Usage: {} <data.json> <save_dir>".format(argv[0]))
    exit(1)

else:
    # Classify images on a case-basis
    json_data = argv[1]
    save_dir= argv[2]


    # Create dir if not already
    try:
        os.mkdir(save_dir)
    except:
        pass


    # Load json data
    with open(json_data, "r+") as json_file:
        content = json_file.read()
        input_data = json.loads(content)


    # Reuse the same figure for all graphs
    fig, ax = plt.subplots(figsize=(16,9))


    # Generate a graph for each case in the input data
    for i in range(len(input_data)):
        # Perim in function of Time
        # BoxSize in function of Time
        ax.cla()
        ax.set_xlabel('Time (frame)')
        ax.set_ylabel('Size (px)')
        ax.scatter([i for i in range(len(input_data[i]["perimiter"]))], list(map(float, input_data[i]["perimiter"])), label="Perimeter(Time)")
        ax.scatter([i for i in range(len(input_data[i]["boxSize"]))], list(map(float, input_data[i]["boxSize"])), label="Diameter(Time)")
        ax.set_title("Variance of Box Diameter and Box Perimiter in function of Time")
        ax.legend()
        save_path = f"{save_dir}/case{i+1}.jpeg"
        fig.savefig(save_path, dpi=300)


    # Perim in function of PolypSize
    # BoxSize in function of PolypSize
    ax.cla()
    ax.set_xlabel('Polyp Size (mm)')
    ax.set_ylabel('Average Size (px)')
    ax.scatter(list(map(lambda x: int(x["polypSize"]), input_data)), [np.average(list(map(float, case['perimiter']))) for case in input_data], s=[len(case['perimiter'])/2 for case in input_data], label="Perim(PolypSize)")
    ax.legend()
    ax.scatter(list(map(lambda x: int(x["polypSize"]), input_data)), [np.average(list(map(float, case['boxSize']))) for case in input_data], s=[len(case['boxSize'])/2 for case in input_data], label="boxSize(PolypSize)")
    ax.legend()
    ax.set_title("Average Box Perimiter and Diameter for each Polyp Size Per Case")
    fig.savefig(f"{save_dir}/dataset.jpeg", dpi=300)


