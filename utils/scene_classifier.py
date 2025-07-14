# utils/scene_classifier.py

import torch
from torchvision import models, transforms
from PIL import Image

MODEL_PATH = "models/places365/resnet18_places365.pth.tar"
LABELS_PATH = "models/places365/categories_places365.txt"

# Load scene categories
with open(LABELS_PATH) as f:
    classes = [line.strip().split(' ')[0][3:] for line in f]

# Load ResNet18 pre-trained on Places365
model = models.resnet18(num_classes=365)
checkpoint = torch.load(MODEL_PATH, map_location=torch.device('cpu'), weights_only=False)
state_dict = {k.replace('module.', ''): v for k, v in checkpoint['state_dict'].items()}
model.load_state_dict(state_dict)
model.eval()

# Image preprocessing pipeline
transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

def classify_scene(image_path):
    img = Image.open(image_path).convert('RGB')
    input_tensor = transform(img).unsqueeze(0)
    with torch.no_grad():
        logits = model(input_tensor)
        probs = torch.nn.functional.softmax(logits, dim=1)
        top_prob, top_idx = probs[0].topk(1)
    return classes[top_idx], float(top_prob)
