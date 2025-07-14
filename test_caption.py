from utils.caption import build_prompt, generate_caption
from utils.environment import get_environmental_cue

image_path = "data/test_images/sample.jpg"

# Simulated input from detection + spatial reasoning
object_labels = ["person", "dog", "bicycle", "stop sign", "car", "truck"]
spatial_descriptions = [
    "person is riding a bicycle",
    "dog is right of person",
    "stop sign is above the scene",
    "car is parked near truck"
]
environment = get_environmental_cue(image_path, object_labels)

# Build prompt
prompt = build_prompt(object_labels, spatial_descriptions, environment)
print("🧾 Prompt to GPT:\n", prompt, "\n")

# Generate caption
caption = generate_caption(prompt)
print("📝 Generated Caption:\n", caption)
