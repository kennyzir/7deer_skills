---
name: seo-backlink-submitter
description: 批量将网站提交到 AI 工具目录和 SEO 目录，获取反向链接。触发条件：用户说"提交网站到目录"、"SEO 外链"、"目录提交"、或"submit site to directories"。
---

# SEO Backlink Submitter

## 功能说明

批量将网站提交到 AI 工具目录和 SEO 目录，获取反向链接。自动检测目录是否接受免费提交，支持 Playwright 浏览器自动化表单填写。

## 数据格式（必须提供）

```json
{
  "name": "网站名称",
  "url": "https://example.com",
  "description": "网站描述",
  "email": "contact@example.com",
  "category": "Developer Tools",
  "tags": ["AI", "Agents", "Automation"]
}
```

## 执行流程

### Step 1：准备工作

确认系统已安装 Playwright：
```bash
pip install playwright && playwright install chromium
```

### Step 2：批量提交

运行 `scripts/batch_submit.py`：

```bash
# Navigate to the skill directory
cd .agent/skills/seo-backlink-submitter

python scripts/batch_submit.py \
  --site "https://你的网站.com" \
  --data '{"name":"网站名称","url":"https://你的网站.com","description":"描述","email":"邮箱","category":"Developer Tools"}' \
  --directories "references/directories.txt"
```

### Step 3：单目录检测

检测某个目录是否接受免费提交：

```bash
python scripts/check_directory.py https://aitoolshunt.com/submit
```

### Step 4：单目录提交

直接向某个目录提交：

```bash
python scripts/quick_submit.py https://aitoolshunt.com/submit \
  --data '{"name":"名称","url":"https://网站.com","description":"描述","email":"邮箱"}'
```

## 目录列表

目录列表位于 `references/directories.txt`，包含以下分类：
- AI Skills / Agent Skills Marketplaces
- Agent Skills Directories
- AI Tool Directories（ProductHunt、Futurepedia、FutureTools 等）
- Developer/Tools Directories（StackShare、DevPost 等）
- GitHub Awesome Lists

## 输出格式

提交结果以 JSON 格式保存，包含：

| 字段 | 说明 |
|------|------|
| directory | 目录名称 |
| url | 提交页面 URL |
| status | success / failed / paid / needs_login / error |
| timestamp | 提交时间 |
| error | 错误原因（如有） |

## 注意事项

- 部分目录需要账号登录，这类目录会被标记为 `needs_login`
- 收费目录会被标记为 `paid`，跳过提交
- 每个目录之间添加 2-5 秒延迟，避免触发反爬
- 定期检查目录政策变化，部分目录可能从免费变为收费
- 建议分批次提交，每次不超过 10 个目录

## 依赖

- Python 3.8+
- playwright (`pip install playwright && playwright install chromium`)
- aiohttp（用于异步 HTTP 请求）
