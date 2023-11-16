import os
import streamlit as st
from transcribe import convert_audio_to_txt, get_video_id, get_transcript
from logo import render_logo
import math
from db import get_answer, get_top_citations, process_youtube_url, handle_search_query, find_timestamp, download_spacy
from pytube import YouTube
import tempfile
from dotenv import load_dotenv

# Set the page configuration
st.set_page_config(layout="wide")

load_dotenv()

# Render the logo
render_logo()

# Custom CSS to change button styling
st.markdown(
    """
    <style>
    .stButton > button {
        color: black;  /* Text color */
        border: 1px solid rgba(0, 0, 0, 0.1);  /* Less prominent border */
        background-color: rgba(255, 255, 255, 0.8);  /* Slightly transparent background */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Semantic Search Section
youtube_link = st.text_input("Enter your YouTube video link here")
timestamp = 0

col1, col2 = st.columns([6, 4])

if youtube_link:
    with col1:
        video_player = st.empty()
        video_player.video(youtube_link, format="video/mp4", start_time=timestamp)

    video_id = get_video_id(youtube_link)

    # Get the transcript
    transcript = get_transcript(video_id)

    # Process the YouTube URL
    query_engine = process_youtube_url(youtube_link)

    with col2:
        with st.expander("**Vector Augmented Search**"):
            # Input for search query
            search_query = st.text_input("Enter your search query")

            if search_query:
                # Handle the search query
                response = handle_search_query(query_engine, search_query)

                answer = get_answer(response)
                st.markdown(f"**Answer:** \n {answer}")

                citations = get_top_citations(response)

                if citations:
                    top_citations = citations[0]
                    st.write(top_citations["text"])
                    timestamp = find_timestamp(top_citations["text"], transcript)

                    if st.button(f"Jump to {timestamp}"):
                        # Update the video player to start at the selected timestamp
                        timestamp = math.floor(timestamp)

else:
    # Prompt user to enter a YouTube link
    st.warning(
        "Please enter a YouTube link above to display the video and enable search."
    )
