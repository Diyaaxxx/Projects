import cv2
import numpy as np
import tensorflow as tf
import pickle

# Load trained model
model = tf.keras.models.load_model("gesture_model.h5")

# Load labels
with open("labels.pkl", "rb") as f:
    labels = pickle.load(f)

cap = cv2.VideoCapture(0)  # Open webcam

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Preprocess frame
    img = cv2.resize(frame, (64, 64)) / 255.0
    img = np.expand_dims(img, axis=0)

    # Predict gesture
    prediction = model.predict(img)
    class_id = np.argmax(prediction)
    gesture_name = list(labels.keys())[class_id]  # Get gesture label

    # Display result
    cv2.putText(frame, f"Gesture: {gesture_name}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Gesture Recognition", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
