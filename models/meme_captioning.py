from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import torch
import requests
import textwrap
import imageio

# Load BLIP model once
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def generate_caption_from_image(image_path: str) -> str:
    """Generate a visual description of the image using BLIP."""
    image = Image.open(image_path).convert("RGB")
    inputs = processor(image, return_tensors="pt")
    outputs = model.generate(**inputs)
    description = processor.decode(outputs[0], skip_special_tokens=True)
    print("🧠 Scene Description:", description)
    return description

def generate_funny_meme_text(description: str, temperature: float = 0.7) -> str:
    """Use Mistral (via Ollama) to generate a funny, sarcastic meme caption."""
    prompt = (
        f"You're an expert meme creator. Write one funny, sarcastic internet-style meme caption "
        f"for this scene:\n\n"
        f"{description}\n\n"
        f"Keep it witty, short, and relatable. Just return the meme caption only."
    )

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "temperature": temperature,  # 🔥 Now using dynamic temperature
                "stream": False
            }
        )
        response.raise_for_status()

        raw = response.json()["response"]
        print("🪵 Raw Mistral output:", raw)

        # Extract and clean first line only
        best_line = raw.strip().split('\n')[0]
        best_line = best_line.lstrip("1234567890. ").strip().strip('"')

        print("🤣 Meme Caption (used):", best_line)
        return best_line

    except Exception as e:
        print(f"⚠️ Failed to generate meme caption: {e}")
        return "When you fix one bug and five more appear."

def create_meme(image_path: str, caption: str, output_path: str):
    """Draw the meme caption onto the image and save it."""
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("arial.ttf", 36)
    except:
        font = ImageFont.load_default()

    # Wrap caption if too long
    wrapped_text = textwrap.fill(caption, width=40)

    # Calculate text position (centered horizontally, near bottom)
    text_bbox = draw.textbbox((0, 0), wrapped_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_x = (image.width - text_width) // 2
    text_y = image.height - text_height - 20

    # Draw black outline for readability
    outline_range = 2
    for dx in range(-outline_range, outline_range + 1):
        for dy in range(-outline_range, outline_range + 1):
            draw.text((text_x + dx, text_y + dy), wrapped_text, font=font, fill="black")

    # Draw white caption text
    draw.text((text_x, text_y), wrapped_text, font=font, fill="yellow")

    image.save(output_path)
    print("✅ Meme saved as:", output_path)

def generate_gif_from_meme(image_path="output_meme.jpg", output_gif="output_meme.gif"):
    """Generate a Giphy-style animated GIF from a meme image."""
    frames = []
    original = Image.open(image_path).convert("RGB")

    # Create fade-in effect
    for i in range(10):
        enhancer = ImageEnhance.Brightness(original)
        frame = enhancer.enhance(0.5 + (i / 20))
        frames.append(frame)

    # Create fade-out effect
    for i in range(10):
        enhancer = ImageEnhance.Brightness(original)
        frame = enhancer.enhance(1 - (i / 20))
        frames.append(frame)

    # Save animated GIF
    imageio.mimsave(output_gif, frames, duration=0.1, loop=0)
    print(f"🎞️ GIF saved as: {output_gif}")
