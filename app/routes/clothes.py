
import os
from fastapi import APIRouter, Depends, Query, Form, File, UploadFile
from sqlalchemy.orm import Session
from app.models import Clothing
from app.database import get_db
from typing import List

router = APIRouter()

@router.post("/upload-clothes")
async def upload_clothes(
    user_id: int = Form(...), 
    image: UploadFile = File(...), 
    warmth_level: int = Form(...), 
    waterproof: bool = Form(...), 
    item_type: str = Form(...), 
    db: Session = Depends(get_db)
):
    # 保存先ディレクトリのパス
    upload_dir = "uploads"

    # ディレクトリが存在しない場合は作成
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    
    # 画像保存の処理
    image_path = os.path.join(upload_dir, image.filename)
    with open(image_path, "wb") as f:
        f.write(await image.read())
    
    # データベース登録
    new_clothing = Clothing(
        user_id=user_id,
        image_url=image_path,
        warmth_level=warmth_level,
        waterproof=waterproof,
        item_type=item_type
    )
    db.add(new_clothing)
    db.commit()
    db.refresh(new_clothing)
    return {"message": "Clothing registered successfully", "clothing": new_clothing}

@router.get("/clothes/{user_id}")
def get_clothes(user_id: int, db: Session = Depends(get_db)):
    clothes = db.query(Clothing).filter(Clothing.user_id == user_id).all()
    return clothes

@router.get("/recommend-clothes")
def recommend_clothes(
    temperature: float = Query(...),  # 必須パラメータ: 気温
    is_raining: bool = Query(...),    # 必須パラメータ: 雨が降っているかどうか
    db: Session = Depends(get_db)
):
    """
    温度と雨の条件に基づいて服装を提案します。
    """

    # デフォルトで提案するアイテムタイプ
    item_types = ["トップス", "ボトムス", "アウター", "シューズ", "アクセサリー"]

    # 提案の初期化
    suggestions = {}

    # アイテムごとに条件を満たす服を選択
    for item_type in item_types:
        query = db.query(Clothing).filter(Clothing.item_type == item_type)

        # ロジック：気温と雨による条件分岐
        if temperature <= 1:
            if is_raining:
                # 1度以下かつ雨: 暖かさ5 & 防水
                query = query.filter(Clothing.warmth_level == 5, Clothing.waterproof == True)
            else:
                # 1度以下かつ晴れ: 暖かさ合計が23以上になるように提案
                query = query.order_by(Clothing.warmth_level.desc())
        elif 1 < temperature <= 10:
            if is_raining:
                # 1〜10度かつ雨: 暖かさ合計が22以上 & 防水
                query = query.filter(Clothing.waterproof == True).order_by(Clothing.warmth_level.desc())
            else:
                # 1〜10度かつ晴れ: 暖かさ合計が20以上
                query = query.order_by(Clothing.warmth_level.desc())
        elif 10 < temperature <= 18:
            if is_raining:
                # 10〜18度かつ雨: 暖かさ合計が15~20 & 防水
                query = query.filter(Clothing.waterproof == True).order_by(Clothing.warmth_level.desc())
            else:
                # 10〜18度かつ晴れ: 暖かさ合計が15~18
                query = query.order_by(Clothing.warmth_level.desc())
        elif 18 < temperature <= 25:
            if is_raining:
                # 18〜25度かつ雨: 暖かさ合計が10~15 & 防水
                query = query.filter(Clothing.waterproof == True).order_by(Clothing.warmth_level.asc())
            else:
                # 18〜25度かつ晴れ: 暖かさ合計が7~12
                query = query.order_by(Clothing.warmth_level.asc())
        elif temperature > 25:
            if is_raining:
                # 25度以上かつ雨: 暖かさ合計が7以下 & 防水
                query = query.filter(Clothing.waterproof == True).order_by(Clothing.warmth_level.asc())
            else:
                # 25度以上かつ晴れ: 暖かさ合計が5以下
                query = query.order_by(Clothing.warmth_level.asc())

        # 最適な服装を1つ選択
        suggestions[item_type] = query.first()

    # 提案を返す
    return [
        {
            "item_type": item_type,
            "warmth_level": suggestion.warmth_level if suggestion else None,
            "waterproof": suggestion.waterproof if suggestion else None,
            "image_url": suggestion.image_url if suggestion else None,
        }
        for item_type, suggestion in suggestions.items()
        if suggestion
    ]

