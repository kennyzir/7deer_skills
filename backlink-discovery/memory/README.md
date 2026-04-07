# Memory Directory

This directory stores discovered backlink opportunities for your projects.

## Structure

Each project gets its own subdirectory:

```
memory/
├── your-project-name/
│   ├── platforms.json    # Discovered platforms and opportunities
│   └── summary.md        # Summary report
└── another-project/
    ├── platforms.json
    └── summary.md
```

## Usage

When you run the backlink discovery engine, it will automatically create a subdirectory for your project and store the results here.

Example:
```bash
python scripts/discovery_engine.py --domain example.com
```

This will create `memory/example_com/` with the discovered opportunities.

## .gitignore

Add your project-specific directories to `.gitignore` to keep them private:

```
memory/*/
!memory/README.md
```
