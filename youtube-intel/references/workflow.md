# Workflow · v2.0

## Discovery 完整工作流

```
用户输入类目请求
       ↓
┌─────────────────────────────────────────┐
│ 第一步：需求分析                          │
│  - 识别模糊性                            │
│  - 拆解为子分类                          │
│  - 确认用户真正想要的                     │
└─────────────────────────────────────────┘
       ↓
┌─────────────────────────────────────────┐
│ 第二步：策略制定                          │
│  - 为每个子分类制定搜索词                  │
│  - 确定数据源和优先级                     │
│  - 确认预期结果数量                       │
└─────────────────────────────────────────┘
       ↓
┌─────────────────────────────────────────┐
│ 第三步：数据获取                          │
│  - browser 打开 YouTube 搜索页            │
│  - 抓取原始视频列表                       │
│  - 对每个子分类重复                       │
└─────────────────────────────────────────┘
       ↓
┌─────────────────────────────────────────┐
│ 第四步：数据清洗                          │
│  - 去重（同一 video_id 只保留一条）        │
│  - 过滤广告和噪音                         │
│  - 统一播放量格式（统一为数字）             │
│  - 分类标记（content_type / intent）      │
│  - 频道聚合                               │
└─────────────────────────────────────────┘
       ↓
┌─────────────────────────────────────────┐
│ 第五步：识别筛选                          │
│  - 计算竞争度                             │
│  - 识别爆款规律                           │
│  - 找出切入机会                           │
│  - 排序优先级                             │
└─────────────────────────────────────────┘
       ↓
┌─────────────────────────────────────────┐
│ 第六步：保存呈现                          │
│  - 写入 memory                           │
│  - 输出结构化报告                         │
│  - 标注置信度                             │
└─────────────────────────────────────────┘
```

---

## 第一步：需求分析（Detail）

### 识别模糊性

拿到一个类目请求，先问自己：
1. 这个类目太宽吗？（"AI"、"内容创作" → 太宽）
2. 用户的实际目标是什么？（发现机会？竞品监测？找选题？）
3. 一个词能代表他想做的事吗？

### 拆分检查清单

如果类目符合以下任一特征，**必须拆分**：
- [ ] 是整个行业大类（AI、电商、内容创作）
- [ ] 搜索结果里会出现互相无关的内容
- [ ] 用户说"我想做这个"但没有指定具体方向

### 拆分方法

```
母类目：AI 工具
  ↓ 头脑风暴子分类
AI 图像工具
AI 编程工具
AI 写作工具
AI 视频工具
AI 语音/音频工具
AI 办公工具
AI 搜索引擎
AI 提示词工具
  ↓ 确认用户意图
最终子分类列表：[用户确认]
```

### 输出格式

```
【需求分析】
原始输入："{用户说的}"
分析结果：
  - 粒度过粗，已拆解为 [N] 个子分类
  - [子分类1]（搜索词：xxx）
  - [子分类2]（搜索词：xxx）
  ...
确认：以上拆分是否准确？
```

---

## 第二步：策略制定（Detail）

### 搜索词矩阵

对每个子分类，构建搜索词矩阵：

```
子分类：AI 编程工具

核心词：    AI programming tools 2025
           AI coding assistant tools
长尾词：    best AI code generator, AI pair programmer
对比词：    Cursor vs Copilot, Claude vs GPT coding
竞品词：    Cursor AI alternatives, GitHub Copilot alternatives
趋势词：    AI coding viral 2025, AI programmer news
```

### 选择搜索 URL

YouTube 搜索参数：
```
https://www.youtube.com/results?search_query={关键词}
https://www.youtube.com/results?search_query={关键词}&sr=agd%3A%21{{filter}}
```

常用 filter：
- `EAAqBwgK` = 今日
- `CAISBAgAEAE%3D` = 本周
- `CAISBAgAGAE%3D` = 本月
- `EgIgAQ%3D%3D` = 视频（不含 Shorts）

### 输出格式

```
【搜索策略】
类目：AI 编程工具

数据源：YouTube 搜索（browser 抓取）

搜索计划：
  [1] 核心词：AI programming tools 2025
      → 预期：30 条视频，置信度 🟢 高
      
  [2] 对比词：best AI coding tools comparison
      → 预期：20 条视频，置信度 🟢 高
      
  [3] 竞品词：Cursor vs Copilot vs Claude
      → 预期：15 条视频，置信度 🟡 中
      
合并去重后预计：50-60 条独立视频
```

---

## 第三步：数据获取（Detail）

### 抓取流程

```
browser.open(url="https://www.youtube.com/results?search_query=xxx")
    ↓
等待页面加载（3-5秒）
    ↓
browser.snapshot() → 获取页面内容
    ↓
解析字段（标题、频道、播放量、发布时间、URL）
    ↓
提取 video_id 和频道 handle
    ↓
保存为 raw_video 记录
```

### 反爬处理

如果 YouTube 返回错误页面：
1. 等待 5-10 秒重试
2. 换一个搜索词
3. 尝试 Google 搜索 YouTube 视频（备用）

### 频道页抓取（补充数据）

对重要频道，单独访问频道页获取：
- 订阅数
- 总视频数
- 频道简介

```
browser.open(url="https://www.youtube.com/@xxx/videos")
```

---

## 第四步：数据清洗（Detail）

### 过滤规则（优先级：高）

```
[1] 广告过滤
    - 如果标题包含 "Sponsored" / "Ad" / "广告"
    - 如果描述包含 "sponsored by"
    → 标记 is_noise = true

[2] 无效内容过滤
    - 标题与目标子分类完全无关
    - 重复视频（同一 video_id）
    → 标记 is_noise = true

[3] 非相关格式过滤（视情况）
    - 纯音乐 / 纯游戏画面（如果要找教程类）
```

