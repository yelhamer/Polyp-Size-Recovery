#!/usr/bin/python3


import os
import cv2
import sys
import shutil
import numpy as np
import argparse
import subprocess
from sys import argv


images_patches = {}


#### Segment a single image into many patches of resolution (patch_height, patch_width) ###
def segmentImage(patch_save_dir, image, patch_dims):
    # Get the id of the last patch in the patches dir
    patch_id = len(list(os.walk(patch_save_dir))[0][2])

    # Extract params
    patch_height, patch_width = patch_dims

    # Loop through all patches and extract each one (segmentation is done through the first axis first)
    for i in range(int(image.shape[0]/patch_dims[0])+1):
        for j in range(int(image.shape[1]/patch_dims[1])+1):
            # id of current patch
            patch_id += 1
            current_image_id = list(images_patches.keys())[-1]

            # Increase the number of patches for the last image in the dictionary
            images_patches[current_image_id] += 1

            # Extract Patch and save it to the patches_dir under its corresponding id
            patch = image[i*patch_height:(i+1)*patch_height, j*patch_width:(j+1)*patch_width]
            patch_pathname = os.path.join(patch_save_dir, f"{patch_id}.png")
            cv2.imwrite(patch_pathname, patch)


    return None


### Construct an image of dimensions $image_dims from corresponding array of patches ###
def constructImage(patches, image_dims):
    # Retrieve dimensional information
    patch_height, patch_width = patches[0].shape[0:2]
    print(patches[0].shape)
    image_height, image_width, _ = image_dims

    # Construct image canvas array
    image = np.zeros(image_dims)

    # Loop through patches and fill them into the image's blank canvas
    for i in range(int(image_height/patch_height)+1):
        for j in range(int(image_width/patch_width)+1):
            image[i*patch_height:(i+1)*patch_height, j*patch_width:(j+1)*patch_width] = patches.pop(0)


    return image


### Loop through images in a directory and extract patches from each one ###
def createPatches(img_dir, intermediate_save_dir, patch_dims=(150, 150), empty_patch_dir=True):
    # Enumerate images in dir, and make sure they're in order (necessary for when segmenting images and their corresponding mask images)
    images = list(os.walk(img_dir))[0]
    images = list(map(lambda x: os.path.join(images[0], x), images[2]))
    #get_name_int = lambda x: int(os.path.splitext(os.path.basename(x))[0])
    images.sort()
    
    # Directory to which we save the intermediate patches
    patch_save_dir = os.path.join(intermediate_save_dir, "patches")

    # If directory already exists, delete all of content to prevent it from getting mixed up with the patches
    if empty_patch_dir and os.path.exists(patch_save_dir):
        try:
            shutil.rmtree(patch_save_dir)
        except Exception as e:
            print(e)
            sys.exit(e.errno)
    
    # Create patches directory
    if not os.path.exists(patch_save_dir):
        try:
            os.makedirs(patch_save_dir)
        except Exception as e:
            print(e)
            sys.exit(1)

    # Segment all images in the provided directory
    for img in images:
        # Read passed image
        image = cv2.imread(img)
        image_id = (len(images_patches)+1, image.shape)
    
        # Get image ID and initilize its number of patches to zero
        images_patches[image_id] = 0

        # Segment the image
        segmentImage(patch_save_dir, image, patch_dims)


    return None



### Construct back the images from their corresponding patches ###
def constructImages(images_save_dir, intermediate_save_dir, clear_image_save_dir=True):
    # Create dedicated save directory
    patches_dir = os.path.join(intermediate_save_dir, "predicted")
  
    # Directory which will contain the predicted patches
    patches=[]

    # Clear constructed-images directory if instructed to
    if clear_image_save_dir and os.path.exists(images_save_dir):
        try:
            shutil.rmtree(images_save_dir)
        except Exception as e:
            print(e)
            sys.exit(e.errno)

    # Create the predicted patches dir
    if not os.path.exists(images_save_dir):
        try:
            os.makedirs(images_save_dir)
        except Exception as e:
            print(e)
            sys.exit(1)

    
    # Enumerate the patches (in our case the predictions) directory, and make sure they're in order
    patches = list(os.walk(patches_dir))[0]
    patches = list(map(lambda x: os.path.join(patches[0], x), patches[2]))
    get_name_int = lambda x: int(os.path.splitext(os.path.basename(x))[0])
    patches.sort(key=get_name_int)


    # Loop through and construct all images
    for i in images_patches:
        # The patches that will be passed to the constructImage function to construct the image from
        p = []

        # Retrieve all patches (from the filesystem), and append them to a per-image list
        for _ in range(images_patches[i]):
            p.append(cv2.imread(patches.pop(0)))

        # Construct image from corresponding patches
        image_id, image_shape = i
        image = constructImage(p, image_shape)
        cv2.imwrite(os.path.join(images_save_dir, f"{image_id}.png"), image)


    return None



