---
name: roblox-site-architect
description: 专用于构建高流量 Roblox 游戏工具站的 SEO 架构与工程化方法论。从给定游戏词到最终上线部署的完整流程，包含每日自动关键词挖掘→页面构建→部署管道。
metadata:
  version: "3.1"
---

# 🏗️ Roblox Site Architect (RSA) Protocol v3.0

**Role**: SEO Architect (流量架构师)
**Core Function**: 拿到一个 Roblox 游戏名，从零构建完整工具站，并建立每日自动运营管道。

---

## ⚡ 执行原则（强制）

### 🚫 不要每步都问确认 — 直接执行
Skill 写了流程 → 直接走 → 遇到障碍再报告。

### 🚫 Hub 页面不需要确认
`/codes`, `/tier-list`, `/calculator` 等是**默认组成部分**，直接执行。

### 🚫 不要脑补，先调查
没看过游戏本身，不准说"这个游戏没有计算需求"。

### 📁 项目路径默认规则
新站点：`/Users/zirer/Projects/{domain-name}/`

### ⚠️ 两个已验证的同名 skill 禁止混淆
- **`research/roblox-keyword-to-page`** — {site-a}.gg 每日运营管道（41页）
- **`research/block-tales-site`** — {site-b}.com 每日运营管道

本 skill（`roblox-site-architect`）用于**从零新建站点**，不是运营已有站点。

---

## 完整架构

```
RSA Protocol 分两部分：

Part A: 新站构建（一次性）
  Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5

Part B: 每日运营管道（持续）
  定时 cron job 自动运行
  关键词挖掘 → 缺口分析 → 页面构建 → 部署 → 报告
```

---

# Part A: 新站构建（一次性）

## 📐 5 Phase 流程图

```
Phase 1              Phase 2              Phase 3              Phase 4              Phase 5
游戏调研        →    关键词挖掘       →    站点规划           →    站点构建          →   上线部署
(GAME RESEARCH)       (KEYWORD MINING)       (SITE PLANNING)        (SITE BUILDING)        (DEPLOY)
─────────────────────────────────────────────────────────────────────────────────────────────────
• 确认游戏信息        • 多源关键词抓取      • 选页面类型          • 搭建基础框架        • SEO 审计
• 找游戏数据源        • 价值评估            • 规划 Calculator     • 生成所有页面        • 验证构建
• 确定工具类型        • 决策矩阵            • 写游戏数据          • 填充内容           • 部署
• 找竞品站点                                  • 配 game.config   • 验证 Build          • 提交索引
```

---

## Phase 1: 游戏调研（GAME RESEARCH）

**目标**：确认游戏信息、数据来源、工具类型

### Step 1.1: 确认游戏基础信息

```bash
# 搜索游戏
web_search "Roblox {游戏名} official site:roblox.com"

# 确认游戏 ID（在 Roblox URL 里）
# https://www.roblox.com/games/{GAME_ID}/...
```

必查信息：
| 字段 | 来源 |
|------|------|
| 游戏名 | Roblox 商店页 |
| 游戏 ID | URL 中的数字 |
| 开发者 | Roblox 商店页 |
| 类型（Genre）| Roblox 商店页 |
| 当前版本 | YouTube 搜索 "Update" |
| 热度数据 | Roblox 商店页（喜欢/访问）|

### Step 1.2: 判断工具类型（决策树）

```
游戏有哪些可"算"机制？
│
├─ 有属性点/技能点分配？
│   └─ → 加点模拟器（Stat Calculator）
│
├─ 有抽卡/开箱/Gacha？
│   └─ → 抽卡模拟器（Fruit/Loot Simulator）
│
├─ 有武器/角色有不同数值？
│   └─ → DPS计算器 / 伤害计算器
│
├─ 有升级/刷装备机制？
│   └─ → 升级路线计算器 / 刷怪路线
│
├─ 有多个角色/宠物/坐骑可以比较？
│   └─ → Tier List（排行比较工具）
│
└─ 有代码兑换系统？
    └─ → Codes 页面（+ 监控自动化）
```

**每种工具类型都必须实现为独立页面。**

### Step 1.3: 找游戏数据源

按优先级：
1. **YouTube 视频描述** — 创作者自己列的 Related Keywords
2. **Gaming Media** — Beebom, PCGamesN, Eurogamer, Pocket Tactics, Game8
3. **Roblox Wiki** — 官方 Wiki（如果有）
4. **Reddit** — 信号源，不是确认源
5. **TikTok** — 热度信号，不是数据源

---

## Phase 2: 关键词挖掘（KEYWORD MINING）

### Step 2.1: 多源关键词抓取

**来源一：YouTube 视频描述（最重要）**
```bash
# 搜索游戏最新视频
web_search "site:youtube.com {游戏名} update 2026"
```

在视频描述底部找 "Related Keywords" 块 — 这是创作者自己的 SEO 目标词，高价值。

**来源二：Gaming Media**
```bash
web_search "{游戏名} codes wiki guide Beebom"
web_search "{游戏名} tier list PCGamesN"
```

**来源三：Google 相关搜索**
```bash
web_search "{游戏名} calculator"
web_search "{游戏名} simulator"
web_search "{游戏名} codes free"
```

### Step 2.2: 关键词分类

| 类型 | 示例关键词 | 页面类型 |
|------|-----------|---------|
| Codes | `{游戏名} codes 2026`, `free {游戏名} codes` | `/codes` |
| Calculator | `{游戏名} calculator`, `{游戏名} damage calculator` | `/calculator` |
| Tier List | `{游戏名} tier list`, `best {游戏名} weapons` | `/tier-list` |
| Guide | `{游戏名} guide`, `{游戏名} beginner guide` | `/beginner-guide` |
| Wiki | `{游戏名} wiki`, `{游戏名} all items` | `/wiki` |
| Update | `{游戏名} update`, `{游戏名} new update` | `/updates` |

### Step 2.3: 价值评估

| 信号 | 评估 |
|------|------|
| YouTube 50K+ views in <7 days | 高流量，确认需求 |
| Gaming media "new" 标签 | 新鲜内容，竞争不充分 |
| Beebom/PCGamesN 列出 | 高权威信号 |
| Reddit only（无 gaming media）| 未确认信号，仅监控 |
| YouTube description "Related Keywords" | 高意图，创作者验证 |

### Step 2.4: 决策

