import json
import os
import numpy as np
from utils.detect import detect_objects

def compute_iou(boxA, boxB):
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])
    interArea = max(0, xB - xA) * max(0, yB - yA)
    if interArea == 0:
        return 0.0
    boxAArea = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
    boxBArea = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])
    return interArea / float(boxAArea + boxBArea - interArea)

def evaluate_map(ground_truth_path, image_dir, iou_threshold=0.5):
    with open(ground_truth_path, 'r') as f:
        ground_truth = json.load(f)

    all_precisions = []

    for filename, gt_objects in ground_truth.items():
        image_path = os.path.join(image_dir, filename)
        predictions = detect_objects(image_path)
        print(f"🔍 Predictions for {filename}:")
        for p in predictions:
            print(p)


        matched = set()
        true_positives = 0
        false_positives = 0

        for pred in predictions:
            pred_label = pred['label']
            pred_bbox = pred['bbox']

            found_match = False
            for i, gt in enumerate(gt_objects):
                if i in matched:
                    continue
                if pred_label == gt['label']:
                    iou = compute_iou(pred_bbox, gt['bbox'])
                    if iou >= iou_threshold:
                        true_positives += 1
                        matched.add(i)
                        found_match = True
                        break

            if not found_match:
                false_positives += 1

        false_negatives = len(gt_objects) - len(matched)
        precision = true_positives / (true_positives + false_positives + 1e-6)
        recall = true_positives / (true_positives + false_negatives + 1e-6)

        print(f"{filename} — Precision: {precision:.3f}, Recall: {recall:.3f}")
        all_precisions.append(precision)

    mAP = np.mean(all_precisions)
    print(f"\n📊 Mean Average Precision (mAP): {mAP:.4f}")

if __name__ == "__main__":
    evaluate_map("ground_truth.json", "data/test_images")
    
