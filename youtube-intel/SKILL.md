---
name: youtube-intel
description: YouTube内容情报与竞品监测。当用户需要分析YouTube频道、追踪竞品动态、发现内容机会时触发。功能：1) Monitoring - 监测指定频道的更新频率、内容方向、数据表现；2) Discovery - 输入类目/关键词，扫描市场机会与竞争程度。用于选题策划、竞品分析、内容策略制定。
---

# youtube-intel · YouTube内容情报

> **版本：** v2.0 — 重构版
> **核心理念：** 情报工作不是搜一个词等结果就完了。需求分析 → 策略制定 → 数据获取 → 清洗识别 → 保存呈现，缺一不可。

---

## 两种模式

### Monitoring（竞品监测）

**触发词**：
- "盯着 XXX 频道"
- "监测这几个频道"
- "这个频道最近发了什么"

---

### Discovery（选题发现）

**触发词**：
- "我想做 XX 类目，有没有机会"
- "帮我扫描 XX 市场"
- "分析这个赛道"

> ⚠️ 注意：Discovery 模式按下方六步工作流执行，**不**是搜一个词就出报告。

---

## Discovery 六步工作流

```
第一步：需求分析     ← 理解用户真正想要什么，识别模糊性
第二步：策略制定     ← 确定搜索词、子分类、数据源
第三步：数据获取     ← 执行搜索
第四步：数据清洗     ← 去重、过滤噪音、统一格式
第五步：识别筛选     ← 识别子分类、竞争度、机会点
第六步：保存呈现     ← 写入 memory，输出结构化报告
```

---

## 第一步：需求分析

**目标：** 拿到一个类目请求时，先理解用户真正要的是什么。

**执行原则：永远先分析，再动手搜。**

### 3. 判断类目粒度

| 粒度 | 示例 | 是否需要拆分 |
|------|------|------------|
| 模糊大类 | "AI"、"内容创作"、"电商" | ❌ 需拆分 |
| 明确子分类 | "AI 图像生成"、"YouTube 剪辑技巧" | ✅ 可直接搜 |
| 竞品监测 | "盯着 @某某频道" | ✅ 进入 Monitoring |

### 4. 模糊类目必须拆分

如果用户说"AI 工具"，直接拆解：

```
AI 工具
  ├── AI 图像工具（Midjourney、Stable Diffusion...）
  ├── AI 编程工具（Cursor、Copilot...）
  ├── AI 写作工具（Jasper、Claude...）
  ├── AI 视频工具（Sora、Runway...）
  ├── AI 语音/音频工具（ElevenLabs...）
  └── AI 办公工具（Notion AI、Gamma...）
```

**原则：** 一个搜索词 = 一个明确的子分类。找不到子分类就问用户。

### 5. 需求记录

把分析结果明确告知用户：
```
分析：
- 你说的"XXX"我理解为：[具体是什么]
- 拆解为以下子分类：[列表]
- 每个子分类独立搜索：[关键词列表]
```

---

## 第二步：策略制定

**目标：** 为每个子分类制定搜索策略。

### 6. 制定搜索词矩阵

对每个子分类，确定：

```
子分类：AI 图像工具
├── 核心搜索词：AI image generator tools 2025
├── 长尾搜索词：best AI art tools comparison, free AI image generator
├── 竞品搜索词：Midjourney alternatives, Stable Diffusion vs DALL-E
└── 趋势搜索词：AI image generator viral 2025
```

### 7. 确定数据源优先级

| 数据源 | 用途 | 置信度 |
|--------|------|--------|
| YouTube 搜索（browser 抓取） | 热门视频、竞争度 | 🟢 高 |
| YouTube 频道页（browser 抓取） | 频道详细数据 | 🟢 高 |
| Social Blade | 订阅数、趋势 | 🟡 中 |
| Google 搜索 | 舆情热度佐证 | 🟡 中 |
| X（Twitter）| 新产品动态 | 🟡 中 |

### 8. 搜索执行计划

在开始抓取前，先告诉用户：

```
搜索策略：
- 类目：AI 图像工具
- 搜索词：AI image generator tools 2025
- 数据源：YouTube 搜索 + 频道页
- 预期结果数：20-30 条视频
- 置信度：🟡 中（YouTube 模糊化数据）
```

---

## 第三步：数据获取

**使用 browser 工具执行搜索。**

### YouTube 搜索

```
URL 格式：https://www.youtube.com/results?search_query={关键词}
```

### 解析字段（from snapshot）

| 字段 | 解析规则 |
|------|---------|
| 标题 | heading 或 link 的 text |
| 频道名 | "前往频道：XXX" 或 @xxx 格式 |
| 播放量 | "X万次观看" / "X次观看" → 转换为数字 |
| 发布时间 | "X个月前" / "X天前" / "X年前" → 天数 |
| 视频 URL | link href → /watch?v=XXX |
| 视频 ID | 从 URL 提取 video_id |

### 数据记录格式

每条视频记录：

```yaml
video:
  title: string
  video_id: string        # 从 URL 提取
  url: string             # https://www.youtube.com/watch?v=XXX
  channel_name: string
  channel_handle: string  # @xxx 格式
  views: number           # 播放量（统一为数字）
  views_display: string   # 原始显示文本
  published_days_ago: number
  published_display: string
  duration: string        # 时长
  is_short: boolean       # 是否 Shorts
```

