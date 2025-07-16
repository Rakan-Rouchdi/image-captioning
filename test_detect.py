# test_detect.py

from utils.detect import detect_objects

# Provide the path to any test image (put it in 'data/test_images/' or wherever you want)
image_path = "data/test_images/sample3.jpg"

# Run YOLO detection
results = detect_objects(image_path)

# Print results to terminal
for obj in results:
    label = obj['label']
    bbox = obj['bbox']
    conf = obj['confidence']
    print(f"{label} @ {bbox} (confidence: {conf:.2f})")
