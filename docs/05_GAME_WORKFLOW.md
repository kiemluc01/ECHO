# ECHO — Game Workflow by Stage

## Stage 0 — Login / bootstrap

```text
Open app
→ authenticate
→ load profile
→ choose character
→ download only required content
→ connect realtime
→ receive world snapshot
```

**Failure:** network unavailable → cached shell + retry; no authoritative state mutation locally.

## Stage 1 — Tutorial

Goal: teach the 4 essential actions.

1. Move
2. Attack
3. Loot
4. Equip

Tutorial also demonstrates the first Memory Event.

### Example
Player enters a hidden cave.

Server creates:
`DISCOVERY:CAVE_001`

UI:
> “The world will remember this discovery.”

## Stage 2 — Daily loop

```text
Login
 ↓
Daily missions
 ↓
Choose activity
 ├─ Explore
 ├─ Gather
 ├─ Dungeon
 ├─ Craft
 └─ Trade
 ↓
Reward
 ↓
Upgrade
 ↓
Check Memory / Echo feed
```

## Stage 3 — Exploration workflow

```text
Enter zone
→ inspect interactables
→ move to POI
→ solve small mechanic / combat gate
→ collect item
→ server validates
→ Memory Event created
→ discovery flag stored
```

## Stage 4 — Combat workflow

### Pre-combat
- server assigns entity IDs;
- client receives snapshot;
- skill cooldown state synchronized.

### During combat
- client sends intent;
- server validates range/cooldown/resource;
- server calculates damage/status/loot eligibility;
- state delta returned.

### Post-combat
- loot transaction committed;
- combat event published;
- significant outcomes may create Memory Event.

## Stage 5 — Crafting workflow

```text
Open recipe
→ validate recipe
→ validate materials
→ reserve/consume materials
→ roll quality/stats on server
→ create item
→ audit event
```

No client-side stat roll.

## Stage 6 — Marketplace workflow

```text
Seller selects item
→ server validates ownership
→ item locked for listing
→ listing created
→ buyer searches
→ buyer confirms
→ DB transaction moves currency + item
→ fee removed
→ events published
```

## Stage 7 — Personal Memory

Memory categories shown as timeline cards:
- First Discovery
- Greatest Victory
- Rare Find
- Near Death
- Guild Milestone
- Market Deal

Each card can include:
- timestamp;
- zone;
- short title;
- rarity/importance;
- associated item or event.

## Stage 8 — Collective Memory

Every action is not automatically public. The Memory Service selects events by configured importance.

```text
Raw domain event
→ significance filter
→ privacy/visibility check
→ aggregate
→ world memory
```

## Stage 9 — Echo reaction

### Example: “Whispering Fog”

Condition:
- ≥500 player deaths in zone within 24h.

Reaction:
- zone visual changes;
- new enemy variant;
- rare material chance increases;
- NPC dialog changes;
- event timer starts.

Event expiry:
- 3 hours.

### Player-facing sequence

```text
Death statistics threshold reached
        ↓
Server activates event
        ↓
Push announcement
        ↓
Map gets new visual state
        ↓
New enemy/event appears
        ↓
Players investigate
        ↓
Memories created
```

## Stage 10 — World discovery chain

An Echo reaction may have phases:

### Phase A — Signal
Anomaly begins.

### Phase B — Investigation
Players discover clues.

### Phase C — Community milestone
Required number of clues collected.

### Phase D — Resolution
Boss/NPC/area becomes available.

### Phase E — Permanent memory
World records the event in history.

## Stage 11 — Season flow

```text
Season announcement
→ preload assets
→ launch theme
→ new Echo rules
→ weekly world changes
→ season quests
→ season shop
→ final event
→ archive season memories
```

## Stage 12 — Offline / reconnect

When disconnected:
- allow only non-authoritative UI navigation;
- queue no gameplay result as final truth;
- on reconnect request state version;
- server sends delta or full resync.

## Stage 13 — Admin / GM workflow

```text
Monitor metric
→ identify abnormal state
→ inspect evidence
→ enable/disable Echo rule
→ force/expire World Change if needed
→ audit reason
```

No direct editing of balances/items outside controlled tools with audit logs.

## 14. State machines

### Character session

`OFFLINE → CONNECTING → CONNECTED → IN_GAME → RECONNECTING → CONNECTED/LOGOUT`

### Marketplace listing

`DRAFT → ACTIVE → LOCKED → SOLD/EXPIRED/CANCELLED`

### World change

`PROPOSED → VALIDATED → ACTIVE → EXPIRED/REVERTED`

### Echo rule

`DRAFT → ACTIVE → PAUSED → RETIRED`
