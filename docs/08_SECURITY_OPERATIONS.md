# ECHO — Security, Anti-Cheat & Operations

## 1. Trust boundary

Untrusted:
- client coordinates;
- claimed damage;
- claimed loot;
- claimed inventory;
- claimed currency;
- client timestamps.

Trusted:
- server simulation;
- database transactions;
- signed configuration;
- server time.

## 2. Anti-cheat model

### Server validation
Validate:
- movement speed;
- attack cooldown;
- skill resource;
- target distance;
- loot ownership;
- node availability;
- quest state.

### Anomaly detection
Track:
- impossible movement;
- impossible action rate;
- repeated rare-drop patterns;
- abnormal marketplace transfers;
- unusual account graph behavior.

Do not auto-ban solely from one weak signal. Route high-risk cases to a review workflow or escalating controls.

## 3. Idempotency / replay protection

Every state-changing API has:
- request ID;
- actor ID;
- idempotency key when required;
- server timestamp;
- audit reason.

## 4. Payments

Payment flow:

```text
Mobile Store / Payment Provider
→ receipt/token
→ backend verification
→ entitlement transaction
→ ledger/audit
→ client refresh
```

Never trust a client-side “payment success” flag.

## 5. Observability

### Metrics
- API RPS
- p50/p95/p99 latency
- WebSocket active connections
- game tick lag
- reconnect rate
- DB connection usage
- Redis latency
- event-bus consumer lag
- economy source/sink rates

### Logs
Structured JSON with:
- timestamp;
- requestId;
- accountId/characterId where permitted;
- worldId;
- endpoint/command;
- result code.

## 6. Admin roles

| Role | Scope |
|---|---|
| Support | read player state, support actions |
| GM | world event controls |
| Economy Analyst | economy reports, no direct item edits |
| Developer | technical diagnostics |
| Super Admin | audited high-risk operations |

## 7. Operational controls

For economy/world changes:
- dry-run mode;
- preview impact;
- explicit confirmation;
- audit log;
- rollback/expiry where possible.

## 8. Disaster recovery

### Recovery priorities
1. Preserve currency/item integrity.
2. Restore authentication.
3. Restore world/session availability.
4. Rebuild analytics asynchronously.

### Backups
- managed DB backups;
- point-in-time recovery where available;
- periodic restore drills.
