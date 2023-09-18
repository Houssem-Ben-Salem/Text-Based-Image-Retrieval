from elasticsearch import Elasticsearch
import config

es = Elasticsearch(hosts=config.ES_HOSTS)

def start_elasticsearch_scroll(batch_size=config.BATCH_SIZE):
    """
    Start a new scroll and fetch the first batch of results.
    Returns the scroll ID and the batch of images.
    """
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
        "size": batch_size
    }
    response = es.search(index=config.INDEX_NAME, body=query_body, scroll='1m')
    return response['_scroll_id'], response['hits']['hits']

def continue_elasticsearch_scroll(scroll_id, batch_size=config.BATCH_SIZE):
    """
    Continue an existing scroll using the given scroll ID.
    Returns the updated scroll ID and the next batch of images.
    """
    response = es.scroll(scroll_id=scroll_id, scroll='1m')
    return response['_scroll_id'], response['hits']['hits']

def fetch_batch_from_elasticsearch(start_from=0, batch_size=config.BATCH_SIZE):
    body = {
        "query": {
            "match_all": {}
        },
        "size": batch_size,
        "from": start_from
    }
    response = es.search(index=config.INDEX_NAME, body=body)
    return response.get('hits', {}).get('hits', [])

def update_image_validity(id, is_valid):
    body = {
        "doc": {
            "is_valid": is_valid
        }
    }
    es.update(index=config.INDEX_NAME, id=id, body=body)
