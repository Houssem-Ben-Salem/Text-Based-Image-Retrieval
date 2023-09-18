# image_validation.py
from elasticsearch import Elasticsearch
import requests
from PIL import Image
from io import BytesIO
import logging

# Set up logging
logging.basicConfig(filename="image_validation.log", level=logging.INFO)

es = Elasticsearch(hosts=["http://localhost:9200"])

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

def validate_and_flag_images():
    # Initial search to start the scrolling
    query_body = {
        "query": {
            "bool": {
                "must_not": {
                    "exists": {
                        "field": "is_valid"
                    }
                }
            }
        },
        "size": 1000  # Using a smaller chunk size for better management with Scroll API
    }
    
    page = es.search(
        index='flickrdata',
        scroll='2m',
        body=query_body
    )
    
    sid = page['_scroll_id']
    scroll_size = len(page['hits']['hits'])

    while scroll_size > 0:
        for image in page['hits']['hits']:
            image_url = image['_source']['image_url']
            is_valid = is_valid_image(image_url)
            
            es.update(
                index="flickrdata",
                id=image['_id'],
                body={
                    "doc": {
                        "is_valid": is_valid
                    }
                }
            )

            logging.info(f"Processed image with ID: {image['_id']}")

        # Use the scroll API to get the next batch of images
        page = es.scroll(scroll_id=sid, scroll='2m')
        sid = page['_scroll_id']
        scroll_size = len(page['hits']['hits'])

if __name__ == "__main__":
    validate_and_flag_images()