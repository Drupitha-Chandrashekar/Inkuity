import os
import io
import base64
import pickle
import requests
import numpy as np
import faiss
import torch
from io import BytesIO
from pathlib import Path
from fastapi.staticfiles import StaticFiles

import torchvision.transforms as transforms
from PIL import Image, ImageDraw, ImageFont
from torchvision.models import resnet50, ResNet50_Weights
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse, FileResponse
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware



# ========== FastAPI App Setup ==========
app = FastAPI(title="Art Theft Detection API",description="API for detecting similar artwork and generating images from sketches")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== Configuration ==========
BASE_DIR = Path(__file__).parent
ART_DIR = BASE_DIR / "art_images"  # Directory where your art images are stored
ART_DIR.mkdir(exist_ok=True)

# Mount static directory for serving images
app.mount("/art_images", StaticFiles(directory=ART_DIR), name="art_images")
app.mount("/artvee", StaticFiles(directory="D:/faiss3/artvee"), name="artvee")

# ========== Fix for PyTorch OpenMP ==========
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# ========== Load FAISS and Features ==========
try:
    index = faiss.read_index(str(BASE_DIR / "../art_index.faiss"))
    
    with open(BASE_DIR / "../image_paths.pkl", "rb") as f:
        image_paths = pickle.load(f)
    
    with open(BASE_DIR / "../features.pkl", "rb") as f:
        features = pickle.load(f)
    
    # Normalize features for cosine similarity
    norm_features = features / np.linalg.norm(features, axis=1, keepdims=True)
except Exception as e:
    raise RuntimeError(f"Failed to load FAISS index or features: {str(e)}")

# ========== Load Pretrained ResNet50 ==========
try:
    weights = ResNet50_Weights.DEFAULT
    model = resnet50(weights=weights)
    model.eval()
    model = torch.nn.Sequential(*(list(model.children())[:-1]))  # Remove final classification layer
    
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
except Exception as e:
    raise RuntimeError(f"Failed to load ResNet50 model: {str(e)}")

# ========== Helper Functions ==========
def extract_feature(img: Image.Image) -> np.ndarray:
    """Extract feature vector from image using ResNet50"""
    try:
        img_tensor = transform(img).unsqueeze(0)
        with torch.no_grad():
            vec = model(img_tensor).squeeze().numpy()
        return np.expand_dims(vec.astype("float32"), axis=0)
    except Exception as e:
        raise ValueError(f"Feature extraction failed: {str(e)}")

def cosine_similarity(query_vec, feature_matrix, top_k=3):
    """Calculate cosine similarity between query vector and feature matrix"""
    query_norm = query_vec / np.linalg.norm(query_vec)
    sims = np.dot(feature_matrix, query_norm.T).flatten()
    top_indices = np.argsort(sims)[-top_k:][::-1]
    return top_indices, sims[top_indices]

def validate_image(file: UploadFile):
    """Validate uploaded image file"""
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        contents = file.file.read()
        image = Image.open(BytesIO(contents)).convert("RGB")
        return image
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image file")

# ========== Endpoints ==========
@app.post("/detect-art-theft/")
async def detect_art_theft(
    file: UploadFile = File(..., description="Image file to check for similar artwork"),
    use_cosine: bool = Form(False, description="Use cosine similarity instead of FAISS distance")
):
    """
    Detect similar artwork in the database
    
    Parameters:
    - file: Uploaded image file
    - use_cosine: If True, uses cosine similarity instead of FAISS distance
    
    Returns:
    - matches: List of similar image paths
    - distances: List of distances (if use_cosine=False)
    - cosine_similarities: List of similarity scores (if use_cosine=True)
    """
    try:
        # Validate and process uploaded image
        image = validate_image(file)
        query_feature = extract_feature(image)
        
        # Find similar images
        if use_cosine:
            top_indices, top_scores = cosine_similarity(query_feature[0], norm_features)
            matches = [str(Path(image_paths[i]).relative_to(BASE_DIR.parent)) for i in top_indices]
            return JSONResponse(content={
                "matches": matches,
                "cosine_similarities": [float(s) for s in top_scores]
            })
        else:
            D, I = index.search(query_feature, k=3)
            matches = [str(Path(image_paths[i]).relative_to(BASE_DIR.parent)) for i in I[0]]
            return JSONResponse(content={
                "matches": matches,
                "distances": [float(d) for d in D[0]]
            })
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

@app.get("/art-image/{image_path:path}")
async def get_art_image(image_path: str):
    """Serve art images from the database"""
    try:
        full_path = BASE_DIR.parent / image_path
        if not full_path.exists():
            raise HTTPException(status_code=404, detail="Image not found")
        return FileResponse(full_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve image: {str(e)}")

# ========== Image Generation Endpoint ==========
SD_API = "http://127.0.0.1:7860/sdapi/v1"

@app.post("/generate-image/")
async def generate_image(
    prompt: Optional[str] = Form(None),
    image: UploadFile = File(...),
    denoising_strength: float = Form(0.75, ge=0.1, le=1.0),
    steps: int = Form(20, ge=1, le=150)
):
    """
    Generate an image from a sketch using Stable Diffusion
    
    Parameters:
    - prompt: Text prompt for image generation
    - image: Uploaded sketch image
    - denoising_strength: Control how much the image changes (0.1-1.0)
    - steps: Number of diffusion steps
    
    Returns:
    - Generated image as PNG
    """
    try:
        # Validate and encode image
        image_data = await image.read()
        encoded_image = base64.b64encode(image_data).decode("utf-8")
        control_image = f"data:image/png;base64,{encoded_image}"

        # Prepare payload for Stable Diffusion
        payload = {
            "init_images": [control_image],
            "steps": steps,
            "denoising_strength": denoising_strength,
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

        if prompt and prompt.strip():
            payload["prompt"] = prompt.strip()

        # Call Stable Diffusion API
        response = requests.post(f"{SD_API}/img2img", json=payload)
        response.raise_for_status()
        result = response.json()

        # Process and watermark the generated image
        output_image_b64 = result["images"][0]
        output_bytes = base64.b64decode(output_image_b64)
        image = Image.open(BytesIO(output_bytes)).convert("RGBA")
        
        # Add watermark
        watermark_layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(watermark_layer)
        
        try:
            font = ImageFont.truetype("arial.ttf", 36)
        except IOError:
            font = ImageFont.load_default()
        
        watermark_text = "© AI Generated"
        text_bbox = draw.textbbox((0, 0), watermark_text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        x = image.width - text_width - 10
        y = image.height - text_height - 10
        draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, 128))
        
        watermarked_image = Image.alpha_composite(image, watermark_layer)
        
        # Return the image
        buffer = BytesIO()
        watermarked_image.convert("RGB").save(buffer, format="PNG")
        buffer.seek(0)
        
        return StreamingResponse(buffer, media_type="image/png")

    except requests.RequestException as e:
        raise HTTPException(
            status_code=502,
            detail=f"Stable Diffusion API error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Image generation failed: {str(e)}"
        )

# ========== Health Check ==========
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Art theft detection service is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
    