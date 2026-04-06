# youtube-intel 数据模型参考

## Channel 数据结构

```yaml
channel:
  name: string           # 频道名称
  url: string            # YouTube频道URL (https://www.youtube.com/@handle)
  handle: string         # @xxx 格式
  subscribers: number   # 订阅数（估算值）
  avg_views: number     # 平均播放量（估算值）
  total_videos: number  # 总视频数（估算值）
  created_date: string  # 频道创建日期（估算）
  last_updated: string  # 最后更新时间 ISO8601
```

## Video 数据结构

```yaml
video:
  title: string          # 视频标题
  url: string           # 视频URL (/watch?v=xxx)
  views: number         # 播放量
  likes: number         # 点赞数（如果有）
  published_at: string  # 发布时间
  published_days_ago: number  # 发布天数
  duration: string     # 视频时长
  channel: string       # 频道名
```

## Market Analysis 数据结构

```yaml
market_analysis:
  keyword: string           # 搜索关键词
  search_date: string       # 搜索日期 ISO8601
  total_results: number     # YouTube搜索结果总数
  top_channels:
    - name: string
      subscriber_count: string
      avg_views: number
      video_count_in_results: number
      content_direction: string
  competition_level: "high" | "medium" | "low"
  data_source: "browser" | "youtube_api" | "social_blade"
  data_confidence: "high" | "medium" | "low"
  notes: string
```

## Memory 存储格式

频道监测档案: `memory/channels/{channel-handle}.md`

```markdown
# Channel: @{handle}

## 基本信息
- 频道名: {name}
- URL: {url}
- 最后更新: {timestamp}

## 最新数据
- 订阅数: {subscribers}
- 平均播放: {avg_views}

## 最近视频
{video list}

## 趋势分析
{trend analysis}
```

## 报告输出格式

Discovery 报告: `memory/reports/discovery_{keyword}_{date}.md`

Monitoring 报告: 直接输出到对话或飞书文档
