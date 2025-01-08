from fastapi import FastAPI
from app.database import Base, engine
from app.routes import users, clothes, locations, weather
from app.routes.weather import router as weather_router
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
import os

load_dotenv()

# テーブルを作成
Base.metadata.create_all(bind=engine)

# FastAPI アプリケーションのインスタンスを作成
app = FastAPI()

# 静的ファイルの設定
upload_dir = os.getenv("UPLOAD_DIR", "uploads")
app.mount("/uploads", StaticFiles(directory=upload_dir), name="uploads")

# CORS設定を追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        os.getenv("FRONTEND_URL", "https://weather-clothes-app.vercel.app")
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルートの登録
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(clothes.router, prefix="/clothes", tags=["Clothes"])
app.include_router(weather_router, prefix="/weather", tags=["Weather"])
app.include_router(locations.router, prefix="/locations", tags=["Locations"])
