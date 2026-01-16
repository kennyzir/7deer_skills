---
name: rpg-stat-catalyst
description: A core TypeScript library for RPG game mathematics. Handles attribute points, leveling curves, and stat derivation (HP, Dmg, etc.).
---

# RPG Stat Catalyst

A mathematical core for Role-Playing Games (RPGs) to handle character progression and stat calculation.

## Requirements
- TypeScript
- No external runtime dependencies

## Usage

1. Copy `resources/types.ts` and `resources/calculator.ts` to your project (e.g., `lib/rpg/`).

2. Initialize the engine with your game's specific configuration:

```typescript
import { RPGEngine } from '@/lib/rpg/calculator';

// 1. Define your game rules
const DevilHunterConfig = {
    baseHP: 100,
    hpPerLevel: 2,
    pointsPerLevel: 5,
    validAttributes: ['STR', 'CON', 'TEC', 'INT'],
    attributeMultipliers: {
        'CON': 5, // 1 CON = 5 HP
        'STR': 0,
    }
};

const engine = new RPGEngine(DevilHunterConfig);

// 2. Use it in your UI components
const level = 50;
const availablePoints = engine.calculateAvailablePoints(level);
const maxHP = engine.calculateMaxHP(level, 100, 'CON'); // Level 50, 100 CON

console.log(`At level ${level}, you have ${availablePoints} points.`);
console.log(`Max HP: ${maxHP}`);
```

## Extending
For complex logic (like "Innate Talents" or "Hybrid Multipliers"), extend the `RPGEngine` class:

```typescript
class AdvancedEngine extends RPGEngine {
    calculateStats(stats: CharacterStats) {
        // ... custom logic ...
    }
}
```
