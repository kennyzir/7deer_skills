# Survive Zombie Arena — 建站执行参考

## 项目信息
```
游戏: Survive Zombie Arena
开发商: Nectarforge Studios
Game ID: 114204398207377
上线: 2025-12-13
访问量: 170.8M visits
域名: {site-domain}.net
临时 CF Pages: https://a1121481.{project-name}.pages.dev
```

## 关键词研究结论（Step 1）

### 高需求关键词
| 关键词 | 竞争度 | 优先级 |
|--------|--------|--------|
| survive zombie arena codes | 高 | P0 |
| survive zombie arena tier list | 中 | P0 |
| survive zombie arena best class | 中 | P0 |
| survive zombie arena beginner guide | 低 | P0 |
| survive zombie arena weapons | 低 | P1 |
| survive zombie arena wave guide | 低 | P1 |
| survive zombie arena loadout | 低 | P1 |
| survive zombie arena necromancer | 低 | P1 |
| survive zombie arena credits | 低 | P1 |

### 竞品分析
| 竞品 | URL | 弱点 |
|------|-----|------|
| {site-domain}.com (wiki) | {site-domain}.com | 有首页但无结构化攻略 |
| IGN Wiki | ign.com/survive-zombie-arena-roblox | 只有 codes |
| games.gg | games.gg/roblox/guides | 无专属 codes 页 |
| ProGameGuides | progameguides.com | 无武器库 |

## 路由架构（Hub + Spoke）
```
/                           主页
/codes                      Codes 列表 ✅
/classes                    职业总览 ✅
/classes/[slug]             职业详情 ×9 ✅
/tier-list                  排行榜 ✅
/weapons                    武器表 ✅
/wave-guide                 波浪攻略 ✅
/loadouts                   Build 推荐 ✅
/credits-guide              Credits 路线 ✅
/beginner-guide             新手指南 ✅
/updates                    版本动态 ✅
/about                      关于页 ✅
/terms                      服务条款 ✅
/privacy-policy             隐私政策 ✅
/sitemap.xml                ✅
/robots.txt                 ✅
/not-found.tsx              404 ✅
```

## 技术栈
- Next.js 15 App Router + `output: 'export'`
- Tailwind CSS v4 (`@tailwindcss/postcss`)
- TypeScript
- Cloudflare Pages (`wrangler pages deploy`)
- 项目路径: `<project-root>`

## 关键陷阱（遇到过的）

### 1. `yield` 是 JS 保留字
data.ts 里对象属性不能用 `yield`，会报 `Expected '</', got 'yield'`。用 `amount` 代替。

### 2. sitemap.ts 缺 `export const dynamic = 'force-static'`
Next.js App Router + `output: export` 模式，sitemap 和 robots 路由必须有此 export，否则 build 失败。

### 3. robots.txt 不能用 `robots.ts`（App Router）
App Router 的 `robots.ts` 在 `output: export` 模式下需要额外配置。直接放 `public/robots.txt` 更简单。

### 4. Tailwind v4 需要 `@tailwindcss/postcss`
`postcss.config.mjs` 必须用 `@tailwindcss/postcss`（不是 `tailwindcss/postcss`），package.json 也要对应加 `@tailwindcss/postcss: ^4.0.0`。

### 5. 404 页面文件名必须是 `not-found.tsx`
不是 `404.tsx`。Next.js App Router 用 `not-found.tsx` 处理 404。

## 部署命令
```bash
cd <project-root>

# 首次创建 Cloudflare Pages 项目
npx wrangler pages project create {project-name} --production-branch=main

# 部署（每次更新）
npx wrangler pages deploy out/ --project-name={project-name}

# 域名绑定（需要 Cloudflare Dashboard 手动操作）
# Pages → {project-name} → Custom domains → 添加 {site-domain}.net
# CNAME 指向: a1121481.{project-name}.pages.dev
```

## 验证命令
```bash
# 所有页面 HTTP 200
for page in codes tier-list classes weapons wave-guide loadouts credits-guide beginner-guide updates about terms privacy-policy; do
  echo -n "$page: "; curl -s -o /dev/null -w "%{http_code}" "https://a1121481.{project-name}.pages.dev/$page"
done

# sitemap 包含所有页面
curl -s https://a1121481.{project-name}.pages.dev/sitemap.xml | grep -o '<loc>[^<]*</loc>' | wc -l
# 应输出 26+
```

## Sitemap 内容（26 页）
- 13 个静态路由
- 9 个职业详情页（`/classes/[slug]`）
- 4 个武器详情页（`/weapons/[slug]`）— 注：本次未实现 weapons/[slug]，可直接访问 `/weapons` 总览页

## data.ts 结构
```ts
export const GAME_CONFIG = { seo, stats, links }
export const ACTIVE_CODES = [{ code, reward, source, reliability }]
export const EXPIRED_CODES = [{ code, reward, expired }]
export const CLASSES = [{ slug, name, rarity, description, soloTier, teamTier, abilities, bestFor }]
export const WEAPONS = [{ slug, name, type, damage, fireRate, magSize, unlockWave, tier }]
export const WAVE_STRATEGY = { early, mid, late }
export const LOADOUTS = [{ slug, name, description, class, weapons, upgrades, creditsGoal, tier }]
```

## Footer 导航模板
```tsx
<Link href="/about">About</Link>
<Link href="/terms">Terms</Link>
<Link href="/privacy-policy">Privacy</Link>
```
