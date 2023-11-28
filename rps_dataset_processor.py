import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import MobileNet
from tensorflow.keras.applications.mobilenet import preprocess_input
from tensorflow.keras.preprocessing import image

# Load pre-trained MobileNet model
model = MobileNet(weights='imagenet')

def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    return preprocess_input(x)

def predict_hand_sign(img_path):
    preprocessed_img = preprocess_image(img_path)
    preds = model.predict(preprocessed_img)
    # Process the predictions as needed for your application
    return preds  # You can return the predictions or process them further

def process_rps_dataset(dataset_path):
    predictions = []
    for subfolder in os.listdir(dataset_path):
        subfolder_path = os.path.join(dataset_path, subfolder)
        if os.path.isdir(subfolder_path):
            for filename in os.listdir(subfolder_path):
                if filename.endswith(".jpg"):
                    img_path = os.path.join(subfolder_path, filename)
                    pred = predict_hand_sign(img_path)
                    predictions.append(pred)
    return predictions
