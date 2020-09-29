import base64
from base64 import b64encode
from io import BytesIO
from typing import Optional
from threading import Thread

import requests
from fastapi import FastAPI, HTTPException
from PIL import Image
from starlette.responses import RedirectResponse

from models import ConvertImage, CropImage, ResizeImage
from lib import get_b64_size

app = FastAPI()

@app.get("/")
async def index():
    return RedirectResponse(url="/docs")

@app.get("/crop/")
async def crop_remote(url: str = 'https://s.gravatar.com/avatar/434d67e1ebc4109956d035077ef5adb8', height: int = 250, width: int = 250, x: int = 0, y: int = 0, image_format: str = 'JPEG'):
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=f'Server returned error {response.status_code}.')

    if len(response.content) > 20971520:
        raise HTTPException(status_code=413, detail="Content is too large.")

    image_buffer = BytesIO()
    content = BytesIO(response.content)
    content.seek(0)
    image = Image.open(content)
    
    cropped_image = image.crop((x, y, width+x, height+y))
    cropped_image.save(image_buffer, format=image_format)
    
    b64_image = base64.b64encode(image_buffer.getvalue())

    image_buffer.close()
    cropped_image.close()
    content.close()
    cropped_image.close()
    
    return {'image': b64_image}

@app.post("/crop/")
async def crop_local(data: CropImage):
    b64_image = data.get('base64_image')

    if get_b64_size(b64_image) > 20971520:
        raise HTTPException(status_code=413, detail="Content is too large.")

    height = data.get('height')
    width = data.get('width')
    x = data.get('x')
    y = data.get('y')
    image_format = data.get('image_format')

    image_buffer = BytesIO()
    content = BytesIO(base64.b64decode(b64_image))
    content.seek(0)
    image = Image.open(content)

    cropped_image = image.crop((x, y, width+x, height+y))
    cropped_image.save(image_buffer, format=image_format)
    
    b64_image = base64.b64encode(image_buffer.getvalue())

    image_buffer.close()
    cropped_image.close()
    content.close()
    cropped_image.close()

    return {'image': b64_image}

@app.get("/convert/")
async def convert_remote(url: str = 'https://s.gravatar.com/avatar/434d67e1ebc4109956d035077ef5adb8', image_format: str = 'JPEG'): # see here for supported formats: https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=f'Server returned error {response.status_code}.')

    if len(response.content) > 20971520:
        raise HTTPException(status_code=413, detail="Content is too large.")
    
    image_buffer = BytesIO()
    content = BytesIO(response.content)
    content.seek(0)
    image = Image.open(content)
    
    image.save(image_buffer, format=image_format)
    
    b64_image = base64.b64encode(image_buffer.getvalue())

    image_buffer.close()
    content.close()
    image.close()

    return {'image': b64_image}

@app.post("/convert/")
async def convert_local(data: ConvertImage):
    b64_image = data.get('base64_image')

    if get_b64_size(b64_image) > 20971520:
        raise HTTPException(status_code=413, detail="Content is too large.")
    
    image_format = data.get('image_format')

    image_buffer = BytesIO()
    content = BytesIO(base64.b64decode(b64_image))
    content.seek(0)
    image = Image.open(content)
    
    image.save(image_buffer, format=image_format)
    
    b64_image = base64.b64encode(image_buffer.getvalue())
    
    image_buffer.close()
    content.close()
    image.close()

    return {'image': b64_image}

@app.get("/resize/")
async def resize_remote(url: str = 'https://s.gravatar.com/avatar/434d67e1ebc4109956d035077ef5adb8', height: int = 250, width: int = 250, image_format: str = 'JPEG', resample: Optional[int] = 1):
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=f'Server returned error {response.status_code}.')

    if len(response.content) > 20971520:
        raise HTTPException(status_code=413, detail="Content is too large.")
    
    image_buffer = BytesIO()
    content = BytesIO(response.content)
    content.seek(0)
    image = Image.open(content)

    resized = image.resize((width, height), resample=resample)
    resized.save(image_buffer, format=image_format)

    b64_image = base64.b64encode(image_buffer.getvalue())

    image_buffer.close()
    image.close()
    content.close()
    resized.close()

    return {'image': b64_image}

@app.post("/resize/")
async def resize_local(data: ResizeImage):
    b64_image = data.get('base64_image')

    if get_b64_size(b64_image) > 20971520:
        raise HTTPException(status_code=413, detail="Content is too large.")
    
    image_format = data.get('image_format')
    width = data.get('width')
    height = data.get('height')
    resample = data.get('resample')

    image_buffer = BytesIO()
    content = BytesIO(base64.b64decode(b64_image))
    content.seek(0)
    image = Image.open(content)

    resized = image.resize((width, height), resample=resample)
    resized.save(image_buffer, format=image_format)

    b64_image = base64.b64encode(image_buffer.getvalue())
    
    image.close()
    resized.close()
    content.close()
    image_buffer.close()

    return {'image':b64_image}

