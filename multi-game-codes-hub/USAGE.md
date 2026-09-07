# Multi-Game Codes Hub Usage

## Input

Create a JSON file containing the target site's base URL and code data:

```json
{
  "gameName": "Your Game Name",
  "gameSlug": "your-game-slug",
  "baseUrl": "https://example.com",
  "activeCodes": [
    {
      "code": "CODE123",
      "reward": "50 Spins",
      "expiryDate": "2026-04-30",
      "conditions": "Optional"
    }
  ],
  "expiredCodes": [
    {
      "code": "OLDCODE",
      "reward": "25 Spins"
    }
  ],
  "redemptionSteps": [
    "Open the game's menu.",
    "Enter a supplied code in the code field."
  ],
  "faq": [
    {
      "question": "Where is the code field?",
      "answer": "The supplied source says it is in the game menu."
    }
  ]
}
```

`gameName`, `gameSlug`, and `baseUrl` are required. Code arrays default to empty; entries support only `code`, `reward`, `expiryDate`, and `conditions`, with `code` and `reward` required. Optional `redemptionSteps` is a string array, and optional `faq` entries contain only `question` and `answer`. Unknown fields fail validation instead of being ignored.

## Generate

From this Skill directory:

```bash
python3 resources/generate_code_page.py \
  --input resources/examples/yba_codes.json \
  --output /tmp/yba-codes-page.tsx
```

The bundled template is found relative to the generator script, independent of the current working directory. Explicit `--input`, `--output`, and `--template` paths resolve normally from the caller's current directory unless absolute.

Example with a caller-relative custom template:

```bash
python3 /path/to/multi-game-codes-hub/resources/generate_code_page.py \
  --input ./game.json \
  --output ./page.tsx \
  --template ./custom-template.tsx
```

## Generated values

The generator replaces:

- game name and slug;
- canonical/breadcrumb base URL;
- active and expired code arrays;
- optional supplied redemption steps and FAQ entries;
- detected reward summary;
- current UTC month, year, and date.

Generation fails instead of writing a partial page when input validation fails or an unknown `{{...}}` template variable remains.

## Integration

The default page imports `@/components/CopyButton`. Copy [resources/components/CopyButton.tsx](resources/components/CopyButton.tsx) to the matching project alias or adjust the import. The optional [resources/components/CodeTable.tsx](resources/components/CodeTable.tsx) and [resources/schemas/faq_schema.ts](resources/schemas/faq_schema.ts) can be adapted separately.

Run the target application's typecheck, lint, and build after integrating the generated file. The generator renders supplied data but does not verify whether codes work.

## Not implemented

The repository does not include code discovery/monitoring, automatic validity checks, update commands, multilingual generation, or deployment automation. Those are roadmap capabilities, not current commands.
