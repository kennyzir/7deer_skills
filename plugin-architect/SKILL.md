---
name: plugin-architect
description: 构建 AI Skills/Plugins 的标准方法论 (Based on Anthropic Standard)
version: 1.0
---

# 🏗️ Plugin Architect Protocol

本 Skill 定义了本项目构建 **AI Plugins** 的唯一标准。所有 Skill 的创建与修改必须遵循此方法论。

## When This Skill Applies
*   当用户要求"创建一个新 Skill"时。
*   当需要重构现有 Skills 以符合标准时。
*   当需要为 Skill 添加外部工具 (MCP) 或快捷指令 (Slash Commands) 时。

## Instructions

一个完整的 **Plugin (Skill System)** 由四个核心组件构成。

### 1. The Identity (`plugin.json`)
插件的身份证。定义插件在系统中的唯一标识。
*   **Location**: `.agent/.claude-plugin/plugin.json` (Global) 或 `skill-name/plugin.json` (Local)
*   **Schema**:
    ```json
    {
      "schema_version": "1.0",
      "name": "devil-hunter-nexus-plugin",
      "description": "The cognitive engine and SEO factory for Roblox game sites.",
      "version": "1.0.0",
      "authors": ["Devil Hunter Team"]
    }
    ```

### 2. The Logic (`SKILL.md`)
AI 的思维链。必须包含明确的触发条件 (Trigger) 和结构化指令。

*   **Location**: `.agent/skills/<skill-name>/SKILL.md`
*   **Frontmatter**: Must include `name` and `description`.
*   **Mandatory Sections**:
    1.  `## When This Skill Applies`: 明确的触发条件 (Contextual Triggers)。
        *   *Good*: "When the user asks to analyze SEO metadata."
        *   *Bad*: "Use this for SEO."
    2.  `## Instructions`: 具体的操作步骤、原则或代码规范。
    3.  `## Actions` (Optional): 可用的工具或脚本引用。

### 3. The Interface (`commands/`)
用户的快捷入口。定义以 `/` 开头的显式调用指令。

*   **Location**: `.agent/commands/<command-name>.md`
*   **Format**:
    ```markdown
    ---
    description: Audit the current page for SEO compliance
    argument-hint: [url or path]
    active-skills: [nextjs-seo-foundations]
    ---
    
    # /audit-seo
    
    1. Check presence of Metadata (Title, Description).
    2. Validate JSON-LD Schema.
    3. Report missing 'canonical' tags.
    ```

### 4. The Tooling (`.mcp.json`)
外部能力的延伸。通过 Model Context Protocol 连接真实世界。

*   **Location**: `.agent/.mcp.json`
*   **Usage**: 如果 Skill 需要执行复杂脚本 (e.g., Python Script, Database Query)，需在此注册 MCP Server。

---

## Workflow: How to Build a New Skill

1.  **Define Intent**: 是"思维模式" (Thinking) 还是"具体操作" (Action)?
    *   *Thinking* -> 重点编写 `SKILL.md` 的 Instructions。
    *   *Action* -> 重点编写 `commands/` 和 `scripts/`。

2.  **Create Directory**: `mkdir .agent/skills/<skill-name>`

3.  **Draft SKILL.md**:
    *   Copy metadata template.
    *   Write strict "When This Skill Applies" triggers.
    *   Write verifiable Instructions.

4.  **Register Command (Optional)**:
    *   If user needs frequent access, create `.agent/commands/<skill-shortcut>.md`.

5.  **Validation**:
    *   Ask AI: "Does this skill structure match the `plugin-architect` standard?"
