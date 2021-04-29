import base64
from io import BytesIO
from typing import Optional

import requests
from fastapi import FastAPI, HTTPException
from starlette.responses import RedirectResponse, Response, FileResponse

from image import convert, crop, resize
from lib import get_b64_size
from models import ConvertImage, CropImage, ResizeImage

app = FastAPI()


@app.get("/", response_class=RedirectResponse)
async def index():
    """
    Redirects to the docs.
    """
    return RedirectResponse(url="/redoc")


@app.get("/crop/", response_class=FileResponse)
async def crop_remote(url: str = 'https://s.gravatar.com/avatar/434d67e1ebc4109956d035077ef5adb8', height: int = 250, width: int = 250, x: int = 0, y: int = 0, image_format: str = 'JPEG'):
    """
    Crops an image at the specified URL. 

     * Variable `url` specifies the remote URL to pull the image from.
     * Variables `x` and `y` specify the origin point of the crop. 
     * The variables `width` and `height` specify the width and height of the output crop. 
     * The `image_format` variable can be any output format supported by Pillow. See here: https://tinyurl.com/yymmmpwk
     * Output is a an image file. Defaults to JPEG.
    """
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code,
                            detail=f'Server returned error {response.status_code}.')

    if len(response.content) > 20971520:
        raise HTTPException(status_code=413, detail="Content is too large.")

    print(image_format)

    content = BytesIO(response.content)
    content.seek(0)

    image_buffer = crop(content, x, y, width, height, image_format)

    content.close()

    return Response(image_buffer.getvalue(), status_code=200)


@app.post("/crop/", response_class=FileResponse)
async def crop_local(data: CropImage):
    """
    Crop the specified base64 image. Image must be in the form of a base64 string, regardless of format. See here for supported formats: https://tinyurl.com/yymmmpwk

     * Variable `url` specifies the remote URL to pull the image from.
     * Variables `x` and `y` specify the origin point of the crop. 
     * The variables `width` and `height` specify the width and height of the output crop. 
     * The `image_format` variable can be any output format supported by Pillow. See here: https://tinyurl.com/yymmmpwk
     * Output is a an image file. Defaults to JPEG.
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

    image_buffer = crop(content, x, y, width, height, image_format)

    content.close()

    return Response(image_buffer.getvalue(), status_code=200)


@app.get("/convert/", response_class=FileResponse)
async def convert_remote(url: str = 'https://s.gravatar.com/avatar/434d67e1ebc4109956d035077ef5adb8', image_format: str = 'JPEG'):
    """
    Converts image at specified URL to specified format. JPEG is assumed if no format specified. Allowed formats: https://tinyurl.com/yymmmpwk
    """
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code,
                            detail=f'Server returned error {response.status_code}.')

    if len(response.content) > 20971520:
        raise HTTPException(status_code=413, detail="Content is too large.")

    content = BytesIO(response.content)
    content.seek(0)

    image_buffer = convert(content, image_format)

    content.close()

    return Response(image_buffer.getvalue(), status_code=200)


@app.post("/convert/", response_class=FileResponse)
async def convert_local(data: ConvertImage):
    """
    Converts incoming base64 images of any compatible formats to the specified output format. If no format specified, JPEG is assumed. See here for compatible incoming and outgoing formats: https://tinyurl.com/yymmmpwk
    """
    b64_image = data.get('base64_image')

    if get_b64_size(b64_image) > 20971520:
        raise HTTPException(status_code=413, detail="Content is too large.")

    image_format = data.get('image_format')

    content = BytesIO(base64.b64decode(b64_image))
    content.seek(0)

    image_buffer = convert(content, image_format)

    content.close()

    return Response(image_buffer.getvalue(), status_code=200)


@app.get("/resize/", response_class=FileResponse)
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
     * Output is a an image file. Defaults to JPEG.
    """
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code,
                            detail=f'Server returned error {response.status_code}.')

    if len(response.content) > 20971520:
        raise HTTPException(status_code=413, detail="Content is too large.")

    content = BytesIO(response.content)
    content.seek(0)

    image_buffer = resize(content, width, height, image_format, resample)

    content.close()

    return Response(image_buffer.getvalue(), status_code=200)


@app.post("/resize/", response_class=FileResponse)
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
     * Output is a an image file. Defaults to JPEG.
    """
    b64_image = data.get('base64_image')

    if get_b64_size(b64_image) > 20971520:
        raise HTTPException(status_code=413, detail="Content is too large.")

    image_format = data.get('image_format')
    width = data.get('width')
    height = data.get('height')
    resample = data.get('resample')

    content = BytesIO(base64.b64decode(b64_image))
    content.seek(0)

    image_buffer = resize(content, width, height, image_format, resample)

    content.close()

    return Response(image_buffer.getvalue(), status_code=200)
