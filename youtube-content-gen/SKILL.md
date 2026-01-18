---
name: youtube-content-gen
description: A complete pipeline to convert YouTube videos into high-quality, SEO-optimized guide pages using Gemini AI.
---

# YouTube Content Generator

A "video-to-page" pipeline that automates the creation of high-quality guide pages from YouTube videos. It extracts transcripts, analyzes content with Gemini AI, and generates Next.js pages with SEO best practices.

## Resources Included

### Scripts (`resources/scripts/`)
-   **`video_processor.py`**: The main entry point. Orchestrates the flow.
-   **`transcript_extractor.py`**: Wraps `youtube-transcript-api` to get subtitles.
-   **`content_analyzer.py`**: Uses Gemini API to understand video content and structure the page.
-   **`page_generator.py`**: Renders Jinja2 templates into `.tsx` and `.module.css` files.
-   **`image_handler.py`**: Downloads and optimizes video thumbnails.

### Templates (`resources/templates/`)
-   **`page.tsx.j2`**: Next.js page template with built-in Schema.org, responsive video embed, and SEO metadata.
-   **`page.module.css.j2`**: Matching CSS module for the generated page.

## Usage

### 1. Installation

Install the required Python dependencies:

```bash
pip install -r resources/requirements.txt
```

Set your Gemini API key:

```powershell
$env:GEMINI_API_KEY = "your_api_key_here"
```

### 2. Generate a Page

**From a YouTube URL:**

```bash
python resources/scripts/video_processor.py --url "https://www.youtube.com/watch?v=VIDEO_ID"
```

**From a Keyword (Auto-Search):**

```bash
python resources/scripts/video_processor.py --keyword "game topic to search"
```

The script will:
1.  Analyze the video.
2.  Generate a new page in `app/guides/[topic-slug]/`.
3.  Download images to `public/images/guides/[topic-slug]/`.
4.  Print a report.

### 3. Verify

Run the build to ensure everything is correct:

```bash
npm run build
```
