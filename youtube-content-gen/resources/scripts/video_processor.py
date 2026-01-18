import argparse
import os
import sys
import json
from urllib.parse import parse_qs, urlparse

# Import local modules
# (assuming running from the scripts dir or proper path setup)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import transcript_extractor
import content_analyzer
import image_handler
import page_generator
import keyword_searcher

def extract_video_id(url: str) -> str:
    """Extracts video ID from a YouTube URL."""
    try:
        query = parse_qs(urlparse(url).query)
        if 'v' in query:
            return query['v'][0]
        # Handle short URLs (youtu.be/ID)
        path = urlparse(url).path
        if path.startswith('/'):
               return path[1:]
        return path
    except:
        return None

def main():
    parser = argparse.ArgumentParser(description="YouTube to SEO Page Generator")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--url", help="YouTube Video URL")
    group.add_argument("--keyword", help="Keyword to search for")
    
    args = parser.parse_args()
    
    video_url = args.url
    
    # --- Step 0: Input Parsing ---
    if args.keyword:
        print(f"🔎 Mode: Keyword Search ('{args.keyword}')")
        results = keyword_searcher.search_videos_by_keyword(args.keyword)
        if not results:
            print("❌ No videos found.")
            return
        
        print("\nFound Videos:")
        for i, res in enumerate(results):
            print(f"{i+1}. {res['title']} ({res['url']})")
        
        # Auto-select the first one for automation (or ask user in interactive mode)
        # For this script, we default to #1
        print("\n👉 Auto-selecting top result...")
        video_url = results[0]['url']

    if not video_url:
        print("❌ Invalid Video URL")
        return

    video_id = extract_video_id(video_url)
    print(f"🎬 Processing Video: {video_url} (ID: {video_id})")

    # --- Step 1 & 2: Transcript & Info ---
    print("⏳ extracting transcript...")
    transcript_data = transcript_extractor.get_transcript(video_id)
    if not transcript_data:
        print("❌ Failed to get transcript. Video might not have captions.")
        return
    
    print(f"✅ Transcript extracted ({len(transcript_data['transcript_text'].split())} words)")

    # --- Step 3: AI Analysis ---
    print("🧠 Analyzing content with Gemini...")
    # Passing a placeholder title if not fetched via API, but transcript fetcher doesn't return title easily without API key
    # Ideally yt-dlp would get metadata. For now passing ID/URL as title context or upgrading extracter.
    # Let's trust content_analyzer to handle it, or fetch title too.
    # Actually, for better results, let's just pass "YouTube Video {video_id}" if title missing.
    ai_data = content_analyzer.analyze_video_content(transcript_data['transcript_text'], f"Video ID: {video_id}")
    
    if not ai_data:
        print("❌ AI Analysis failed.")
        return
    
    # Inject video ID into data for the template
    ai_data['video_id'] = video_id
    
    print(f"✅ AI Analysis Complete. Slug: {ai_data.get('slug')}")
    print(f"   Title: {ai_data.get('title')}")

    # --- Step 4: Images ---
    print("🖼️ Downloading images...")
    # Determine output base path (project root)
    # Assuming script is in .agent/skills/youtube-content-gen/resources/scripts/
    # And we want to write to project root data
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, '../../../../../')) # Adjust based on depth
    
    # Or just use current working directory if user runs from root
    project_root = os.getcwd() 
    
    image_output_dir = os.path.join(project_root, 'public', 'images', 'guides', ai_data['slug'])
    image_handler.get_video_images(video_id, image_output_dir)
    print(f"✅ Images saved to {image_output_dir}")

    # --- Step 5: Page Generation ---
    print("📝 Generating Page Code...")
    template_dir = os.path.join(script_dir, '../templates')
    result = page_generator.generate_page_files(ai_data, template_dir, project_root)
    
    print("\n" + "="*50)
    print("✅ SUCCESS! Page Generated:")
    print(f"   Page: {result['page_path']}")
    print(f"   CSS:  {result['css_path']}")
    print("="*50)
    print("\nNext Steps:")
    print("1. Review the generated page content.")
    print("2. Run 'npm run build' to verify.")

if __name__ == "__main__":
    main()
