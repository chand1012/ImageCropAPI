import base64
from io import BytesIO

import requests
from fastapi import FastAPI, HTTPException
from PIL import Image

from models import ConvertImage, CropImage

app = FastAPI()

@app.get("/crop/")
async def get_and_crop(url: str = 'https://s.gravatar.com/avatar/434d67e1ebc4109956d035077ef5adb8', height: int = 250, width: int = 250, x: int = 0, y: int = 0, image_format: str = 'JPEG'):
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=f'Server returned error {response.status_code}.')

    image = Image.open(BytesIO(response.content))

    cropped_image = image.crop((x, y, width+x, height+y))

    image_buffer = BytesIO()

    cropped_image.save(image_buffer, format=image_format)
    cropped_image.close()

    b64_image = base64.b64encode(image_buffer.getvalue())
    image_buffer.close()

    return {'image': b64_image}

@app.post("/crop/")
async def get_and_crop_post(data: CropImage):
    b64_image = data.get('base64_image')
    height = data.get('height')
    width = data.get('width')
    x = data.get('x')
    y = data.get('y')
    image_format = data.get('image_format')

    image = Image.open(BytesIO(base64.b64decode(b64_image)))

    cropped_image = image.crop((x, y, width+x, height+y))

    image_buffer = BytesIO()

    cropped_image.save(image_buffer, format=image_format)
    cropped_image.close()

    b64_image = base64.b64encode(image_buffer.getvalue())
    image_buffer.close()

    return {'image': b64_image}

@app.get("/convert/")
async def convert_remote(url: str = 'https://s.gravatar.com/avatar/434d67e1ebc4109956d035077ef5adb8', image_format: str = 'JPEG'): # see here for supported formats: https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=f'Server returned error {response.status_code}.')

    image = Image.open(BytesIO(response.content))

    image_buffer = BytesIO()

    image.save(image_buffer, format=image_format)
    image.close()

    b64_image = base64.b64encode(image_buffer.getvalue())
    image_buffer.close()

    return {'image': b64_image}

@app.post("/convert/")
async def convert_local(data: ConvertImage):
    b64_image = data.get('url')
    image_format = data.get('image_format')

    image = Image.open(BytesIO(base64.b64decode(b64_image)))

    image_buffer = BytesIO()

    image.save(image_buffer, format=image_format)
    image.close()

    b64_image = base64.b64encode(image_buffer.getvalue())
    image_buffer.close()

    return {'image': b64_image}

