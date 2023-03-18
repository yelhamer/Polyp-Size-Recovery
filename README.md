# PVT based Blood Vessel Segmentation and Polyp Size Estimation in Colonoscopy Images

Authors: Insaf Setitra, Yuji Iwahori, Yacine Elhamer, Anais Mezrag, Shinji Fukui, Kunio Kasugai

Digital Object Identifier: 10.5220/0011666700003411

This is the code for the aforementioned paper presented at the 12th ICPRAM on the 24th of February 2023.
The code is structured into 4 folders:\
    - Data augmentation: includes the code used to implement the data augmentation that has been performed on the SUN dataset. \
    - Training and testing: includes the code for the UNet and PPVT models. \
    - Information extraction: includes the information extration algorithm. \
    - Post processing: includes the code used for processing of the Neural Networks' output.
The training and testing folder includes the jupyter notebooks used to train the model.

## Abstract
> The size of colorectal polyps is one of the factors conditioning the risk of synchronous and metachronous colorectal cancer (CRC). In this work, we are interested in the automatic measurement of polyp sizes in colonoscopy videos. The study is performed in two steps: (1) first the detection and segmentation of the polyp by the neural network Polyp-PVT and then (2) the classification of the polyp into different classes (type of disease, size of the polyp). This is done by extracting information from blood vessels, a parameter that has a low variability and is present in the majority of colonoscopic videos. This method has been validated by two local Hepato-Gastro-Enterology specialists. Once the size of the polyp is extracted, a classification of polyps as susceptible malignant (polyp size ≥ 6 mm) and susceptible benign (polyp size < 6 mm) is performed. Our approach reaches an accuracy of 85.61% for the first category and 73.92% for the second one and is comparable to human classification which is estimated to 52% for beginners and 71% for experts endoscopists.

## Running the code

### Getting the code

You can download a copy of all the files in this repository by cloning the git repository:

```
git clone https://github.com/yelhamer/Polyp-Size-Recovery
```

The files can then be moved onto the target environment, be it your local machine or a GPU-powered cloud instance.

### Preparring the environment

Regarding the models, you can use the jupyter notebooks to automate the environment setup.

For the other code however, you will need to setup the environment manually by installing the required python libraries.

You can do so using the provided requirements file, by using the following command:

```
pip install -r requirements.txt
```

### Information regarding using the models

Please keep in mind that the trained SUN models have been omitted from this code, and you will have to train the model yourself.

Keep in mind also that we were unable to train the used models on the standard Google Collab GPU, since they required more VRAM than provided.

## License

All source code is made available under a BSD 3-clause license. You can freely use and modify the code, without warranty, so long as you provide attribution to the authors.

The manuscript text is not open source. The authors reserve the rights to the article content, which has been published in the proceedings of the ICPRAM 2023 conference.