### Run the predictions against the obtained patches ###
def runPrediction(intermediate_dir, model_dir="./Polyp-PVT", log_file=None):
    # Path Variables
    patches_dir = os.path.join(intermediate_dir, "patches")
    predictions_dir = os.path.join(intermediate_dir, "predicted")
    #script_pathname = os.path.join(model_dir, "test.sh")
    script_pathname = "test.sh"
    results_dir = os.path.join(model_dir, "result_map/PolypPVT/Vessels/")
    
    # Dataset Variables
    dataset_dir = os.path.join(model_dir, "dataset/TestDataset/Vessels")
    images_dir = os.path.join(dataset_dir, "images")
    masks_dir = os.path.join(dataset_dir, "masks")

    # Check if the dataset path exists already, if so, remove pre-existing images and masks
    if os.path.exists(dataset_dir):
        # Remove images
        if os.path.exists(images_dir):
            try:
                shutil.rmtree(images_dir)
            except Exception as e:
                print(e)
                sys.exit(e.errno)

        # Remove masks
        if os.path.exists(masks_dir):
            try:
                shutil.rmtree(masks_dir)
            except Exception as e:
                print(e)
                sys.exit(e.errno)

    if os.path.exists(predictions_dir):
        try:
            shutil.rmtree(predictions_dir)
        except Exception as e:
            print(e)
            sys.exit(e.errno)
    
    # Create dataset path along with the images and masks directory
    try:
        # PS. the dataset folder will be created part of the images_dir treeline
        os.makedirs(images_dir)
        os.makedirs(masks_dir)
        os.makedirs(predictions_dir)
    except Exception as e:
        print(e)
        sys.exit(1)


    # Copy the patches into the models masks dir
    # (this is pointless, but since the model is configured to use a single dataloader function for both testing and training, I just kept it as is)
    for i in os.listdir(patches_dir):
        try:
            shutil.copy(os.path.join(patches_dir, i), images_dir)
            shutil.copy(os.path.join(patches_dir, i), masks_dir)
        except Exception as e:
            print(e)
            sys.exit(e.errno)
    
    
    ### Run The Prediction ###
    print("Running the prediction")
    process = subprocess.Popen(f"cd {model_dir} && ./{script_pathname}", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    while process.poll() is None:
        line = process.stdout.readline()
        line = line.decode('utf-8')
        print(line, end='')


    # Copy the predictions into the intermediate directory
    for i in os.listdir(results_dir):
        try:
            shutil.copy(os.path.join(results_dir, i), predictions_dir)
        except Exception as e:
            print(e)
            sys.exit(e.errno)



    return None    




##### Main #####
if __name__ == "__main__":
    # Initialize parser object
    parser = argparse.ArgumentParser(description="Segment images into patches of equal dimensions")
   
    ### Params ###
    parser.add_argument("input_images_dir", metavar="input_images_dir", help="The directory containing the input images to run the prediction against")
    parser.add_argument("predicted_masks_dir", metavar="predicted-mask-dir", help="The directory in which the predictions should be saved")
    parser.add_argument("--patch-dimensions", nargs=2, type=int, default=(150, 150), help="Patch dimensions separated by a space")
    parser.add_argument("--intermediate-save-dir", default="./tmp", help="The directory in which the temporary patches and their corresponding predictions will be stored")
    parser.add_argument("--keep-patches", action='store_true', help="Patches are deleted after prediction by default")
    parser.add_argument("--model-path", default='./Polyp-PVT', help="The model's path")


    args = parser.parse_args()


    # Segment the images into patches
    createPatches(args.input_images_dir, args.intermediate_save_dir, patch_dims=args.patch_dimensions, empty_patch_dir=True)
    
    # Run prediction on those patches
    runPrediction(args.intermediate_save_dir, model_dir=args.model_path, log_file=None)
    
    # Reconstruct the prediction results into original-scale images
    constructImages(args.predicted_masks_dir, args.intermediate_save_dir, clear_image_save_dir=True)



