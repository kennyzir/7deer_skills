# Multi-Game Codes Hub - Usage Guide

Quick reference for generating code pages for any Roblox game.

## Quick Start (5 Minutes)

### Step 1: Prepare Your Data

Create a JSON file with your game's codes:

```json
{
  "gameName": "Your Game Name",
  "gameSlug": "your-game-slug",
  "activeCodes": [
    {
      "code": "CODE123",
      "reward": "50 Spins",
      "expiryDate": "2026-04-30",
      "conditions": "None"
    }
  ],
  "expiredCodes": [
    {
      "code": "OLDCODE",
      "reward": "25 Spins"
    }
  ]
}
```

### Step 2: Generate the Page

```bash
python resources/generate_code_page.py \
  --input yba_codes.json \
  --output ./src/app/yba/page.tsx
```

### Step 3: Done!

Your page is ready at `/yba` with:
- ✅ Active codes with copy buttons
- ✅ Redemption guide
- ✅ FAQ with Schema markup
- ✅ Expired codes reference
- ✅ SEO optimized metadata

## Common Scenarios

### Scenario 1: Batch Create Multiple Games

```bash
# Create codes for multiple games at once
for game in yba kaizen blue-lock volleyball; do
  python resources/generate_code_page.py \
    --input "${game}_codes.json" \
    --output "./src/app/${game}/page.tsx"
done
```

### Scenario 2: Update Existing Page

```bash
# Just regenerate with updated JSON
python resources/generate_code_page.py \
  --input yba_codes.json \
  --output ./src/app/yba/page.tsx
```

### Scenario 3: Add New Code to Existing Page

Edit your JSON file and add the new code:

```json
{
  "activeCodes": [
    {
      "code": "NEWCODE2026",
      "reward": "100 Spins",
      "expiryDate": "2026-05-01",
      "conditions": "NEW - Apr 4, 2026"
    }
  ]
}
```

Then regenerate:

```bash
python resources/generate_code_page.py \
  --input yba_codes.json \
  --output ./src/app/yba/page.tsx
```

## Template Customization

The template uses these placeholders:

- `{{gameName}}` - Full game name
- `{{gameSlug}}` - URL slug
- `{{rewards}}` - Auto-extracted reward types
- `{{activeCodesData}}` - JSON array of active codes
- `{{expiredCodesData}}` - JSON array of expired codes
- `{{lastUpdated}}` - Current date
- `{{currentMonth}}` - Current month name
- `{{currentYear}}` - Current year

## File Structure

```
multi-game-codes-hub/
├── SKILL.md                          # Full documentation
├── USAGE.md                          # This file
├── resources/
│   ├── generate_code_page.py        # Main generator script
│   ├── templates/
│   │   └── codes_page.tsx           # Page template
│   ├── components/
│   │   ├── CopyButton.tsx           # Copy button component
│   │   └── CodeTable.tsx            # Code table component
│   ├── schemas/
│   │   └── faq_schema.ts            # Schema generators
│   └── examples/
│       ├── yba_codes.json           # Example: YBA
│       └── kaizen_codes.json        # Example: Kaizen
```

## Tips & Best Practices

1. **Update Frequency**: Update codes daily or when new updates drop
2. **Expiry Tracking**: Always include `expiryDate` for time-sensitive codes
3. **Conditions**: Use `conditions` field for level requirements or group membership
4. **SEO**: The generator automatically creates SEO-optimized metadata
5. **Schema**: FAQ Schema is auto-generated for Google rich results

## Troubleshooting

### Issue: Template not found

```bash
# Specify full path to template
python resources/generate_code_page.py \
  --input yba_codes.json \
  --output ./src/app/yba/page.tsx \
  --template .agent/skills/multi-game-codes-hub/resources/templates/codes_page.tsx
```

### Issue: Invalid JSON

Validate your JSON file:

```bash
python -m json.tool yba_codes.json
```

### Issue: Missing rewards in meta description

The generator auto-detects rewards from the `reward` field. Ensure your rewards contain keywords like:
- "Spin", "Spins"
- "Cash", "Yen", "Money"
- "Arrow", "Arrows"
- "Gem", "Gems"

## Next Steps

After generating your page:

1. ✅ Test the page locally: `npm run dev`
2. ✅ Check for linting errors: `npm run lint`
3. ✅ Verify Schema markup: [Google Rich Results Test](https://search.google.com/test/rich-results)
4. ✅ Add internal links to related pages
5. ✅ Deploy and monitor traffic

## Examples

See `resources/examples/` for complete working examples:
- `yba_codes.json` - Your Bizarre Adventure
- `kaizen_codes.json` - Kaizen

## Support

For issues or questions, refer to the main SKILL.md documentation.
