---
name: backlink-intelligence
description: |
  AI/Tools目录外链情报收集与评估。当需要为项目寻找外链机会时使用，包括：
  (1) 搜索免费AI工具目录、SaaS目录、创业目录
  (2) 批量评估目标站点的收费/登录/审核要求
  (3) 记录外链提交结果到memory文件
  (4) 生成待提交清单
  触发场景：用户要求"提交外链"、"找目录"、"增加曝光"、"外链情报"等
---

# Backlink Intelligence

## Overview

自动收集和评估AI工具目录、SaaS目录等外链机会，提高外链提交效率。

## Workflow

### Step 1: 确定目标项目信息

收集待提交的网站信息：
- 网站URL
- 一句话描述
- 详细描述（可选）
- 类别标签
- 联系邮箱

> 如果用户未提供，使用项目默认信息或询问用户

### Step 2: 搜索目录

使用以下关键词搜索（根据目标类型选择）：

**AI/Agent相关**：
- `AI tools directory submit free 2026`
- `AI agent marketplace directory submit`
- `submit your AI tool free`
- `LLM agent tools directory`

**通用SaaS/Startup**：
- `SaaS tools directory submit free`
- `free startup directories submit`
- `submit your startup free`

**游戏/工具类**：
- `gaming tools directory submit free`
- `Roblox tools directory submit`
- `developer tools directory free`

**中文目录**：
- `AI工具导航 提交`
- `工具导航 收录`

### Step 3: 评估目标

使用浏览器访问submit页面，评估以下条件：

| 条件 | 评估标准 |
|------|----------|
| 收费？ | 看pricing页面，$0=免费，其他=收费 |
| 登录？ | 需要注册/登录=需账号 |
| 审核？ | 有审核期=记录时间 |
| 表单？ | 复杂表单=效率低 |

**判断标准**：
- ✅ 可以提交：无收费、无需登录、表单简单
- ⚠️ 待处理：需要账号/验证
- ❌ 放弃：收费、需要复杂登录、上传图片

### Step 4: 记录结果

将结果写入 `memory/[项目名]-外链记录.md`，格式：

```markdown
# [项目名] 外链提交记录

## 网站信息
- **网站**: [URL]
- **描述**: [描述]
- **类别**: [类别]

## ✅ 成功提交
| 目录 | URL | 状态 | 备注 |
|------|-----|------|------|

## ❌ 失败/放弃
| 目录 | 原因 | 日期 |
|------|------|------|

## 📊 统计
- **成功**: X个
- **失败**: X个

## 🔄 待处理
- [待办项]
```

### Step 5: 输出清单

向用户报告：
- 成功提交的目录数
- 失败/放弃的目录及原因
- 待处理事项（需要用户配合的账号等）

## 常用目录参考

### 已知免费/简单
| 目录 | URL | 备注 |
|------|-----|------|
| AI Tool Hunt | https://aitoolshunt.com | 免费，需邮件 |
| StartupInspire | https://www.startupinspire.com | 有免费选项，需注册 |

### 已知收费
| 目录 | 收费 | 备注 |
|------|------|------|
| Futurepedia | $247+ | 贵 |
| Toolify | $99 | 中 |
| TAAFT | $49-347 | 中 |
| Aitoolnet | $9.9 | 便宜 |

### 已知需登录
- BetaList (X登录)
- 600.tools (Google/GitHub)
- SaaSHub (域名邮箱验证)

## Tips

1. **批量测试**：先测试5-10个目录，快速判断成功概率
2. **优先免费**：2026年大多数AI目录都收费了，免费的很少
3. **中文目录**：竞争较少，可能更容易通过
4. **GitHub列表**：awesome-xxx系列可以提交PR
5. **社区发帖**：Reddit indiehackers, r/aiagents 等