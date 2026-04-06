# Environment Setup Notes

## Installation Commands (one-time setup)

### yt-dlp
```bash
pip3 install yt-dlp
# Path: $(python3 -m site --user-base)/bin/yt-dlp
```

### Miniforge (FFmpeg + Whisper dependencies)
```bash
# Download miniforge
curl -sL "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-arm64.sh" -o /tmp/miniforge.sh
chmod +x /tmp/miniforge.sh
/bin/bash /tmp/miniforge.sh -b -p /tmp/miniforge

# Install ffmpeg
/tmp/miniforge/bin/conda install -y ffmpeg -c conda-forge

# Install whisper
/tmp/miniforge/bin/pip install openai-whisper
```

## Permanent PATH Setup

Add to shell profile (~/.zshrc):
```bash
export PATH="/tmp/miniforge/bin:$(python3 -m site --user-base)/bin:$PATH"
```

## Tool Versions (last verified)
- ffmpeg: 8.0.1 (via conda-forge)
- yt-dlp: latest
- whisper: OpenAI Whisper CLI

## Common Issues

### "ffmpeg: command not found"
PATH doesn't include miniforge. Always run: `export PATH="/tmp/miniforge/bin:$PATH"`

### "HTTP Error 403: Forbidden" on YouTube download
Use `--extractor-args "youtube:player_client=android"` with yt-dlp.
This bypasses YouTube's bot detection which blocks the web client.

### "exec format error" when running ffmpeg
Wrong binary architecture. Do NOT use:
- `https://johnvansickle.com/ffmpeg/` (Linux static builds)
- `https://evermeet.cx/ffmpeg/` (may be wrong arch)

Use conda's ffmpeg: `/tmp/miniforge/bin/ffmpeg`

### Whisper model download slow
First run downloads the model (~72MB for 'tiny'). Subsequent runs reuse cached model.

### Memory issues
Whisper 'tiny' model uses ~1GB RAM. On constrained systems, stop other processes first.
