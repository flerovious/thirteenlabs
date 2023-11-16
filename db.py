from llama_index.readers import YoutubeTranscriptReader
from llama_index import VectorStoreIndex
from llama_index.query_engine import CitationQueryEngine
from llama_index.response.schema import RESPONSE_TYPE
import streamlit as st
from dotenv import load_dotenv
import spacy
from spacy.cli.download import download

load_dotenv()


# Function to process YouTube URL
@st.cache_resource
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
        citation_chunk_size=32,
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
        text = source_node.node.get_text().replace("\n", " ")

        citations.append(
            {
                "text": text,
            }
        )

    return citations


@st.cache_resource
def download_spacy():
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")
    return nlp


def find_timestamp(top_citations_text, text_segments):
    best_similarity = 0
    best_match_timestamp = None
    nlp = download_spacy()

    for citation_text in top_citations_text:
        for segment in text_segments:
            citation_doc = nlp(citation_text)
            segment_doc = nlp(segment["text"])
            similarity = citation_doc.similarity(segment_doc)

            if similarity > best_similarity:
                best_similarity = similarity
                best_match_timestamp = segment["start"]

    return best_match_timestamp
