# test_scene.py

from utils.scene_classifier import classify_scene

scene, confidence = classify_scene("data/test_images/sample.jpg")
print(f"🏞️ Scene: {scene[0].replace('_', ' ')} ({confidence:.2f} confidence)")
