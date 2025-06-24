from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse, StreamingResponse
from PIL import Image, ImageDraw, ImageFont
import base64, io, requests
import numpy as np
import torch
import torchvision.transforms as transforms
from torchvision.models import resnet50, ResNet50_Weights
import faiss, pickle

app = FastAPI()

# === Load FAISS index and features ===
index = faiss.read_index("art_index.faiss")
with open("image_paths.pkl", "rb") as f:
    image_paths = pickle.load(f)
with open("features.pkl", "rb") as f:
    features = pickle.load(f)

norm_features = features / np.linalg.norm(features, axis=1, keepdims=True)

# === Load ResNet50 without final classification layer ===
weights = ResNet50_Weights.DEFAULT
model = resnet50(weights=weights)
model = torch.nn.Sequential(*list(model.children())[:-1])
model.eval()

# === Image Preprocessing ===
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

def extract_feature(img: Image.Image) -> np.ndarray:
    img_tensor = transform(img).unsqueeze(0)
    with torch.no_grad():
        vec = model(img_tensor).squeeze().numpy()
    return np.expand_dims(vec.astype("float32"), axis=0)

def cosine_similarity(query_vec, feature_matrix):
    query_norm = query_vec / np.linalg.norm(query_vec)
    sims = np.dot(feature_matrix, query_norm.T).flatten()
    return sims

# === Main Endpoint ===
@app.post("/process/")
async def process_image(prompt: str = Form(""), image: UploadFile = File(...)):
    try:
        # Load image
        contents = await image.read()
        input_image = Image.open(io.BytesIO(contents)).convert("RGB")

        # Step 1: Feature Extraction
        query_feature = extract_feature(input_image)

        # Step 2: FAISS L2 Search on entire dataset
        D, I = index.search(query_feature, k=10)
        faiss_matches = [image_paths[i] for i in I[0]]

        # Step 3: Cosine similarity only for top-3 FAISS matches
        top_features = norm_features[I[0][:3]]
        cos_scores = cosine_similarity(query_feature[0], top_features)
        top_cos_indices = np.argsort(cos_scores)[-3:][::-1]
        final_matches = [faiss_matches[i] for i in top_cos_indices]
        final_scores = [float(cos_scores[i]) for i in top_cos_indices]

        # Step 4: Stable Diffusion Call
        encoded_image = base64.b64encode(contents).decode("utf-8")
        control_image = f"data:image/png;base64,{encoded_image}"
        payload = {
            "init_images": [control_image],
            "steps": 20,
            "denoising_strength": 0.75,
            "alwayson_scripts": {
                "controlnet": {
                    "args": [{
                        "enabled": True,
                        "input_image": control_image,
                        "module": "invert",
                        "model": "control_v11p_sd15_scribble [d4ba51ff]",
                        "weight": 1.0,
                        "resize_mode": "Crop and Resize",
                        "guidance": 1.0,
                        "control_mode": "Balanced",
                        "pixel_perfect": True,
                        "control_guidance_start": 0,
                        "control_guidance_end": 1
                    }]
                }
            }
        }

        if prompt.strip():
            payload["prompt"] = prompt.strip()

        response = requests.post("http://127.0.0.1:7860/sdapi/v1/txt2img", json=payload)
        response.raise_for_status()
        output_image_b64 = response.json()["images"][0]
        output_bytes = base64.b64decode(output_image_b64)
        gen_image = Image.open(io.BytesIO(output_bytes)).convert("RGBA")

        # Step 5: Apply Watermark
        watermark_text = "© AI Generated"
        watermark_layer = Image.new("RGBA", gen_image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(watermark_layer)
        try:
            font = ImageFont.truetype("arial.ttf", 36)
        except IOError:
            font = ImageFont.load_default()

        text_bbox = draw.textbbox((0, 0), watermark_text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        x = gen_image.width - text_width - 10
        y = gen_image.height - text_height - 10
        draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, 128))
        final_image = Image.alpha_composite(gen_image, watermark_layer)

        # Final Image Response
        buffer = io.BytesIO()
        final_image.convert("RGB").save(buffer, format="PNG")
        buffer.seek(0)

        return StreamingResponse(buffer, media_type="image/png", headers={
            "X-Similar-Images": ", ".join(final_matches),
            "X-Cosine-Scores": ", ".join([f"{s:.4f}" for s in final_scores])
        })

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
