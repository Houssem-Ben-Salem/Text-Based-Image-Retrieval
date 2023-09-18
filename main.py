import concurrent.futures
import config
from es_operations import start_elasticsearch_scroll, continue_elasticsearch_scroll, update_image_validity
from image_validator import is_valid_image
import logging
from logger_setup import setup_logger

# Setting up the logger
setup_logger()

def validate_and_update(image_data):
    image_url = image_data['_source']['image_url']
    is_valid = is_valid_image(image_url)
    
    # Update the Elasticsearch index to flag this image.
    update_image_validity(image_data['_id'], is_valid)

    # Logging for progress tracking
    logging.info(f"Processed image with ID: {image_data['_id']}. Valid: {is_valid}")

def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=config.MAX_WORKERS) as executor:
        # Start the Scroll API and fetch the first batch
        scroll_id, image_batch = start_elasticsearch_scroll()

        while image_batch:  # Continue as long as there are images in the batch
            logging.info(f"Processing batch with Scroll ID: {scroll_id}")
            executor.map(validate_and_update, image_batch)

            # Fetch the next batch using Scroll API
            scroll_id, image_batch = continue_elasticsearch_scroll(scroll_id)

if __name__ == "__main__":
    main()