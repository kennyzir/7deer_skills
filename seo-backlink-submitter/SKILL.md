---
name: seo-backlink-submitter
description: 为网站生成目录提交计划，并在用户显式授权时通过浏览器填写单个或批量目录表单。适用于“提交网站到目录”“SEO 外链”“目录提交”或“submit site to directories”等请求。
---

# SEO Backlink Submitter

这个 Skill 使用统一的安全模型处理单目录和批量目录：默认只读取本地配置、验证输入并输出 dry-run 计划，不访问目录网站；只有命令中明确加入 `--submit` 才允许浏览器访问和点击提交。

## 目标数据

按 [targets/README.md](targets/README.md) 创建本地 JSON：

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

`name`、`url`、`description`、`email` 是必需字符串；`category` 和 `tags` 可选。URL 必须是无内嵌凭据的绝对 HTTP(S) URL。

## 单目录流程

先运行默认 dry-run；它不会导入 Playwright，也不会访问网络：

```bash
python scripts/submit_to_directory.py \
  --directory https://directory.example/submit \
  --target targets/example-com.json
```

人工核对目标和目录后，显式加入 `--submit` 才执行真实提交：

```bash
python scripts/submit_to_directory.py \
  --directory https://directory.example/submit \
  --target targets/example-com.json \
  --submit
```

兼容入口 `scripts/quick_submit.py` 接受完全相同的参数并转发到上述逻辑；它同样默认 dry-run，不含硬编码目录。

## 批量流程

目录文本每行一个 HTTP(S) URL，空行和 `#` 注释会被忽略。可以使用 [references/directories.txt](references/directories.txt)，也可以按项目维护自己的文件。

默认只输出离线批量计划：

```bash
python scripts/batch_submit.py \
  --target targets/example-com.json \
  --directories references/directories.txt
```

核对计划后，显式加入 `--submit` 才逐项打开浏览器并尝试提交：

```bash
python scripts/batch_submit.py \
  --target targets/example-com.json \
  --directories references/directories.txt \
  --submit
```

批量入口复用单目录入口的目标验证和真实提交函数，不会先默认联网检测再自动提交。

## 可选的只读目录检测

需要主动检查页面是否存在表单、登录、付费或反向链接要求时，可明确运行联网检测器：

```bash
python scripts/check_directory.py https://directory.example/submit
```

检测结果只是页面启发式判断，不会点击提交。

## 提交安全条件

- 没有 `--submit` 时，单目录、批量和兼容入口都不得访问网络。
- 真实提交前，页面必须成功匹配并填写 `name`、`url`、`description`、`email` 四个字段；缺少任何一个都会关闭浏览器、返回错误且不查询或点击提交控件。
- `category` 是可选字段，未匹配不会阻止四个必需字段完整的提交。
- `submit_triggered` 只表示脚本点击了提交控件，不代表目录方接收、审核、发布或产生了反向链接。
- 登录、验证码、付费墙或不受支持的表单需要人工处理；不要绕过访问控制。
- 凭据和项目目标文件不得写入仓库；当前 `.gitignore` 已排除 `targets/` 下的项目数据。

## 输出与退出状态

- dry-run 输出 `not_submitted` 和待处理目录，不写结果文件。
- 真实单目录成功点击时输出 `submit_triggered`。
- 批量真实提交逐项输出 `submit_triggered` 或 `error`；任一错误会使批量命令非零退出。
- 输入错误返回退出码 2；浏览器、依赖、字段或提交控件错误返回非零状态并打印明确原因。

## 依赖

- Python 3.8+
- Playwright 仅用于真实提交：`python3 -m pip install playwright && playwright install chromium`
- `aiohttp` 仅用于显式运行 `check_directory.py`
