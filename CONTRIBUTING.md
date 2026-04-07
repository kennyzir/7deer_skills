# Contributing to 7Deer Skills

Thanks for contributing.

This repository is a library of reusable skills, prompts, scripts, templates, and supporting resources for AI agent workflows. Contributions should keep the repository modular, safe to publish, and easy to reuse.

## What to Contribute

Good contributions include:

- New self-contained skills
- Improvements to existing `SKILL.md` documentation
- Better examples, templates, and scripts
- Fixes for portability, safety, or clarity
- Cleanup of public-facing docs and repository structure

## Repository Rules

Please follow these rules before opening a pull request:

- Keep each skill in its own top-level directory.
- Every skill must include a `SKILL.md`.
- Put supporting code and reference material inside that skill's `resources/`, `references/`, `scripts/`, or similarly scoped subdirectories.
- Do not mix private workspace data with reusable public skills.
- Do not commit secrets, API keys, tokens, cookies, or local environment files.
- Do not commit generated private reports, personal notes, outreach targets, or customer/project-specific data unless they are explicitly sanitized and intended to be public.

## New Skill Checklist

When adding a new skill, include:

- A clear directory name
- `SKILL.md` with purpose, inputs, outputs, and usage steps
- Any required scripts, templates, or references
- Dependency notes if the skill needs Python, Node.js, or external tools
- Sanitized examples only

Recommended `SKILL.md` structure:

1. Name
2. Purpose
3. Included resources
4. Requirements
5. Usage instructions
6. Example workflow
7. Notes or limitations

## Pull Request Guidelines

- Keep pull requests focused.
- Prefer one skill or one logical change per PR.
- Explain why the change is useful.
- Mention any breaking changes to existing paths or expected usage.
- Update `README.md` if you add or remove a top-level skill.

## Security and Privacy

Before submitting:

- Remove all secrets and credentials
- Replace real IDs and tokens with placeholders such as `your_api_key_here`
- Sanitize any domain-specific memory, exports, CSV files, or outreach data
- Review `.gitignore` rules if your change introduces new generated or sensitive file types

If your change affects repository safety or disclosure risk, also review [SECURITY.md](./SECURITY.md).

## Review Expectations

Maintainers may request changes for:

- Public safety concerns
- Missing documentation
- Overly project-specific content
- Unclear ownership or purpose
- Low reusability

## License

By contributing, you agree that your contributions will be licensed under the MIT License in this repository.
