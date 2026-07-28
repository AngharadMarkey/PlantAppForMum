import os
import json
import io
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from google import genai
from google.genai import types
from PIL import Image

app = FastAPI(title="Mum's Plant Care App")

# ---------------------------------------------------------------------------
# GEMINI API SETUP
# ---------------------------------------------------------------------------
# Render will inject GEMINI_API_KEY from Environment Variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

PROMPT = """
Identify the plant or flower in this image. 
Provide practical garden care advice.

Return ONLY a valid JSON object matching this schema (do not wrap in markdown quotes):
{
  "plant_name": "Common Name (Latin Name)",
  "best_time_to_plant": "When and where to plant",
  "watering_needs": "Watering frequency and volume",
  "flowering_duration": "Flowering period and duration",
  "pruning_advice": "Pruning / cutting back guidance (e.g., deadheading advice)",
  "sunlight": "Sunlight requirements"
}
"""

@app.post("/api/identify")
async def identify_plant(file: UploadFile = File(...)):
    if not client:
        raise HTTPException(
            status_code=500, 
            detail="GEMINI_API_KEY environment variable is not configured on the server."
        )

    try:
        # Process input image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))

        # Query Gemini 2.0 Flash
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=[PROMPT, image],
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )

        return JSONResponse(content=json.loads(response.text))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

# ---------------------------------------------------------------------------
# PWA STATIC FILES & ROUTING
# ---------------------------------------------------------------------------
# Serve static assets (manifest, service worker, icons, CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve main PWA index at root
@app.get("/")
async def serve_index():
    return FileResponse("static/index.html")

# Root aliases for PWA manifest & service worker compliance on iOS Safari
@app.get("/manifest.json")
async def serve_manifest():
    return FileResponse("static/manifest.json")

@app.get("/sw.js")
async def serve_sw():
    return FileResponse("static/sw.js", media_type="application/javascript")

@app.get("/icon-192.png")
async def serve_icon():
    return FileResponse("static/icon-192.png")