#!/bin/bash
# youtube-transcribe workflow script
# Usage: ./transcribe.sh <youtube_url> [language]
# Requires: yt-dlp, ffmpeg (conda env), whisper CLI
# PATH setup: Ensure yt-dlp, ffmpeg, whisper are on your PATH

set -e

export PATH="/tmp/miniforge/bin:$(python3 -m site --user-base)/bin:$PATH"

WORKSPACE="${WORKSPACE:-$(pwd)}"
TODAY=$(date +%Y-%m-%d)
MEMORY_FILE="${WORKSPACE}/memory/${TODAY}.md"
AUDIO_DIR="/tmp/yt_audio"
mkdir -p "${AUDIO_DIR}"

# Dynamic tool discovery
YTDLP=$(command -v yt-dlp 2>/dev/null || echo "yt-dlp")
FFMPEG=$(command -v ffmpeg 2>/dev/null || echo "ffmpeg")
WHISPER=$(command -v whisper 2>/dev/null || echo "whisper")

URL="$1"
LANG="${2:-en}"

if [ -z "$URL" ]; then
  echo "Usage: $0 <youtube_url> [language]"
  exit 1
fi

# Step 1: Extract video ID
VIDEO_ID=$(echo "$URL" | grep -oE 'v=[^&]+' | cut -d= -f2 | head -1)
if [ -z "$VIDEO_ID" ]; then
  echo "Error: Could not extract video ID from URL"
  exit 1
fi
echo "[*] Video ID: ${VIDEO_ID}"

# Step 2: Get video metadata
echo "[*] Fetching video metadata..."
TITLE=$($YTDLP --extractor-args "youtube:player_client=android" \
  --print title --no-warnings "https://www.youtube.com/watch?v=${VIDEO_ID}" 2>/dev/null || echo "Unknown")
CHANNEL=$($YTDLP --extractor-args "youtube:player_client=android" \
  --print channel --no-warnings "https://www.youtube.com/watch?v=${VIDEO_ID}" 2>/dev/null || echo "Unknown")
DURATION=$($YTDLP --extractor-args "youtube:player_client=android" \
  --print duration_string --no-warnings "https://www.youtube.com/watch?v=${VIDEO_ID}" 2>/dev/null || echo "Unknown")
echo "[*] Title: ${TITLE}"
echo "[*] Channel: ${CHANNEL}"
echo "[*] Duration: ${DURATION}"

# Step 3: Download audio (with android → web fallback)
AUDIO_FILE="${AUDIO_DIR}/${VIDEO_ID}.mp3"
MP4_FILE="${AUDIO_DIR}/${VIDEO_ID}.mp4"

if [ -f "${MP4_FILE}" ] || [ -f "${AUDIO_FILE}" ]; then
  echo "[*] Audio file already exists, skipping download."
else
  echo "[*] Downloading audio (trying android client first)..."
  DOWNLOAD_LOG=$($YTDLP -x --audio-format mp3 --audio-quality 0 \
    --extractor-args "youtube:player_client=android" \
    -f "best[ext=mp4]/best" \
    -o "${AUDIO_DIR}/${VIDEO_ID}.%(ext)s" \
    "https://www.youtube.com/watch?v=${VIDEO_ID}" 2>&1 || true)

  # Check if android failed (GVS PO Token required)
  if [ ! -f "${MP4_FILE}" ] && [ ! -f "${AUDIO_FILE}" ]; then
    echo "[*] Android client failed, trying web client..."
    $YTDLP -x --audio-format mp3 --audio-quality 0 \
      -o "${AUDIO_DIR}/${VIDEO_ID}.%(ext)s" \
      "https://www.youtube.com/watch?v=${VIDEO_ID}" 2>&1 | grep -v "^Deprecated\|^NotOpenSSL\|^Warning:"
  fi

  # If still no audio, exit with error
  if [ ! -f "${MP4_FILE}" ] && [ ! -f "${AUDIO_FILE}" ]; then
    echo "Error: Audio download failed. Check yt-dlp output above."
    exit 1
  fi
fi

# Step 4: Convert to MP3 if needed
if [ -f "${MP4_FILE}" ]; then
  echo "[*] Converting MP4 to MP3..."
  $FFMPEG -i "${MP4_FILE}" -vn -acodec libmp3lame -q:a 2 "${AUDIO_FILE}" -y 2>/dev/null
  rm -f "${MP4_FILE}"
fi

# Step 5: Transcribe
TRANSCRIPT_FILE="${AUDIO_DIR}/${VIDEO_ID}_transcript.txt"
if [ ! -f "${TRANSCRIPT_FILE}" ]; then
  echo "[*] Transcribing (model=tiny, lang=${LANG})..."
  $WHISPER "${AUDIO_FILE}" \
    --model tiny \
    --language "${LANG}" \
    --output_dir "${AUDIO_DIR}" \
    --output_format txt 2>&1 | grep -v "^Deprecated\|^UserWarning"
  # Rename whisper output to expected path
  [ -f "${AUDIO_DIR}/${VIDEO_ID}.txt" ] && mv "${AUDIO_DIR}/${VIDEO_ID}.txt" "${TRANSCRIPT_FILE}"
fi

if [ ! -f "${TRANSCRIPT_FILE}" ]; then
  echo "Error: Transcript file not created"
  exit 1
fi

TRANSCRIPT=$(cat "${TRANSCRIPT_FILE}")
echo "[*] Transcript ready (${#TRANSCRIPT} chars)"

# Step 6: Save to memory
MEMORY_ENTRY="
## YouTube 转录: ${TITLE}

- **URL**: https://www.youtube.com/watch?v=${VIDEO_ID}
- **频道**: ${CHANNEL}
- **时长**: ${DURATION}
- **日期**: ${TODAY}

### 摘要
<!-- TODO: Add 3-5 sentence summary of the video's main points -->

### 关键引用
<!-- TODO: Add notable quotes -->

### 核心洞察
<!-- TODO: Add 1-3 key insights -->

\`\`\`
$(cat "${TRANSCRIPT_FILE}")
\`\`\`
"

echo "${MEMORY_ENTRY}" >> "${MEMORY_FILE}"
echo "[*] Saved to ${MEMORY_FILE}"

# Cleanup
rm -f "${AUDIO_DIR}/${VIDEO_ID}.mp4" "${AUDIO_DIR}/${VIDEO_ID}.mp3"

echo "[OK] Done. Transcript saved to memory."
