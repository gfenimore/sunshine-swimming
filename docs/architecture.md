# Architecture & Decision Log

## System Architecture

```
┌─────────────────────────────────────────────────────┐
│  BROWSER (client-side)                              │
│                                                     │
│  Custom Intake Form (index.html)                    │
│  ├── Step 1: Routing (location, pool, lesson type)  │
│  ├── Step 2: Swimmer details                        │
│  ├── Step 3: Parent/contact info                    │
│  └── Step 4: Logistics                              │
│                                                     │
│  Routing Logic (JavaScript):                        │
│  ├── Outside Manatee County → DECLINE (inline msg)  │
│  ├── Pool not heated → DECLINE (inline msg)         │
│  ├── Nonprofit → SUBMIT with tag "nonprofit"        │
│  └── Qualified → SUBMIT with tag "qualified"        │
│                                                     │
│  Unqualified leads NEVER leave the browser.         │
└──────────────┬──────────────────────────────────────┘
               │ POST (JSON) — qualified/nonprofit only
               ▼
┌──────────────────────────┐
│  ZAPIER                  │
│  Webhook (Catch Hook)    │
│  ├── Filter: qualified   │──→ Create Client in HB (notes = all form data)
│  └── Filter: nonprofit   │──→ Create Client in HB (notes = "NONPROFIT")
└──────────────┬───────────┘
               │
               ▼
┌──────────────────────────────────────────────────────┐
│  HONEYBOOK (Essentials, $49/mo annual)               │
│                                                      │
│  Trigger: New client created                         │
│  ├── Auto-create project (30-min lesson type)        │
│  ├── Send Welcome Email (immediate)                  │
│  ├── Wait 1 day → Send Water Safety Email            │
│  ├── Wait 1 day → Send Ready to Book Email           │
│  └── Move pipeline → "Qualified"                     │
│                                                      │
│  Scheduler:                                          │
│  ├── 30-min + 60-min session types                   │
│  ├── M–F 9am–6pm, 30-min buffer                     │
│  └── SMS reminders: 24hr + 1hr before               │
└──────────────────────────────────────────────────────┘
```

## Decision Log

### 2026-03 — Platform Selection
**Decision:** HoneyBook Essentials over Go High Level, Dubsado, Jobber, Constant Contact, and duct-tape stacks.  
**Rationale:** Best ratio of capability to complexity for a non-technical solopreneur. $49/mo vs $97+ for GHL. Excellent mobile app (she manages from poolside). Native SMS reminders included.  
**Risk:** Feb 2025 price hike (89% on Starter) signals more increases possible. Data export is limited (no bulk file export).

### 2026-04 — Form Architecture (Path A)
**Decision:** Custom HTML form + Zapier webhook instead of HoneyBook native forms.  
**Rationale:** HB forms cannot branch automations based on field values. One automation per form fires on ALL submissions. No conditional routing. No public API.  
**Trade-off:** Adds Zapier dependency ($0–20/mo) but gains full routing control client-side.

### 2026-04 — SMS Strategy
**Decision:** HB automated reminders + Amanda's personal phone for conversational texting.  
**Rationale:** HB SMS is one-way only (clients can't reply). Amanda's personal texting (rain cancellations, schedule changes, check-ins) IS her competitive advantage. Don't automate it away.  
**Future option:** Google Voice (free) for a separate business number if she wants to separate personal/business.

### 2026-04 — Zapier Limitation Discovery
**Finding:** HB's Zapier integration has NO "Create Project" action — only "Create Client."  
**Workaround:** Trigger HB's native automation on "new client created" to auto-generate project + fire welcome sequence. Actually better — decouples automation from any specific form source.
