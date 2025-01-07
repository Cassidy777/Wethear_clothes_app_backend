from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Prefecture

router = APIRouter()

@router.get("/")
def get_locations(db: Session = Depends(get_db)):
    """
    都道府県リストを取得するエンドポイント
    """
    locations = db.query(Prefecture).all()
    if not locations:
        return {"error": "No locations found"}
    
    return [
        {
            "id": location.id,
            "name": location.name,
            "en_name": location.en_name,
            "latitude": location.latitude,
            "longitude": location.longitude,
        }
        for location in locations
    ]
