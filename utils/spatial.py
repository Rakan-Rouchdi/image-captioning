from  utils.detect import detect_objects

def get_center(bbox):
    """
    Returns the center (x, y) of a bounding box.
    bbox format: [x1, y1, x2, y2]
    """
    x1, y1, x2, y2 = bbox
    center_x = (x1 + x2) / 2
    center_y = (y1 + y2) / 2
    return center_x, center_y

def describe_spatial_relationships(detections, distance_threshold=100):
    """
    Generate spatial relationships between detected objects.
    Output: list of strings describing pairwise spatial relationships.
    """
    relationships = []
    seen_pairs = set()

    # Extract (label, center, bbox) for each object
    objects = [(d["label"], get_center(d["bbox"]), d["bbox"]) for d in detections]

    for i in range(len(objects)):
        label_a, center_a, bbox_a = objects[i]

        for j in range(i + 1, len(objects)):
            label_b, center_b, bbox_b = objects[j]

            pair_key = tuple(sorted((label_a, label_b)))
            if pair_key in seen_pairs:
                continue
            seen_pairs.add(pair_key)

            dx = center_b[0] - center_a[0]
            dy = center_b[1] - center_a[1]

            if abs(dx) < distance_threshold:
                if center_a[1] < center_b[1]:
                    relation = f"{label_a} is above {label_b}"
                else:
                    relation = f"{label_a} is below {label_b}"
            elif abs(dy) < distance_threshold:
                if center_a[0] < center_b[0]:
                    relation = f"{label_a} is left of {label_b}"
                else:
                    relation = f"{label_a} is right of {label_b}"
            else:
                # General left/right as fallback
                if center_a[0] < center_b[0]:
                    relation = f"{label_a} is left of {label_b}"
                else:
                    relation = f"{label_a} is right of {label_b}"

            relationships.append(relation)

    return relationships

