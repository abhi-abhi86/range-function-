// filepath: /Project-Last-Stand/Project-Last-Stand/src/game/mechanics.ts

interface Player {
    id: string;
    position: { x: number; y: number };
    health: number;
    armor: number;
    inventory: InventoryItem[];
}

interface InventoryItem {
    name: string;
    type: string; // e.g., weapon, healing, utility
    quantity: number;
}

class GameMechanics {
    private players: Player[];

    constructor() {
        this.players = [];
    }

    addPlayer(player: Player) {
        this.players.push(player);
    }

    movePlayer(playerId: string, newPosition: { x: number; y: number }) {
        const player = this.players.find(p => p.id === playerId);
        if (player) {
            player.position = newPosition;
        }
    }

    takeDamage(playerId: string, damage: number) {
        const player = this.players.find(p => p.id === playerId);
        if (player) {
            const effectiveDamage = Math.max(damage - player.armor, 0);
            player.health -= effectiveDamage;
            if (player.health <= 0) {
                this.removePlayer(playerId);
            }
        }
    }

    healPlayer(playerId: string, healAmount: number) {
        const player = this.players.find(p => p.id === playerId);
        if (player) {
            player.health += healAmount;
        }
    }

    removePlayer(playerId: string) {
        this.players = this.players.filter(p => p.id !== playerId);
    }

    getPlayerStats(playerId: string) {
        return this.players.find(p => p.id === playerId);
    }
}