- **高价值**（高流量 + 低中竞争 + 低制作成本）→ 立即建
- **数据有误**（竞品数据过时/错误）→ 修正数据，不建新页
- **未确认信号**（仅 Reddit）→ 加入观察清单，不上线
- **无机会** → 报告"无新关键词"并结束

---

## Phase 3: 站点规划（SITE PLANNING）

### Step 3.1: 确定站点结构

基于 Phase 1-2 的调研结果，生成站点地图。

**必备页面**：

```
Hub 页面（核心变现页）:
  /calculator          ← 主工具页（必须）
  /codes               ← 兑换码（高流量）
  /tier-list           ← 排行榜

辅助内容页:
  /beginner-guide      ← 新手攻略
  /updates             ← 更新日志
  /wiki                ← 百科

技术页:
  /about               ← 关于
  /terms               ← 服务条款
  /privacy-policy      ← 隐私政策
  /not-found.tsx       ← 404
```

### Step 3.2: Calculator 类型选择（5种）

#### 类型 A：加点模拟器（Stat/Build Calculator）
**适用**：有属性点、技能树、觉醒系统的游戏
**功能**：选择加点方案 → 计算总属性/战斗力
**数据模型**：
```typescript
interface StatBuild {
  id: string;
  name: string;
  description: string;
  stats: Record<string, number>; // { strength: 50, defense: 200, ... }
  totalPower: number;
  bestFor: string[];
  tier: 'S' | 'A' | 'B' | 'C';
}
```

#### 类型 B：抽卡/掉落模拟器（Loot/Fruit Simulator）
**适用**：有抽卡、开箱、掉落的游戏
**功能**：模拟抽奖 → 展示结果（概率公示）
**数据模型**：
```typescript
interface LootPool {
  id: string;
  name: string;
  rarity: 'Legendary' | 'Epic' | 'Rare' | 'Common';
  probability: number; // 0.01 = 1%
  image?: string;
  description: string;
}

interface GachaBanner {
  id: string;
  name: string;
  startDate: string;
  endDate: string;
  rates: { legendary: number; epic: number; rare: number; common: number; };
  items: LootPool[];
}
```

#### 类型 C：伤害/DPS 计算器（Damage Calculator）
**适用**：有武器、技能伤害值的游戏
**功能**：选择武器+技能 → 计算理论 DPS
**数据模型**：
```typescript
interface Weapon {
  id: string;
  name: string;
  damage: number;
  attackSpeed: number; // 秒/次
  criticalRate: number;
  criticalDamage: number;
  element?: string;
}

interface DamageResult {
  weaponId: string;
  avgDPS: number;
  maxDPS: number; // 暴击时
  effectiveDPS: number; // 考虑防御后
}
```

#### 类型 D：升级/刷怪路线计算器（Progression Calculator）
**适用**：有等级、刷怪、农场机制的游戏
**数据模型**：
```typescript
interface FarmSpot {
  id: string;
  name: string;
  location: string;
  levelRequired: number;
  expPerHour: number;
  goldPerHour: number;
  bestWeapon: string;
}
```

#### 类型 E：掉落表模拟器（Drop Table Simulator）
**适用**：有 Boss 掉落、宝箱掉落的游戏
**数据模型**：
```typescript
interface DropTable {
  sourceName: string;
  drops: {
    itemName: string;
    rarity: string;
    dropRate: number; // 0.05 = 5%
    minQuantity: number;
    maxQuantity: number;
  }[];
}
```

---

## Phase 4: 站点构建（SITE BUILDING）

### ⚠️ HARD STOP — 第零步：强制预检（必须完成才能开始建站）

**这是本 skill 最高频失误点。**

#### 第零步：读游戏数据参考文件

先检查是否有该游戏的 session 数据文件：

```
skill_view(name='roblox-site-architect', file_path='references/{game-slug}-game-data.md')
```

**如果文件存在 → 用文件里的真实数据建站，不准自己编造任何游戏数值。**
**如果文件不存在 → 先完成 Phase 1 + Phase 2 调研，拿到真实数据后再建站。**

#### 第零步：视觉素材规范（HARD STOP — 建站前必须完成）

所有视觉素材**必须**来自真实游戏截图或自定义 SVG，**禁止用 emoji 或占位符**。

##### 素材清单

| 素材 | 文件路径 | 规格 | 来源 |
|------|---------|------|------|
| **Favicon** | `public/favicon.svg` | SVG，32×32 | 自定义 SVG（游戏主题图标） |
| **App Icon** | `public/favicon.svg` | 同上，共用 SVG | 同上 |
| **Hero 背景图** | `public/hero-bg.jpg` | 1280×720，JPG | YouTube 视频截图 |
| **OG 社交分享图** | `public/og-default.jpg` | 1200×630，JPG | YouTube 视频截图 resize |

##### SVG Favicon 规范（强制）

```
技术要求：
- 格式：SVG（矢量，可缩放）
- 尺寸：viewBox="0 0 32 32"（渲染为 32×32 / 16×16）
- 放在 public/ 目录，通过 layout.tsx 引用
- 引用方式：<link rel="icon" href="/favicon.svg" type="image/svg+xml" />
- 禁止只用 emoji 字符（♠️ / ⛏️ 等）作为 favicon

设计规范：
- 深色渐变背景：#1e1e3f → #0d0d1a
- 主体图形：游戏的代表性符号（pickaxe / sword / gem 等）
- 金属光泽效果：金色/银色调点缀（#f59e0b / #94a3b8）
- 风格：简洁扁平化，辨识度强，缩到 16×16 仍可辨认

{Game Name} 参考实现：
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1e1e3f"/>
      <stop offset="100%" stop-color="#0d0d1a"/>
    </linearGradient>
  </defs>
  <rect width="32" height="32" rx="6" fill="url(#bg)"/>
  <!-- 简化镐头形状，金色手柄，银色刃口 -->
  ...
</svg>
```

##### Hero 背景图规范

