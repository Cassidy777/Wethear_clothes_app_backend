import requests
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Prefecture

router = APIRouter()

@router.get("/weather/{prefecture_id}")
def get_weather(prefecture_id: int, db: Session = Depends(get_db)):
    """
    都道府県の天気予報を取得するエンドポイント
    """
    # 都道府県情報を取得
    prefecture = db.query(Prefecture).filter(Prefecture.id == prefecture_id).first()
    if not prefecture:
        return {"error": "Prefecture not found"}  # 404 の原因

    print(f"Fetched Prefecture: {prefecture.name}, {prefecture.latitude}, {prefecture.longitude}")  # デバッグ用

    # Open-Meteo APIのURL
    url = f"https://api.open-meteo.com/v1/forecast"
    
    # APIに送信するパラメータ
    params = {
        "latitude": prefecture.latitude,
        "longitude": prefecture.longitude,
        "hourly": "temperature_2m,precipitation",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "current_weather": True,
        "timezone": "Asia/Tokyo",
    }

    # APIリクエスト
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return {"error": "Failed to fetch weather data"}  # 外部 API エラー

    # 結果をJSONで返す
    return response.json()
