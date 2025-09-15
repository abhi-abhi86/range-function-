export interface PlayerStats {
    health: number;
    armor: number;
    inventory: InventoryItem[];
}

export interface InventoryItem {
    id: string;
    name: string;
    quantity: number;
}

export interface AIState {
    state: 'looting' | 'patrolling' | 'investigating' | 'engaging' | 'healing';
    target?: string; // ID of the target player or item
}

export interface GameEnvironment {
    biome: string;
    pointsOfInterest: POI[];
}

export interface POI {
    id: string;
    name: string;
    location: { x: number; y: number };
}