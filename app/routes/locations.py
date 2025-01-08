from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Prefecture
from typing import List
from app.schemas import PrefectureSchema  # Pydantic スキーマをインポート

router = APIRouter()

@router.get("/", response_model=List[PrefectureSchema])
def get_locations(db: Session = Depends(get_db)):
    """
    都道府県リストを取得するエンドポイント
    """
    locations = db.query(Prefecture).all()
    return locations
