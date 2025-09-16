# --- Resource Classes ---
class Resource(pygame.sprite.Sprite):
    def __init__(self, kind, pos):
        super().__init__()
        self.kind = kind
        if kind == 'health':
            img_path = os.path.join('assets', 'health_pack.png')
            color = (255, 0, 0)
        elif kind == 'armor':
            img_path = os.path.join('assets', 'armor.png')
            color = (0, 200, 255)
        else:
            img_path = os.path.join('assets', 'weapon.png')
            color = (255, 255, 0)
        if os.path.exists(img_path):
            self.image = pygame.image.load(img_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (32, 32))
        else:
            self.image = create_placeholder_surface(32, 32, color)
        self.rect = self.image.get_rect(center=pos)
import pygame
import math
import random
import os

# --- Constants and Settings ---
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
CAPTION = "PROJECT: LAST STAND V2"
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
GRAY = (160, 160, 160)
DARK_GRAY = (50, 50, 50)
PLAYER_COLOR = (200, 220, 255) # Placeholder color for player sprite
ZOMBIE_COLOR = (100, 150, 100) # Placeholder for zombie sprite
BRUTE_COLOR = (150, 100, 100) # Placeholder for brute sprite
BULLET_COLOR = (255, 255, 0)
XP_COLOR = (100, 100, 255)

# --- Asset Loading ---
# We will use placeholder graphics for now.
# To use real images, create an 'assets' folder and place your images there.
# Example: player_img = pygame.image.load(os.path.join('assets', 'player.png')).convert_alpha()
# You would then replace the placeholder surfaces in the class __init__ methods.

def create_placeholder_surface(width, height, color):
    """Creates a simple colored surface to stand in for a real image."""
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    surface.fill(color)
    return surface

# --- Game Object Classes (Using Pygame Sprites) ---

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Animation frames
        self.anim_frames = []
        for fname in ['player_walk1.png', 'player_walk2.png']:
            fpath = os.path.join('assets', fname)
            if os.path.exists(fpath):
                img = pygame.image.load(fpath).convert_alpha()
                img = pygame.transform.scale(img, (40, 40))
                self.anim_frames.append(img)
        # Fallback to static image
        if not self.anim_frames:
            player_img_path = os.path.join('assets', 'player.png')
            if os.path.exists(player_img_path):
                self.anim_frames = [pygame.transform.scale(pygame.image.load(player_img_path).convert_alpha(), (40, 40))]
            else:
                img = create_placeholder_surface(40, 40, PLAYER_COLOR)
                pygame.draw.rect(img, GRAY, (30, 17, 20, 6))
                self.anim_frames = [img]
        # Shooting and death frames
        shoot_path = os.path.join('assets', 'player_shoot.png')
        self.shoot_frame = pygame.transform.scale(pygame.image.load(shoot_path).convert_alpha(), (40, 40)) if os.path.exists(shoot_path) else self.anim_frames[0]
        dead_path = os.path.join('assets', 'player_dead.png')
        self.dead_frame = pygame.transform.scale(pygame.image.load(dead_path).convert_alpha(), (40, 40)) if os.path.exists(dead_path) else self.anim_frames[0]
        self.image = self.anim_frames[0]
        self.rect = self.image.get_rect(center=(x, y))
        self.pos = pygame.math.Vector2(self.rect.center)
        # Player Stats
        self.speed = 5
        self.max_hp = 100
        self.hp = self.max_hp
        self.last_shot_time = 0
        self.shot_cooldown = 200 # milliseconds, can be upgraded
        self.xp = 0
        self.level = 1
        self.xp_to_next_level = 100
        self.anim_index = 0
        self.anim_timer = 0
        self.state = 'idle' # idle, walk, shoot, dead

    def update(self):
        self.handle_input()
        self.rotate_towards_mouse()
        # Animation logic
        if self.state == 'dead':
            self.image = self.dead_frame
        elif self.state == 'shoot':
            self.image = self.shoot_frame
        elif self.state == 'walk':
            self.anim_timer += 1
            if self.anim_timer % 10 == 0:
                self.anim_index = (self.anim_index + 1) % len(self.anim_frames)
            self.image = self.anim_frames[self.anim_index]
        else:
            self.image = self.anim_frames[0]
        self.rect = self.image.get_rect(center=self.rect.center)
        # Keep player within screen boundaries
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(SCREEN_WIDTH, self.rect.right)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(SCREEN_HEIGHT, self.rect.bottom)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        velocity = pygame.math.Vector2(0, 0)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            velocity.y = -1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            velocity.y = 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            velocity.x = -1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            velocity.x = 1
        if velocity.length() > 0:
            velocity.normalize_ip()
            self.pos += velocity * self.speed
            self.rect.center = self.pos
            self.state = 'walk'
        else:
            self.state = 'idle'

    def rotate_towards_mouse(self):
        mouse_pos = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_pos - self.pos
        angle = -math.degrees(math.atan2(rel_y, rel_x))
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)
    
    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.shot_cooldown:
            self.last_shot_time = current_time
            mouse_pos = pygame.mouse.get_pos()
            self.state = 'shoot'
            return Bullet(self.rect.centerx, self.rect.centery, mouse_pos)
        return None

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0
            self.state = 'dead'
            self.kill()
        return self.hp <= 0

    def gain_xp(self, amount):
        self.xp += amount
        while self.xp >= self.xp_to_next_level:
            self.level_up()
    
    def level_up(self):
        self.xp -= self.xp_to_next_level
        self.level += 1
        self.xp_to_next_level = int(self.xp_to_next_level * 1.5)
        # Return True to signal the game loop to show the upgrade screen
        return True


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target_pos):
        super().__init__()
        self.image = create_placeholder_surface(10, 10, BULLET_COLOR)
        self.rect = self.image.get_rect(center=(x, y))
        self.pos = pygame.math.Vector2(x, y)
        self.speed = 15
        
        direction = (pygame.math.Vector2(target_pos) - self.pos).normalize()
        self.velocity = direction * self.speed

    def update(self):
        self.pos += self.velocity
        self.rect.center = self.pos
        # Kill bullet if it goes off-screen
        if not pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT).contains(self.rect):
            self.kill()


