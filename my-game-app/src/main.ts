import { GameEngine } from './game/engine';

const gameEngine = new GameEngine();

function gameLoop() {
    gameEngine.update();
    gameEngine.render();
    requestAnimationFrame(gameLoop);
}

gameEngine.start();
gameLoop();