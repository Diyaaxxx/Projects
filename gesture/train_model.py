import cv2
import numpy as np
import os
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from sklearn.model_selection import train_test_split

# Load images and labels
def load_images(directory, img_size=(64, 64)):
    X, Y = [], []
    labels = {gesture: i for i, gesture in enumerate(os.listdir(directory))}

    for gesture, label in labels.items():
        path = os.path.join(directory, gesture)
        for img_name in os.listdir(path):
            img_path = os.path.join(path, img_name)
            img = cv2.imread(img_path)
            img = cv2.resize(img, img_size) / 255.0  # Normalize
            X.append(img)
            Y.append(label)

    return np.array(X), np.array(Y), labels

X, Y, labels = load_images("dataset/")

# Split data
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

# Build CNN model
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)),
    MaxPooling2D(2, 2),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(len(labels), activation='softmax')  # Number of gestures
])

# Compile model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train model
model.fit(X_train, Y_train, epochs=20, validation_data=(X_test, Y_test))

# Save trained model
model.save("gesture_model.h5")

# Save labels
import pickle
with open("labels.pkl", "wb") as f:
    pickle.dump(labels, f)
