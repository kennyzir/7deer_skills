# 快速示例：生成游戏代码页面

以下命令均从仓库根目录执行，不需要切换工作目录。默认模板由生成器相对 Skill 根定位。

## 生成

```bash
python3 multi-game-codes-hub/resources/generate_code_page.py \
  --input examples/quick-game-codes/sample_codes.json \
  --output /tmp/7deer-quick-game-codes.tsx
```

示例输入的 `baseUrl` 是 `https://example.com`。用于真实站点时必须替换成目标站点 URL。

## 自动断言结果

```bash
python3 - <<'PY'
from pathlib import Path

content = Path("/tmp/7deer-quick-game-codes.tsx").read_text(encoding="utf-8")
assert 'const baseUrl = "https://example.com";' in content
assert "canonical: `${baseUrl}/${gameSlug}`" in content
assert "GULLIBLE" in content
assert "{{" not in content and "}}" not in content
assert "jujutsucalc.com" not in content
print("quick-game-codes example passed")
PY
```

输出包含 active/expired 代码区、复制按钮、兑换指南、FAQ/Breadcrumb Schema 和使用当前 UTC 日期的 metadata。生成器只渲染输入数据，不验证兑换码是否真实有效。
