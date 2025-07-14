# utils/environment.py

from PIL import Image
import numpy as np

def estimate_brightness(image_path):
    """Estimate brightness to guess day vs night."""
    image = Image.open(image_path).convert("L")  # grayscale
    pixels = np.array(image)
    avg_brightness = np.mean(pixels)
    return avg_brightness

def get_environmental_cue(image_path, object_labels):
    """
    Infer environment based on detected objects and image brightness.
    """
    # Basic object heuristics
    labels = set(label.lower() for label in object_labels)

    if {"car", "stop sign", "truck", "bicycle"}.intersection(labels):
        location = "outdoor street scene"
    elif {"sofa", "tv", "laptop", "table"}.intersection(labels):
        location = "indoor room"
    elif {"tree", "dog", "bench"}.intersection(labels):
        location = "park or outdoor area"
    else:
        location = "general environment"

    # Estimate brightness
    brightness = estimate_brightness(image_path)
    lighting = "in daylight" if brightness > 100 else "at night or in dim light"

    return f"{location} {lighting}"
