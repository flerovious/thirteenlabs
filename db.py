# youtube_processing.py

from llama_index.readers import YoutubeTranscriptReader
from llama_index import VectorStoreIndex
from llama_index.query_engine import CitationQueryEngine
from llama_index.response.schema import RESPONSE_TYPE


# Function to process YouTube URL
def process_youtube_url(youtube_url: str):
    reader = YoutubeTranscriptReader(
        collection_name="youtube_collection",
        persist_directory="data_connectors/youtube_collection",
    )

    documents = reader.load_data(ytlinks=[youtube_url])
    index = VectorStoreIndex.from_documents(documents)

    query_engine = CitationQueryEngine.from_args(
        index,
        similarity_top_k=3,
        # here we can control how granular citation sources are, the default is 512
        citation_chunk_size=512,
    )

    return query_engine


# Function to handle search query
def handle_search_query(query_engine: CitationQueryEngine, query_text: str):
    response = query_engine.query(query_text)
    return response


# Function to get answer
def get_answer(response: RESPONSE_TYPE):
    return response.response


# Function to get text of top citations
def get_top_citations(response: RESPONSE_TYPE):
    citations = []
    for source_node in response.source_nodes:
        video_id = source_node.node.get_metadata_str().split()[-1]
        text = response.source_nodes[0].node.get_text().replace("\n", " ")

        citations.append(
            {
                "video_id": video_id,
                "text": text,
            }
        )
    return citations
