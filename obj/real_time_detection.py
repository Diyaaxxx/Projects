import cv2

# Open webcam or video file
cap = cv2.VideoCapture(0)  # Change to "video.mp4" for a video file

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    results = model(frame)  # Run YOLO on the frame

    # Show results
    results.show()

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
