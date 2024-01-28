import random
random.seed(0)
import numpy as np
np.random.seed(0)

import tensorflow as tf
tf.random.set_seed(0)

import os
import json
from zipfile import ZipFile
from PIL import Image

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models
# from keras.applications import ImageDataGenerator
# from keras import layers, models

kaggle_credentials = json.load(open("kaggle.json"))
os.environ['KAGGLE_USERNAME'] = kaggle_credentials["username"]
os.environ['KAGGLE_KEY'] = kaggle_credentials["key"]

base_dir = 'plantvillage dataset/color'

#######Testing for opening one image
image_path = 'plantvillage dataset/color/Apple___Cedar_apple_rust/025b2b9a-0ec4-4132-96ac-7f2832d0db4a___FREC_C.Rust 3655.JPG'

# Read the image
img = mpimg.imread(image_path)

print(img.shape)
# Display the image
plt.imshow(img)
plt.axis('off')  # Turn off axis numbers
plt.show()

####### End test

#Training paramenters to reduce memory usage
img_size = 224
batch_size = 32

# Image Data Generator. Generate batches of tensor image data with real-time data augmentation.
data_gen = ImageDataGenerator(
    rescale=1./255, # Normalzing pixel values to between 0 and 1 for better memory usage
    validation_split=0.2  # Use 20% of data for validation, 80% for training
)

# Training data Generator. Takes the path to a directory & generates batches of augmented data.
train_generator = data_gen.flow_from_directory(
    base_dir,
    target_size=(img_size, img_size), #Resizing all images to 224*224
    batch_size=batch_size, #arbitrarily mid sized batch size to reduce memory usage
    subset='training',
    class_mode='categorical'
)

# Validation data Generator
validation_generator = data_gen.flow_from_directory(
    base_dir,
    target_size=(img_size, img_size),
    batch_size=batch_size,
    subset='validation', #Only 20% will be reserved for validation
    class_mode='categorical'
)

### Setting up the Convolution Neural Network Model Definition
model = models.Sequential() # Simple sequential model

model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(img_size, img_size, 3))) # 32 kernels/filters of 3x3 size, with 3 channels due to rgb
model.add(layers.MaxPooling2D(2, 2)) # Find different important features using max pooling, and reduce to 2x2

model.add(layers.Conv2D(64, (3, 3), activation='relu')) # Another convolution layer
model.add(layers.MaxPooling2D(2, 2))


model.add(layers.Flatten())
model.add(layers.Dense(256, activation='relu'))
model.add(layers.Dense(train_generator.num_classes, activation='softmax')) # 38 output neurons corresponding to the number of classses or diseases

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy']) # Optimizing and setting loss function and metric

# Training the Model
history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // batch_size,  # Number of steps per epoch
    epochs=5,  # Number of times the model trains on the entire dataset
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // batch_size  # Validation steps
)

# Model Evaluation
print("Evaluating model...")
val_loss, val_accuracy = model.evaluate(validation_generator, steps=validation_generator.samples // batch_size)
print(f"Validation Accuracy: {val_accuracy * 100:.2f}%")

# Plot training & validation accuracy values
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()

# Plot training & validation loss values
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()

class_indices = {v: k for k, v in train_generator.class_indices.items()}
# saving the class names as json file
json.dump(class_indices, open('class_indices.json', 'w'))


# Function to Load and Preprocess the Image using Pillow. Normalizing to our model.
def load_and_preprocess_image(image_path, target_size=(224, 224)):
    # Load the image
    img = Image.open(image_path)
    # Resize the image
    img = img.resize(target_size)
    # Convert the image to a numpy array
    img_array = np.array(img)
    # Add batch dimension
    img_array = np.expand_dims(img_array, axis=0)
    # Scale the image values to [0, 1]
    img_array = img_array.astype('float32') / 255.
    return img_array

# Function to Predict the Class of an Image
def predict_image_class(model, image_path, class_indices):
    preprocessed_img = load_and_preprocess_image(image_path)
    predictions = model.predict(preprocessed_img)
    predicted_class_index = np.argmax(predictions, axis=1)[0]
    predicted_class_name = class_indices[predicted_class_index]
    return predicted_class_name

# image_path = 'test_apple_black_rot.JPG'
# image_path = 'test_blueberry_healthy.jpg'
image_path = 'test_potato_early_blight.jpg'
predicted_class_name = predict_image_class(model, image_path, class_indices)

# Output the result
print("Predicted Class Name:", predicted_class_name)
model.save('plant_disease_prediction_model.h5')