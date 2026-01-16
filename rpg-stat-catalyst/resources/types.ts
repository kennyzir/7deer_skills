export type AttributeKey = string;

export interface CharacterStats {
    level: number;
    baseStats: Record<AttributeKey, number>;
    allocatedPoints: Record<AttributeKey, number>;
    // Optional: Add more fields as needed for your specific game
    [key: string]: any;
}

export interface EffectiveStats {
    stats: Record<AttributeKey, number>;
    maxHP: number;
    availablePoints: number;
    spentPoints: number;
    // Optional: Add derived stats like 'mana', 'stamina' here
}

export interface GameConfig {
    baseHP: number;
    hpPerLevel: number;
    pointsPerLevel: number;
    validAttributes: AttributeKey[];
    attributeMultipliers?: Record<AttributeKey, number>; // e.g. { CON: 5 } means 1 CON = 5 HP
}
