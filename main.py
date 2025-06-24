import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"  # Fix OpenMP DLL issue on Windows

from glob import glob
from PIL import Image
import numpy as np
import torch
import torchvision.transforms as transforms
from torchvision.models import resnet50, ResNet50_Weights
import faiss

# ====== Config ======
dataset_path = "D:\\faiss3\\artvee"
query_img_path = "C:\\Users\\ADMIN\\Downloads\\1_5_892f3f03-95af-41fd-bc46-67d61f772c47.jpg"
MAX_IMAGES = None  # Limit for testing, set None to process all

# ====== Load Image Paths ======
image_paths = glob(os.path.join(dataset_path, "*.jpg"))
if MAX_IMAGES:
    image_paths = image_paths[:MAX_IMAGES]
print("Found", len(image_paths), "images")

# ====== Load Pretrained Model ======
weights = ResNet50_Weights.DEFAULT
model = resnet50(weights=weights)
model.eval()
model = torch.nn.Sequential(*(list(model.children())[:-1]))  # Remove final classification layer

# ====== Image Transform ======
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# ====== Extract Features ======
def extract_features(paths):
    features = []
    for i, path in enumerate(paths):
        image = Image.open(path).convert("RGB")
        img_tensor = transform(image).unsqueeze(0)
        with torch.no_grad():
            vec = model(img_tensor).squeeze().numpy()
        features.append(vec)
        if i % 10 == 0:
            print(f"Processed {i+1}/{len(paths)}")
    return np.array(features).astype("float32")

features = extract_features(image_paths)

# ====== Build FAISS Index ======
dim = features.shape[1]
index = faiss.IndexFlatL2(dim)
index.add(features)

# ====== Query ======
query_feature = extract_features([query_img_path])
D, I = index.search(query_feature, k=3)

# ====== Show Matches ======
print("Top matches:")
for idx in I[0]:
    print(image_paths[idx])