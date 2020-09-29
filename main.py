import base64
from io import BytesIO
from typing import Optional

import requests
from fastapi import FastAPI, HTTPException
from PIL import Image
from starlette.responses import RedirectResponse

from lib import get_b64_size
from models import Base64ImageResponse, ConvertImage, CropImage, ResizeImage

app = FastAPI()

@app.get("/")
async def index():
    """
    Redirects to the docs.
    """
    return RedirectResponse(url="/redoc")

@app.get("/crop/", response_model=Base64ImageResponse)
async def crop_remote(url: str = 'https://s.gravatar.com/avatar/434d67e1ebc4109956d035077ef5adb8', height: int = 250, width: int = 250, x: int = 0, y: int = 0, image_format: str = 'JPEG'):
    """
    Crops an image at the specified URL. 

     * Variable `url` specifies the remote URL to pull the image from.
     * Variables `x` and `y` specify the origin point of the crop. 
     * The variables `width` and `height` specify the width and height of the output crop. 
     * The `image_format` variable can be any output format supported by Pillow. See here: https://tinyurl.com/yymmmpwk
     * Output is a JSON object containing exactly one variable: `image`. The string following is the base64 image in the format that was specified.
    """
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

@app.post("/crop/", response_model=Base64ImageResponse)
async def crop_local(data: CropImage):
    """
    Crop the specified base64 image. Image must be in the form of a base64 string, regardless of format. See here for supported formats: https://tinyurl.com/yymmmpwk
    
     * Variable `url` specifies the remote URL to pull the image from.
     * Variables `x` and `y` specify the origin point of the crop. 
     * The variables `width` and `height` specify the width and height of the output crop. 
     * The `image_format` variable can be any output format supported by Pillow. See here: https://tinyurl.com/yymmmpwk
     * Output is a JSON object containing exactly one variable: `image`. The string following is the base64 image in the format that was specified.
    """
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

@app.get("/convert/", response_model=Base64ImageResponse)
async def convert_remote(url: str = 'https://s.gravatar.com/avatar/434d67e1ebc4109956d035077ef5adb8', image_format: str = 'JPEG'):
    """
    Converts image at specified URL to specified format. JPEG is assumed if no format specified. Allowed formats: https://tinyurl.com/yymmmpwk
    """
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

@app.post("/convert/", response_model=Base64ImageResponse)
async def convert_local(data: ConvertImage):
    """
    Converts incoming base64 images of any compatible formats to the specified output format. If no format specified, JPEG is assumed. See here for compatible incoming and outgoing formats: https://tinyurl.com/yymmmpwk
    """
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

@app.get("/resize/", response_model=Base64ImageResponse)
async def resize_remote(url: str = 'https://s.gravatar.com/avatar/434d67e1ebc4109956d035077ef5adb8', height: int = 250, width: int = 250, image_format: str = 'JPEG', resample: Optional[int] = 1):
    """
    Resizes image at URL specified to the specified output resolution and format. 

     * `url` specifies the image URL.
     * The variables `width` and `height` specify the width and height of the output resize. 
     * The `image_format` variable can be any output format supported by Pillow. See here: https://tinyurl.com/yymmmpwk
     * Variable `resample` is used to specify the resample mode used by Pillow. See here: https://tinyurl.com/y3jo6aph
        * `Image.NEAREST = 0`
        * `Image.LANCZOS = 1`
        * `Image.BILINEAR = 2`
        * `Image.BICUBIC = 3`
        * `Image.BOX = 4`
        * `Image.HAMMING = 5`
     * Output is a JSON object containing exactly one variable: `image`. The string following is the base64 image in the format that was specified.
    """
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

@app.post("/resize/", response_model=Base64ImageResponse)
async def resize_local(data: ResizeImage):
    """
    Resizes incoming base64 image.

     * `b64_image` is the base64 image of any supported format. See here for supported inputs: https://tinyurl.com/yymmmpwk
     * The variables `width` and `height` specify the width and height of the output resize. 
     * The `image_format` variable can be any output format supported by Pillow. See here: https://tinyurl.com/yymmmpwk
     * Variable `resample` is used to specify the resample mode used by Pillow. See here: https://tinyurl.com/y3jo6aph
        * `Image.NEAREST = 0`
        * `Image.LANCZOS = 1`
        * `Image.BILINEAR = 2`
        * `Image.BICUBIC = 3`
        * `Image.BOX = 4`
        * `Image.HAMMING = 5`
     * Output is a JSON object containing exactly one variable: `image`. The string following is the base64 image in the format that was specified.
    """
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

