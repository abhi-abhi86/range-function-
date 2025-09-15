import { PlayerStats } from '../types';
import { GameMechanics } from '../game/mechanics';

export class PlayerController {
    private stats: PlayerStats;
    private mechanics: GameMechanics;

    constructor(stats: PlayerStats, mechanics: GameMechanics) {
        this.stats = stats;
        this.mechanics = mechanics;
    }

    public handleInput(input: string): void {
        switch (input) {
            case 'moveUp':
                this.move('up');
                break;
            case 'moveDown':
                this.move('down');
                break;
            case 'moveLeft':
                this.move('left');
                break;
            case 'moveRight':
                this.move('right');
                break;
            case 'attack':
                this.attack();
                break;
            case 'interact':
                this.interact();
                break;
            default:
                console.log('Unknown input');
        }
    }

    private move(direction: string): void {
        console.log(`Moving ${direction}`);
        // Implement movement logic here
    }

    private attack(): void {
        console.log('Attacking');
        // Implement attack logic here
    }

    private interact(): void {
        console.log('Interacting with the environment');
        // Implement interaction logic here
    }

    public getStats(): PlayerStats {
        return this.stats;
    }

    public updateStats(newStats: PlayerStats): void {
        this.stats = { ...this.stats, ...newStats };
    }
}