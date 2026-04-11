---
name: seo-link-strategy
description: |
  给定一个网站 URL + 发件邮箱，输出完整外链建设方案 + 个性化邮件 + Gmail 自动发送。
  触发条件：用户说"分析外链策略"、"建设外链"、"外链方案"。
  输入：网站 URL + 发件人名字 + 发件邮箱
  输出：策略报告 + 个性化邮件 + 自动发送
---

# SEO Link Strategy — 外链自动化三阶

**核心：不凭空判断，基于真实数据生成。**

---

## 第一阶段：动态平台发现 + 联系人检测

### 核心逻辑（动态发现，不锁死平台数量）

```
目标 URL → 提取关键词 → 动态搜索 → 发现平台 → 保存到数据库
                                              ↓
                                    外链库（随时间积累变强）
```

### 执行方式（自动化脚本）

```bash
# 动态发现新平台（搜索 + 检测联系人）
python3 scripts/outreach_db.py <网站URL> --type <类型> --max 15

# 列出已有平台库
python3 scripts/outreach_db.py --list

# 只生成搜索查询（不实际搜索）
python3 scripts/outreach_db.py <网站URL> --query-only
```

### 动态发现流程

```
Step 1: 从 URL 提取关键词
        example.com → [your product keywords]
        ↓
Step 2: 生成搜索查询（基于关键词 + "alternatives"/"submit"/"tools I use"）
        "geography game best free alternatives 2026"
        "free game submit directory"
        ... 共 20 个查询
        ↓
Step 3: DuckDuckGo 搜索，提取结果中的域名
        发现新平台（如 technew24.com, game4life.com 等）
        ↓
Step 4: 对比已有数据库（去重）
        新平台进入 Step 5 检测
        已存在平台跳过
        ↓
Step 5: Playwright 检测每个新平台的：
        - 联系邮箱（从页面/页脚提取）
        - 提交表单 URL
        - 是否需要登录/付费
        ↓
Step 6: 自动分类 P0/P1/P2 → 保存到数据库
```

### 数据库存储

| 文件 | 内容 |
|------|------|
| `memory/outreach_db/platforms.json` | 所有发现的平台，含联系人、状态、层级 |
| `memory/outreach_db/email_history.json` | 已发送邮件历史 |

### 平台分级（自动 + 动态）

| 层级 | 判断逻辑 | 行动 |
|------|---------|------|
| 🔴 P0 | Alternatives 文章（标题含 best/alternatives） | 优先发邮件 |
| 🟡 P1 | 有表单可免费提交 / 目录站 | 目录提交 |
| 🟢 P2 | 需登录 / 需付费 / 社区 | 长尾覆盖 |

### 查询已有库

```bash
# 查看所有平台
python3 scripts/outreach_db.py --list

# 只看有邮箱的 P0 平台
python3 scripts/outreach_db.py --list --tier P0 --has-email
```


**网站类型：** `game` | `tool` | `saas` | `content` | `blog`

**示例：**
```bash
python3 scripts/contact_discoverer.py https://example.com --type game --tiers P0
```

### 内置外链平台分级体系（22个平台）

| 层级 | 类型 | 价值 | 平台数 |
|------|------|------|--------|
| 🔴 P0 | Alternatives 文章站 | 最高，SEO流量大 | 8个 |
| 🟡 P1 | 目录站 + 资源页 | 中等 | 5个 |
| 🟢 P2 | 社区 + GitHub | 长尾覆盖 | 8个 |

#### P0 平台库（Alternatives 文章站）

| 平台 | 联系人 | 验证状态 |
|------|--------|---------|
| TechCult | info@techcult.com | ⚠️ 需手动确认 |
| Beebom | contact@beebom.com | ✅ 已验证 |
| PrivacySavvy | info@privacysavvy.com | ⚠️ 需手动确认 |
| Tech4Fresher | admin@tech4fresher.com | ✅ 已验证 |
| SolutionSuggest | editor@solutionsuggest.com | ✅ 已验证 |
| GeckoAndFly | contact@geckoandfly.com | ✅ |
| GameRant | tips@gamerant.com | ✅ |
| AlternativeTo | (产品页) | 自助提交 |

#### P1 平台库（目录站）

| 平台 | 提交方式 |
|------|---------|
| FreeArcade | 免费发布 |
| SilverGames | 免费发布 |
| itch.io | 社区发帖 |
| CrazyGames | 申请收录 |
| HTML5GameDevs | 免费提交 |

#### P2 平台库（社区）

| 平台 | 执行方式 |
|------|---------|
| Reddit r/geoguessr | 发帖介绍 |
| Reddit r/gaming | 发帖（遵守规则）|
| GitHub awesome-geography | PR 提交 |
| Sheppard Software | 联系提交 |
| LizardPoint | 联系提交 |

### 框架匹配逻辑

