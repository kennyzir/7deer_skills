#!/bin/bash
# fetch_subscriptions.sh
# 通过 OpenClaw agent 抓取 YouTube 订阅频道视频
# 用法: ./fetch_subscriptions.sh [输出JSON路径]
#
# 依赖:
#   - openclaw CLI 已安装并配置
#   - 已在终端登录过 YouTube（OpenClaw browser 使用同一浏览器 session）
#
# 示例:
#   ./fetch_subscriptions.sh ./data/videos.json

set -euo pipefail

OUTPUT="${1:-./data/reports/openclaw_subscriptions_videos.json}"

PROMPT='Use the browser tool to inspect https://www.youtube.com/feed/subscriptions in the current OpenClaw browser session. Scroll down several times to load more items (at least 3-5 scrolls). Return strict JSON with this exact structure:
{
  "logged_in": boolean,
  "evidence": "string describing login status",
  "videos": [
    {
      "title": "video title string",
      "channel_name": "channel name",
      "published_text": "e.g. 2 days ago",
      "view_text": "e.g. 123K views",
      "url": "https://www.youtube.com/watch?v=...",
      "source_name": "Subscriptions"
    }
  ]
}
Set source_name to "Subscriptions" for every item. Do not use web_search or web_fetch.'

echo "[youtube-game-keywords] 开始抓取订阅频道..."

response=$(openclaw agent --agent main --message "$PROMPT" --json 2>&1)
payload=$(echo "$response" | python3 -c "import sys,json; print(json.load(sys.stdin)['result']['payloads'][0]['text'])" 2>&1)

logged_in=$(echo "$payload" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('logged_in', False))" 2>&1)

if [ "$logged_in" != "True" ] && [ "$logged_in" != "true" ]; then
  evidence=$(echo "$payload" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('evidence', 'unknown'))" 2>&1)
  echo "[youtube-game-keywords] ERROR: YouTube 未登录 - $evidence" >&2
  exit 1
fi

mkdir -p "$(dirname "$OUTPUT")"
videos=$(echo "$payload" | python3 -c "import sys,json; d=json.load(sys.stdin); print(json.dumps(d.get('videos', []), ensure_ascii=False, indent=2))" 2>&1)
echo "$videos" > "$OUTPUT"

count=$(echo "$videos" | python3 -c "import sys,json; print(len(json.load(sys.stdin)))" 2>&1)
echo "[youtube-game-keywords] 抓取完成，共 $count 条视频，保存至 $OUTPUT"
