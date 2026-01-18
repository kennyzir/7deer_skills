from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

def get_transcript(video_id: str) -> dict:
    """
    Retrieves the transcript for a given YouTube video ID.
    """
    try:
        # List available transcripts
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # Try to fetch manually created transcripts first, then generated
        try:
            transcript = transcript_list.find_manually_created_transcript(['en'])
        except:
            try:
                transcript = transcript_list.find_generated_transcript(['en'])
            except:
                 # Fallback to any available transcript
                transcript = transcript_list.find_transcript(['en'])

        transcript_data = transcript.fetch()
        
        formatter = TextFormatter()
        full_text = formatter.format_transcript(transcript_data)
        
        return {
            "video_id": video_id,
            "transcript_text": full_text,
            "segments": transcript_data
        }
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return None
