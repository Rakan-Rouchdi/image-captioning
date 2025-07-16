import torch
from torchvision import models, transforms
from PIL import Image
import os

# Load category labels from local file
def load_categories():
    category_file = os.path.join("models", "categories_places365.txt")
    if not os.path.exists(category_file):
        raise FileNotFoundError(
            f"Missing category file: {category_file}\n"
            "Download it from:\n"
            "https://raw.githubusercontent.com/csailvision/places365/master/categories_places365.txt"
        )
    with open(category_file) as f:
        classes = [line.strip().split(' ')[0][3:] for line in f]
    return classes

# Load model weights from local file
def load_model():
    model_path = os.path.join("models", "resnet18_places365.pth.tar")
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Missing model file: {model_path}\n"
            "Download it from:\n"
            "http://places2.csail.mit.edu/models_places365/resnet18_places365.pth.tar"
        )
    model = models.resnet18(num_classes=365)
    checkpoint = torch.load(model_path, map_location=torch.device('cpu'))
    state_dict = {k.replace('module.', ''): v for k, v in checkpoint['state_dict'].items()}
    model.load_state_dict(state_dict)
    model.eval()
    return model

# Image transformation
transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],  # ImageNet/Places365 mean
        std=[0.229, 0.224, 0.225]
    )
])

# Classify scene
def classify_scene(image_path):
    image = Image.open(image_path).convert('RGB')
    input_tensor = transform(image).unsqueeze(0)

    model = load_model()
    categories = load_categories()

    with torch.no_grad():
        output = model(input_tensor)
        probs = torch.nn.functional.softmax(output[0], dim=0)
        top_idx = probs.argmax().item()
        return categories[top_idx], probs[top_idx].item()
