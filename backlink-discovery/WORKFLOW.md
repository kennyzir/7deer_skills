# Backlink Discovery — 执行流程

## 触发

用户说"发现 [URL] 的外链机会"或"找 [URL] 的外链平台"

## Step 1：解析 URL

从用户输入提取目标 URL。

## Step 2：生成发现任务 Prompt

生成一个完整的发现任务 prompt，包含：
- 目标 URL
- 种子关键词（从 URL 实时提取）
- 搜索指令（多轮搜索，每轮派生长尾词）
- 输出指令（写入 platforms.json + 生成 summary.md）

## Step 3：触发发现 Agent

```javascript
sessions_spawn(
  task: "【发现任务 prompt】",
  runtime: "isolated",
  cleanup: "keep"  // 保留 session，用户可查询状态
)
```

## Step 4：立即返回

```
已启动 {URL} 的外链发现任务
- 目标：300 个平台
- 发现中，后台运行
- 查询结果：skills/backlink-discovery/memory/{域名}/platforms.json
完成后自动写入 summary.md
```

## Step 5：Agent 端执行（隔离 session 内部）

Agent 内部执行以下任务：

### 关键词提取

从 URL 提取种子关键词：

```
https://robloxcalc.com
→ roblox, calculator, math, lua, game calculator, game, tool
```

### 多轮搜索（使用 web_search 工具）

Round 1: 用种子关键词搜索，发现初始平台
Round 2: 从 Round 1 结果派生新关键词，继续搜索
Round 3+: 重复，直到 300 个平台或无新发现

每轮至少搜索 5 个不同查询。

### 分类判断

对每个发现的平台判断：
- 平台类型（论坛/GitHub/Wiki/Alternatives/目录等）
- 最佳外链方式
- 相关度分数（0-1）

### 写入数据库

每轮结束后写入 platforms.json（避免丢失进度）。

### 达到 300 个平台 → 停止

生成 summary.md，输出最终报告。

## Step 6：用户查询

用户说"查询 https://xxx.com 的发现结果"

→ 读 platforms.json → 返回汇总

## 数据存储

```
memory/backlink-discovery/{提取的域名}/
├── platforms.json      # 所有发现平台
├── keywords.json      # 用过的关键词
├── search_rounds.json # 每轮记录
└── summary.md        # 最终报告
```

## 注意事项

- 触发后立即返回，不等待发现完成
- 发现 session 在后台独立运行
- 不同 URL 的发现任务互不干扰
- platforms.json 每轮追加，不覆盖
