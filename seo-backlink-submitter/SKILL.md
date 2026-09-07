---
name: seo-backlink-submitter
description: 批量将网站提交到 AI 工具目录和 SEO 目录，获取反向链接。触发条件：用户说"提交网站到目录"、"SEO 外链"、"目录提交"、或"submit site to directories"。
---

# SEO Backlink Submitter

## 功能说明

批量将网站提交到 AI 工具目录和 SEO 目录，获取反向链接。自动检测目录是否接受免费提交，支持 Playwright 浏览器自动化表单填写。单目录辅助器默认只生成 dry-run 计划，只有显式传入 `--submit` 才允许访问网络和点击提交按钮。

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

默认 dry-run 不需要浏览器依赖。批量检测或真实提交前，确认系统已安装 Playwright：
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

使用 [targets/README.md](targets/README.md) 约定的 JSON 文件准备单目录提交。以下命令只校验输入并显示计划，不访问目录网站：

```bash
python scripts/submit_to_directory.py \
  --directory https://aitoolshunt.com/submit \
  --target targets/your-domain-com.json
```

人工核对 dry-run 输出后，才可显式授权一次真实提交：

```bash
python scripts/submit_to_directory.py \
  --directory https://aitoolshunt.com/submit \
  --target targets/your-domain-com.json \
  --submit
```

`submit_triggered` 只表示浏览器已经点击提交控件，不代表目录方已经审核或收录。缺少 Playwright、找不到表单字段或提交控件、输入 JSON 无效时，脚本会以非零状态退出并给出错误。

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
- playwright（仅真实提交需要：`pip install playwright && playwright install chromium`）
- aiohttp（`check_directory.py` 需要）