class Enemy(pygame.sprite.Sprite):
    """Base class for all enemy types."""
    def __init__(self, player):
        super().__init__()
        self.player = player
        # Animation frames
        self.anim_frames = []
        for fname in ['enemy_walk1.png', 'enemy_walk2.png']:
            fpath = os.path.join('assets', fname)
            if os.path.exists(fpath):
                img = pygame.image.load(fpath).convert_alpha()
                img = pygame.transform.scale(img, (40, 40))
                self.anim_frames.append(img)
        if not self.anim_frames:
            enemy_img_path = os.path.join('assets', 'enemy.png')
            if os.path.exists(enemy_img_path):
                self.anim_frames = [pygame.transform.scale(pygame.image.load(enemy_img_path).convert_alpha(), (40, 40))]
            else:
                img = create_placeholder_surface(40, 40, (180, 180, 220))
                self.anim_frames = [img]
        dead_path = os.path.join('assets', 'enemy_dead.png')
        self.dead_frame = pygame.transform.scale(pygame.image.load(dead_path).convert_alpha(), (40, 40)) if os.path.exists(dead_path) else self.anim_frames[0]
        self.image = self.anim_frames[0]
        self.spawn_offscreen()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.anim_index = 0
        self.anim_timer = 0
        self.state = 'walk' # walk, dead

    def spawn_offscreen(self):
        side = random.choice(['top', 'bottom', 'left', 'right'])
        if side == 'top':
            x = random.randint(0, SCREEN_WIDTH)
            y = -50
        elif side == 'bottom':
            x = random.randint(0, SCREEN_WIDTH)
            y = SCREEN_HEIGHT + 50
        elif side == 'left':
            x = -50
            y = random.randint(0, SCREEN_HEIGHT)
        else: # right
            x = SCREEN_WIDTH + 50
            y = random.randint(0, SCREEN_HEIGHT)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        if self.state == 'dead':
            self.image = self.dead_frame
        else:
            # Animation logic
            self.anim_timer += 1
            if self.anim_timer % 12 == 0:
                self.anim_index = (self.anim_index + 1) % len(self.anim_frames)
            # Rotate to face the player
            direction = self.player.pos - self.pos
            angle = -math.degrees(math.atan2(direction.y, direction.x))
            frame = self.anim_frames[self.anim_index]
            self.image = pygame.transform.rotate(frame, angle)
            self.rect = self.image.get_rect(center=self.pos)
            # Move towards the player
            if direction.length() > 0:
                direction.normalize_ip()
                self.pos += direction * self.speed
                self.rect.center = self.pos

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.state = 'dead'
            self.kill()
            return True
        return False


class Zombie(Enemy):
    def __init__(self, player, wave):
        self.original_image = create_placeholder_surface(30, 30, ZOMBIE_COLOR)
        super().__init__(player)
        self.speed = 1.5 + (wave * 0.1)
        self.hp = 25
        self.damage = 10
        self.xp_reward = 10


