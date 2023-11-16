import streamlit as st
from transcribe import get_video_id, get_transcript
from logo import render_logo
import math
from db import process_youtube_url, handle_search_query

# Set the page configuration
st.set_page_config(layout="wide")

# Render the logo
render_logo()

# Custom CSS to change button styling
st.markdown("""
    <style>
    .stButton > button {
        color: black;  /* Text color */
        border: 1px solid rgba(0, 0, 0, 0.1);  /* Less prominent border */
        background-color: rgba(255, 255, 255, 0.8);  /* Slightly transparent background */
    }
    </style>
    """, unsafe_allow_html=True)

# Semantic Search Section
youtube_link = st.text_input("Enter your YouTube video link here")

if youtube_link:
    # Display the video
    video_player = st.empty()
    video_player.video(youtube_link, format="video/mp4")

    video_id = get_video_id(youtube_link)

    # Get the transcript
    transcript = get_transcript(video_id)

    # Process the YouTube URL
    query_engine = process_youtube_url(youtube_link)

    # Input for search query
    search_query = st.text_input("Enter your search query")

    if search_query:
        # Handle the search query
        response = handle_search_query(query_engine, search_query)
        st.write(response)

    # Container to hold the transcript buttons
    transcript_container = st.container()

    # Iterate over each transcript entry
    for idx, entry in enumerate(transcript):
        if transcript_container.button(entry['text'], key=f"btn_{idx}"):
            # Update the video player to start at the selected timestamp
            video_player.video(youtube_link, format="video/mp4", start_time=math.floor(entry['start']))
else:
    # Prompt user to enter a YouTube link
    st.warning("Please enter a YouTube link above to display the video and enable search.")
