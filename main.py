import os
import json
import asyncio
import random
from datetime import datetime
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

app = FastAPI(title="Apex Performance Nexus Prototype")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Apex Performance Nexus Backend ✅"}


@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}


@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        from database import db
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except ImportError:
        response["database"] = "❌ Database module not found"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response


def _random_biometrics() -> dict:
    """Generate a realistic-looking biometrics payload"""
    # Heart rate around athlete effort, include small variance
    hr_base = 140
    heart_rate = [max(45, random.gauss(hr_base, 3)) for _ in range(30)]
    payload = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "heartRate": heart_rate,
        "emgSignals": {"channels": [abs(random.gauss(0.25, 0.08)) for _ in range(8)]},
        "motionCapture": {"x": random.uniform(-1, 1), "y": random.uniform(0, 2), "z": random.uniform(-1, 1)},
        "oxygenSaturation": round(random.uniform(93, 99), 2),
        "lactateThreshold": round(random.uniform(3.5, 6.0), 2),
        "neuralActivity": {
            "alpha": round(random.uniform(8, 12), 2),
            "beta": round(random.uniform(12, 30), 2),
            "gamma": round(random.uniform(30, 45), 2),
            "delta": round(random.uniform(0.5, 4), 2),
            "theta": round(random.uniform(4, 8), 2),
        },
        "athleteId": "demo-athlete",
        "sessionId": "demo-session",
    }
    return payload


@app.get("/api/biometrics/sample")
def biometrics_sample():
    return _random_biometrics()


async def biometrics_event_stream() -> AsyncGenerator[bytes, None]:
    """Simple Server-Sent Events stream that emits biometrics frames ~5Hz"""
    try:
        while True:
            data = _random_biometrics()
            msg = f"data: {json.dumps(data)}\n\n"
            yield msg.encode("utf-8")
            await asyncio.sleep(0.2)
    except asyncio.CancelledError:
        return


@app.get("/api/biometrics/stream")
async def biometrics_stream():
    return StreamingResponse(biometrics_event_stream(), media_type="text/event-stream")


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
