import streamlit as st
from transcribe import get_video_id, get_transcript
from logo import render_logo

# Render the logo
render_logo()

# Semantic Search Section
youtube_link = st.text_input("Enter your youtube video link here")

if youtube_link:
    # Display the video
    st.video(youtube_link)
else:
    # Prompt user to enter a YouTube link
    st.warning(
        "Please enter a YouTube link above to display the video and enable search."
    )

if youtube_link:
    # Placeholder for search results
    transcript_results = st.empty()

    video_id = get_video_id(youtube_link)

    # Get the transcript
    transcript = get_transcript(video_id)

    # Displaying a the transcript json
    transcript_results.markdown(transcript)
