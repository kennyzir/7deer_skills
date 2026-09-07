# Legacy Roblox Site Architect Materials

Files in this directory are historical case studies and execution notes retained for retrospective value. They are not current instructions, are not loaded by default, and may contain stale metrics, unsupported claims, obsolete architecture, or project-specific assumptions.

Use a legacy file only when a user explicitly requests that case or when a named retrospective is needed for a current decision. Revalidate every external fact, path, command, and capability before reuse. Current work follows `roblox-site-architect/SKILL.md` and its active pipeline contract instead.

## Retired v3 bundle

The v3 bundle was retired in v4 because it was not a complete starter: its configuration and data access schemas conflicted, required Next.js project files were missing, analytics/domain values were placeholders, and its installation/deployment scripts had unsafe defaults that could install packages, create commits, and push without a stage-level authorization gate. The bundle was deleted rather than moved here so it cannot be mistaken for a current starter.

The deleted files remain recoverable from Git history for forensic comparison. Do not copy or execute that historical bundle as a current starter; rebuild any needed capability against the v4 pipeline contract and validate it independently.
