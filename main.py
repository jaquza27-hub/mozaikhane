from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import time

app = FastAPI(title="MozaikHane API", version="1.0")

# CORS ayarları (Tüm cihazlardan ve domainlerden gelen isteklere izin verilir)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ortak Bellek / Veritabanı Simülasyonu (Üretimde SQLite veya PostgreSQL'e bağlanabilir)
database = {
    "stats": {
        "total_visitors": 0,
        "active_users": 1
    },
    "grids": {} # Her kategori için kiralama verileri burada tutulacak
}

class GridUpdateModel(BaseModel.Data):
    grid_data: dict

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
def save_grid(category: str, payload: dict):
    database["grids"][category] = payload.get("grid_data", {})
    return {"status": "success", "category": category}