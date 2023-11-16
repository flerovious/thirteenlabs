from youtube_transcript_api import YouTubeTranscriptApi
import whisper
import time

model = whisper.load_model("base")
output_file = "sample"

def get_video_id(youtube_link: str):
    """
    Returns the video id from a youtube link

    Args:
        youtube_link (str): A youtube video link (for example: https://www.youtube.com/watch?v=Rp9h4YEV6Rk)

    Returns:
        str: video_id (for example: Rp9h4YEV6Rk)
    """
    video_id = youtube_link.split("=")[-1]
    return video_id


def get_transcript(video_id: str):
    """
    Return the transcript of a YouTube video

    Args:
        video_id (str): video_id of youtube video

    Returns:
        List[Dict[str, str]]: transcript of the video
    """
    try:
        # get the transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])

        return transcript
    except Exception as e:
        return f"An error occurred: {e}"


def convert_audio_to_txt(audio_file: str):
    try:
        result = model.transcribe(audio_file)
        transcript = result['text']

        with open(output_file+"_"+int(time.time())+".txt", 'w') as f:
            f.write(transcript)
    except Exception as e:
        return "You stoopid"
