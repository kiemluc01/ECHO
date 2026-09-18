# ECHO — Product Requirements Document (PRD)

## 1. Product summary

**Working title:** ECHO
**Platform:** iOS / Android
**Genre:** Online 3D RPG + social simulation + dynamic world
**Primary session:** 5–15 minutes
**Secondary session:** 30–60 minutes for dungeon, events and social play
**Target:** Players who enjoy progression, discovery, collection, economy and seeing persistent consequences in a shared world.

### One-line value proposition

> Explore a persistent 3D world whose future content is shaped by the collective history of its players.

## 2. Problem / opportunity

Most progression games have a static content loop: the developer creates the map, quest, boss and rewards; players consume them. ECHO adds a second loop: **player actions become signals that can influence future content**.

The product opportunity is to make the player feel that:
- what they did mattered;
- discoveries are socially valuable;
- the server has history;
- returning to the game can reveal consequences of previous behavior.

## 3. Product pillars

### P1 — Persistent memory
Important actions create Memory Events.

Examples:
- first player discovery;
- world boss defeat;
- unusual route used repeatedly;
- market shortage;
- large guild contribution;
- repeated player deaths in a zone.

### P2 — Reactive world
The server converts aggregated patterns into bounded world changes.

Examples:
- a new NPC appears;
- a forgotten shrine unlocks;
- a resource becomes scarce;
- a hidden event becomes available;
- an enemy variant is introduced.

### P3 — Progression
Character level, gear, collection, crafting and reputation provide familiar progression.

### P4 — Economy
Players gather, craft, consume and trade. The economy is designed around transparent sources and sinks.

### P5 — Social history
Guilds, shared discoveries and server-wide milestones create collective stories.

## 4. Personas

### Persona A — Progression Player
Wants clear goals, upgrades and efficient farming.

### Persona B — Explorer
Wants mysteries, secrets, rare discoveries and unusual interactions.

### Persona C — Trader/Crafter
Wants market activity, crafting depth and resource arbitrage.

### Persona D — Social Player
Wants guild identity, cooperative events and shared achievements.

## 5. Core loop

```text
Explore → Gather/Fight → Loot → Upgrade/Craft → Discover/Trade
                         ↓
                   Memory Event
                         ↓
              Echo aggregation/anomaly
                         ↓
                World reaction/event
                         ↓
                   Explore again
```

## 6. Game systems

### 6.1 Character
- Level and XP
- Base attributes
- Equipment
- Skills
- Cosmetic appearance
- Titles / achievements

### 6.2 World
- Hub city
- 3–5 PvE zones for MVP
- Dungeon instances
- World event area
- Resource nodes
- NPCs

### 6.3 Gear
- Common → Uncommon → Rare → Epic → Legendary
- Affixes
- Upgrade level
- Equipment score

### 6.4 Gathering / crafting
MVP professions:
- Foraging
- Mining
- Blacksmithing
- Alchemy

### 6.5 Memory
Memory Event categories:
- DISCOVERY
- COMBAT
- ECONOMY
- SOCIAL
- EXPLORATION
- FAILURE
- COLLECTION

Memory has two layers:
- **Personal Memory:** tied to a player.
- **World Memory:** aggregated across many players.

### 6.6 Echo Engine
The Echo Engine does not directly modify arbitrary database fields. It creates a proposed **World Change** with:
- trigger rule;
- evidence window;
- threshold;
- impact scope;
- start/end time;
- audit trail.

Examples:

```text
IF deaths(zone_04, 24h) >= 500
THEN create event "Whispering Fog"
```

```text
IF first_discovery(item_X) exists
THEN create world announcement + lore entry
```

```text
IF herb_supply / herb_demand < 0.20 for 6h
THEN activate "Herbalist Caravan"
```

## 7. Monetization product principles

Initial model:
- cosmetic items;
- season pass;
- convenience subscriptions;
- inventory/character slots;
- selected time-saving boosts.

Avoid designing mandatory spending gates for core progression in MVP.

## 8. User stories

### Epic: Onboarding
**US-001** As a new player, I want a short tutorial so I can understand movement, combat and inventory.

**Acceptance criteria**
- Tutorial completes in ≤15 minutes for a first-time player.
- Player completes movement, attack, loot and equip flows.
- Server persists tutorial completion.

### Epic: Exploration
**US-010** As an explorer, I want to discover hidden locations so that I can create rare memories.

**Acceptance criteria**
- At least 5 hidden points exist in MVP zones.
- First discovery is persisted server-side.
- Discovery can trigger a world announcement or lore update according to configured rules.

### Epic: Economy
**US-020** As a trader, I want to list items on the marketplace so other players can buy them.

**Acceptance criteria**
- Listing validates item ownership.
- Seller cannot spend/list the same item twice.
- Purchase is atomic: item ownership and currency movement either both succeed or both fail.
- Transaction fee is applied.

### Epic: Memory
**US-030** As a player, I want important things I did to be remembered so my character develops a history.

**Acceptance criteria**
- Significant actions create Memory Events.
- Memory events are deduplicated where required.
- Personal memory page displays the event timeline.

### Epic: World reaction
**US-040** As a player, I want the world to react to collective behavior so the server feels alive.

**Acceptance criteria**
- Echo rules are configurable by operations staff.
- A world change stores trigger evidence.
- Changes are reversible/expirable.
- Every change is auditable.

## 9. MVP scope

### In scope
- Account/login
- Character creation
- Hub city
- 3 PvE zones
- 1 dungeon
- 1 world boss
- 4 gathering/crafting systems
- Gear progression
- Inventory
- Marketplace
- Personal Memory timeline
- 10–20 Echo rules
- 5 reactive world events
- Basic guilds
- Daily quests
- Cosmetic store
- Season pass skeleton

### Out of scope
- PvP ranking
- Player housing customization beyond cosmetic starter version
- Cross-region server migration
- Fully procedural maps
- Player-generated scripts/code
- Fully autonomous AI NPCs

## 10. Product KPIs

These are operational targets for validation, not guaranteed outcomes:

| Metric | MVP measurement |
|---|---|
| Tutorial completion | % of new accounts finishing onboarding |
| D1/D7 retention | measured by cohort |
| Avg session length | minutes/session |
| Sessions/player/day | average |
| Marketplace participation | % active users listing or buying |
| Memory creation rate | memory events / DAU |
| World reaction discovery | % players encountering a reactive event |
| Crash-free sessions | client stability |
| API p95 latency | endpoint group |
| Economy inflation | gold creation vs destruction |

## 11. Product risks

| Risk | Impact | Mitigation |
|---|---|---|
| World reactions feel random | High | Show cause/effect messaging and evidence |
| Economy inflation | High | tune sinks and server-side caps |
| Cheating | High | authoritative server and anomaly detection |
| Content production cost | Medium | bounded event templates |
| Mobile performance | High | stylized assets, LOD, batching, budgets |
| New players feel behind | High | catch-up systems and rotating zones |

## 12. Definition of Done for gameplay feature

A feature is done when:
- product behavior is documented;
- server validation exists;
- happy-path and failure tests exist;
- telemetry exists;
- client UI/UX is implemented;
- exploit paths are reviewed;
- rollback/admin operation is available when the feature affects economy or world state.
