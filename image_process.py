import os
import cv2
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from keras.utils import to_categorical
from keras.callbacks import EarlyStopping
from keras.regularizers import l1, l2
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np

X = []
y = []

categories = ["paper", "rock", "scissors"]

standard_size = (100, 100)  # Smaller standard size

dataset_path = "c:\TDS\TraitementDeSignaux/Dataset"

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

early_stopping = EarlyStopping(monitor='val_loss', patience=5)

# Define the model
model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=X_train.shape[1:], kernel_regularizer=l2(0.02), bias_regularizer=l1(0.02)))
model.add(MaxPooling2D(pool_size=(2, 2)))

# Dropout Layer
model.add(Dropout(0.3))

model.add(Conv2D(64, (3, 3), activation='relu', kernel_regularizer=l2(0.02), bias_regularizer=l1(0.02)))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(128, activation='relu', kernel_regularizer=l2(0.02), bias_regularizer=l1(0.02)))

# Another Dropout Layer
model.add(Dropout(0.5))

model.add(Dense(3, activation='softmax'))  # 3 classes for rock, paper, scissors

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
history = model.fit(X_train, y_train, epochs=20, validation_data=(X_test, y_test), callbacks=[early_stopping])

# Save the model
model.save('model.keras')


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