```
获取方式：
1. YouTube 搜索游戏名，找 gameplay 视频（推荐：游戏官方频道 / 大型创作者）
2. 提取视频 ID，从 YouTube thumbnail API 下载：
   curl -sL "https://img.youtube.com/vi/{videoId}/maxresdefault.jpg" -o public/hero-bg.jpg
3. 如果 maxresdefault 不存在，降级到 sddefault：sddefault.jpg

验证（必须执行）：
1. file public/hero-bg.jpg  → 确认是 JPEG
2. 用 PIL 检查尺寸：python3 -c "from PIL import Image; img=Image.open('public/hero-bg.jpg'); print(img.size)"
   → 必须是 1280×720 或更大，4:3 视频（如 1920×1080）crop/resize 到 1280×720
3. vision_analyze(image_url="file:///Users/zirer/Projects/{project}/public/hero-bg.jpg", question="Is this a real game screenshot? Describe what you see.")
   → 确认是真实游戏画面，排除频道封面、intro、logo

如果 YouTube 截图质量太差（640×480 sddefault）：用 PIL resize 到 1280×720，注明"low-res upscaled"
```

##### OG 社交分享图规范

```
尺寸：1200×630 px（JPG，质量 85）
命名：public/og-default.jpg（固定名称，所有页面默认共享）

生成方式：
python3 -c "
from PIL import Image
img = Image.open('public/hero-bg.jpg')
# Crop/resize to 1200x630 (approx 1.91:1 ratio)
w, h = img.size
target_ratio = 1200/630
current_ratio = w/h
if current_ratio > target_ratio:
    new_w = int(h * target_ratio)
    offset = (w - new_w) // 2
    img = img.crop((offset, 0, offset + new_w, h))
else:
    new_h = int(w / target_ratio)
    offset = (h - new_h) // 2
    img = img.crop((0, offset, w, offset + new_h))
img = img.resize((1200, 630), Image.LANCZOS)
img.save('public/og-default.jpg', 'JPEG', quality=85)
print('OG image saved: 1200x630')
"

在 layout.tsx 的 metadata 中引用：
openGraph: {
  images: [{ url: '/og-default.jpg', width: 1200, height: 630 }],
}
twitter: {
  card: 'summary_large_image',
  images: ['/og-default.jpg'],
}
```

##### 第零步验证清单（必须逐项确认）

开始 Step 4.1 前，输出以下验证结果：

```
[RSA 预检]
✅ 游戏数据文件已读：{文件名}
✅ 数据字段对照：{列出我即将写入的字段 vs 参考文件里的字段，全部匹配}
✅ 模板站组件已对照：{列出已核对的组件}
✅ 视觉素材已获取：
   - public/favicon.svg  — {已验证/未完成}
   - public/hero-bg.jpg  — {已验证/未完成，尺寸}
   - public/og-default.jpg — {已验证/未完成，尺寸}
✅ 视觉素材来源审查：{确认来自真实游戏截图，不是 emoji/占位符}
✅ 无自创数据：{确认没有编造任何游戏数值}
→ 可以开始建站
```

**没有输出这个验证清单，不准进入 Step 4.1。**

---

#### 第零步：对照模板站组件

**从 `resources/` 复制模板文件**（真实存在），比从头写更稳：

```
skill_dir = ~/.hermes/skills/.archive/roblox-site-architect/resources/
```

| 组件 | 资源路径 | 说明 |
|------|---------|------|
| `src/components/Header.tsx` | `resources/components/Header.tsx` | 顶部导航 |
| `src/components/Footer.tsx` | `resources/components/Footer.tsx` | 底部免责 |
| `src/lib/layout.tsx` | `resources/lib/layout.tsx` | 根布局（含 SEO metadata） |
| `src/lib/data.ts` | `resources/lib/data.ts` | 数据读取函数 |
| `src/lib/seo.ts` | `resources/lib/seo.ts` | Schema 构建函数 |
| `src/lib/globals.css` | `resources/lib/globals.css` | Tailwind 入口 |
| `public/robots.txt` | `resources/public/robots.txt` | 爬虫规则 |
| `scripts/deploy.sh` | `resources/scripts/deploy.sh` | 部署脚本 |

**复制命令（Python subprocess）：**

```python
import shutil, os
src = '/Users/zirer/.hermes/skills/.archive/roblox-site-architect/resources'
dst = '/Users/zirer/Projects/{project-name}'

for item in ['components', 'lib', 'public', 'scripts']:
    src_path = f'{src}/{item}'
    if os.path.exists(src_path):
        shutil.copytree(src_path, f'{dst}/{item}', dirs_exist_ok=True)
        print(f'Copied: {item}/')
```

**同时对照 block-tales-site 架构清单**（补充核对）：

```
skill_view(name='roblox-site-architect', file_path='references/block-tales-site-architecture.md')
```

必须核对的动态数据文件（需根据游戏重写，不能直接复制）：

| 组件 | 说明 |
|------|------|
| `src/data/{type}.json` | 主数据文件（pickaxes.json / bosses.json 等）|
| `src/app/sitemap.ts` | 动态 sitemap |
| `src/app/[slug]/page.tsx` | 动态详情页（如果游戏有可索引项）|

#### 第零步验证清单（必须逐项确认）

开始 Step 4.1 前，输出以下验证结果：

```
[RSA 预检]
✅ 游戏数据文件已读：{文件名}
✅ 数据字段对照：{列出我即将写入的字段 vs 参考文件里的字段，全部匹配}
✅ 模板站组件已复制：{列出已从 resources/ 复制的组件}
✅ 视觉素材已获取：
   - public/favicon.svg  — {已验证/未完成}
   - public/hero-bg.jpg  — {已验证/未完成，尺寸}
   - public/og-default.jpg — {已验证/未完成，尺寸}
✅ 视觉素材来源审查：{确认来自真实游戏截图，不是 emoji/占位符}
✅ 无自创数据：{确认没有编造任何游戏数值}
→ 可以开始建站
```

**没有输出这个验证清单，不准进入 Step 4.1。**

---

### Step 4.1: 初始化项目

**从 `resources/` 复制模板文件**（真实存在），再按需修改。不要自己从零写配置文件。

```bash
SKILL_DIR="$HOME/.hermes/skills/.archive/roblox-site-architect/resources"
PROJ="/Users/zirer/Projects/{domain-name}"

# 1. 创建目录结构
mkdir -p "$PROJ"/src/{app,components,lib,data}
mkdir -p "$PROJ"/public
mkdir -p "$PROJ"/scripts

# 2. 复制 components/
cp "$SKILL_DIR"/components/*.tsx "$PROJ"/src/components/

# 3. 复制 lib/
cp "$SKILL_DIR"/lib/*.tsx "$PROJ"/src/lib/
cp "$SKILL_DIR"/lib/*.ts "$PROJ"/src/lib/
cp "$SKILL_DIR"/lib/*.css "$PROJ"/src/lib/

# 4. 复制 config/ → 根目录
cp "$SKILL_DIR"/config/package.json "$PROJ"/
cp "$SKILL_DIR"/config/postcss.config.mjs "$PROJ"/

# 5. 复制 public/
cp "$SKILL_DIR"/public/robots.txt "$PROJ"/public/

# 6. 复制 scripts/
cp "$SKILL_DIR"/scripts/*.sh "$PROJ"/scripts/

# 7. 根目录配置文件
cp "$SKILL_DIR"/game.config.json "$PROJ"/src/data/game.config.json

echo "Done. Now edit game.config.json and the data files to match your game."
```

