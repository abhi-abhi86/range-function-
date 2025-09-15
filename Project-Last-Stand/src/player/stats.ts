class PlayerStats {
    health: number;
    maxHealth: number;
    armor: number;
    maxArmor: number;
    inventory: string[];

    constructor(maxHealth: number, maxArmor: number) {
        this.maxHealth = maxHealth;
        this.health = maxHealth;
        this.maxArmor = maxArmor;
        this.armor = 0;
        this.inventory = [];
    }

    takeDamage(amount: number): void {
        const effectiveDamage = Math.max(0, amount - this.armor);
        this.health = Math.max(0, this.health - effectiveDamage);
        this.armor = Math.max(0, this.armor - amount);
    }

    heal(amount: number): void {
        this.health = Math.min(this.maxHealth, this.health + amount);
    }

    addArmor(amount: number): void {
        this.armor = Math.min(this.maxArmor, this.armor + amount);
    }

    addItem(item: string): void {
        this.inventory.push(item);
    }

    removeItem(item: string): void {
        const index = this.inventory.indexOf(item);
        if (index > -1) {
            this.inventory.splice(index, 1);
        }
    }

    getStats(): { health: number; armor: number; inventory: string[] } {
        return {
            health: this.health,
            armor: this.armor,
            inventory: this.inventory,
        };
    }
}