from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict

app = FastAPI(title="MozaikHane API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ortak Bellek Veritabanı
database = {
    "stats": {
        "total_visitors": 0,
        "active_users": 1
    },
    "grids": {} 
}

class GridPayload(BaseModel):
    grid_data: Dict[str, Any] = {}

@app.get("/api/stats")
def get_stats():
    return database["stats"]

@app.post("/api/stats/visit")
def increment_visitor():
    database["stats"]["total_visitors"] += 1
    return {"total_visitors": database["stats"]["total_visitors"]}

@app.get("/api/grid/{category}")
def get_grid(category: str):
    return database["grids"].get(category, {})

@app.post("/api/grid/{category}")
def save_grid(category: str, payload: Dict[str, Any]):
    # Gelen veri ister direkt dict olsun ister grid_data içinde gelsin, ikisini de yakala
    if "grid_data" in payload:
        database["grids"][category] = payload["grid_data"]
    else:
        database["grids"][category] = payload
    return {"status": "success", "category": category, "saved_items": len(database["grids"][category])}
