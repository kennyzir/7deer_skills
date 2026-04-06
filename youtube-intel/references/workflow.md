# youtube-intel 工作流参考

## Discovery 完整工作流

### Phase 1: 关键词扫描
1. 用 `browser` 工具打开 YouTube 搜索页
2. 输入目标关键词/类目
3. `snapshot` 获取搜索结果
4. 解析前20-30个视频的：标题、频道名、播放量、发布时间

### Phase 2: 频道详情抓取
1. 识别搜索结果中的独立频道
2. 对每个目标频道用 `browser` 访问频道页
3. 获取订阅数、总视频数、频道简介
4. 从频道页提取最近5-10个视频的数据

### Phase 3: 数据分析
1. 计算市场集中度（前3名吃掉多少流量）
2. 识别内容差异化机会
3. 评估切入难度

### Phase 4: 报告生成
1. 按模板格式化输出
2. 标注数据置信度
3. 如需要，输出到飞书文档

---

## Monitoring 完整工作流

### Phase 1: 初始化/读取历史
1. 检查 `memory/channels/{handle}.md` 是否存在
2. 读取历史数据（订阅数、最近视频列表、上次更新时间）

### Phase 2: 抓取最新数据
1. `browser` 访问频道页面
2. `snapshot` 获取最新视频列表
3. 对比历史数据，计算变化

### Phase 3: 趋势分析
1. 更新订阅数趋势
2. 识别新爆款视频
3. 分析内容方向变化

### Phase 4: 更新档案
1. 写入 `memory/channels/{handle}.md`
2. 输出变化报告到对话

---

## Skill 配置

Skill配置：`memory/youtube-intel-config.md`

```yaml
# youtube-intel 全局配置

## 默认设置
default_output: "chat"  # chat | feishu | notion
data_source_priority:
  - browser
  - social_blade
  - youtube_api

## 速率限制
browser_interval_ms: 2000
social_blade_interval_ms: 5000

## 置信度设置
min_samples_for_high_confidence: 10
```

---

## 常见问题处理

### YouTube 搜索被拦截
- 备选：使用 `web_search` + `web_fetch` 组合
- 再备选：直接用 `browser` 打开 YouTube 主页再跳转搜索

### 播放量显示模糊（"1万次观看"）
- 记录为近似值
- 在报告中标注"约"

### Social Blade 速率限制
- 每个请求间隔 ≥5秒
- 遇到429直接跳过，标记数据源为 fallback
