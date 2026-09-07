---
name: seo-link-strategy
description: Research backlink opportunities, record contact evidence, and generate personalized local outreach drafts from user-provided product and contact data. Use for backlink planning and draft preparation; never send messages or submit forms without explicit authorization for the exact target and payload.
---

# SEO Link Strategy

Build an evidence-backed backlink opportunity list and prepare local outreach drafts. Discovery, evidence capture, draft generation, and external execution are separate states.

This Skill does not ship a current directory of platforms or verified contacts. Candidates come from the user or from research performed at runtime. Never treat a guessed address, old list, search snippet, or role-based email pattern as an observed contact.

## Operating boundary

Default work is research and local draft preparation. Do not send Gmail or other messages, submit forms, purchase placements, call paid/mutating services, or change remote systems by default.

Before any external side effect:

1. show the exact target, payload, account, and expected effect;
2. obtain explicit user authorization for that specific action;
3. execute only the authorized action; and
4. record the actual result and UTC time, including failures or uncertainty.

A draft is `not-sent`. An opportunity is not a backlink. An attempted submission is not completed unless a real result supports that state.

## Evidence contract

Each opportunity or contact record must support these fields:

| Field | Requirement |
|---|---|
| `name` | User-provided or runtime-discovered platform/contact label. |
| `source_url` | Exact page where the opportunity or contact evidence was observed. |
| `observed_at` | UTC timestamp for the actual observation, or `null`. |
| `status` | `observed` only with captured evidence and time; otherwise `unknown`. |
| `email` / `emails` | Values present in captured evidence; never constructed from hints. |
| `notes` | Limits, conflicts, access failures, payment/login requirements, or next check. |

Keep sources and observation times when data is handed from research to drafting. If a page cannot be checked, preserve the candidate with `status: unknown` rather than filling likely values.

## 1. Normalize captured contact evidence

Use [scripts/contact_discoverer.py](scripts/contact_discoverer.py) after the user or an available research tool supplies candidate URLs and captured page text. The script is offline: it extracts addresses only from the supplied capture and makes no network request.

Input JSON:

```json
{
  "opportunities": [
    {
      "name": "Example Directory",
      "source_url": "https://directory.example/contact",
      "observed_at": "2030-01-15T09:45:00Z",
      "captured_text": "Contact: editor@example.com",
      "notes": "Captured from the public contact page."
    },
    {
      "name": "Unreviewed Candidate",
      "source_url": "https://candidate.example/contact"
    }
  ]
}
```

Run:

```bash
python3 scripts/contact_discoverer.py --input candidates.json
python3 scripts/contact_discoverer.py --input candidates.json --output contacts.json
```

Without `--output`, JSON goes to stdout. An existing output path is never overwritten. The first record can become `observed`; the second remains `unknown` with no invented email.

## 2. Generate local drafts

Use [scripts/email_generator.py](scripts/email_generator.py) with user-provided product, sender, and contact data. It performs no browsing and contains no sending implementation.

```json
{
  "product": {
    "name": "Example Product",
    "url": "https://product.example",
    "tagline": "User-provided product description",
    "selling_points": ["User-provided differentiator"]
  },
  "sender": {
    "name": "Your Name",
    "email": "your_email@example.com"
  },
  "contacts": [
    {
      "name": "Example Directory",
      "email": "editor@example.com",
      "source_url": "https://directory.example/contact",
      "observed_at": "2030-01-15T09:45:00Z",
      "status": "observed",
      "context": "User-provided reason this audience is relevant."
    }
  ]
}
```

Run:

```bash
python3 scripts/email_generator.py --input outreach-input.json
python3 scripts/email_generator.py --input outreach-input.json --output drafts.json
```

The output marks every draft `delivery_status: not-sent`. Invalid inputs fail before output creation, and existing output files are not replaced.

## 3. Review and optional execution

Review source freshness, recipient relevance, claims, product links, sender identity, and applicable platform rules. Remove unsupported personalization instead of presenting inference as observation.

If the user later authorizes sending or submitting, use an appropriate external tool only for the approved target and payload. Store a separate result record with fields such as `attempted_at`, `status`, `result_id`, and `error`. Do not rewrite the draft-generation output to imply delivery.
