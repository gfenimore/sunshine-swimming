# Sunshine Swimming — Business Systems Implementation

**Client:** Amanda · Sunshine Swimming · Manatee County, FL  
**Consultant:** Garry Fenimore  
**Status:** POC / Working Model  
**Stack:** Custom HTML Form → Zapier → HoneyBook Essentials ($49/mo)

---

## What This Project Does

Automates lead qualification, client onboarding, and communication for a solo mobile swim coach who teaches 7–9 private lessons per day at clients' homes (seasonal April–October).

**Before:** Google Form → Google Sheet → manual email → manual scheduling → manual reminders  
**After:** Smart form (auto-qualifies) → Zapier → HoneyBook (auto-emails, auto-reminders, CRM)

---

## Project Structure

```
sunshine-swimming/
├── README.md                          ← You are here
├── docs/
│   ├── architecture.md                ← System architecture & decisions
│   ├── work-plan.html                 ← Implementation work plan (interactive)
│   ├── client-proposal.html           ← Client-facing systems plan
│   └── build-plan.html                ← Internal HoneyBook build plan
├── src/
│   ├── form/
│   │   └── index.html                 ← Production intake form (single file)
│   ├── email-templates/
│   │   ├── 01-welcome.html            ← Welcome & Policies
│   │   ├── 02-water-safety.html       ← Water Safety Do's & Don'ts
│   │   ├── 03-ready-to-book.html      ← Ready to Book? nudge
│   │   └── 04-decline-referral.html   ← Polite decline with referrals
│   ├── scripts/
│   │   └── scrub-client-data.py       ← xlsx → HoneyBook-ready CSV
│   └── zapier/
│       └── webhook-test.html          ← Zapier webhook test harness
├── data/
│   ├── raw/                           ← Amanda's original data (gitignored)
│   └── processed/                     ← Cleaned CSVs for import
├── tests/
│   └── test-scenarios.md              ← LOTR-themed test cases
└── .vscode/
    └── settings.json                  ← VS Code workspace config
```

---

## Quick Start

1. Open this folder in VS Code
2. Open `src/form/index.html` — Live Preview to see the intake form
3. Run `python3 src/scripts/scrub-client-data.py` to generate the HB import CSV
4. Open `src/zapier/webhook-test.html` in a browser to test the Zapier webhook

---

## Key Decisions

| Decision | Choice | Why |
|---|---|---|
| CRM Platform | HoneyBook Essentials | Best solo-operator fit, $49/mo, excellent mobile app |
| Form approach | Custom HTML (not HB native) | HB forms can't branch automations on field values |
| Form → CRM bridge | Zapier (single webhook) | HB has no public API; Zapier is the only bridge |
| SMS strategy | HB reminders + Amanda's personal phone | HB SMS is one-way/automated only; her personal texting IS the brand |
| Hosting | WordPress (sunshineswimming.com/inquiry) | Same domain, existing hosting |

---

## Open Items

- [ ] Amanda's referral swim school names (for decline messages)
- [ ] Session price confirmation ($50 on website vs $60 in build plan)
- [ ] $75 deposit policy — integrate with HB invoicing?
- [ ] Annual vs. monthly billing decision
- [ ] Amanda's logo file for form header
- [ ] Constant Contact migration or keep separate?

---

## Test Data

All test records use LOTR character names with real Manatee County addresses.  
See `tests/test-scenarios.md` for the full test matrix.
