#!/bin/bash
# youtube-intel: 抓取YouTube频道数据
# Usage: ./fetch_channel.sh <channel_url_or_handle>

set -e

CHANNEL_INPUT="$1"
OUTPUT_DIR="${OUTPUT_DIR:-./data}"

if [ -z "$CHANNEL_INPUT" ]; then
    echo "Usage: $0 <channel_url_or_handle>"
    exit 1
fi

# 解析频道URL或handle
if [[ "$CHANNEL_INPUT" =~ ^@ ]]; then
    HANDLE="$CHANNEL_INPUT"
    CHANNEL_URL="https://www.youtube.com/$HANDLE/videos"
else
    CHANNEL_URL="$CHANNEL_INPUT"
    HANDLE=$(echo "$CHANNEL_URL" | grep -oP '@[^/]+' | head -1)
fi

mkdir -p "$OUTPUT_DIR/channels"
OUTPUT_FILE="$OUTPUT_DIR/channels/${HANDLE#@}.json"

echo "Fetching channel: $HANDLE"
echo "Output: $OUTPUT_FILE"

# 使用 yt-dlp 获取频道信息（如果可用）
if command -v yt-dlp &> /dev/null; then
    yt-dlp --dump-json \
           --playlist-end 10 \
           "$CHANNEL_URL" > "$OUTPUT_FILE.tmp" 2>/dev/null
    
    # 提取基本信息
    python3 -c "
import json
import sys
from datetime import datetime

data = []
with open('$OUTPUT_FILE.tmp') as f:
    for line in f:
        data.append(json.loads(line))

print(f'Fetched {len(data)} videos')
# 可以添加更多数据处理逻辑
"
    mv "$OUTPUT_FILE.tmp" "$OUTPUT_FILE"
    echo "Done: $OUTPUT_FILE"
else
    echo "yt-dlp not found. Please install: pip install yt-dlp"
    exit 1
fi
