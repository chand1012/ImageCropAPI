from typing import Optional
from pydantic import BaseModel


class CropImage(BaseModel):
    base64_image: str
    height: int
    width: int
    x: int
    y: int
    image_format: Optional[str] = 'JPEG'


class ConvertImage(BaseModel):
    base64_image: str
    image_format: Optional[str] = 'JPEG'


class ResizeImage(BaseModel):
    base64_image: str
    image_format: Optional[str] = 'JPEG'
    width: int
    height: int
    resample: Optional[int] = 1


class Base64ImageResponse(BaseModel):
    image: str
