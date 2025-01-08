from pydantic import BaseModel

class PrefectureSchema(BaseModel):
    id: int
    name: str
    en_name: str
    latitude: float
    longitude: float

    class Config:
        # `orm_mode` の代わりに `from_attributes` を指定
        from_attributes = True
