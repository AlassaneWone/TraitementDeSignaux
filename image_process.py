import os
import math
import cv2
from keras.models import Sequential, Model
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from keras.utils import to_categorical
from keras.callbacks import EarlyStopping
from keras.regularizers import l1, l2
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np

from keras.utils import get_custom_objects
from keras.layers import Activation

X = []
y = []

categories = ["paper", "rock", "scissors"]

standard_size = (100, 100)  # Smaller standard size

dataset_path = "TraitementDeSignaux/Dataset"

def process_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, standard_size)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (5, 5), 0)
    edges = cv2.Canny(img_blur, 50, 50)
    edges = cv2.convertScaleAbs(edges)  # Convert image to 8-bit before finding contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mask = np.zeros_like(img_gray)
    cv2.drawContours(mask, contours, -1, (255), thickness=cv2.FILLED)
    result = cv2.subtract(img_gray, cv2.bitwise_not(mask))  # Subtract mask from grayscale image
    return result.flatten()

def load_data(category):
    path = os.path.join(dataset_path, category)
    images = [os.path.join(path, img) for img in os.listdir(path) if img.endswith(".png")]
    for img in images:
        processed_image = process_image(img)
        X.append(processed_image)
        y.append(categories.index(category))

# Load data
for category in categories:
    load_data(category)


# Convert X and y to numpy arrays
X = np.array(X)
y = np.array(y)

# Convert labels to one-hot vectors
y = to_categorical(y)

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Reshape the data
X_train = X_train.reshape(-1, 100, 100, 1)
X_test = X_test.reshape(-1, 100, 100, 1)

#early_stopping = EarlyStopping(monitor='val_loss', patience=5)

from keras.backend import sigmoid

def swish(x, beta = 1):
    return (x * sigmoid(beta * x))

get_custom_objects().update({'swish': Activation(swish)})

# Define the model
model = Sequential()

# First Convolutional Layer with Regularization
model.add(Conv2D(64, (3, 3), activation='swish', input_shape=X_train.shape[1:], kernel_regularizer=l2(0.02), bias_regularizer=l1(0.02)))
model.add(MaxPooling2D(pool_size=(2, 2)))

# Dropout Layer
model.add(Dropout(0.3))

# Second Convolutional Layer with Regularization
model.add(Conv2D(64, (3, 3), activation='swish', kernel_regularizer=l2(0.02), bias_regularizer=l1(0.02)))
model.add(MaxPooling2D(pool_size=(2, 2)))

# Third Convolutional Layer
model.add(Conv2D(128, (3,3), activation='swish'))
model.add(MaxPooling2D(2,2))

# Fourth Convolutional Layer
model.add(Conv2D(128, (3,3), activation='swish'))
model.add(MaxPooling2D(2,2))

# Flatten Layer
model.add(Flatten())

# Dense Layer with Regularization
model.add(Dense(512, activation='swish', kernel_regularizer=l2(0.02), bias_regularizer=l1(0.02)))

# Dropout Layer
model.add(Dropout(0.5))

# Output Layer
model.add(Dense(3, activation='softmax'))  # 3 classes for rock, paper, scissors

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
history = model.fit(X_train, y_train, epochs=50, validation_data=(X_test, y_test))

# Save the model
model.save('model.keras')

# Save the model
model.save('TraitementDeSignaux/model.keras')

for j in range(len(model.layers)):
    # Specify the layer to visualize
    layer_to_visualize = model.layers[j]  

    # Create a new model that outputs the feature maps
    visualization_model = Model(inputs=model.input, outputs=layer_to_visualize.output)

    # Use this model to predict on an image to get the feature maps
    # Here, we use the first image in the test set as an example
    feature_maps = visualization_model.predict(X_test[0].reshape(1, 100, 100, 1))

    # Check if the layer is a convolutional layer, a pooling layer, a dense layer, or a dropout layer
    if len(feature_maps.shape) == 4:
        # Calculate the grid size to match the number of feature maps
        grid_size = math.ceil(math.sqrt(feature_maps.shape[-1]))

        # Now, you can visualize the feature maps
        plt.figure(figsize=(10, 10))
        plt.suptitle(f'Feature Maps of Layer {j+1} ({type(layer_to_visualize).__name__})')
        for i in range(feature_maps.shape[-1]):
            plt.subplot(grid_size, grid_size, i+1)
            plt.imshow(feature_maps[0, :, :, i], cmap='viridis')
            plt.axis('off')
    elif isinstance(layer_to_visualize, (Dense, Dropout, Flatten)) and len(feature_maps.shape) == 2:
        # Visualize the output of Dense, Dropout, and Flatten layers
        plt.figure(figsize=(10, 2))
        plt.suptitle(f'Output of Layer {j+1} ({type(layer_to_visualize).__name__})')
        plt.imshow(feature_maps, cmap='viridis')
        plt.axis('off')


# Plot training & validation accuracy values
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')


# Plot training & validation loss values
plt.subplot(1, 2, 2)
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')

plt.tight_layout()
plt.show()