# main.py

import argparse
import time
import tracemalloc
from utils.detect import detect_objects
from utils.spatial import describe_spatial_relationships
from utils.caption import build_prompt, generate_caption
from utils.environment import get_environmental_cue

def run_pipeline(image_path):
    print(f"\n📸 Running pipeline for image: {image_path}\n")

    # Start tracking memory
    tracemalloc.start()

    # 1. Object Detection
    start = time.time()
    detections = detect_objects(image_path)
    detect_time = time.time() - start

    object_labels = [d["label"] for d in detections]
    print(f"🧠 Detected Objects:\n  {object_labels}")

    # 2. Spatial Reasoning
    spatial_descriptions = describe_spatial_relationships(detections)
    if spatial_descriptions:
        print("\n📐 Spatial Relationships:")
        for rel in spatial_descriptions:
            print(f" - {rel}")
    else:
        print("\n📐 Spatial Relationships: None detected.")

    # 3. Environmental Cues
    environment = get_environmental_cue(image_path, object_labels)
    print(f"\n🌿 Environment Cue:\n  {environment}")

    # 4. Build Prompt
    prompt = build_prompt(object_labels, spatial_descriptions, environment)
    print(f"\n🧾 Prompt to GPT:\n{prompt}")

    # 5. Caption Generation
    start_caption = time.time()
    caption = generate_caption(prompt)
    caption_time = time.time() - start_caption

    print(f"\n📝 Caption:\n  {caption}")

    # 6. Inference & Memory Stats
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print("\n⏱️ Performance Stats:")
    print(f" - Object Detection Time: {detect_time:.2f} seconds")
    print(f" - Caption Generation Time: {caption_time:.2f} seconds")
    print(f" - Total Pipeline Time: {detect_time + caption_time:.2f} seconds")
    print(f" - Peak Memory Usage: {peak / 1024:.2f} KB")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Smart Image Captioning CLI")
    parser.add_argument("--image", required=True, help="Path to input image")
    args = parser.parse_args()

    run_pipeline(args.image)