### 字段标准化

```python
def parse_views(text):
    """播放量解析"""
    if "万次观看" in text:
        return int(text.replace("万次观看","")) * 10000
    elif "次观看" in text:
        return int(text.replace("次观看","").replace(",",""))
    elif "K" in text:
        return int(float(text.replace("K","")) * 1000)
    elif "M" in text:
        return int(float(text.replace("M","")) * 1000000)
    else:
        return None

def parse_published(text):
    """发布时间解析"""
    if "秒" in text:
        return int(text.replace("秒钟","").replace("秒","")) / 86400
    elif "分钟" in text:
        return int(text.replace("分钟","")) / 1440
    elif "小时" in text:
        return int(text.replace("小时","")) / 24
    elif "天" in text:
        return int(text.replace("天","").replace("日前",""))
    elif "个月" in text:
        return int(text.replace("个月","").replace("个月前","")) * 30
    elif "年" in text:
        return int(text.replace("年","").replace("年前","")) * 365
    else:
        return None
```

### 频道聚合

```python
def aggregate_channels(videos):
    channels = {}
    for video in videos:
        handle = video['channel_handle']
        if handle not in channels:
            channels[handle] = {
                'name': video['channel_name'],
                'handle': handle,
                'videos': [],
                'views_list': [],
            }
        channels[handle]['videos'].append(video)
        channels[handle]['views_list'].append(video['views'])
    
    for handle, ch in channels.items():
        ch['total_videos'] = len(ch['videos'])
        ch['avg_views'] = sum(ch['views_list']) / len(ch['views_list'])
        ch['max_views'] = max(ch['views_list'])
        ch['is_established'] = ch['total_videos'] >= 3 and ch['avg_views'] > 200000
        ch['is_emerging'] = ch['total_videos'] <= 2 and ch['max_views'] > 500000
    
    return channels
```

---

## 第五步：识别筛选（Detail）

### 竞争度计算

```python
def assess_competition(videos, channels):
    views = [v['views'] for v in videos]
    avg_views = sum(views) / len(views)
    median_views = sorted(views)[len(views)//2]
    top_views = sorted(views, reverse=True)[:3]
    top3_share = sum(top_views) / sum(views) if views else 0
    
    established = sum(1 for c in channels.values() if c['is_established'])
    
    if top_views[0] > 1000000 and established > 5:
        level = "red"
    elif top_views[0] > 300000 or established >= 2:
        level = "yellow"
    elif top_views[0] < 300000 or len(channels) < 5:
        level = "green"
    else:
        level = "blank"
    
    return {
        'total_videos': len(videos),
        'unique_channels': len(channels),
        'avg_views': avg_views,
        'median_views': median_views,
        'top_video_views': top_views[0] if top_views else 0,
        'top3_traffic_share': round(top3_share * 100, 1),
        'established_channels': established,
        'competition_level': level,
    }
```

### 机会识别启发式

```python
def find_opportunities(videos, channels, competition):
    opportunities = []
    
    # 格式机会：某类内容少
    content_type_count = {}
    for v in videos:
        ct = v.get('content_type', 'other')
        content_type_count[ct] = content_type_count.get(ct, 0) + 1
    
    if content_type_count.get('tutorial', 0) < 3:
        opportunities.append({
            'type': 'format',
            'description': '教程类内容稀缺',
            'suggested_angle': '从零开始教学类',
        })
    
    # 时机机会：新话题
    recent_videos = [v for v in videos if v.get('is_emerging')]
    if recent_videos:
        opportunities.append({
            'type': 'timing',
            'description': f'最近30天有 {len(recent_videos)} 条新视频，市场在升温',
        })
    
    # 差异化机会：垂直角度无人占
    # （需要人工判断，这里给出数据支撑）
    
    return opportunities
```

### 爆款规律提取

```python
def extract_viral_patterns(videos):
    viral = [v for v in videos if v.get('is_viral')]
    patterns = []
    
    for v in viral:
        # 标题分析
        title = v['title']
        has_number = any(c.isdigit() for c in title)
        has_strong_word = any(w in title for w in ['Best', 'Top', ' vs ', 'Review', 'FREE'])
        
        patterns.append({
            'video_id': v['video_id'],
            'views': v['views'],
            'published_days_ago': v['published_days_ago'],
            'title_features': {
                'has_number': has_number,
                'has_strong_word': has_strong_word,
                'length': len(title),
            }
        })
    
    return patterns
```

---

## 第六步：保存呈现（Detail）

### Memory 保存

```python
def save_to_memory(report, sub_category_slug):
    date = datetime.now().strftime('%Y-%m-%d')
    path = f"memory/content-discovery/{sub_category_slug}/{date}.md"
    
    content = f"""# Content Discovery · {sub_category_slug}
**日期：** {date}
**搜索词：** {report['search_strategy']['primary_keyword']}
**置信度：** {'🟢 高' if report['confidence'] == 'high' else '🟡 中' if report['confidence'] == 'medium' else '🔴 低'}

## 需求分析
{report['demand_analysis']}

## 搜索策略
{report['search_strategy']}

## 竞争度评估
{report['competition']}

## 机会识别
{report['opportunities']}

## 原始数据
（{len(report['raw_videos'])} 条视频）

## 爆款规律
{report['viral_patterns']}
"""
    
    write_file(path, content)
    return path
```

### 输出检查清单

在输出最终报告前，检查：
- [ ] 每个子分类都有竞争度评级
- [ ] 置信度已标注
- [ ] 机会有数据支撑
- [ ] 风险有说明
- [ ] 结果已保存到 memory
