import os
import json
from google import genai
from google.genai import types

def analyze_video_content(transcript_text: str, video_title: str) -> dict:
    """
    Analyzes the video transcript using Gemini to generate SEO content.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")

    client = genai.Client(api_key=api_key)

    prompt = f"""
    You are an expert SEO Content Strategist for a gaming website.
    Analyze the following YouTube video transcript and generate a comprehensive guide structure.

    Video Title: {video_title}
    Transcript:
    {transcript_text[:25000]}  # Truncate if too long, though Gemini context is large

    Task:
    1. Identify the core topic (Concept, Item, Quest, Boss, etc.).
    2. Determine the search intent (Informational, Transactional, etc.).
    3. Create a clean URL slug (kebab-case).
    4. Write a Compelling H1 Title (SEO optimized).
    5. Write a Meta Description (150-160 chars).
    6. Extract "Quick Answer" content (direct answer to the user's main question).
    7. Generate 5-8 FAQ pairs (Question & Answer) based on the transcript.
    8. Create a structural outline (H2 headings and bullet points for content).
    9. Determine the best category (Guides, Codes, Tier List, etc.).

    Output strict JSON format:
    {{
        "slug": "string",
        "title": "string",
        "description": "string",
        "category": "string",
        "quick_answer": "string",
        "faqs": [
            {{"question": "string", "answer": "string"}}
        ],
        "outline": [
            {{"h2": "string", "content_points": ["string", "string"]}}
        ],
        "tags": ["string"]
    }}
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash", # Using flash for speed/cost, adjust as needed
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        
        return json.loads(response.text)
    except Exception as e:
        print(f"Error during AI analysis: {e}")
        return None
