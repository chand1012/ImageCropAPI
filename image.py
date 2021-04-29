# all image functions

from io import BytesIO
from typing import Optional

from PIL import Image


def crop(image_buffer: BytesIO, x: int, y: int, width: int, height: int, image_format: str) -> BytesIO:
    image = Image.open(image_buffer)

    output = BytesIO()

    cropped_image = image.crop((x, y, width+x, height+y))

    cropped_image.save(output, image_format.upper())

    output.seek(0)

    image.close()
    image_buffer.close()
    cropped_image.close()

    return output


def convert(image_buffer: BytesIO, image_format: str) -> BytesIO:
    image = Image.open(image_buffer)

    output = BytesIO()

    image.save(output, image_format.upper())

    output.seek(0)

    image_buffer.close()
    image.close()

    return output


def resize(image_buffer: BytesIO, width: int, height: int, image_format: str, resample: int = 1) -> BytesIO:

    image = Image.open(image_buffer)
    output = BytesIO()
    resized = image.resize((width, height), resample=resample)
    resized.save(output, format=image_format)
    output.seek(0)
    image.close()
    image_buffer.close()
    resized.close()

    return output
