from PIL import Image
import numpy as np
from utils.scene_classifier import classify_scene

def estimate_brightness(image_path):
    """Estimate brightness to guess day vs night."""
    image = Image.open(image_path).convert("L")  # grayscale
    pixels = np.array(image)
    avg_brightness = np.mean(pixels)
    return avg_brightness

def get_environmental_cue(image_path, object_labels):
    """
    Infer environment using scene classification + detected objects + brightness.
    """

    # 1. Try scene classification
    try:
        scene, confidence = classify_scene(image_path)
    except Exception as e:
        print(f"⚠️ Scene classification failed: {e}")
        scene = None
        confidence = 0

    # 2. General fallback logic based on COCO-style categories
    labels = set(label.lower() for label in object_labels)

    if confidence < 0.30:
        # COCO-style generalized groups
        indoor_objects = {"sofa", "tv", "laptop", "bed", "refrigerator", "oven", "sink", "dining table", "toilet"}
        outdoor_street_objects = {"car", "truck", "bus", "bicycle", "motorcycle", "traffic light", "stop sign", "parking meter"}
        nature_objects = {"tree", "bench", "dog", "cat", "horse", "bird"}
        water_objects = {"boat", "surfboard"}
        people_objects = {"person"}

        if labels & indoor_objects:
            scene = "indoor environment"
        elif labels & outdoor_street_objects:
            scene = "urban outdoor scene"
        elif labels & nature_objects:
            scene = "natural outdoor area"
        elif labels & water_objects:
            scene = "near water or coastal scene"
        elif labels & people_objects:
            scene = "human activity area"
        else:
            scene = "unclassified environment"

    # 3. Brightness estimation
    brightness = estimate_brightness(image_path)
    lighting = "in daylight" if brightness > 100 else "at night or in dim light"

    # Final combined cue
    return f"{scene} {lighting}"