**不要用 `@import "tailwindcss"`**（这是 Tailwind v4 语法，装的是 v3 会报 `Module not found`）。正确写法：

```
/* src/app/globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### Step 4.2: 配置 game.config.json

在 `/src/data/game.config.json` 创建：

```json
{
  "game": {
    "name": "{游戏名}",
    "robloxId": "{GAME_ID}",
    "developer": "{开发者名}",
    "genre": "{类型}",
    "currentVersion": "{版本号}",
    "lastUpdated": "{YYYY-MM-DD}"
  },
  "stats": {
    "visits": "{访问量}",
    "favorites": "{收藏数}",
    "onlineNow": "{在线人数}"
  },
  "seo": {
    "siteTitle": "{游戏名} Guide & Tools {年份}",
    "siteDescription": "The ultimate {游戏名} companion — {核心工具}, codes, and guides. Updated {频率}.",
    "baseUrl": "https://{domain-name}",
    "primaryKeywords": ["{游戏名}", "{游戏名} Roblox", "{游戏名} codes"],
    "secondaryKeywords": ["{游戏名} {tool}", "{游戏名} guide", "{游戏名} tier list"]
  },
  "routes": [
    { "path": "/", "title": "{游戏名} Guide", "priority": "1.0" },
    { "path": "/calculator", "title": "{游戏名} Calculator", "priority": "0.9" },
    { "path": "/codes", "title": "{游戏名} Codes", "priority": "0.9" },
    { "path": "/tier-list", "title": "{游戏名} Tier List", "priority": "0.9" },
    { "path": "/beginner-guide", "title": "{游戏名} Beginner Guide", "priority": "0.8" },
    { "path": "/updates", "title": "{游戏名} Updates", "priority": "0.8" }
  ],
  "calculator": {
    "type": "{stat|loot|damage|progression|drop}",
    "dataFile": "{data-calculator.json}"
  }
}
```

### Step 4.3: 生成 Calculator 页面

**数据文件**：`src/data/calculator-{type}.json`
**页面文件**：`src/app/calculator/page.tsx`

**通用结构**：
- `'use client'` 标记（必须，Calculator 是交互式组件）
- `useState` 管理输入状态
- `useMemo` 计算结果（性能关键）
- 实时显示计算结果

**SEO 元数据**：
```typescript
export const metadata: Metadata = {
  title: '{游戏名} Calculator — {具体功能} ({年份})',
  description: 'Calculate {具体功能} for {游戏名}. Updated {日期}.',
};
```

**FAQ Schema**（必须加，Google 精选片段）：
```typescript
generateFaqSchema([
  { question: 'How to use the {游戏名} Calculator?', answer: 'Select your...' },
  { question: 'Is the {游戏名} Calculator free?', answer: 'Yes, completely free.' }
])
```

### Step 4.4: 生成 Codes 页面

Codes 页面的数据结构（`src/data/codes.json`）：

```typescript
interface Code {
  code: string;        // 兑换码
  reward: string;      // 奖励描述
  source: string;       // Beebom / PCGamesN / Reddit
  addedDate: string;    // YYYY-MM-DD
  status: 'active' | 'expired';
  isNew?: boolean;      // 7天内新增的
}
```

Codes 页面的标准结构：
1. **Hero Section** — H1 包含 "Codes" + 游戏名 + 最后更新时间
2. **Active Codes Table** — 绿色徽章 + 一键复制按钮
3. **Expired Codes Section** — 灰色，降低权重
4. **How to Redeem** — 步骤说明
5. **FAQ Schema**

### Step 4.5: 生成 Tier List 页面

Tier List 的数据结构（`src/data/tier-list.json`）：

```typescript
interface TierItem {
  id: string;
  name: string;
  tier: 'S' | 'A' | 'B' | 'C' | 'D';
  image?: string;
  description: string;
  stats?: Record<string, number | string>;
  bestBuilds?: string[];
  counters?: string[];
  updatedDate: string;
}
```

### Step 4.6: 其他页面生成

按照 `routes` 数组，依次生成：
- `/beginner-guide` — 新手攻略
- `/updates` — 更新日志
- `/wiki` — 百科页
- `/about` — 关于页
- `/terms` — 服务条款
- `/privacy-policy` — 隐私政策
- `src/app/not-found.tsx` — 404 页面

### Step 4.7: 技术配置

**tsconfig.json**：
```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": { "@/*": ["./src/*"] }
  }
}
```

**next.config.mjs**（必须是 `.mjs`，不是 `.ts`）：
```javascript
/** @type {import("next").NextConfig} */
const nextConfig = {
  output: "export",
  images: { unoptimized: true },
  trailingSlash: true,
};
export default nextConfig;
```
⚠️ Next.js 14.2 不支持 `next.config.ts`，必须用 `.mjs` 或 `.js`。

**sitemap.ts**（必须加 `export const dynamic = 'force-static'`）：
```typescript
import { MetadataRoute } from 'next';
export const dynamic = 'force-static';
// 从 game.config.json 的 routes 数组生成
```

**robots.ts vs public/robots.txt — 二选一，不要共存。**

**不要用** `yield` 作为变量名（JS 保留字）。

---

## Phase 5: 上线部署（DEPLOY）

### Step 5.1: 构建验证

```bash
cd /Users/zirer/Projects/{domain-name}
npm install
npm run build 2>&1 | tail -30
```

检查：
- 所有路由显示 `○` 或 `●`（没有 `✗`）
- 无 TypeScript 错误
- 无 ESLint 错误

### Step 5.2: SEO 审计（硬性门槛，任一 ✗ 禁止上线）

| 检查项 | 命令/方法 |
|--------|----------|
| robots.txt 存在且可访问 | `curl -s -o /dev/null -w "%{http_code}" https://{url}/robots.txt` → 200 |
| sitemap.xml 包含全部页面 | `curl -s {url}/sitemap.xml \| grep -c '<loc>'` → 应 >10 |
| 每个页面有 `<title>` | 浏览器 DevTools 检查 |
| Canonical URL 正确 | 检查源码 |
| Schema 无 JSON-LD 语法错误 | [validator.schema.org](https://validator.schema.org) |
| LCP < 4s（移动端） | PageSpeed Insights |

### Step 5.3: Git 提交

⚠️ **Terminal foreground blocking issue**: `git commit` 在 terminal() 调用时可能被 foreground 进程管理器拦截。

**Workaround — 用 Python subprocess：**

```python
import subprocess
result = subprocess.run(
    ['git', 'add', '-A'],
    cwd='/Users/zirer/Projects/{domain-name}',
    capture_output=True, text=True
)
print("STDOUT:", result.stdout)

result = subprocess.run(
    ['git', 'commit', '-m', 'feat: initial {游戏名} site — calculator, codes, tier-list'],
    cwd='/Users/zirer/Projects/{domain-name}',
    capture_output=True, text=True
)
print("STDOUT:", result.stdout, "STDERR:", result.stderr)

result = subprocess.run(
    ['git', 'push'],
    cwd='/Users/zirer/Projects/{domain-name}',
    capture_output=True, text=True
)
print("STDOUT:", result.stdout)
```

**不要用** `terminal()` 调用 git commit/push — 会被 foreground manager 拦截。

### Step 5.4: Cloudflare Pages 部署

⚠️ **wrangler pages project create 必须先跑**，项目不存在时直接 deploy 会报 "Project not found"。

```bash
# 1. 创建 Cloudflare Pages 项目（仅首次需要）
wrangler pages project create {project-name} --production-branch=main

# 2. 部署 out/ 目录
wrangler pages deploy out --project-name={project-name}
```

**如果域名已添加到 Cloudflare**：
- 登录 Cloudflare Dashboard → Pages → `{project-name}` 项目 → Settings → Custom domains → 添加 `{site-domain}.gg`

**验证域名**：
```bash
# 用 browser_navigate 打开正式域名，不要用 urllib（SSL 问题）
browser_navigate url="https://{site-domain}.gg"
```

### Step 5.5: 验证上线

```bash
# 1. 所有 Hub 页面 200 OK
for page in calculator codes tier-list beginner-guide updates wiki about terms privacy-policy; do
  code=$(curl -s -o /dev/null -w "%{http_code}" "https://<deployment-url>/$page")
  [ "$code" != "200" ] && echo "FAIL: $page → $code"
done

# 2. sitemap 包含全部页面（应为 20+）
curl -s "<deployment-url>/sitemap.xml" | grep -c '<loc>'

# 3. 404 页面正常
curl -s -o /dev/null -w "%{http_code}" "https://<deployment-url>/nonexistent-page"
# 应输出 404
```

---

# Part B: 每日运营管道（持续）

## 概述：自动关键词→页面→部署管道

这是从 **{site-a}.gg** 和 **{site-b}.com** 两个站点验证过的每日运营逻辑。

```
每天定时触发：
  YouTube 关键词挖掘
      ↓
  价值评估 + 缺口分析
      ↓
  发现新关键词？
      ├─ 是 → 构建新页面 → Build验证 → Git push → 自动部署
      └─ 否 → [SILENT] 输出，不打扰
```

**已验证的工作流（直接复用）**：
- `research/roblox-keyword-to-page` — {site-a}.gg 每日管道
- `research/block-tales-site` — {site-b}.com 每日管道

---

## 创建每日 cron job

### Step B-1: 确定项目对应的 skill

| 游戏站 | Skill |
|--------|-------|
| {site-a}.gg | `research/roblox-keyword-to-page` |
| {site-b}.com | `research/block-tales-site` |
| **新站点** | 需要创建新的每日运营 skill（见 Step B-2） |

### Step B-2: 为新站点创建每日运营 skill

**触发条件**：用户说"为 {游戏名} 建立每日关键词监控"

创建 skill：`/Users/zirer/.hermes/skills/{game-name}-keyword-to-page/SKILL.md`

```markdown
---
name: {game-name}-keyword-to-page
description: {游戏名} 每日关键词挖掘 → 页面构建 → 部署管道。定时 cron job 驱动。
category: research
---

# {游戏名} Keyword Mining & Page Pipeline

目标网站：{domain-name}（{repo-name} 仓库）

## 仓库信息

```
路径:      /Users/zirer/Projects/{repo-name}
技术栈:    Next.js + TypeScript (App Router)
部署:      git push → Cloudflare Pages 自动部署
数据文件:  src/data/game.config.json, src/data/{type}.json
lib:       src/lib/data.ts
Sitemap:   src/app/sitemap.ts
siteUrl:   https://{domain-name}
```

## Step 1: 关键词挖掘

### 数据源（按可靠性排序）

1. **YouTube 搜索结果页**（唯一可靠源）
   - 视频 views = 真实搜索需求
   - 路径：`https://www.youtube.com/results?search_query={游戏名}+{keyword}`
   - ⚠️ 只用搜索结果列表页；点进视频详情页在 cron 环境全部被封

2. **Gaming Media**
   - Beebom, PCGamesN, Eurogamer, Pocket Tactics, Game8
   - 找 patch notes、update 内容

3. **Reddit**
   - 信号源，不是确认源
   - 找 "what happened to X", "secret", "unlock" 类型问题

4. **Game8 / Sportskeeda**
   - patch notes 页面

⚠️ **cron 环境必封**：Reddit oEmbed、Fandom Wiki、Google/Bing、YouTube oEmbed API、Roblox 游戏页。

### 并行挖掘（用 delegate_task 并行跑）

```
子任务1：YouTube 搜索 "{游戏名} {keyword}"
子任务2：site:reddit.com "{游戏名} {keyword}"
子任务3："{游戏名} {keyword}" update OR patch OR new
子任务4：site:game8.com "{游戏名}"
```

**cron 环境 Yahoo 搜索可用**（Bing/Google 全被 CAPTCHA 挡）。

### 关键词派生方向

- 版本内容：`update`, `patch`, `demo`, `new`
- 机制问题：`how to beat`, `weakness`, `攻略`, `guide`
- 社区问题：`secret`, `hidden`, `unlock`, `code`
- 热门内容：搜 YouTube 侧边栏 related suggestions
- 被删除内容：`deleted`, `removed`, `nerfed`

---

## Step 2: 价值评估

| 维度 | 高 | 中 | 低 |
|------|----|----|-----|
| 搜索量 | YouTube >50K views | 10K-50K | <10K |
| 竞争度 | 大站已占首位 | 小站有覆盖 | 无SEO页面 |
| 制作成本 | 需要视频嵌入/复杂交互 | boss页模板即可 | 顺手做 |
| 收益 | 长尾流量入口 | 补充覆盖 | 微不足道 |

**"无新内容"标准：**
1. 所有已知内容已有对应页面
2. 无新 Update 内容词
3. 无明显内容缺口
4. YouTube 无 >10K views 新视频

---

## Step 3: 缺口分析

必须核查已有页面列表：

```bash
# 所有页面
find src/app -type f -name "page.tsx" | sort

# 数据文件内容
node -e "console.log(Object.keys(require('./src/data/game.config.json').routes || {}))"
```

---

## Step 4: 页面构建

### 页面模板（通用）

```tsx
import type { Metadata } from "next";
import Link from "next/link";
import { siteConfig } from "@/data/site";
import { getCurrentMonthYear } from "@/lib/site-date";
import { buildBreadcrumbSchema } from "@/lib/seo";

const monthYear = getCurrentMonthYear();

export const metadata: Metadata = {
  title: `{游戏名} {PageName} (${monthYear}) — {Primary Keyword}`,
  description: `{含关键词，≤160字符，含价值主张}`,
  alternates: { canonical: `${siteConfig.domain}/{page-slug}` },
};

export default function Page() {
  const breadcrumbSchema = buildBreadcrumbSchema([
    { name: "Home", item: siteConfig.domain },
    { name: "{PageName}", item: `${siteConfig.domain}/{page-slug}` }
  ]);

  return (
    <main className="mx-auto max-w-5xl px-4 py-10">
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(breadcrumbSchema) }} />
      {/* 页面内容 */}
    </main>
  );
}
```

---

## Step 5: 数据更新

```typescript
// 添加到对应的数据文件
// brainrots[] / codes[] / bosses[] 等
```

---

## Step 6: Sitemap 同步

检查 `src/app/sitemap.ts` 是否包含新页面路由：

```typescript
// changeFrequency — 只有 /codes 和 /updates 是 daily
route === "/codes" || route === "/updates" ? "daily" : "weekly"

// priority — 只有首页/codes/tier-list/calculator 是 0.9
route === "" ? 1
  : route === "/codes" || route === "/tier-list" || route === "/calculator" ? 0.9
  : 0.8
```

---

## Step 7: Build 验证

```bash
cd /Users/zirer/Projects/{repo-name} && npm run build 2>&1 | tail -30
```

- `○ /new-page` 或 `● /new-page` 必须出现
- 无 `error` 行
- ⚠️ TypeScript lint 噪声（来自 node_modules）不算是失败，exit_code: 0 + 页面路径出现 = 真验证

---

## Step 8: 部署

⚠️ **Terminal foreground blocking issue**: 用 Python subprocess，不要用 terminal() 调用 git：

```python
import subprocess
result = subprocess.run(
    ['git', 'add', '-A'],
    cwd='/Users/zirer/Projects/{repo-name}',
    capture_output=True, text=True
)
result = subprocess.run(
    ['git', 'commit', '-m', 'feat: add {keyword} page'],
    cwd='/Users/zirer/Projects/{repo-name}',
    capture_output=True, text=True
)
print("STDERR:", result.stderr)
result = subprocess.run(
    ['git', 'push'],
    cwd='/Users/zirer/Projects/{repo-name}',
    capture_output=True, text=True
)
```

⚠️ HTTPS push 超时 fallback：
```bash
git remote set-url origin git@github.com:kennyzir/{repo-name}.git && git push && git remote set-url origin https://github.com/kennyzir/{repo-name}.git
```

---

## [SILENT] 输出规则

> ⚠️ 这是独立于"无新内容"报告的输出指令。cron job 的分发层会：
> - 收到 `[SILENT]` → 抑制交付，不发报告
> - 收到任何其他内容 → 正常发报告

**必须输出 `[SILENT]` 的条件（同时满足）：**
- 判定结果：没有高价值新关键词
- 输出内容仅有：`"今日无新增关键词"` 或类似短句
- 即：发现=报告，**未发现=输出精确 `[SILENT]`，不多说一个字**

**禁止输出 `[SILENT]` 的情况：**
- 发现新关键词，有页面要构建 → 正常写报告
- 有 Update 发布或代码变更 → 正常写报告
- 输出内容超过一行 → 永远不是 SILENT

**输出格式模板（有新内容）：**
```
✅ 部署成功
关键词：[新发现的关键]
页面：/xxx
commit: xxx
```

**输出格式模板（无新内容）：**
```
今日无新增关键词，继续监控。
```

---

## 每周节奏

游戏更新通常在**周六**发布。周六白天 cron 大概率无新内容，周六 22:00 后才是真正窗口。

---

## 坑

0. **🚫 不要跳过 YouTube 调研就用假数据建站**
   这是本 skill 最高频失误。上一轮 {project-name} 就是没做 YouTube 调研，导致用假数据（6个乱编的pickaxe、错误的power值）建了一个垃圾站。
   **正确流程（Phase 1 + Phase 2 必须先跑完）**：
   - Phase 1：浏览器打开 Roblox 商店页 → 记录真实游戏ID/类型/在线人数/收藏数
   - Phase 2：YouTube 搜索 "site:youtube.com {游戏名} update 2026" → 找4-5个真实视频 → 逐个点进描述里挖游戏机制数据
   - **没看到真实游戏数据（pickaxe列表/video views/升级路径），不准开始建站**
   - 真实数据示例（AlphaShoe/74views视频）：Coal→Stone→Crystal→Crystal II 升级路径，1500个pickaxe后出Crystal
   - 真实数据示例（Bax/318万订阅）："I Took {Game Name} TOO FAR" → 揭露 Tier 10 系统

0b. **🚫 不要跳过 Header/Footer/动态路由等核心组件**
   本 skill 最高频失误第二名：把 block-tales-site 当"参考资料"而不是"施工标准"，导致建出来的站缺导航、缺 Footer、缺动态详情页、缺数据管道。
   **每次建新站，对照 `references/block-tales-site-architecture.md` 的核对清单逐项确认。**
   必须覆盖：layout.tsx（含 Header+Footer）、Header.tsx、Footer.tsx、lib/data.ts、lib/seo.ts、sitemap.ts 动态读取、[slug] 动态页、scripts/git-deploy.py、public/og-default.svg

0c. **🚫 HARD STOP 没有执行机制**
   HARD STOP 写了"读完才能继续"，但没有验证手段，导致 agent 读完仍然跳过。
   **第零步验证清单必须输出，不输出就不能进入 Step 4.1。**

1. sitemap 忘记更新 — 新页面加 sitemap 才能被 Google 发现
2. `${monthYear}` 在 build 时 Next.js 自动替换，不需要手动处理
3. 动态路由 `[slug]` 的 OpenGraph 需要 `generateMetadata`，不能用静态 export
4. YouTube 搜索结果页是唯一可靠数据源；视频详情页/oEmbed/cron 全部不可用
5. browser_navigate 后**立即** browser_snapshot，不滚动
6. 不要在 subagent 里跑 browser — 超时，在主 session 串行
7. YouTube URL 不带 `sp=` 参数 — 直接 `?search_query=...`
8. **数据驱动的 [slug] 路由**：添加到对应的数据数组后，generateStaticParams() 自动捕获，无需额外配置
9. **PageIntro 组件路径**是 `@/components/ui/PageIntro`
10. **Git push 用 Python subprocess**，terminal() 调用 git 会被 foreground manager 拦截
11. **`@import "tailwindcss"` 是 v4 语法**，装的是 v3 会导致 `Module not found: Can't resolve 'tailwindcss'` 错误。正确写法是 `@tailwind base; @tailwind components; @tailwind utilities;`
12. **`next.config.ts` Next.js 14.2 不支持** — 会报错 "configuring Next.js via 'next.config.ts' is not supported"。改用 `next.config.mjs`
13. **wrangler pages deploy 前必须先 `wrangler pages project create`** — 否则报 "Project not found"
14. **`execute_code` 写 TSX/JSON 文件会破坏内容** — execute_code 的 Python triple-quoted heredoc 写入多行内容时，会引入隐性字符错误（实践验证：money-making page 写坏，build 报 "Unexpected token `main`"）。写 TSX/JSON → 用 `write_file`。execute_code 只用于：目录创建、subprocess 调用、JSON 数据读取验证。
```

### Step B-3: 创建 cron job

```bash
cronjob action=create \
  name="{游戏名} 每日关键词挖掘" \
  prompt="## 任务：{游戏名} 每日关键词挖掘 & 页面更新

目标网站：{domain-name}（{repo-name} 仓库）

### 工作流程

**第一步：加载 skill**
先加载：`skill_view(name='{game-name}-keyword-to-page')`
严格按照 skill 的步骤执行。

**第二步：关键词挖掘**
按照 skill Step 1 执行多源关键词挖掘。

**第三步：缺口分析 + 页面构建**
按照 skill Step 2-4 执行。

**第四步：Build 验证 + 部署**
按照 skill Step 7-8 执行。

**第五步：输出报告**
有新内容：正常报告（关键词、页面路径、commit）
无新内容：输出精确 `[SILENT]`，不多说一个字" \
  schedule="0 11 * * *" \
  repeat=365 \
  deliver=origin \
  skills='["{game-name}-keyword-to-page"]'
```

---

## Calculator 工具页 — 完整模板

### 数据模型速查

| 类型 | 数据文件 | 页面路由 | 核心功能 |
|------|---------|---------|---------|
| A: Stat | `calculator-stat.json` | `/calculator` | 加点方案→总战力 |
| B: Loot | `calculator-loot.json` | `/calculator` | 模拟抽卡/掉落概率 |
| C: Damage | `calculator-damage.json` | `/calculator` | DPS 计算 |
| D: Progression | `calculator-progression.json` | `/calculator` | 刷怪路线/升级时间 |
| E: Drop | `calculator-drop.json` | `/calculator` | Boss 掉落模拟 |

### Calculator 页面模板（类型 A: Stat Calculator）

```tsx
'use client';

import { useState, useMemo } from 'react';
import type { Metadata } from 'next';

import CALCULATOR_DATA from '@/data/calculator-stat.json';

interface StatBuild {
  id: string;
  name: string;
  description: string;
  stats: Record<string, number>;
  totalPower: number;
  bestFor: string[];
  tier: 'S' | 'A' | 'B' | 'C';
}

const ALL_STATS = ['strength', 'defense', 'agility', 'intelligence', 'luck'] as const;

const TIER_COLORS: Record<string, string> = {
  S: 'bg-red-500/20 text-red-400 border-red-500/40',
  A: 'bg-orange-500/20 text-orange-400 border-orange-500/40',
  B: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/40',
  C: 'bg-gray-500/20 text-gray-400 border-gray-500/40',
};

const STAT_ICONS: Record<string, string> = {
  strength: '💪',
  defense: '🛡️',
  agility: '⚡',
  intelligence: '🧠',
  luck: '🎲',
};

export default function CalculatorPage() {
  const [selectedBuildId, setSelectedBuildId] = useState<string | null>(null);
  const [customStats, setCustomStats] = useState<Record<string, number>>({
    strength: 0, defense: 0, agility: 0, intelligence: 0, luck: 0,
  });
  const [activeTab, setActiveTab] = useState<'presets' | 'custom'>('presets');

  const builds = CALCULATOR_DATA.builds as StatBuild[];

  const customTotalPower = useMemo(() => {
    return Object.values(customStats).reduce((sum, v) => sum + v, 0);
  }, [customStats]);

  const getCustomTier = (power: number): string => {
    if (power >= 300) return 'S';
    if (power >= 200) return 'A';
    if (power >= 100) return 'B';
    return 'C';
  };

  const selectedBuild = builds.find((b) => b.id === selectedBuildId);

  const handleStatChange = (stat: string, delta: number) => {
    setCustomStats((prev) => ({
      ...prev,
      [stat]: Math.max(0, prev[stat] + delta),
    }));
  };

  return (
    <div className="max-w-5xl mx-auto px-4 py-10">
      {/* Hero */}
      <div className="mb-8">
        <h1 className="text-3xl font-extrabold tracking-tight mb-2">
          {CALCULATOR_DATA.gameName} Calculator
        </h1>
        <p className="text-gray-500">
          Plan your build and calculate stats. Updated {CALCULATOR_DATA.lastUpdated}.
        </p>
      </div>

      {/* Tab: Presets vs Custom */}
      <div className="flex gap-2 mb-6">
        <button
          onClick={() => setActiveTab('presets')}
          className={`px-4 py-2 rounded-lg font-semibold text-sm ${
            activeTab === 'presets' ? 'bg-blue-600 text-white' : 'bg-slate-100 dark:bg-slate-800'
          }`}
        >
          Preset Builds
        </button>
        <button
          onClick={() => setActiveTab('custom')}
          className={`px-4 py-2 rounded-lg font-semibold text-sm ${
            activeTab === 'custom' ? 'bg-blue-600 text-white' : 'bg-slate-100 dark:bg-slate-800'
          }`}
        >
          Custom Build
        </button>
      </div>

      {activeTab === 'presets' && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
          {builds.map((build) => (
            <button
              key={build.id}
              onClick={() => setSelectedBuildId(build.id)}
              className={`p-4 rounded-xl border text-left ${
                selectedBuildId === build.id
                  ? 'border-blue-500 bg-blue-50 dark:bg-blue-950/30'
                  : 'border-slate-200 dark:border-slate-700 hover:border-blue-300'
              }`}
            >
              <div className="flex justify-between items-start mb-2">
                <span className="font-bold">{build.name}</span>
                <span className={`text-xs px-2 py-0.5 rounded border font-mono ${TIER_COLORS[build.tier]}`}>
                  T{build.tier}
                </span>
              </div>
              <p className="text-xs text-gray-500 mb-3">{build.description}</p>
              <div className="text-sm font-mono text-amber-500 font-bold">
                Power: {build.totalPower.toLocaleString()}
              </div>
            </button>
          ))}
        </div>
      )}

      {activeTab === 'custom' && (
        <div className="mb-8">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">
            {ALL_STATS.map((stat) => (
              <div key={stat} className="p-4 rounded-xl bg-slate-50 dark:bg-slate-900 border">
                <div className="flex justify-between items-center mb-2">
                  <span className="font-semibold text-sm">
                    {STAT_ICONS[stat]} {stat.charAt(0).toUpperCase() + stat.slice(1)}
                  </span>
                  <span className="font-mono font-bold text-blue-600">{customStats[stat]}</span>
                </div>
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => handleStatChange(stat, -5)}
                    className="w-8 h-8 rounded-lg bg-slate-200 dark:bg-slate-700 font-bold"
                  >
                    −
                  </button>
                  <input
                    type="range"
                    min={0}
                    max={300}
                    value={customStats[stat]}
                    onChange={(e) => setCustomStats((prev) => ({ ...prev, [stat]: Number(e.target.value) }))}
                    className="flex-1 accent-blue-600"
                  />
                  <button
                    onClick={() => handleStatChange(stat, 5)}
                    className="w-8 h-8 rounded-lg bg-slate-200 dark:bg-slate-700 font-bold"
                  >
                    +
                  </button>
                </div>
              </div>
            ))}
          </div>

          <div className="p-6 rounded-xl bg-gradient-to-br from-blue-50 to-purple-50 border">
            <div className="flex justify-between items-center mb-4">
              <span className="font-bold text-lg">Your Build</span>
              <span className={`text-sm px-3 py-1 rounded-full border font-mono ${TIER_COLORS[getCustomTier(customTotalPower)]}`}>
                T{getCustomTier(customTotalPower)}
              </span>
            </div>
            <div className="text-4xl font-black text-center">
              {customTotalPower.toLocaleString()}
              <span className="text-lg text-gray-500 font-normal ml-2">Total Power</span>
            </div>
          </div>
        </div>
      )}

      {selectedBuild && (
        <div className="mt-8 p-6 rounded-xl border">
          <h2 className="text-xl font-bold mb-4">{selectedBuild.name} — Full Stats</h2>
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 mb-4">
            {ALL_STATS.map((stat) => (
              <div key={stat} className="p-3 rounded-lg bg-slate-50 dark:bg-slate-900 text-center">
                <div className="text-xs text-gray-500 uppercase">{stat}</div>
                <div className="text-xl font-black">{selectedBuild.stats[stat] || 0}</div>
              </div>
            ))}
          </div>
          <div className="p-4 rounded-lg bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-900">
            <h3 className="font-bold mb-2">Best For</h3>
            <div className="flex flex-wrap gap-2">
              {selectedBuild.bestFor.map((tag) => (
                <span key={tag} className="px-3 py-1 rounded-full bg-amber-100 dark:bg-amber-900/40 text-sm">
                  {tag}
                </span>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* FAQ Section */}
      <div className="mt-12 p-6 rounded-xl border">
        <h2 className="text-xl font-bold mb-4">Frequently Asked Questions</h2>
        <div className="space-y-4">
          <div>
            <h3 className="font-semibold mb-1">How accurate is the calculator?</h3>
            <p className="text-gray-600 dark:text-gray-400 text-sm">
              Stats are based on official game data and community testing. Formulas are updated with each new game version.
            </p>
          </div>
          <div>
            <h3 className="font-semibold mb-1">Is the calculator free to use?</h3>
            <p className="text-gray-600 dark:text-gray-400 text-sm">
              Yes, completely free. No login or account required.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
```

---

## References（参考文件索引）

| 文件 | 内容 |
|------|------|
| `references/block-tales-site-architecture.md` | 模板站完整架构对照清单（layout/Header/Footer/data/lib/sitemap/[slug]） |
| `references/keyword-to-page-pipeline.md` | 关键词挖掘 7 步管道 |
| `references/{game-name}-game-data.md` | 游戏数据示例（codes、更新时间线） |
| `references/codes-hub-template.md` | Codes 页面模板 |
| `references/pickaxe-tycoon-game-data.md` | {Game Name} session data (YouTube creators, pickaxe list, tier system, codes status) |
| `references/pickaxe-tycoon-retrospective.md` | 建站复盘文档（2026-05-27）：过程回顾、Bug清单、经验总结、方法复盘，下次建站前必读 |

⚠️ `resources/` 目录是**真实存在的**，不要无视它。Step 4.1 应该从这里复制模板文件，而不是自己从零写。

## 已验证的每日运营 Skill（直接使用）

| Skill | 适用站点 |
|-------|---------|
| `research/roblox-keyword-to-page` | {site-a}.gg（41页，每日运营中）|
| `research/block-tales-site` | {site-b}.com（每日运营中）|
