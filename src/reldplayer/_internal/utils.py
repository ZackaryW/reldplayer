from functools import cache
from PIL import Image
import base64
import io
import PIL.Image

@cache
def base64_to_image(base64_str: str) -> Image.Image:
    img = PIL.Image.open(io.BytesIO(base64.b64decode(base64_str)))
    return img
