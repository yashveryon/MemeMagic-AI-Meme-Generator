from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse, Response
from models.meme_captioning import (
    generate_caption_from_image,
    generate_funny_meme_text,
    create_meme,
    generate_gif_from_meme  # 🆕 import GIF generator
)
import shutil
import os

router = APIRouter(
    prefix="/meme",
    tags=["Meme Generator"]
)

@router.post("/generate")
async def generate_meme(
    file: UploadFile = File(...),
    custom_caption: str = Form(None),
    temperature: float = Form(0.7)  # 🔥 NEW: Accept temperature from frontend
):
    try:
        # Step 1: Save uploaded image temporarily
        temp_path = "temp_uploaded_image.jpg"
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        print("📁 Uploaded image saved.")

        # Step 2: Use custom caption if provided, else generate via BLIP + Mistral
        if custom_caption:
            caption = custom_caption.strip()
            print("✏️ Using custom caption:", caption)
        else:
            description = generate_caption_from_image(temp_path)
            caption = generate_funny_meme_text(description, temperature=temperature)  # 🔥 Use temperature

        # Step 3: Draw caption onto the image
        output_path = "output_meme.jpg"
        create_meme(temp_path, caption, output_path)

        # Step 4: Cleanup temporary file
        os.remove(temp_path)

        print("✅ Meme generated:", output_path)

        # Step 5: Return image with caption in header
        response = FileResponse(output_path, media_type="image/jpeg")
        response.headers["X-Caption"] = caption
        return response

    except Exception as e:
        print("❌ Error:", str(e))
        raise HTTPException(status_code=500, detail=f"Something went wrong: {str(e)}")

# 🆕 Endpoint for GIF generation on demand
@router.post("/gif")
async def convert_meme_to_gif():
    try:
        input_path = "output_meme.jpg"
        output_path = "output_meme.gif"

        if not os.path.exists(input_path):
            raise HTTPException(status_code=404, detail="Meme image not found.")

        generate_gif_from_meme(input_path, output_path)
        print("🎞️ Meme converted to GIF.")
        return FileResponse(output_path, media_type="image/gif")

    except Exception as e:
        print("❌ GIF Generation Error:", str(e))
        raise HTTPException(status_code=500, detail=f"GIF generation failed: {str(e)}")
