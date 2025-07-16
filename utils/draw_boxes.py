import cv2
import os
import random
import colorsys

def is_contrasting_with_white(rgb):
    """
    Check if color is dark enough to contrast with white text.
    """
    r, g, b = rgb
    brightness = (r * 299 + g * 587 + b * 114) / 1000
    return brightness < 180

def is_brown(hue):
    """
    Roughly detect brown hues in HSV (between 30° and 50°).
    """
    return 30/360 < hue < 50/360

def get_class_colors(labels):
    class_colors = {}
    for label in labels:
        while True:
            # Generate random hue, saturation and value
            h = random.random()
            s = random.uniform(0.5, 1)
            v = random.uniform(0.4, 0.8)

            if is_brown(h):
                continue  # Skip brown tones

            r, g, b = [int(x * 255) for x in colorsys.hsv_to_rgb(h, s, v)]
            if is_contrasting_with_white((r, g, b)):
                class_colors[label] = (r, g, b)
                break
    return class_colors

def draw_boxes(image_path, detections, output_path):
    """
    Draw bounding boxes, labels, and confidence scores on the image.
    Args:
        image_path: path to the input image
        detections: list of dicts with keys ['label', 'bbox', 'confidence']
        output_path: path to save the annotated image
    """
    image = cv2.imread(image_path)
    class_colors = get_class_colors([d["label"] for d in detections])

    for det in detections:
        label = det["label"]
        bbox = det["bbox"]  # [x1, y1, x2, y2]
        confidence = det["confidence"]

        color = class_colors[label]
        x1, y1, x2, y2 = map(int, bbox)

        # Draw box
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)

        # Label with confidence
        label_text = f"{label} {confidence:.2f}"
        (text_width, text_height), _ = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        cv2.rectangle(image, (x1, y1 - text_height - 10), (x1 + text_width, y1), color, -1)
        cv2.putText(image, label_text, (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    # Save image
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cv2.imwrite(output_path, image)
