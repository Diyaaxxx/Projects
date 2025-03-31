import cv2
import numpy as np

# ✅ Specify absolute paths for YOLO model files
weights_path = "C:/Users/KIIT0001/Desktop/python/obj/yolov3.weights"
config_path = "C:/Users/KIIT0001/Desktop/python/obj/yolov3.cfg"
names_path = "C:/Users/KIIT0001/Desktop/python/obj/coco.names"
image_path = "C:/Users/KIIT0001/Desktop/python/obj/img1.jpg"

# ✅ Load YOLO model
print("[INFO] Loading YOLO model...")
net = cv2.dnn.readNet(weights_path, config_path)
print("[INFO] YOLO model loaded successfully.")

# ✅ Load COCO class labels
print("[INFO] Loading class labels...")
try:
    with open(names_path, "r") as f:
        classes = [line.strip() for line in f.readlines()]
    print(f"[INFO] Loaded {len(classes)} class labels.")
except FileNotFoundError:
    print(f"[ERROR] COCO names file not found: {names_path}")
    exit()

# ✅ Load and validate input image
print(f"[INFO] Loading image from {image_path}...")
image = cv2.imread(image_path)
if image is None:
    print(f"[ERROR] Could not read image from {image_path}")
    exit()
print("[INFO] Image loaded successfully.")

# ✅ Resize the image to a medium display size
scale_percent = 75  # Adjust percentage as needed (75% of original size)
width = int(image.shape[1] * scale_percent / 100)
height = int(image.shape[0] * scale_percent / 100)
image = cv2.resize(image, (width, height))

# ✅ Get image dimensions
height, width, _ = image.shape

# ✅ Preprocess the image for YOLO
blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), swapRB=True, crop=False)
net.setInput(blob)

# ✅ Get output layer names
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# ✅ Run YOLO object detection
print("[INFO] Running YOLO object detection...")
outputs = net.forward(output_layers)

# ✅ Process detection results
boxes, confidences, class_ids = [], [], []
for output in outputs:
    for detection in output:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        if confidence > 0.5:
            # Convert YOLO box format to standard (x, y, w, h)
            center_x, center_y, w, h = (detection[:4] * [width, height, width, height]).astype(int)
            x, y = center_x - w // 2, center_y - h // 2

            boxes.append([x, y, w, h])
            confidences.append(float(confidence))
            class_ids.append(class_id)

# ✅ Apply Non-Maximum Suppression (NMS) to remove overlapping boxes
indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

# ✅ Draw bounding boxes on the image
if len(indices) > 0:
    for i in indices.flatten():
        x, y, w, h = boxes[i]
        label = f"{classes[class_ids[i]]}: {confidences[i]:.2f}"
        color = (0, 255, 0)  # Green box

        # Draw bounding box
        cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)

        # Create background rectangle for text
        (text_width, text_height), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 1.0, 2)
        cv2.rectangle(image, (x, y - text_height - 10), (x + text_width, y), (0, 0, 0), -1)  # Black background
        cv2.putText(image, label, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 3)  # Green text

# ✅ Display output image in medium size window
cv2.namedWindow("Object Detection", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Object Detection", 900, 600)  # Medium-sized window
cv2.imshow("Object Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
