import streamlit as st
from elasticsearch import Elasticsearch
from googletrans import Translator  # Make sure to install this library

# --- Elasticsearch Setup ---
es = Elasticsearch(hosts=["http://localhost:9200"])

translator = Translator()

def search_elasticsearch(query, language, size=5, start_from=0):
    if language != "English":
        # Translate the query to English
        translated = translator.translate(query, src=language.lower(), dest='en')
        query = translated.text

    body = {
        "query": {
            "bool": {
                "must": {
                    "match": {
                        "tags": query
                    }
                },
                "filter": {
                    "term": {"is_valid": True}
                }
            }
        },
        "size": size,
        "from": start_from
    }
    response = es.search(index='flickrdata', body=body)
    return response

# --- Styling ---
st.markdown("""
<style>
    body {
        color: #fff;
        background-color: #4F8BF9;
    }
    .stButton>button {
        color: #4F8BF9;
        background-color: #fff;
        border-radius: 2em;
    }
</style>
    """, unsafe_allow_html=True)

# --- App Title ---
st.title('Flickr Image Search 🖼️')

st.write("Welcome to Flickr Image Search! Type in tags and find relevant images. Let's get started!")

# Inputs
with st.container():
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        query = st.text_input('Search for images by tags:', '')
    with col2:
        language = st.selectbox("Choose language:", ["English", "French", "Arabic", "Spanish", "German"])
    with col3:
        num_images = st.number_input('N° Images to Display', min_value=1, step=5, value=5)
    with col4:
        search_button = st.button('Search')

if search_button:
    if query:
        with st.spinner('Searching...'):
            results = search_elasticsearch(query, language, size=num_images)
            hits = results.get('hits', {}).get('hits', [])
                
        if not hits:
            st.info('No matching images found.')
        else:
            # Display images
            for i in range(0, len(hits), 3):
                row_images = [hit['_source']['image_url'] for hit in hits[i:i + 3]]
                image_row = st.columns(3)
                for j, image_url in enumerate(row_images):
                    with image_row[j]:
                        st.image(image_url, caption=f'Image {i + j + 1}', use_column_width=True)
