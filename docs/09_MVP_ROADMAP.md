# ECHO — MVP Roadmap & Delivery Plan

## 1. Team shape

Lean team example:

- 1 PO/BA
- 1 PM/Producer
- 2 Backend engineers
- 2 Unity engineers
- 1 3D artist
- 1 UI/UX designer
- 1 QA
- part-time DevOps

A smaller team can combine PM/BA and use a single backend engineer initially, but scope must shrink accordingly.

## 2. Milestones

### M0 — Foundation
Deliver:
- project repositories;
- CI/CD;
- auth;
- logging/tracing;
- database migrations;
- Unity bootstrap;
- basic network layer.

Exit criteria:
- client can authenticate;
- API health and telemetry available;
- build deploys automatically to test environment.

### M1 — Core gameplay
Deliver:
- character;
- movement;
- combat;
- loot;
- inventory;
- 1 zone;
- tutorial.

Exit criteria:
- end-to-end 10-minute playable loop.

### M2 — Progression / economy
Deliver:
- crafting;
- upgrade;
- gold;
- marketplace;
- ledger;
- daily quest.

Exit criteria:
- buy/sell economy works transactionally;
- basic economy dashboard exists.

### M3 — Memory
Deliver:
- personal timeline;
- discovery system;
- world memory feed;
- event pipeline.

Exit criteria:
- significant actions become visible memories.

### M4 — Echo Engine
Deliver:
- rule engine;
- 5 world reactions;
- admin control;
- world change lifecycle.

Exit criteria:
- controlled test can trigger an event from aggregated behavior.

### M5 — Mobile polish
Deliver:
- performance pass;
- asset streaming;
- UI polish;
- crash analytics;
- reconnect/resync.

Exit criteria:
- target device matrix passes defined performance and stability gates.

### M6 — Closed beta
Deliver:
- guild basics;
- season framework;
- store;
- support tooling;
- anti-abuse controls.

Exit criteria:
- no open critical exploit in economy or progression;
- crash and latency thresholds within defined budget.

## 3. Priority backlog

### P0
- Authentication
- Character
- Movement
- Combat
- Inventory
- Loot
- Server authority
- PostgreSQL ledger
- Memory event

### P1
- Marketplace
- Crafting
- Echo Engine
- World events
- Guild
- Analytics

### P2
- Season pass
- Cosmetic store
- Advanced social features
- Housing
- more dynamic event chains

## 4. Sprint deliverable template

Each story must include:

```text
Goal
Actors
Preconditions
Main flow
Alternative flows
Validation rules
Data impact
API impact
Client impact
Telemetry
Acceptance criteria
Test cases
Rollback/admin impact
```

## 5. Release gates

### Functional gate
- P0 acceptance criteria pass.

### Economy gate
- no known duplicate-currency or duplicate-item path;
- ledger reconciliation passes.

### Performance gate
- target device frame-rate budget met;
- memory and load-time budget met.

### Network gate
- reconnect and resync verified;
- packet loss scenarios tested.

### Security gate
- common client tampering attempts rejected;
- payment entitlement verified server-side.

## 6. First playable vertical slice

The smallest version that proves the concept:

```text
Login
→ Hub
→ Zone
→ Fight 3 enemies
→ Discover hidden object
→ Receive Memory
→ Return Hub
→ View Memory
→ Trigger one Echo event from shared test activity
→ Re-enter zone and see world change
```

This vertical slice proves the unique product thesis before the team invests heavily in marketplace, guilds and long-form content.
