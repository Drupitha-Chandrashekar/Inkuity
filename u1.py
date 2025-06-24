import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"  # For OpenMP issue on Windows

from glob import glob
from PIL import Image
import numpy as np
import torch
import torchvision.transforms as transforms
from torchvision.models import resnet50, ResNet50_Weights
import faiss
import pickle

# ========== CONFIG ==========
dataset_path = "D:\\faiss3\\artvee"  # Path to your folder of artwork images
MAX_IMAGES = None # Set to a number to limit for testing (e.g., 100), or None to include all

# ========== LOAD IMAGE PATHS ==========
image_paths = glob(os.path.join(dataset_path, "*.jpg"))
if MAX_IMAGES:
    image_paths = image_paths[:MAX_IMAGES]
print(f"✅ Found {len(image_paths)} images.")

# ========== LOAD MODEL ==========
weights = ResNet50_Weights.DEFAULT
model = resnet50(weights=weights)
model.eval()
model = torch.nn.Sequential(*(list(model.children())[:-1]))  # Remove classifier layer

# ========== TRANSFORM ==========
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# ========== FEATURE EXTRACTION FUNCTION ==========
def extract_features(paths):
    features = []
    for i, path in enumerate(paths):
        try:
            image = Image.open(path).convert("RGB")
            img_tensor = transform(image).unsqueeze(0)  # Add batch dim
            with torch.no_grad():
                vec = model(img_tensor).squeeze().numpy()
            features.append(vec)
        except Exception as e:
            print(f"⚠️ Error processing {path}: {e}")
            continue
        if i % 10 == 0:
            print(f"Processed {i + 1}/{len(paths)}")
    return np.array(features).astype("float32")

# ========== EXTRACT FEATURES ==========
print("🔍 Extracting features...")
features = extract_features(image_paths)
print(f"📏 Feature array shape: {features.shape}")


# ========== BUILD & SAVE FAISS INDEX ==========
dim = features.shape[1]
index = faiss.IndexFlatL2(dim)
index.add(features)
faiss.write_index(index, "art_index.faiss")
print("💾 Saved FAISS index to art_index.faiss")

# ========== SAVE IMAGE PATHS ==========
with open("image_paths.pkl", "wb") as f:
    pickle.dump(image_paths, f)
    
# Assuming 'features' is the array you used to build FAISS index
with open("features.pkl", "wb") as f:
    pickle.dump(features, f)

print("💾 Saved image paths to image_paths.pkl")

print("✅ FAISS index building completed.")
