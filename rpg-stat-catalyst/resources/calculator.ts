import { CharacterStats, GameConfig } from './types';

export class RPGEngine {
    private config: GameConfig;

    constructor(config: GameConfig) {
        this.config = config;
    }

    /**
     * Calculate total available points based on level
     */
    calculateAvailablePoints(level: number): number {
        return level * this.config.pointsPerLevel;
    }

    /**
     * Calculate total points spent
     */
    calculateSpentPoints(allocatedPoints: Record<string, number>): number {
        return Object.values(allocatedPoints).reduce((sum, val) => sum + val, 0);
    }

    /**
     * Calculate Max HP based on Level and Constitution (or primary vital attribute)
     * Formula: Base + (Level * Growth) + (Attribute * Multiplier)
     */
    calculateMaxHP(level: number, vitalAttributeValue: number, vitalAttributeName: string = 'CON'): number {
        const baseHP = this.config.baseHP + (level * this.config.hpPerLevel);
        const attrMultiplier = this.config.attributeMultipliers?.[vitalAttributeName] || 0;
        const attrBonus = vitalAttributeValue * attrMultiplier;

        return Math.floor(baseHP + attrBonus);
    }

    /**
     * Check if a point can be allocated
     */
    canAllocatePoint(stats: CharacterStats, attribute: string): boolean {
        if (!this.config.validAttributes.includes(attribute)) return false;

        const available = this.calculateAvailablePoints(stats.level);
        const spent = this.calculateSpentPoints(stats.allocatedPoints);

        return spent < available;
    }

    /**
     * Generic stat calculation pipeline
     * Can be extended for specific games
     */
    calculateStats(stats: CharacterStats): Record<string, number> {
        // Base implementation: just sum base + allocated
        const effective: Record<string, number> = {};

        for (const attr of this.config.validAttributes) {
            effective[attr] = (stats.baseStats[attr] || 0) + (stats.allocatedPoints[attr] || 0);
        }

        return effective;
    }
}
