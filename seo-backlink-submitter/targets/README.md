# Targets Directory

This directory stores submission targets and content for your projects.

## Structure

Each project gets its own set of target files:

```
targets/
├── your-domain-com.json           # Site information
├── your-domain-directories.txt    # Directory list
└── your-domain-pr-content.md      # PR/submission content
```

## File Formats

### Site Information (JSON)
```json
{
  "name": "Your Site Name",
  "url": "https://yoursite.com",
  "description": "Brief description",
  "email": "contact@yoursite.com",
  "category": "Category",
  "tags": ["tag1", "tag2"]
}
```

### Directory List (TXT)
```
https://directory1.com
https://directory2.com
https://directory3.com
```

### PR Content (MD)
Markdown file with your submission content, press release, or description.

## Usage

Create your target files, then run:

```bash
python scripts/batch_submit.py --target targets/yoursite-com.json
```

## .gitignore

Add your project-specific files to `.gitignore`:

```
targets/*.json
targets/*.txt
targets/*.md
!targets/README.md
```
