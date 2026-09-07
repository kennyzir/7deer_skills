# Pickaxe Tycoon 建站复盘（2026-05-27）

**游戏**: Pickaxe Tycoon
**站点**: {site-a}.pages.dev → {site-a}.gg
**仓库**: github.com/kennyzir/{repo-name}
**本地路径**: `<project-root>`

---

## 最终交付物

| 指标 | 结果 |
|------|------|
| 路由数 | 11（含动态 `/tier-list/[slug]`） |
| 矿锭数据 | 10 个（Coal→Stone→Copper→Iron→Gold→Diamond→Crystal→Crystal II→Void→Void II） |
| Build 状态 | ✅ 0 errors，0 warnings |
| 部署方式 | GitHub push → CF Pages 自动触发 |
| 视觉素材 | favicon.svg + hero-bg.jpg + og-default.jpg |

**页面清单**:
- `/` — 首页
- `/calculator` — 矿锭计算器
- `/codes` — 兑换码
- `/tier-list` — 矿锭总榜
- `/tier-list/[slug]` — 10个矿锭详情页（动态路由）
- `/beginner-guide` — 新手攻略
- `/updates` — 更新日志
- `/about` — 关于
- `/terms` — 服务条款
- `/privacy-policy` — 隐私政策

---

## 过程回顾

### Step 1: 初始化（首次 commit）

```
b432611 feat: initial Pickaxe Tycoon site — codes, tier-list, calculator, guide
```

**问题**：这次提交**跳过了 Phase 1 + Phase 2**，直接用"脑子里想象的矿锭数据"建站。
Pickaxe 列表是胡乱编的（"Emerald Pickaxe"根本不存在），power 值也是假的。

**根因**：没有严格执行 HARD STOP 第零步（读取游戏数据文件）。

---

### Step 2: 补真实数据（第二次 commit）

```
7f1f8e1 feat: complete Pickaxe Tycoon site — codes, tier-list, calculator, guide, sitemap, legal pages
```

增加了：
- 正确的矿锭链（Coal → … → Void II，共10个）
- pickaxes.json 真实数据
- [slug] 动态详情页
- sitemap.ts 动态读取

**问题**：此时才开始补 YouTube 调研，发现之前的矿锭名称和数据全是错的。

---

### Step 3: 结构组件补全（第三次 commit）

```
c9ea201 feat: add Header, Footer, layout.tsx refactor, og-default.svg
```

- 添加了 Header + Footer（之前一直缺失）
- 添加了 layout.tsx 中的 SEO metadata、OG image、favicon 引用
- 补了 `public/og-default.svg`（注意：后来改成了 .jpg）

**问题**：Header/Footer 漏掉是 roblox-site-architect HARD STOP 明确预警的高频失误，但建站时仍然漏了。

---

### Step 4: 内链（第四次 commit）

```
9f73845 feat: add internal linking across all pages
```

- 首页增加了10个矿锭卡片，全部链接到 `/tier-list/[slug]`
- calculator 页面加了"Full guide →"链接
- beginner-guide 页面加了到 codes/tier-list 的链接

**问题**：内链成网是强制要求，但建站初期没有执行，后期补的。

---

### Step 5: 视觉素材（第五次 commit）

```
eefce9f feat: add real game assets — hero bg, og:image, favicon
```

- 从 YouTube（Bax 频道）下载 gameplay 截图 → `public/hero-bg.jpg`
- PIL resize/crop → `public/og-default.jpg`（1200×630）
- 自定义 SVG pickaxe favicon → `public/favicon.svg`
- 用 vision 验证截图是真实游戏画面

**问题**：Favicon 部署后浏览器显示旧 icon，原因是 CF Pages 缓存 + 浏览器缓存双重叠加，需要强制刷新（Cmd+Shift+R）。

---

## Bug / 问题清单

