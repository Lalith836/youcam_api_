import os
from typing import Optional
import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

load_dotenv()
app = FastAPI(title="Derma-Pilot API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    metrics: dict[str, int] = {}
    history: list[dict[str, str]] = []

class ScanResponse(BaseModel):
    metrics: dict[str, int]
    score: int
    demo: bool = True
    note: str = "Simulated demo values; not a medical assessment."

@app.get("/api/health")
async def health():
    return {"ok": True, "groq_configured": bool(os.getenv("GROQ_API_KEY"))}

@app.post("/api/scan", response_model=ScanResponse)
async def scan_demo():
    # Intentionally simulated. Do not present this as genuine image-based diagnosis.
    metrics = {"hydration": 54, "redness": 32, "spots": 38, "wrinkles": 24, "acne": 41, "oil": 47}
    score = round(100 - (100 - metrics["hydration"] + metrics["redness"] + metrics["spots"] +
                         metrics["wrinkles"] + metrics["acne"] + metrics["oil"]) / 6)
    return ScanResponse(metrics=metrics, score=score)

@app.post("/api/chat")
async def chat(req: ChatRequest):
    key = os.getenv("GROQ_API_KEY", "").strip()
    if not key:
        return {
            "reply": (
                "Demo mode: add GROQ_API_KEY to backend/.env to enable the AI assistant. "
                "For now, keep the routine gentle, introduce one new product at a time, "
                "and use broad-spectrum SPF in the morning. I can't diagnose skin conditions."
            ),
            "demo": True,
        }
    model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    system = (
        "You are Derma-Pilot, an informational skincare assistant. Be concise, kind, and cautious. "
        "You are not a doctor and must not diagnose a condition or promise results. Do not claim to "
        "analyze an image unless an actual image-analysis provider was used. Explain that persistent, "
        "painful, rapidly worsening, or concerning symptoms should be assessed by a qualified clinician. "
        "Avoid prescribing medication. Recommend patch testing and introducing active ingredients gradually. "
        "When discussing ingredient combinations, describe irritation risk conservatively and suggest "
        "professional advice for sensitive skin. The user's metric values are sample demo data, not clinical facts."
    )
    messages = [{"role": "system", "content": system}]
    for item in req.history[-8:]:
        role = item.get("role")
        content = item.get("content", "")
        if role in ("user", "assistant") and content:
            messages.append({"role": role, "content": content[:2000]})
    messages.append({
        "role": "user",
        "content": f"Sample dashboard metrics (not clinical measurements): {req.metrics}\nQuestion: {req.message}"
    })
    try:
        async with httpx.AsyncClient(timeout=35) as client:
            response = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                json={"model": model, "messages": messages, "temperature": 0.35, "max_tokens": 500},
            )
        if response.status_code >= 400:
            raise HTTPException(status_code=502, detail="Groq request failed. Check the model name and API key in backend/.env.")
        data = response.json()
        reply = data["choices"][0]["message"]["content"].strip()
        return {"reply": reply, "demo": False}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=502, detail="Could not reach Groq. Check your connection and backend logs.")
