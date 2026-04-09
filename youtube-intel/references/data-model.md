# Data Model · v2.0

## 原始数据模型（Raw Video Record）

```yaml
raw_video:
  title: string
  video_id: string
  url: string                     # https://www.youtube.com/watch?v=XXX
  channel_name: string
  channel_handle: string         # @xxx
  views_raw: string              # "53万次观看"（原始文本）
  views: number                  # 530000（统一为数字）
  published_raw: string          # "5个月前"（原始文本）
  published_days_ago: number     # 150
  duration: string               # "19:19"
  is_short: boolean
  is_ad: boolean                # 是否广告
  rank: number                  # 在搜索结果中的位置
```

## 清洗后数据模型（Cleaned Video Record）

```yaml
cleaned_video:
  video_id: string
  title: string
  url: string
  channel_name: string
  channel_handle: string
  views: number
  published_days_ago: number
  duration: string
  is_short: boolean
  sub_category: string           # 归属子分类
  content_type:                 # 内容形态
    - "review"                 # 测评/推荐
    - "tutorial"               # 教程
    - "list"                   # 清单/排行
    - "comparison"             # 对比
    - "news"                   # 新闻/新品
    - "opinion"                # 观点
    - "other"
  intent:                       # 用户意图
    - "discover"               # 发现工具
    - "learn"                  # 学习使用
    - "compare"                # 对比选择
    - "工具推荐"
    - "行业趋势"
  is_viral: boolean             # 播放量 > 100万
  is_emerging: boolean          # 发布 < 30天
  is_noise: boolean             # 是否噪音/广告（已过滤）
```

## 频道画像模型（Channel Profile）

```yaml
channel_profile:
  name: string
  handle: string
  url: string                   # YouTube 频道 URL
  subscriber_count: string      # 订阅数（原始文本）
  subscriber_count_raw: number  # 订阅数（估算数字）
  
  # 从当前搜索结果中聚合
  videos_in_results: number     # 本次搜索结果中出现多少次
  avg_views: number            # 平均播放量
  max_views: number            # 最高播放量
  latest_video_days_ago: number
  
  # 内容特征
  content_type_distribution:    # 内容类型分布
    review: number
    tutorial: number
    list: number
    comparison: number
    news: number
    other: number
  
  # 频道标签
  is_established: boolean      # 有多条视频，平均播放较高
  is_emerging: boolean         # 新账号但有爆款
  is_high_volume: boolean       # 头部玩家（结果中占 30%+ 流量）
  is_niche: boolean            # 小众专注（某垂直领域深度内容）
```

## 竞争度评估模型（Competition Assessment）

```yaml
competition_assessment:
  sub_category: string
  
  # 数量指标
  total_videos: number         # 搜索结果总数
  unique_channels: number      # 涉及频道数
  
  # 播放指标
  avg_views: number            # 平均播放量
  median_views: number         # 中位数播放量
  top_video_views: number      # 头部视频播放量
  
  # 格局指标
  established_channels: number  # 成熟玩家数（>3条视频，平均 > 20万）
  emerging_channels: number   # 新兴玩家数（< 3个月，有爆款）
  new entrants_last_30d: number # 30天内新进入者
  
  # 评级
  saturation: "high" | "medium" | "low" | "blank"
  competition_level: "red" | "yellow" | "green"
  
  # 流量集中度
  top3_traffic_share: number   # 前三名吃掉多少流量
  
  # 备注
  notes: string
```

**判断矩阵：**

| 条件 | 竞争评级 |
|------|---------|
| 头部视频 > 100万 AND 成熟频道 > 5 | 🔴 红 |
| 头部 30-100万 OR 成熟频道 2-5 | 🟡 黄 |
| 头部 < 30万 OR 新兴市场 | 🟢 绿 |
| 无充分数据（ < 5条视频） | ⚪ 空白 |

## 机会识别模型（Opportunity）

```yaml
opportunity:
  id: string                   # 机会 ID
  sub_category: string
  type:
    - "differentiation"       # 差异化切入
    - "niche"                 # 小众空白
    - "format"                # 格式差异化
    - "timing"                # 时机窗口
    - "data"                  # 数据驱动
  
  description: string          # 机会描述
  evidence:                    # 数据支撑
    - string
  suggested_angle: string      # 建议切入角度
  suggested_titles:            # 建议标题方向
    - string
  estimated_difficulty: "easy" | "medium" | "hard"
  risk: string                 # 风险提示
  priority: number             # 优先级 1-5
```

## 爆款规律模型（Viral Pattern）

```yaml
viral_pattern:
  video_id: string
  title: string
  views: number
  published_days_ago: number
  channel: string
  
  # 分析字段
  why_viral: string            # 为什么爆
  content_formula: string       # 内容公式（标题/结构/时长）
  topic_tags:                   # 话题标签
    - string
  timing_context: string        # 当时的背景（新品发布? 热点?）
  
  # 可复用规律
  lessons:                     # 可复用的点
    - string
  suggested_replication: string # 如何借鉴
```

## 完整分析报告模型（Discovery Report）

```yaml
discovery_report:
  id: string                   # UUID
  created_at: datetime
  query: string                # 用户原始需求
  decomposed_subcategories:     # 拆解后的子分类
    - sub_category: string
      search_terms: string[]
      competition: CompetitionAssessment
      
  search_strategy:
    sub_category: string
    primary_keyword: string
    keywords: string[]
    sources: string[]
    
  raw_data:
    total_videos: number
    videos: Video[]
    channels: ChannelProfile[]
    
  cleaned_data:
    videos: CleanedVideo[]
    channels: ChannelProfile[]
    
  analysis:
    subcategory_assessments: CompetitionAssessment[]
    opportunities: Opportunity[]
    viral_patterns: ViralPattern[]
    
  confidence: "high" | "medium" | "low"
  confidence_notes: string
  
  # 元数据
  memory_path: string           # 保存路径
  expires_days: number          # 数据有效期（默认30天）
```

## Memory 存储路径

```
memory/content-discovery/
├── {sub-category-slug}/
│   ├── latest.md              # 最新报告（软链接或索引）
│   ├── {YYYY-MM-DD}.md        # 当日报告
│   └── {YYYY-MM-DD}.md        # 历史报告
└── index.md                   # 所有报告索引
```
