from utils.detect import detect_objects
from utils.spatial import describe_spatial_relationships

image_path = "data/test_images/sample3.jpg"
detections = detect_objects(image_path)
relations = describe_spatial_relationships(detections)

for r in relations:
    print(r)
