import cv2
import os

# Define gesture name (change as needed)
gesture_name = "thumbs_up"  # Change to your gesture name
save_dir = f"dataset/{gesture_name}"

# Create dataset directory if not exists
os.makedirs(save_dir, exist_ok=True)

cap = cv2.VideoCapture(0)  # Open webcam
i = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Show the frame
    cv2.imshow("Collecting Data", frame)

    # Save image
    cv2.imwrite(f"{save_dir}/{i}.jpg", frame)
    i += 1

    # Press 'q' to stop collecting images
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
