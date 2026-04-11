---
name: youtube-transcribe
description: YouTube video transcription and memory workflow. Triggers when user shares a YouTube URL and asks to transcribe, get transcript, extract content, "转录", "transcribe this video". Downloads audio via yt-dlp (android client to avoid 403, with web fallback), converts with ffmpeg, transcribes with whisper CLI, then saves full transcript + summary to today's memory file.
---

# YouTube Transcribe Skill

## Tool Discovery

Before running, the agent checks for available tools and sets PATH:

```bash
# Find tools dynamically — don't hardcode paths
export PATH="/tmp/miniforge/bin:$(python3 -m site --user-base)/bin:$PATH"

YTDLP=$(command -v yt-dlp 2>/dev/null || echo "yt-dlp")
FFMPEG=$(command -v ffmpeg 2>/dev/null || echo "ffmpeg")
WHISPER=$(command -v whisper 2>/dev/null || echo "whisper")

# Verify tools exist
for TOOL in "$YTDLP" "$FFMPEG" "$WHISPER"; do
  [ -x "$TOOL" ] || echo "[WARN] Tool not found or not executable: $TOOL"
done
```

**Tool requirements:**

| Tool | Install | Fallback path |
|------|---------|--------------|
| yt-dlp | `pip3 install yt-dlp` | `$(python3 -m site --user-base)/bin/yt-dlp` |
| ffmpeg | `conda install -c conda-forge ffmpeg` | `/tmp/miniforge/bin/ffmpeg` |
| whisper | `pip3 install openai-whisper` | `$(python3 -m site --user-base)/bin/whisper` |

## Environment PATH

```bash
export PATH="/tmp/miniforge/bin:$(python3 -m site --user-base)/bin:$PATH"
```

## Workflow

### Step 1 — Parse YouTube URL

```bash
URL="https://www.youtube.com/watch?v=Q5kYrmzNhcU"
VIDEO_ID=$(echo "$URL" | grep -oE 'v=[^&]+' | cut -d= -f2 | head -1)
# Handles: https://youtu.be/ID, https://www.youtube.com/watch?v=ID&t=..., https://youtube.com/embed/ID
```

### Step 2 — Get Video Metadata

```bash
TITLE=$($YTDLP --extractor-args "youtube:player_client=android" \
  --print title --no-warnings "https://www.youtube.com/watch?v=${VIDEO_ID}" 2>/dev/null)
CHANNEL=$($YTDLP --extractor-args "youtube:player_client=android" \
  --print channel --no-warnings "https://www.youtube.com/watch?v=${VIDEO_ID}" 2>/dev/null)
DURATION=$($YTDLP --extractor-args "youtube:player_client=android" \
  --print duration_string --no-warnings "https://www.youtube.com/watch?v=${VIDEO_ID}" 2>/dev/null)
```

### Step 3 — Download Audio (with Fallback Chain)

```bash
mkdir -p /tmp/yt_audio

# Strategy: try android client first → if GVS PO Token error, fall back to web client
# (web client may 403 on some videos; android client needs PO token for high-quality formats
# but usually succeeds with format 18 even without PO token)

# Attempt 1: android client (works without PO token for format 18)
$YTDLP -x --audio-format mp3 --audio-quality 0 \
  --extractor-args "youtube:player_client=android" \
  -f "best[ext=mp4]/best" \
  -o "/tmp/yt_audio/${VIDEO_ID}.%(ext)s" \
  "https://www.youtube.com/watch?v=${VIDEO_ID}" 2>&1 | grep -v "^Deprecated\|^NotOpenSSL\|^Warning:"

# If android fails (GVS PO Token required), fall back to web
if [ ! -f "/tmp/yt_audio/${VIDEO_ID}.mp4" ] && [ ! -f "/tmp/yt_audio/${VIDEO_ID}.mp3" ]; then
  echo "[*] Android client failed, trying web client..."
  $YTDLP -x --audio-format mp3 --audio-quality 0 \
    -o "/tmp/yt_audio/${VIDEO_ID}.%(ext)s" \
    "https://www.youtube.com/watch?v=${VIDEO_ID}" 2>&1 | grep -v "^Deprecated\|^NotOpenSSL"
fi
```

