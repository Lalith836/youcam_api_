# Derma-Pilot AI — Demo project

A polished, responsive skincare companion prototype built with React, Vite, Recharts, Lucide icons, FastAPI and Groq. The interface is designed for desktop, tablet and mobile, with a mobile drawer and bottom navigation.

## Features

- Premium skincare dashboard with responsive layouts, animated cards, progress ring and trend chart
- Skin journey view with selectable illustrative trend data
- Morning/evening routine checklist with completion state
- Ingredient keyword pairing demo and educational ingredient guide
- AI skin coach connected to the FastAPI backend; uses Groq when an API key is configured
- Camera preview and photo upload UI in the demo scan flow
- Responsive mobile navigation, accessible button labels, reduced-motion support
- No real image-based skin analysis is claimed: the scan and dashboard measurements are simulated demo values

## Requirements

- Node.js 18+ and npm
- Python 3.10+
- A Groq API key for live AI chat (optional; without it the backend responds in demo mode)

## Run the backend (PowerShell)

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `backend/.env` and add your own key:

```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

Get a key at https://console.groq.com/keys. Keep the key in `backend/.env`; never put it in frontend code or commit it to GitHub.

Start the API from the `backend` folder:

```powershell
uvicorn main:app --reload --port 8000
```

API health check: http://localhost:8000/api/health

## Run the frontend (second terminal)

```powershell
cd frontend
npm install
npm run dev
```

Open the local Vite URL, usually http://localhost:5173.

Create a production bundle with:

```powershell
npm run build
npm run preview
```

## Demo notes for judges

- The dashboard scores, progress trends, product names/prices, and product-fit percentages are sample content.
- The scan flow accepts a photo or camera preview for UI demonstration only. The uploaded image is not sent to an image-analysis service, and results remain simulated.
- Groq powers text-based chat only after the backend key is configured. Groq chat is not an image-based skin assessment.
- The ingredient checker is a basic keyword demo, not a complete compatibility/safety engine.
- Product imagery and fonts load from external sources, so an internet connection improves the visual experience.
- The interface offers general skincare education, not medical diagnosis or treatment.
