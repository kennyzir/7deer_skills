# Setup Checklist — SEO Autopilot

快速检查清单，确保所有组件就位。

## 信息收集

| 项目 | 值 |
|------|---|
| 框架 | |
| 报告目录 | |
| 页面目录 | |
| 博客系统 | |
| 导航注册文件 | |
| Sitemap 文件 | |
| SEO 工具文件 | |
| 主 CTA 页面 | |
| 示例落地页 | |
| 示例博客文章 | |
| 部署平台 | |

## 文件清单

- [ ] `.vscode/settings.json` — git autofetch + pullOnFetch
- [ ] `.kiro/hooks/seo-autopilot.kiro.hook` — fileCreated hook
- [ ] `.kiro/steering/seo-autopilot.md` — 处理指令（已替换 placeholder）
- [ ] `{report_dir}/processed.json` — 状态追踪（初始化为空）

## 验证步骤

- [ ] 推送一份测试报告到报告目录
- [ ] 确认 IDE 在 2 分钟内自动 pull
- [ ] 确认 hook 触发并开始处理
- [ ] 确认页面正确生成
- [ ] 确认 git push 成功
- [ ] 确认部署平台自动构建

## 常见问题排查

| 问题 | 检查点 |
|------|--------|
| Hook 不触发 | filePatterns 是否匹配文件名模式？ |
| 自动 pull 不工作 | 重启 IDE，检查 settings.json |
| 页面风格不对 | steering 文件中的示例页面引用是否正确？ |
| 重复生成 | processed.json 是否在每次运行后更新？ |
| git push 失败 | 检查 git 凭证配置 |
| Build 失败 | 确保所有引用的组件/数据在远端存在 |