**Why `--extractor-args "youtube:player_client=android"`**: Web client returns 403 for many videos; android client returns format 18 (mp4, ~480p) without requiring a GVS PO Token, which is sufficient for transcription.

### Step 4 — Convert to MP3 (if needed)

```bash
# If yt-dlp downloaded .mp4 instead of .mp3
if [ -f "/tmp/yt_audio/${VIDEO_ID}.mp4" ]; then
  $FFMPEG -i "/tmp/yt_audio/${VIDEO_ID}.mp4" \
    -vn -acodec libmp3lame -q:a 2 \
    "/tmp/yt_audio/${VIDEO_ID}.mp3" -y 2>/dev/null
  rm -f "/tmp/yt_audio/${VIDEO_ID}.mp4"
fi
```

### Step 5 — Transcribe

```bash
$WHISPER "/tmp/yt_audio/${VIDEO_ID}.mp3" \
  --model tiny \
  --language en \
  --output_dir /tmp/yt_audio \
  --output_format txt 2>&1 | grep -v "^Deprecated\|^UserWarning"

# Whisper outputs to {output_dir}/{filename}.txt
# Rename if needed
[ -f "/tmp/yt_audio/${VIDEO_ID}.txt" ] && \
  mv "/tmp/yt_audio/${VIDEO_ID}.txt" "/tmp/yt_audio/${VIDEO_ID}_transcript.txt"
```

**Model choice**: `tiny` is fastest for English. Use `base` or `small` for better accuracy if time permits.

### Step 6 — Save to Memory

Append to `memory/YYYY-MM-DD.md`:

```markdown
## YouTube 转录: <Video Title>

- **URL**: https://www.youtube.com/watch?v=<video_id>
- **频道**: <channel_name>
- **时长**: <duration>
- **日期**: YYYY-MM-DD

### 摘要
<3-5 sentence summary>

### 关键引用
> "<notable quote>"

### 核心洞察
<1-3 insights>
```

### Step 7 — Post to Feishu (optional)

If user requests it, send a Feishu message with the summary and key quotes.

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `HTTP Error 403` on download | YouTube web client blocked | Use `--extractor-args "youtube:player_client=android"` |
| `android client https formats require a GVS PO Token` | Android client needs PO token for high-quality formats | Fall back to web client; format 18 (mp4) usually still downloads without token |
| `ffmpeg: command not found` | conda env not on PATH | `export PATH="/tmp/miniforge/bin:$PATH"` |
| `ModuleNotFoundError: whisper` | Using wrong python | Use `whisper` CLI directly, not `python3 -m whisper` |
| `exec format error` on ffmpeg | Wrong architecture binary | Use `/tmp/miniforge/bin/ffmpeg` (macOS arm64), not Linux static builds |
| No transcript file created | whisper failed silently | Check whisper output for CUDA/memory errors; try `base` model |
| `NotOpenSSLWarning` | urllib3 v2 + LibreSSL | Ignore; download still succeeds |

## Cleanup

```bash
rm -f /tmp/yt_audio/${VIDEO_ID}.*
```

## When NOT to Use This Skill

- **Video has accurate YouTube captions** → Use `web_fetch` with transcript extraction instead (faster, more accurate, preserves speaker labels)
- **User only wants a summary** → Ask if full transcript is needed before running (5+ min transcription vs instant captions)
- **Video is very long (>30 min)** → Whisper inference takes significant time on CPU; warn user before starting
- **Non-English video** → Specify language with `--language <code>` (e.g., `--language zh` for Chinese); `tiny` model quality degrades significantly for non-English

## One-Time Installation

```bash
# yt-dlp
pip3 install yt-dlp

# Miniforge (ffmpeg + whisper dependencies)
curl -sL "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-arm64.sh" -o /tmp/miniforge.sh
chmod +x /tmp/miniforge.sh
/bin/bash /tmp/miniforge.sh -b -p /tmp/miniforge
/tmp/miniforge/bin/conda install -y ffmpeg -c conda-forge
/tmp/miniforge/bin/pip install openai-whisper

# Add to ~/.zshrc
echo 'export PATH="/tmp/miniforge/bin:$(python3 -m site --user-base)/bin:$PATH"' >> ~/.zshrc
```
