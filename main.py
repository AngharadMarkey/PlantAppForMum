import os
import json
import io
import base64
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse, Response
from groq import Groq

load_dotenv()

app = FastAPI(title="Mum's Plant Care App")

# Initialize Groq client
groq_key = os.getenv("GROQ_API_KEY")
groq_client = Groq(api_key=groq_key) if groq_key else None

PROMPT = """
Identify the plant or flower in this image and provide practical garden care advice.

Return ONLY a valid, raw JSON object matching this schema.
Do NOT use escaped newlines (\\n), backslashes, or markdown quotes inside any field values:

{
  "plant_name": "Common Name (Latin Name)",
  "quick_summary": "1-2 sentence overview of what this plant is.",
  "care_difficulty": "Easy / Moderate / Hard",
  "pet_safety": "Safe for Pets OR Toxic to Dogs/Cats",
  "sunlight": "Full Sun / Partial Shade / Full Shade",
  "watering_needs": "Watering frequency and advice",
  "best_time_to_plant": "When and where to plant",
  "flowering_duration": "Flowering period and duration",
  "pruning_advice": "Pruning / deadheading guidance",
  "common_pests": "Key pests and quick tips"
}
"""

@app.post("/api/identify")
async def identify_plant(file: UploadFile = File(...)):
    if not os.getenv("GROQ_API_KEY"):
        raise HTTPException(
            status_code=500, 
            detail="GROQ_API_KEY environment variable is not configured in .env!"
        )

    try:
        # Read image bytes and encode to base64
        contents = await file.read()
        base64_image = base64.b64encode(contents).decode('utf-8')

        # Send request to Groq Vision
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": PROMPT},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                            },
                        },
                    ],
                }
            ],
            model="qwen/qwen3.6-27b",  # <--- Updated active vision model string
            response_format={"type": "json_object"}
        )

        response_text = chat_completion.choices[0].message.content
        return JSONResponse(content=json.loads(response_text))

    except Exception as e:
        print(f"API Error: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

# ---------------------------------------------------------------------------
# PWA STATIC FILES & ROUTING
# ---------------------------------------------------------------------------
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def serve_index():
    return FileResponse("static/index.html")

@app.get("/manifest.json")
async def serve_manifest():
    return FileResponse("static/manifest.json")

@app.get("/sw.js")
async def serve_sw():
    return FileResponse("static/sw.js", media_type="application/javascript")

@app.get("/icon-192.png")
async def serve_icon():
    icon_path = "static/icon-192.png"
    if os.path.exists(icon_path):
        return FileResponse(icon_path)
    return Response(status_code=204)