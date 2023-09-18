import requests
from PIL import Image
from io import BytesIO

def is_valid_image(url):
    try:
        response = requests.get(url, stream=True, timeout=5)
        response.raise_for_status()
        content_type = response.headers.get('content-type')
        if content_type and 'image' in content_type:
            image = Image.open(BytesIO(response.content))
            image.verify()
            return True
    except:
        pass
    return False
