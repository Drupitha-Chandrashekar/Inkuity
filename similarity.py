import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"  # Fix OpenMP DLL issue on Windows

from glob import glob
from PIL import Image, ImageFile
import numpy as np
import torch
import torchvision.transforms as transforms
from torchvision.models import resnet50, ResNet50_Weights
import faiss

# ====== Handle Truncated Images ======
ImageFile.LOAD_TRUNCATED_IMAGES = True

# ====== Config ======
dataset_path = "D:\\faiss3\\artvee"
query_img_path = "C:\\Users\\ADMIN\\Downloads\\PoplarTree-SamuelEarpLandscapeArtist-oilpainting.jpg"
MAX_IMAGES = None  # ✅ Process only first 2000 images

# ====== Load Image Paths ======
image_paths = glob(os.path.join(dataset_path, "*.jpg"))
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
    valid_paths = []
    for i, path in enumerate(paths):
        try:
            image = Image.open(path).convert("RGB")
            img_tensor = transform(image).unsqueeze(0)
            with torch.no_grad():
                vec = model(img_tensor).squeeze().numpy()
            features.append(vec)
            valid_paths.append(path)
        except Exception as e:
            print(f"Error processing {path}: {e}")
        if i % 10 == 0:
            print(f"Processed {i+1}/{len(paths)}")
    return np.array(features).astype("float32"), valid_paths

# ====== Extract Features for Dataset ======
features, image_paths = extract_features(image_paths)

# ====== Build FAISS Index ======
dim = features.shape[1]
index = faiss.IndexFlatL2(dim)
index.add(features)

# ====== Extract Feature for Query Image ======
query_feature, _ = extract_features([query_img_path])
D, I = index.search(query_feature, k=3)  # Top 3 matches

# ====== Show Matches with Similarity Scores ======
max_distance = np.max(D)

print("\nTop matches with similarity scores:")
for rank, (idx, dist) in enumerate(zip(I[0], D[0])):
    similarity = 1 - (dist / max_distance) if max_distance != 0 else 1.0
    similarity_percent = round(similarity * 100, 2)
    print(f"{rank + 1}. {image_paths[idx]} | Similarity: {similarity_percent}% | Distance: {dist:.4f}")
