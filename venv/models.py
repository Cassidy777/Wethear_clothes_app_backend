from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, TIMESTAMP
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    # リレーション
    clothes = relationship("Clothing", back_populates="user")
    favorites = relationship("FavoriteLocation", back_populates="user")

class Prefecture(Base):
    __tablename__ = "prefectures"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    en_name = Column(String)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

class FavoriteLocation(Base):
    __tablename__ = "favorite_locations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    prefecture_id = Column(Integer, ForeignKey("prefectures.id"), nullable=False)

    user = relationship("User", back_populates="favorites")
    prefecture = relationship("Prefecture")

class Clothing(Base):
    __tablename__ = "clothing"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    image_url = Column(String)
    warmth_level = Column(Integer)
    waterproof = Column(Boolean)
    item_type = Column(String)

    user = relationship("User", back_populates="clothes")
