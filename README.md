# Mum's Plant Care App

A lightweight Progressive Web App (PWA) for identifying plants and generating practical care guides from a camera upload. Made for my mum, based off other similar apps that required a subscription fee.
---

## Features

- **Camera Upload** – Capture or select plant photos on mobile or desktop.
- **Structured Advice** – Provides care difficulty, sunlight, pet safety, watering, planting, flowering, pruning, and pest information.
- **Visual Safety Badges** – Clearly highlights toxicity risks for pets.
- **PWA Enabled** – Install directly to iOS or Android home screens.

---

## Tech Stack

- **Backend:** Python, FastAPI, Uvicorn
- **Frontend:** HTML5, CSS3, JavaScript
- **AI Model:** Groq Vision API (`qwen/qwen3.6-27b`)
- **Deployment:** Render

---

## Project Structure

```text
.
├── main.py              # FastAPI backend & Groq API handler
├── requirements.txt     # Python dependencies
├── .env                 # Local environment variables
└── static/
    ├── index.html       # Main frontend
    ├── manifest.json    # PWA manifest
    ├── sw.js            # Service worker
    └── icon-192.png     # App icon
```

---

## How to Run Locally

### 1. Clone the Repository

### 2. Create a Virtual Environment

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` File

Create a file named `.env` in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### 5. Run the Application

```bash
uvicorn main:app --reload
```

Open your browser and visit:

```text
http://127.0.0.1:8000
```

---


## Deployment (Render)

1. Connect your repository to **Render** and create a **Web Service**.
2. Configure the service with the following settings:
   - **Runtime:** `Python 3`
   - **Build Command:**
     ```bash
     pip install -r requirements.txt
     ```
   - **Start Command:**
     ```bash
     uvicorn main:app --host 0.0.0.0 --port $PORT
     ```
3. Add your `GROQ_API_KEY` in the **Environment Variables** section of the Render dashboard.
4. Deploy the service. Render will build and start the application automatically.

---

## Home Screen Installation

### iOS (Safari)

1. Open the deployed app URL in **Safari**.
2. Tap the **Share** button.
3. Select **Add to Home Screen**.
4. Tap **Add**.

### Android (Chrome)

1. Open the deployed app URL in **Chrome**.
2. Tap the **Menu (⋮)** button.
3. Select **Add to Home screen** (or **Install App**, depending on your device).
4. Confirm by tapping **Add**.