class Brute(Enemy):
    def __init__(self, player, wave):
        self.original_image = create_placeholder_surface(50, 50, BRUTE_COLOR)
        super().__init__(player)
        self.speed = 1 + (wave * 0.05)
        self.hp = 100
        self.damage = 25
        self.xp_reward = 50


class XPDrop(pygame.sprite.Sprite):
    def __init__(self, center_pos, xp_value):
        super().__init__()
        self.image = create_placeholder_surface(12, 12, XP_COLOR)
        self.rect = self.image.get_rect(center=center_pos)
        self.xp_value = xp_value


# --- Game Functions ---
def draw_hud(surface, player, wave, enemies_left):
    font_large = pygame.font.Font(None, 48)
    font_small = pygame.font.Font(None, 36)

    # Wave and Enemy Count
    wave_text = font_large.render(f"WAVE: {wave}", True, WHITE)
    surface.blit(wave_text, (SCREEN_WIDTH - wave_text.get_width() - 20, 20))
    enemies_text = font_small.render(f"ENEMIES: {enemies_left}", True, GRAY)
    surface.blit(enemies_text, (SCREEN_WIDTH - enemies_text.get_width() - 20, 70))
    
    # Player HP Bar
    hp_text = font_small.render("HP", True, WHITE)
    surface.blit(hp_text, (20, 20))
    hp_bar_bg = pygame.Rect(70, 25, 250, 25)
    hp_ratio = max(0, player.hp / player.max_hp)
    hp_bar_fill = pygame.Rect(70, 25, int(250 * hp_ratio), 25)
    pygame.draw.rect(surface, DARK_GRAY, hp_bar_bg, border_radius=5)
    pygame.draw.rect(surface, RED, hp_bar_fill, border_radius=5)
    
    # Player XP Bar
    xp_text = font_small.render("XP", True, WHITE)
    surface.blit(xp_text, (20, 60))
    xp_bar_bg = pygame.Rect(70, 65, 250, 25)
    xp_ratio = max(0, player.xp / player.xp_to_next_level)
    xp_bar_fill = pygame.Rect(70, 65, int(250 * xp_ratio), 25)
    pygame.draw.rect(surface, DARK_GRAY, xp_bar_bg, border_radius=5)
    pygame.draw.rect(surface, BLUE, xp_bar_fill, border_radius=5)
    level_text = font_small.render(f"LVL: {player.level}", True, WHITE)
    surface.blit(level_text, (330, 45))


