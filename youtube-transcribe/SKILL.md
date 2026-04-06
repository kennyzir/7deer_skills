---
name: youtube-transcribe
description: YouTube video transcription and memory workflow. Triggers when user shares a YouTube URL and asks to transcribe, get transcript, or extract content. Also activates when user says "转录", "transcribe this video", "get the content of this video", or "summarize this YouTube video". Downloads audio via yt-dlp (android client to avoid 403), converts with ffmpeg (conda env at /tmp/miniforge), transcribes with whisper CLI, then saves full transcript + summary to today's memory file and optionally pushes a Feishu notification.
---

# YouTube Transcribe Skill

## Environment Prerequisites

The following tools must be available. Check paths before executing:

| Tool | Path | Notes |
|------|------|-------|
| yt-dlp | `$(python3 -m site --user-base)/bin/yt-dlp` | Install: `pip3 install yt-dlp` |
| ffmpeg | `/tmp/miniforge/bin/ffmpeg` | Install: conda install -c conda-forge ffmpeg |
| whisper | `$(python3 -m site --user-base)/bin/whisper` | Install: pip3 install openai-whisper |
| conda | `/tmp/miniforge/bin/conda` | Miniforge3-MacOS-arm64 |

If tools are missing, install before proceeding.

## Workflow

### Step 1 — Parse YouTube URL

Extract video ID from URL:
```bash
# Handles: https://youtu.be/ID, https://www.youtube.com/watch?v=ID&t=..., https://youtube.com/embed/ID
echo "$URL" | grep -oE 'v=[^&]+' | cut -d= -f2
```

### Step 2 — Download Audio

```bash
export PATH="/tmp/miniforge/bin:$(python3 -m site --user-base)/bin:$PATH"
VIDEO_ID="<extracted_id>"
mkdir -p /tmp/yt_audio

yt-dlp -x --audio-format mp3 --audio-quality 0 \
  --extractor-args "youtube:player_client=android" \
  -o "/tmp/yt_audio/${VIDEO_ID}.%(ext)s" \
  "https://www.youtube.com/watch?v=${VIDEO_ID}"
```

**Why `--extractor-args "youtube:player_client=android"`**: Web client returns 403 for this bot; android client works reliably.

### Step 3 — Convert to MP3 (if needed)

If yt-dlp downloaded .mp4 instead of .mp3:
```bash
ffmpeg -i "/tmp/yt_audio/${VIDEO_ID}.mp4" -vn -acodec libmp3lame -q:a 2 "/tmp/yt_audio/${VIDEO_ID}.mp3" -y
```

### Step 4 — Transcribe

```bash
export PATH="/tmp/miniforge/bin:$(python3 -m site --user-base)/bin:$PATH"
whisper "/tmp/yt_audio/${VIDEO_ID}.mp3" \
  --model tiny \
  --language en \
  --output_dir /tmp/yt_audio \
  --output_format txt
```

**Model choice**: `tiny` is fastest for English. Use `base` for better accuracy if time permits.

### Step 5 — Save to Memory

After transcription, append to today's memory file:

File: `memory/YYYY-MM-DD.md`
```
## YouTube 转录: <Video Title>

- **URL**: https://www.youtube.com/watch?v=<video_id>
- **频道**: <channel_name>
- **时长**: <duration>
- **日期**: YYYY-MM-DD

### 摘要
<3-5 sentence summary of the video's main points>

### 关键引用
> "<notable quote>"
> "<notable quote>"

### 核心洞察
<1-3 insights from the video>
```

### Step 6 — Post to Feishu (optional)

If user asks to push results or if the video is relevant to ongoing projects, send transcript snippet to Feishu.

---

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `HTTP Error 403` on download | Web client blocked | Add `--extractor-args "youtube:player_client=android"` |
| `ffmpeg: command not found` | conda env not on PATH | `export PATH="/tmp/miniforge/bin:$PATH"` |
| `ModuleNotFoundError: whisper` | Using wrong python | Use `whisper` CLI directly, not `python3 -m whisper` |
| `exec format error` on ffmpeg | Wrong architecture binary | Use `/tmp/miniforge/bin/ffmpeg` (macOS arm64), not Linux static builds |

---

## Cleanup

Audio files accumulate in `/tmp/yt_audio/`. Optionally clean up after successful transcription:
```bash
rm -f /tmp/yt_audio/${VIDEO_ID}.*
```

## When Not to Use This Skill

- Video has accurate YouTube captions → Use `web_fetch` + transcript API instead (faster, more accurate)
- User only wants a summary → Ask if full transcript is needed before running
- Video is very long (>30 min) → Whisper inference takes significant time; warn user before starting
