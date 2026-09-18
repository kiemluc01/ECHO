# ECHO — Economy & Monetization

## 1. Currencies

### Gold
Earned through gameplay.

Sources:
- quests;
- combat;
- selling items;
- events.

Sinks:
- upgrades;
- crafting fees;
- marketplace fees;
- repair/fast travel if used;
- NPC services.

### Premium Coin
Bought with real money.

Use:
- cosmetics;
- convenience;
- season pass;
- selected account slots.

## 2. Economy diagram

```text
               ┌───────────┐
               │  Monsters │
               └─────┬─────┘
                     ↓
                  Materials
                     ↓
┌──────────┐     Crafting     ┌──────────┐
│ Explorer │ ───────────────→ │ Crafter  │
└────┬─────┘                  └────┬─────┘
     ↓                              ↓
     └──────── Marketplace ←───────┘
                    ↓
                  Buyer
                    ↓
                 Currency
                    ↓
                  Sinks
```

## 3. Marketplace constraints

- tax/fee configurable;
- listing duration configurable;
- maximum listings per account;
- price bounds to reduce manipulation;
- transaction audit log;
- suspicious trading detection.

## 4. Monetization catalog

### Cosmetic
- outfits;
- weapon VFX;
- mount skins;
- emotes;
- titles.

### Convenience
- inventory expansion;
- additional character slot;
- extra expedition slot;
- limited daily auto-collection convenience.

### Subscription
- monthly convenience bundle;
- premium daily reward;
- cosmetic currency.

### Season pass
- free track;
- premium track;
- mostly cosmetic and convenience rewards in initial design.

## 5. Anti-pay-to-win guardrail

Create a policy that every purchasable item is classified as:
`COSMETIC`, `CONVENIENCE`, `PROGRESSION_ASSIST`, or `POWER`.

For MVP, direct `POWER` purchases should be disabled or tightly limited so that normal progression remains viable without payment.

## 6. Economy monitoring

Daily dashboards:
- gold minted;
- gold destroyed;
- premium currency minted/spent;
- item creation/destruction;
- marketplace turnover;
- median prices;
- top 1% holdings;
- suspicious transfer graph;
- sink/source ratio.

## 7. Manipulation controls

- account age requirements for high-value trading;
- trade limits for new accounts;
- abnormal price detection;
- self-trade detection;
- rapid transfer alerts;
- item/currency provenance.
