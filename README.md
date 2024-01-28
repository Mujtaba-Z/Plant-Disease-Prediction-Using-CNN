# Plant-Disease-Prediction-Using-CNN

## Introduction
Welcome to the CNN Plant Disease Predictor repository! This project leverages the power of Convolutional Neural Networks (CNNs) to create a robust and accurate model for predicting plant diseases based on images. With the rise of precision agriculture, early detection of diseases plays a pivotal role in ensuring crop health and maximizing yields. This machine learning solution aims to assist farmers and agronomists in identifying potential issues in plants by analyzing images of their leaves. The repository provides the necessary code, datasets, and documentation to understand, train, and deploy the CNN model for predicting plant diseases. Join us in advancing the intersection of technology and agriculture to foster healthier crops and sustainable farming practices.

## Dependencies
The following dependencies are needed to run the project properly:
1. random
2. numpy
3. tensorflow
4. os
5. json
6. zipfile
7. PIL
8. matplotlib
9. kaggle

## Procuring dataset
This project trains on a set of images, and so naturally, the data set size is quite large. Unfortunately, it cannot be uploaded to GitHub, so below are the instructions to get the data set for yourself. The dataset can be found at https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset. Ensure that it is placed in the same directory as **model_creation.py**
1. First, create a kaggle account at https://www.kaggle.com
2. In settings, create a token and place the downloaded kaggle.json file in the location ~/.kaggle/kaggle.json (on Windows in the location C:\Users\<Windows-username>\.kaggle\kaggle.json
3. Execute the following command in your terminal ```kaggle datasets download -d abdallahalidev/plantvillage-dataset```
4. Unzip the file and place it in the same directory as **model_creation.py**
5. Uploaded are three images by which you can test your model: ```test_apple_black_rot.JPG```, ```test_blueberry_healthy.jpg```, ```test_potato_early_blight.jpg```. Download these to the same directory

## Downloading the model
The model is quite large in size, hence I was not able to upload mine to this repo. Worry not, if you've followed the above steps, then running **model_creation.py** will create and save the model as an .h5 file.

## Results
