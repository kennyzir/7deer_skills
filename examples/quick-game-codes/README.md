# 快速示例：生成游戏代码页面

这个示例展示如何用 `multi-game-codes-hub` 技能在 5 分钟内生成一个完整的游戏代码页面。

## 运行方式

```bash
# 1. 查看示例数据
cat sample_codes.json

# 2. 生成页面
python ../../multi-game-codes-hub/resources/generate_code_page.py \
  --input sample_codes.json \
  --output ./output/page.tsx

# 3. 查看生成结果
cat ./output/page.tsx
```

## 输出包含

- Active / Expired 代码分区
- 一键复制按钮组件
- FAQ Schema 结构化数据
- SEO 优化的 Metadata
- 响应式布局