---

## 第四步：数据清洗

**目标：** 把原始数据变成可分析的情报。**

### 9. 过滤规则

**必须过滤掉：**
- 广告内容（sponsored content、推广视频）
- 与目标子分类明显无关的视频
- 重复视频（同一视频 ID 只保留一条）

**保留观察：**
- Shorts 和长视频分开标记（两者是不同的内容形态）
- 不同频道名但同一人的情况（合并分析）

### 10. 分类标记

对每条视频，标记：

```yaml
video:
  ...
  sub_category: string   # 归属的子分类
  content_type: "review" | "tutorial" | "list" | "comparison" | "news" | "other"
  intent: "discover" | "learn" | "compare" | "工具推荐" | "行业趋势"
  is_viral: boolean       # 是否爆款（播放量 > 100万）
  is_emerging: boolean    # 是否新兴（发布 < 30天）
```

### 11. 频道聚合

同频道的视频合并，计算：

```yaml
channel_profile:
  name: string
  handle: string
  total_videos_in_results: number
  avg_views: number
  max_views: number
  latest_video_days_ago: number
  content_type_distribution: {}
  is_established: boolean   # 有多条视频且平均播放高
  is_emerging: boolean       # 新账号但有爆款
```

---

## 第五步：识别筛选

**目标：** 从清洗后的数据里识别机会和风险。**

### 12. 子分类竞争度评估

```yaml
competition_assessment:
  sub_category: string
  total_videos: number
  unique_channels: number
  avg_views: number
  top_video_views: number
  established_channels: number
  emerging_channels: number
  saturation: "high" | "medium" | "low" | "blank"
  competition_level: "red" | "yellow" | "green"
```

**判断标准：**
- 🔴 红（高竞争）：头部视频 > 100万播放，成熟频道 > 5个
- 🟡 黄（中等竞争）：头部 30-100万，有空间但需要差异化
- 🟢 绿（低竞争 / 空白）：头部 < 30万，或新兴市场
- ⚪ 空白：新出现的子分类，无充分数据

### 13. 切入机会识别

```yaml
opportunity:
  type: "differentiation" | "niche" | "format" | "timing" | "data"
  description: string
  evidence: string[]      # 数据支撑
  suggested_angle: string # 建议切入角度
  risk: string            # 风险提示
```

**常见机会类型：**
- **差异化机会**：头部都在泛谈，垂直场景无人占
- **格式机会**：列表类视频多，教程类少
- **时机机会**：新兴话题，供给还没跟上需求
- **数据机会**：没人用真实数据做对比

### 14. 爆款识别

```yaml
viral_signals:
  video_id: string
  title: string
  views: number
  published_days_ago: number
  why_viral: string       # 分析原因
  lessons: string[]       # 可复用的规律
```

---

## 第六步：保存与呈现

### 15. 保存到 Memory

每个子分类的分析结果保存为：

```
memory/content-discovery/{sub-category-slug}/{date}.md
```

**文件结构：**
```markdown
# Content Discovery · {子分类名}
**日期：** YYYY-MM-DD
**搜索词：** xxx
**数据源：** YouTube 搜索（browser 抓取）
**置信度：** 🟡 中

## 需求分析
[分析过程]

## 搜索策略
[策略]

## 原始数据
[视频列表]

## 清洗后数据
[聚合后的频道数据]

## 竞争度评估
[竞争度评级]

## 机会识别
[机会列表]

## 爆款分析
[爆款规律]
```

### 16. 结构化报告输出

最终输出格式：

```
【Discovery 报告】{类目名}
生成时间：YYYY-MM-DD HH:mm
数据来源：YouTube 直接抓取（置信度：🟡 中）

---

## 🎯 需求确认
你所说的"XXX"已拆解为以下子分类：
1. AI 图像工具（搜索词：xxx）→ 竞争度：🔴 高
2. AI 编程工具（搜索词：xxx）→ 竞争度：🟡 中
...

## 🔍 子分类详细分析
[每个子分类的分析]

## 💡 最高价值机会
[排序后的机会列表，含切入角度和数据支撑]

## ⚠️ 风险提示
[注意事项]

## 📊 数据明细
[备查的原始数据]
```

---

## Monitoring 模式

**流程（保持不变）：**

```
1. 读取 memory 中的频道历史档案
2. browser 访问频道页抓最新数据
3. 对比历史：新增视频、播放变化、趋势判断
4. 更新 memory 档案
5. 输出变化报告
```

---

## 触发规则汇总

| 用户说 | 模式 | 工作流 |
|--------|------|--------|
| "帮我盯着 XXX 频道" | Monitoring | 直接抓频道 → 对比 → 输出 |
| "XX 类目有没有机会" | Discovery | **六步工作流** |
| "分析这个赛道" | Discovery | **六步工作流** |
| "XX 关键词竞争大吗" | Discovery | **六步工作流** |
| "最近有什么新产品" | Discovery | 六步工作流（以"新产品"为子分类） |

---

## 注意事项

- **永远先分析需求再搜索**，不可以用一个搜索词直接出报告
- **模糊类目必须拆分**，否则输出是垃圾
- **置信度必须标注**，不掩盖数据来源的局限性
- **Shorts 和长视频分开分析**，两者是不同市场
- **数据保存到 memory**，形成积累，不每次从零开始
