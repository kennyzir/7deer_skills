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

Create your target files from the skill directory. Every submitter defaults to an offline dry run.

Plan one directory submission:

```bash
python scripts/submit_to_directory.py \
  --directory https://directory.example/submit \
  --target targets/your-domain-com.json
```

Plan all URLs in a directory list:

```bash
python scripts/batch_submit.py \
  --target targets/your-domain-com.json \
  --directories targets/your-domain-directories.txt
```

Review the plan before adding `--submit` to either command. That flag permits real browser navigation, form filling, and submit-button clicks. A `submit_triggered` result means only that the button was clicked; it does not mean the directory accepted or published the listing.

`scripts/quick_submit.py` is a compatibility alias for the single-directory command and accepts the same arguments. It has no built-in targets and is also dry-run by default.

## .gitignore

Add your project-specific files to `.gitignore`:

```
targets/*.json
targets/*.txt
targets/*.md
!targets/README.md
```
