from utils.scene_classifier import classify_scene

scene, confidence = classify_scene("data/test_images/sample3.jpg")
print(f"Scene: {scene}, Confidence: {confidence:.2f}")
