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

with col1:
    st.session_state.search_query = ""
    video_player = st.empty()


def clear_search_query():
    st.session_state.search_query = ""


def play_video(link, timestamp):
    clear_search_query()
    video_player.video(link, format="video/mp4", start_time=timestamp)


if youtube_link:
    play_video(youtube_link, timestamp)

    video_id = get_video_id(youtube_link)

    # Get the transcript
    transcript = get_transcript(video_id)

    # Process the YouTube URL
    query_engine = process_youtube_url(youtube_link)

    with col2:
        with st.form("**Vector Augmented Search**"):
            # Input for search query
            st.session_state.search_query = st.text_input("Enter your search query")

            if st.session_state.search_query:
                # Handle the search query
                with st.spinner("Condensing..."):
                    response = handle_search_query(query_engine, st.session_state.search_query)

                answer = get_answer(response)
                st.markdown(f"**Answer:** \n {answer}")

                citations = get_top_citations(response)

                if citations:
                    top_citations = citations[0]
                    st.write(top_citations["text"])

                    with st.spinner("Finding reference timestamp..."):
                        timestamp = math.floor(find_timestamp(top_citations["text"], transcript))

            formatted_timestamp = timestamp if timestamp > 0 else "start"
            st.form_submit_button(f"Jump to {formatted_timestamp}", on_click=play_video(youtube_link, timestamp))

        # with st.expander("**Condensation**"):


else:
    # Prompt user to enter a YouTube link
    st.warning(
        "Please enter a YouTube link above to display the video and enable search."
    )
