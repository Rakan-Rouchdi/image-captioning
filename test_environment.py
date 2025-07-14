# test_environment.py

from utils.environment import get_environmental_cue
from utils.detect import detect_objects

IMAGE_PATH = "data/test_images/sample.jpg"  # Replace with your own image if needed

# Run YOLO detection first to get object labels
detections = detect_objects(IMAGE_PATH)
object_labels = [d["label"] for d in detections]

# Get environment description
environment = get_environmental_cue(IMAGE_PATH, object_labels)

print(f"🧠 Detected objects: {object_labels}")
print(f"🌍 Estimated environment: {environment}")
