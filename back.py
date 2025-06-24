import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import torch
import torchvision.transforms as transforms
from torchvision.models import resnet50, ResNet50_Weights
import numpy as np
import faiss
import pickle
import io

app = FastAPI()

# ===== Load FAISS Index & Image Paths =====
index = faiss.read_index("art_index.faiss")
with open("image_paths.pkl", "rb") as f:
    image_paths = pickle.load(f)

# ===== Load Features for Cosine Similarity =====
with open("features.pkl", "rb") as f:
    features = pickle.load(f)  # shape: (n_images, 2048)

# Normalize all stored features once for cosine similarity
norm_features = features / np.linalg.norm(features, axis=1, keepdims=True)

# ===== Load Pretrained Model for Feature Extraction =====
weights = ResNet50_Weights.DEFAULT
model = resnet50(weights=weights)
model.eval()
model = torch.nn.Sequential(*(list(model.children())[:-1]))  # Remove classifier layer

# ===== Transform for Image Preprocessing =====
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# ===== Feature Extraction Function =====
def extract_feature(img: Image.Image) -> np.ndarray:
    img_tensor = transform(img).unsqueeze(0)
    with torch.no_grad():
        vec = model(img_tensor).squeeze().numpy()
    return np.expand_dims(vec.astype("float32"), axis=0)

# ===== Cosine Similarity Function =====
def cosine_similarity(query_vec, feature_matrix, top_k=3):
    query_norm = query_vec / np.linalg.norm(query_vec)
    sims = np.dot(feature_matrix, query_norm.T).flatten()
    top_indices = np.argsort(sims)[-top_k:][::-1]
    return top_indices, sims[top_indices]

# ===== Endpoint: Art Theft Detection =====
@app.post("/detect-art-theft/")
async def detect_art_theft(file: UploadFile = File(...), use_cosine: bool = False):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        query_feature = extract_feature(image)

        if use_cosine:
            # Cosine similarity logic
            top_indices, top_scores = cosine_similarity(query_feature[0], norm_features)
            matches = [image_paths[i] for i in top_indices]
            scores = [float(s) for s in top_scores]
            return JSONResponse(content={"matches": matches, "cosine_similarities": scores})
        else:
            # FAISS L2 distance logic
            D, I = index.search(query_feature, k=3)
            matches = [image_paths[i] for i in I[0]]
            distances = [float(d) for d in D[0]]
            return JSONResponse(content={"matches": matches, "distances": distances})
        
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
    