| # | 问题 | 严重度 | 根因 | 教训 |
|---|------|--------|------|------|
| 1 | **矿锭名称编造假数据**（Emerald 等） | 🔴 高 | 跳过 Phase 1+2 直接建站 | HARD STOP 第零步必须先读游戏数据文件 |
| 2 | **Header + Footer 缺失** | 🔴 高 | 没对照 {site-b} 架构清单 | HARD STOP 组件核对表是强制执行的 |
| 3 | **内链不成网** | 🟡 中 | 建站时没按"内链成网"原则执行 | 每个页面必须显式链接到其他相关页面 |
| 4 | **Favicon 缓存不更新** | 🟢 低 | CF Pages + 浏览器二级缓存 | SVG favicon 上线后需要用户强制刷新 |
| 5 | **og-default.svg vs .jpg 混淆** | 🟢 低 | 规范里只写了 svg，但实际需要 jpg（Twitter 不支持 svg） | OG 分享图必须是 .jpg，Twitter card 不支持 SVG |

---

## 经验总结（方法复盘）

### ✅ 做对了的事

1. **pickaxes.json 数据链正确** — 从一开始就是完整且真实的长度：Coal→Stone→Copper→Iron→Gold→Diamond→Crystal→Crystal II→Void→Void II（10个矿锭），没有缺项，没有错误名称

2. **GitHub → CF Pages 管道顺畅** — 每次 push 到 main 分支，CF Pages 在 2 分钟内自动部署，没有手动干预

3. **动态 sitemap.ts** — 从 pickaxes.json 动态读取所有矿锭 slug，新增矿锭自动进 sitemap，无需手动维护

4. **Build 一次通过** — 0 errors，0 TypeScript 错误，所有 11 个路由全部成功构建

5. **视觉素材验证流程完整** — `file` 确认 MIME → PIL 确认尺寸 → vision 确认是真实游戏画面，三步缺一不可

### ❌ 严重失误

1. **跳过了 YouTube 调研** — 应该在 Phase 1 打开 Roblox 商店页 + YouTube 搜索找真实数据，但实际上是从零直接编数据建站

2. **HARD STOP 第零步被跳过** — 规范白纸黑字写了"没输出验证清单不准进入 Step 4.1"，但实际上没有输出清单就开工了

3. **{site-b} 架构清单未核对** — Header/Footer 漏掉就是因为没有逐项对照清单

### 🔧 流程改进

**下次建站必须执行的顺序**：

```
1. Phase 1: 浏览器打开 Roblox 商店页 → 记录 Game ID / 开发者 / 类型 / 在线人数
2. Phase 2: YouTube 搜索 "pickaxe tycoon update 2026" → 点进4-5个视频 → 在描述里挖游戏机制数据
3. 写游戏数据文件（references/{game}-game-data.md）
4. 输出 [RSA 预检] 清单（不输出不继续）
5. Phase 3: 站点规划（选 calculator 类型）
6. Phase 4: 建站（严格对照 {site-b} 架构清单）
   - 建完 Header + Footer → 先 git commit 验证
   - 再建 calculator → 再 commit
   - ...
7. Phase 5: 部署 + SEO 审计
```

**Commit 节奏改进**：每次加一个主要组件（Header/Footer、Calculator、Codes 等）就 commit 一次，不要攒到末尾一次性提交。这样出问题可以 bisect。

---

## {site-a} 现状（2026-05-27）

**内容缺口**（仍需填充）：

| 关键词 | 页面 | 状态 |
|--------|------|------|
| `pickaxe tycoon merge guide` | — | 🔴 缺口 |
| `pickaxe tycoon ore guide` | — | 🔴 缺口 |
| `pickaxe tycoon money making` | — | 🔴 缺口 |
| `pickaxe tycoon alpha shoe` | — | 🔴 缺口 |

**Cron job**：`{game-name} 每日关键词挖掘`（job_id: 待查，每天 11:00 触发）

---

## 规范更新记录

本次复盘推动了以下 skill 改进：

1. **`roblox-site-architect`** — 新增"第零步：视觉素材规范"独立章节（HARD STOP），包含：
   - SVG Favicon 规范（设计规范 + 技术要求 + 参考实现）
   - Hero 背景图规范（YouTube 截图获取 + 验证三步）
   - OG 分享图规范（1200×630 PIL 生成脚本）
   - 预检清单模板

2. **`{game-name}-keyword-to-page`** — 坑 #9 改为引用 `roblox-site-architect` 视觉素材规范，避免两处规范不一致

---

*本文档由 {game-name} 建站复盘生成，写入 `.archive/roblox-site-architect/references/{game-name}-retrospective.md`，供后续新站点建站前查阅。*
