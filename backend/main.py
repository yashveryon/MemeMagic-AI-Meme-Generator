from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from backend.routers import meme  # Your meme router

app = FastAPI(
    title="MemeMagic - AI Meme Generator",
    description="Generate memes from images using AI-generated captions",
    version="1.0.0"
)

# ✅ Enable CORS so frontend can talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to "http://127.0.0.1:5500"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Mount static frontend files (HTML, CSS, JS)
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

# ✅ Serve generated memes from the root directory
app.mount("/memes", StaticFiles(directory="."), name="memes")

# ✅ Homepage loads your frontend index.html
@app.get("/", response_class=HTMLResponse)
async def read_index():
    try:
        with open("frontend/index.html", "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print("🔥 Error loading index.html:", e)
        return HTMLResponse(content="<h1>Internal Server Error</h1>", status_code=500)

# ✅ Meme generation routes (POST /meme/generate)
app.include_router(meme.router)
