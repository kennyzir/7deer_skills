# Security Policy

## Supported Scope

This repository is a public library of reusable skills and resources. Security review primarily focuses on:

- Accidental inclusion of secrets
- Unsafe automation defaults
- Dangerous scripts that could cause destructive behavior when copied into downstream projects
- Sensitive internal data committed by mistake

## Reporting a Problem

If you find a security issue, do not open a public issue with the full details.

Please report it privately by contacting the repository owner through GitHub:

- GitHub profile: https://github.com/kennyzir

Include:

- A short description of the issue
- Affected file paths
- Steps to reproduce, if applicable
- Whether the issue involves exposed credentials, personal data, or destructive automation

## What Should Be Reported

Please report:

- API keys, tokens, cookies, or credentials committed to the repository
- Private or customer-specific data accidentally published
- Scripts that can delete, overwrite, or exfiltrate data without clear safeguards
- Unsafe examples that encourage insecure production use
- Supply-chain risks in checked-in scripts or dependency files

## What Usually Does Not Need a Private Report

These can usually be opened as normal issues:

- Typos
- Broken examples
- Documentation gaps
- Non-sensitive dependency updates
- Feature requests

## Response Goal

The target is to acknowledge valid security reports within a reasonable time and then remove or mitigate the issue as quickly as practical.

## Secret Handling Policy

This repository should not contain:

- Real API keys
- Tokens
- Session cookies
- Private contact databases
- Personal notes or internal operating records that are not intended for public release

Use placeholders such as:

- `your_api_key_here`
- `your_token_here`
- `example.com`

## Safe Contribution Reminder

Before opening a PR, review:

- `.gitignore`
- changed example files
- exported JSON, CSV, or markdown data
- any automation scripts that interact with external services
