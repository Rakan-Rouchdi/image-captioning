from ultralytics import YOLO
import os

# Load YOLO model 
model = YOLO("yolov8n.pt")  # 'n' = nano (fast, lightweight)

def detect_objects(image_path, confidence_threshold=0.3):
    """
    Detect objects in an image using YOLOv8.
    Returns a list of dicts with label, bbox, and confidence.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    results = model(image_path)

    detections = []
    boxes = results[0].boxes

    for i in range(len(boxes)):
        cls_id = int(boxes.cls[i].item())
        label = results[0].names[cls_id]
        conf = boxes.conf[i].item()
        xyxy = boxes.xyxy[i].tolist()  # [x1, y1, x2, y2]

        if conf >= confidence_threshold:
            detections.append({
                "label": label,
                "bbox": xyxy,
                "confidence": conf
            })

    return detections