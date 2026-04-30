# Test Scenarios — LOTR Edition

All test records use Lord of the Rings character names with real Manatee County addresses.

## Routing Test Matrix

| # | Swimmer | Parent | Area | Pool Heated | Type | Expected Route |
|---|---------|--------|------|-------------|------|----------------|
| 1 | Frodo Baggins | Bilbo Baggins | Bradenton | Yes | Paid | ✅ Qualified |
| 2 | Samwise Gamgee | Hamfast Gamgee | Lakewood Ranch | Yes | Paid | ✅ Qualified |
| 3 | Pippin Took | Paladin Took | Parrish / Ellenton | Neighborhood pool | Paid | ✅ Qualified |
| 4 | Merry Brandybuck | Saradoc Brandybuck | Palmetto | Yes | Paid | ✅ Qualified |
| 5 | Arwen Undómiel | Elrond | Outside Manatee County | Yes | Paid | ❌ Decline (area) |
| 6 | Éowyn | Théoden | Bradenton | No | Paid | ❌ Decline (pool) |
| 7 | Legolas Greenleaf | Thranduil | Bradenton | Yes | Paid | ✅ Qualified (Under 6mo) |
| 8 | Gandalf Grey | N/A (adult) | Bradenton | Yes | Paid | ✅ Qualified (adult) |
| 9 | Galadriel | Celeborn | Lakewood Ranch | Yes | Nonprofit | 💜 Nonprofit flow |

## Test Addresses (Real Manatee County)

| Character | Address | Zip |
|-----------|---------|-----|
| Frodo | 5750 12th Street S, Bradenton | 34208 |
| Sam | 16539 Arbor Ridge Trail, Lakewood Ranch | 34211 |
| Pippin | 10632 High Noon Trail, Parrish | 34219 |
| Merry | 1011 14th St W, Palmetto | 34221 |
| Arwen | 5356 35th Terrace N, St Petersburg | 33710 |
| Éowyn | 3605 Riverview Blvd, Bradenton | 34205 |
| Legolas | 3934 75th St W, Bradenton | 34209 |
| Gandalf | 2543 River Preserve Ct, Bradenton | 34208 |
| Galadriel | 14231 Cattle Egret Pl, Lakewood Ranch | 34202 |

## End-to-End Test Procedure

### 1. Form Routing Tests (browser only)
- [ ] Open `src/form/index.html` in browser
- [ ] Test #5 (Arwen): Select "Outside Manatee County" → verify decline message appears
- [ ] Test #6 (Éowyn): Select "Bradenton" + "No" for pool → verify pool decline message
- [ ] Test #9 (Galadriel): Select "Lakewood Ranch" + "Nonprofit" → verify skips to contact step
- [ ] Test #1 (Frodo): Full qualified flow → verify all 4 steps work → verify thank-you screen

### 2. Webhook Tests (requires Zapier)
- [ ] Open `src/zapier/webhook-test.html`
- [ ] Configure Zapier webhook URL
- [ ] Fire Frodo payload → verify arrives in Zapier
- [ ] Fire Galadriel payload → verify arrives with "nonprofit" tag
- [ ] Verify Zapier creates client in HoneyBook

### 3. Automation Tests (requires HoneyBook)
- [ ] Verify new client creation triggers welcome email
- [ ] Wait 1 day → verify water safety email sends
- [ ] Wait 1 more day → verify "ready to book" email sends
- [ ] Check email deliverability across Gmail, Yahoo, Outlook

### 4. Scheduler Tests
- [ ] Create test session for Frodo
- [ ] Verify SMS reminder sends 24hr before
- [ ] Verify SMS reminder sends 1hr before
- [ ] Verify email reminder sends 24hr before
