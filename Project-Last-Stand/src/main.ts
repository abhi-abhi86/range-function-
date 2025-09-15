// filepath: /Project-Last-Stand/Project-Last-Stand/src/main.ts

import { GameEngine } from './game/engine';

const gameEngine = new GameEngine();

function main() {
    gameEngine.initialize();
    gameEngine.startGameLoop();
}

main();