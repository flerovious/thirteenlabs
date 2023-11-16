# youtube_processing.py

from llama_index.readers import YoutubeTranscriptReader
from llama_index.indices import GPTListIndex


# Function to process YouTube URL
def process_youtube_url(youtube_url):
    reader = YoutubeTranscriptReader(
        collection_name="youtube_collection",
        persist_directory="data_connectors/youtube_collection"
    )

    documents = reader.load_data(ytlinks=[youtube_url])
    index = GPTListIndex.from_documents(documents)

    return index.as_query_engine()


# Function to handle search query
def handle_search_query(query_engine, query_text):
    response = query_engine.query(query_text)
    return response