def show_modal(surface, title, message, button_text):
    font_title = pygame.font.Font(None, 80)
    font_message = pygame.font.Font(None, 40)
    font_button = pygame.font.Font(None, 50)

    # Draw a semi-transparent background overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((26, 32, 44, 220))
    surface.blit(overlay, (0, 0))

    # Title
    title_surf = font_title.render(title, True, WHITE)
    title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    surface.blit(title_surf, title_rect)
    
    # Message
    y_offset = title_rect.bottom + 40
    for line in message.split('\n'):
        msg_surf = font_message.render(line, True, GRAY)
        msg_rect = msg_surf.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
        surface.blit(msg_surf, msg_rect)
        y_offset += 40

    # Button
    button_rect = pygame.Rect(0, 0, 250, 70)
    button_rect.center = (SCREEN_WIDTH // 2, y_offset + 80)
    pygame.draw.rect(surface, (74, 85, 104), button_rect, border_radius=10)
    
    btn_surf = font_button.render(button_text, True, WHITE)
    btn_rect = btn_surf.get_rect(center=button_rect.center)
    surface.blit(btn_surf, btn_rect)
    
    pygame.display.flip()
    return button_rect

# --- Main Game Loop ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(CAPTION)
    clock = pygame.time.Clock()
    # Load Free Fire-inspired map
    map_img_path = os.path.join('assets', 'map_freefire.png')
    if os.path.exists(map_img_path):
        map_img = pygame.image.load(map_img_path).convert()
        map_img = pygame.transform.scale(map_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    else:
        map_img = None

    # Sprite Groups
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    xp_drops = pygame.sprite.Group()
    resources = pygame.sprite.Group()

    # Game state variables
    game_state = "start"
    running = True
    wave = 0
    
    def reset_game():
        nonlocal player, wave, safe_zone_radius, battle_royale_active
        # Clear all sprites
        all_sprites.empty()
        enemies.empty()
        bullets.empty()
        xp_drops.empty()
        resources.empty()
        # Create new player
        player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        all_sprites.add(player)
        wave = 0
        safe_zone_radius = min(SCREEN_WIDTH, SCREEN_HEIGHT) // 2
        battle_royale_active = True

    def spawn_battle_royale():
        # Spawn multiple human enemies (battle royale style)
        num_enemies = 20
        for _ in range(num_enemies):
            enemy = Enemy(player)
            all_sprites.add(enemy)
            enemies.add(enemy)
        # Spawn resources randomly on the map
        for _ in range(8):
            kind = random.choice(['health', 'armor', 'weapon'])
            pos = (random.randint(100, SCREEN_WIDTH-100), random.randint(100, SCREEN_HEIGHT-100))
            res = Resource(kind, pos)
            all_sprites.add(res)
            resources.add(res)

    # Initial setup
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    safe_zone_radius = min(SCREEN_WIDTH, SCREEN_HEIGHT) // 2
    battle_royale_active = False

    while running:
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Handle button clicks in different game states
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if game_state == "start" and start_button.collidepoint(event.pos):
                    reset_game()
                    spawn_battle_royale()
                    game_state = "playing"
                elif game_state == "game_over" and restart_button.collidepoint(event.pos):
                    game_state = "start"

        # --- Game State Logic ---
        if game_state == "playing":
            # Shrinking safe zone
            if battle_royale_active and safe_zone_radius > 100:
                safe_zone_radius -= 0.5 # Shrink per frame

            # Player shooting
            if pygame.mouse.get_pressed()[0]: # Left mouse button
                new_bullet = player.shoot()
                if new_bullet:
                    all_sprites.add(new_bullet)
                    bullets.add(new_bullet)

            # Update all sprites
            all_sprites.update()

            # Collision Detection
            # Bullets hitting enemies
            hits = pygame.sprite.groupcollide(enemies, bullets, False, True)
            for enemy, bullet_list in hits.items():
                if enemy.take_damage(len(bullet_list) * 25): # 25 damage per bullet
                    xp_drop = XPDrop(enemy.rect.center, 10)
                    all_sprites.add(xp_drop)
                    xp_drops.add(xp_drop)

            # Enemies hitting player
            player_hits = pygame.sprite.spritecollide(player, enemies, True)
            for enemy in player_hits:
                if player.take_damage(20):
                    game_state = "game_over"

            # Player collecting XP
            xp_collected = pygame.sprite.spritecollide(player, xp_drops, True)
            for xp in xp_collected:
                if player.gain_xp(xp.xp_value):
                    player.hp = min(player.max_hp, player.hp + 25)
                    player.shot_cooldown = max(50, player.shot_cooldown * 0.9)

            # Player picking up resources
            picked = pygame.sprite.spritecollide(player, resources, True)
            for res in picked:
                if res.kind == 'health':
                    player.hp = min(player.max_hp, player.hp + 40)
                elif res.kind == 'armor':
                    player.max_hp += 20
                    player.hp = min(player.max_hp, player.hp + 20)
                elif res.kind == 'weapon':
                    player.shot_cooldown = max(30, player.shot_cooldown * 0.8)

            # Check for last player standing
            if not enemies:
                battle_royale_active = False
                game_state = "game_over"

            # Check if player is outside safe zone
            dist_to_center = math.hypot(player.pos.x - SCREEN_WIDTH // 2, player.pos.y - SCREEN_HEIGHT // 2)
            if dist_to_center > safe_zone_radius:
                player.take_damage(1) # Damage per frame outside safe zone

        # --- Drawing ---
        # Draw map background
        if map_img:
            screen.blit(map_img, (0, 0))
        else:
            # Simple terrain: grass, water, buildings
            screen.fill((60, 180, 90)) # Grass
            pygame.draw.rect(screen, (70, 130, 180), (200, 600, 300, 120)) # Water
            pygame.draw.rect(screen, (120, 120, 120), (800, 200, 120, 180)) # Building
            pygame.draw.rect(screen, (120, 120, 120), (400, 300, 80, 80)) # Building
            pygame.draw.rect(screen, (120, 120, 120), (1000, 600, 100, 100)) # Building

        # Draw shrinking safe zone
        if game_state == "playing" and battle_royale_active:
            pygame.draw.circle(screen, (60, 180, 255), (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), int(safe_zone_radius), 4)

        if game_state == "start":
            start_message = "Battle Royale! Survive and be the last player standing.\n\nCONTROLS:\n[W][A][S][D] or Arrows to Move\n[MOUSE] to Aim & [LEFT CLICK] to Shoot"
            start_button = show_modal(screen, "BATTLE ROYALE", start_message, "START GAME")
        elif game_state == "game_over":
            game_over_message = "Game Over!"
            restart_button = show_modal(screen, "GAME OVER", game_over_message, "RESTART")
        elif game_state == "playing":
            all_sprites.draw(screen)
            draw_hud(screen, player, 1, len(enemies))
            pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()

if __name__ == '__main__':
    main()
