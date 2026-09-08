# Roblox Homepage Ranking Auditor

A Codex-compatible Agent Skill for auditing Roblox and game-site homepages against the RB Auto Golden Homepage model.

## What it does

- reconstructs the homepage primary player job and main engine;
- separates homepage structural potential from factual, runtime, and technical execution;
- scores eight structural dimensions out of 100;
- maps query-family ownership between `/` and child routes;
- detects empty keyword modules, generic content, fake tier lists, duplicate full tools, and internal-link gaps;
- writes evidence-backed audit artifacts and minimal repair work orders.

## Install

Copy the folder into the skill directory your Codex workspace scans. Current Codex repositories commonly use:

```text
.agents/skills/roblox-homepage-ranking-auditor/
```

For a repository that already uses a different compatible skill root, keep the folder intact and place it under that root.

## Invoke

```text
Use $roblox-homepage-ranking-auditor to audit the current homepage. Do not modify code. Inspect the repository, build/exported HTML, runtime tool behavior, and P0 child routes. Write artifacts under artifacts/homepage-audit/.
```

## Quick scanner

```bash
pip install -r .agents/skills/roblox-homepage-ranking-auditor/requirements.txt
python .agents/skills/roblox-homepage-ranking-auditor/scripts/audit_homepage.py \
  --url "https://example.com/" \
  --game-name "Example Game" \
  --output "artifacts/homepage-audit/homepage_machine_evidence.json"
```

The scanner gathers deterministic HTML evidence. Codex must still perform the semantic audit defined in `SKILL.md`.