| 网站类型 | 匹配 P0 平台 |
|---------|------------|
| game | TechCult, Beebom, PrivacySavvy, Tech4Fresher, SolutionSuggest + 游戏目录 |
| tool | TechCult, Beebom, AlternativeTo, Tech4Fresher + 工具目录 |
| saas | ProductHunt, AlternativeTo, G2, Capterra + 行业文章站 |
| content | TechCult, Beebom, GeckoAndFly, GameRant |
| blog | TechCult, Beebom, GeckoAndFly |

### 输出

- 每个 P0/P1 平台 → 邮箱 + Twitter + 作者名 + 验证状态
- 标记哪些平台需要手动处理（无公开邮箱）

---

## 第二阶段：个性化邮件生成

### 执行方式（自动化脚本）

```bash
python3 scripts/email_generator.py <网站URL> --sender-name "<名字>" --sender-email "<邮箱>"
```

**或手动传入联系人列表**（由第一阶段提供）

### 核心逻辑

```
1. 对每个有邮箱的 P0 平台：
   ↓
2. 自动访问其 Alternatives 文章 URL
   ↓
3. 提取：真实文章标题 + 已收录竞品列表
   ↓
4. 竞品对比：你的产品 vs 已收录 → 生成差异化 USP
   ↓
5. 填充邮件模板 → 完整个性化邮件
```

### 竞品分析逻辑

- 脚本自动抓取目标平台的实际文章页面
- 从页面提取已收录的竞品名称（如：geotastic, geoguessr）
- 与你的产品 USP 对比，排除已有角度
- 输出：你的产品在这个文章里的差异化角度

**示例输出（Tech4Fresher）：**
```
文章: "10 Best GeoGuessr Alternatives to Play in 2025"
已收录竞品: geotastic, geoguessr
差异化USP:
  - 100% free, no account required
  - H5 iframe format
  - Multiple modes (Duels + Multiplayer)
邮件角度: "covers 2 competitors. YourProduct differentiates with: 100% free..."
```

### 邮件模板库

| 模板 | 适用平台类型 | 特点 |
|------|------------|------|
| alternatives_article | Alternatives文章站 | 附 USP + 文章标题 |
| game_directory | 游戏目录 | 强调即时可玩性 |
| resource_page | 资源页 | 强调读者价值 |
| general | 其他 | 通用介绍 |

### 输出

每封邮件包含：
- 收件人（从第一阶段获取）
- 个性化 Subject（基于实际文章标题）
- 正文（基于实际文章内容 + 差异化 USP）
- 你的网站链接

---

## 第三阶段：Gmail 自动发送

### 执行方式

使用 browser(profile=user) 打开 Gmail，填表发送：

```javascript
browser(action=open, profile=user, url="https://mail.google.com/mail/u/0/#inbox")
→ 点击 Compose
→ 填入邮件内容（from email_generator）
→ 检查邮件内容（确认产品链接存在）
→ 点击 Send
→ 等待 "Message sent"
→ 重复
```

### 发送流程

1. **展示邮件内容** → 用户确认后发送
2. **如果需要付费**：记录 → 跳过 → 告知用户
3. **如果发送失败**（网络/2FA）：记录 → 提示用户手动处理
4. **发送后更新记录**：每个邮件标记 ✅ 已发送 + 时间

---

## 三阶段完整使用方式

### 用户输入

```
网站：https://example.com
发件邮箱：your_email@example.com
发件人名字：YourName
```

### 执行序列

```
第一阶段：
python3 scripts/contact_discoverer.py https://example.com --type game --tiers P0
→ 输出：Tech4Fresher ✅ / SolutionSuggest ✅ / Beebom ✅ / PrivacySavvy ⚠️

第二阶段：
python3 scripts/email_generator.py https://example.com --sender-name YourName --sender-email your_email@example.com
→ 输出：3 封个性化邮件（Subject + 正文 + 链接）

第三阶段：
browser → Gmail → 逐封发送
```

### 完整输出文件

| 文件 | 内容 |
|------|------|
| `scripts/contact_discoverer.py` | 平台分级 + 联系人发现 |
| `scripts/email_generator.py` | 文章抓取 + 个性化邮件生成 |
| `memory/<网站>-外链策略.md` | 策略报告存档 |
| `memory/<网站>-联系人.md` | 联系人记录 |
| `memory/<网站>-邮件草稿.md` | 生成邮件存档 |

---

## 注意事项

- **永远先分析再推荐**：不推荐没有匹配依据的外链路径
- **发邮件前必须展示邮件内容**：用户确认后再发送（或用户已明确授权）
- **如果对方要求付费**：记录 → 跳过，回复"我们只做免费外链"
- **无邮箱的平台**：使用 Twitter DM / LinkedIn 代替
- **PRODUCT_DB 维护**：新产品先注册到 `email_generator.py` 的 `PRODUCT_DB`
