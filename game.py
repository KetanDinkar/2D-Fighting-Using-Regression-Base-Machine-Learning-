import raylibpy
import random
import time
import os

# Constants
MOVE_X = 3  # Reduced for smoother movement
MOVE_Y = 12  # Increased for faster jump
MAX_HEALTH = 100
SCREEN_WIDTH = 16 * 100
SCREEN_HEIGHT = 9 * 100
FPS = 60
MOVE_LOG_FILE = "player_moves.txt"
MAX_MOVES_TO_ANALYZE = 100  # Limit analysis to last 100 moves
MOVE_FRAME_TIME = 0.1  # Reduced for smoother animations
ATTACK_TIME = 0.5  # Seconds for regular attacks
SPECIAL_ATTACK_TIME = 0.6  # Seconds for special attacks (punch/kick 3, 5)
CROUCH_TIME = 0.3  # Seconds for crouch
JUMP_TIME = 0.3  # Reduced for faster jump

class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 221
        self.height = 363
        self.health = MAX_HEALTH
        self.is_jumping = False
        self.is_moving = False
        self.is_kicking = False
        self.is_punching = False
        self.is_blocking = False
        self.is_crouch = False
        self.move_position = 0
        self.kick = 0
        self.punch = 0
        self.last_hit_time = 0.0
        self.combo_count = 0
        self.damage_flash_time = 0.0

class Cpu(Player):
    def __init__(self):
        super().__init__()
        self.player_punch_count = 0
        self.player_kick_count = 0
        self.preferred_counter = None
        self.memory = []
        self.block_modifier = 0
        self.punch_modifier = 0
        self.kick_modifier = 0

def log_player_move(action):
    """Log player action to a file with a timestamp."""
    with open(MOVE_LOG_FILE, "a") as f:
        f.write(f"{time.time()},{action}\n")

def reset_move_log():
    """Clear the player_moves.txt file."""
    with open(MOVE_LOG_FILE, "w") as f:
        f.write("")

def analyze_moves_on_loss():
    """Analyze the last 100 moves from file and return dominant action."""
    if not os.path.exists(MOVE_LOG_FILE):
        return None
    action_counts = {"punch": 0, "kick": 0, "block": 0, "crouch": 0, "jump": 0, "move": 0}
    with open(MOVE_LOG_FILE, "r") as f:
        moves = f.readlines()[-MAX_MOVES_TO_ANALYZE:]  # Read last 100 lines
        for line in moves:
            try:
                _, action = line.strip().split(",")
                if action in action_counts:
                    action_counts[action] += 1
            except ValueError:
                continue  # Skip malformed lines
    max_action = max(action_counts, key=action_counts.get)
    if action_counts[max_action] >= 10:  # Higher threshold for reliability
        return max_action
    return None

def update_cpu_strategy(cpu, dominant_action):
    """Update CPU strategy based on dominant player action."""
    cpu.block_modifier = 0
    cpu.punch_modifier = 0
    cpu.kick_modifier = 0
    if dominant_action == "punch":
        cpu.preferred_counter = "punch"
        cpu.block_modifier = 50
        cpu.kick_modifier = 30
    elif dominant_action == "kick":
        cpu.preferred_counter = "kick"
        cpu.block_modifier = 50
        cpu.kick_modifier = 30
    else:
        cpu.preferred_counter = None

def get_texture_for_state(player, cpu, textures, is_cpu, moving_backward):
    """Return the appropriate texture based on character state."""
    if is_cpu:
        if cpu.is_jumping:
            return textures[20]  # cpu_jump
        if cpu.is_moving and not cpu.is_jumping:
            if moving_backward:
                return textures[19] if cpu.move_position == 1 else textures[18]  # cpu_move2, cpu_move1
            return textures[18] if cpu.move_position == 1 else textures[19]  # cpu_move1, cpu_move2
        if cpu.is_blocking:
            return textures[31]  # cpu_block
        if cpu.is_punching:
            return textures[26 + (cpu.punch - 1)]  # cpu_punch1-5
        if cpu.is_kicking:
            return textures[21 + (cpu.kick - 1)]  # cpu_kick1-5
        if cpu.is_crouch:
            return textures[16]  # cpu_crouch
        return textures[17]  # cpu_stand
    else:
        if player.is_crouch:
            return textures[0]  # player_crouch
        if player.is_jumping:
            return textures[4]  # player_jump
        if player.kick:
            return textures[5 + (player.kick - 1)]  # player_kick1-5
        if player.is_blocking:
            return textures[15]  # player_block
        if player.is_punching:
            return textures[10 + (player.punch - 1)]  # player_punch1-5
        if player.is_moving and not player.is_jumping:
            if raylibpy.is_key_down(raylibpy.KEY_A) and not raylibpy.is_key_down(raylibpy.KEY_D):
                return textures[3] if player.move_position == 1 else textures[2]  # player_move2, player_move1
            return textures[2] if player.move_position == 1 else textures[3]  # player_move1, player_move2
        return textures[1]  # player_stand

def reset_round(player, cpu):
    """Reset player and CPU state for a new round."""
    player.health = MAX_HEALTH
    player.x = SCREEN_WIDTH // 2 - player.width // 2 - 300
    player.y = SCREEN_HEIGHT - player.height - 180
    player.is_jumping = False
    player.is_moving = False
    player.is_kicking = False
    player.is_punching = False
    player.is_blocking = False
    player.is_crouch = False
    player.move_position = 0
    player.kick = 0
    player.punch = 0
    player.combo_count = 0
    player.damage_flash_time = 0.0

    cpu.health = MAX_HEALTH
    cpu.x = SCREEN_WIDTH // 2 + cpu.width // 2 + 100
    cpu.y = SCREEN_HEIGHT - cpu.height - 180
    cpu.is_jumping = False
    cpu.is_moving = False
    cpu.is_kicking = False
    cpu.is_punching = False
    cpu.is_blocking = False
    cpu.is_crouch = False
    cpu.move_position = 0
    cpu.kick = 0
    cpu.punch = 0
    cpu.combo_count = 0
    cpu.damage_flash_time = 0.0

def main():
    raylibpy.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "2D Fighting Game with Nemesis System")
    raylibpy.set_target_fps(FPS)
    raylibpy.init_audio_device()  # Initialize audio device

    # Load and play background music
    try:
        music = raylibpy.load_music_stream("D:\\programs\\c++\\games\\game_5\\b.mp3")
        raylibpy.play_music_stream(music)
        raylibpy.set_music_volume(music, 1.0)  # Set volume to 100%
    except Exception as e:
        print(f"Error loading music: {e}")

    # Load hit sounds
    try:
        playerhit = raylibpy.load_music_stream("D:\\programs\\c++\\games\\game_5\\p1.mp3")
        raylibpy.play_music_stream(playerhit)
        raylibpy.set_music_volume(playerhit, 4.0)
        cpuhit = raylibpy.load_music_stream("D:\\programs\\c++\\games\\game_5\\p2.mp3")
        raylibpy.play_music_stream(cpuhit)
        raylibpy.set_music_volume(cpuhit, 4.0)
    except Exception as e:
        print(f"Error loading hit sounds: {e}")

    game_over = False
    match_over = False  # Track if the match (3 rounds) is over
    player_rounds_won = 0
    cpu_rounds_won = 0
    current_round = 1
    hb = 0  # 1 for player round win, 2 for CPU round win
    round_end_time = 0.0  # Time when round ends
    frame_time = raylibpy.get_time()
    kick_start_time = 0.0
    punch_start_time = 0.0
    cpu_punch_start_time = 0.0
    cpu_kick_start_time = 0.0
    cpu_crouch_start_time = 0.0
    cpu_start_delay = 2.5
    cpu_start_time = raylibpy.get_time()
    last_regen_time = raylibpy.get_time()
    shake_time = 0.0
    screen_shake = raylibpy.Vector2(0, 0)
    nemesis_update_time = raylibpy.get_time()

    player = Player()
    player.x = SCREEN_WIDTH // 2 - player.width // 2 - 300
    player.y = SCREEN_HEIGHT - player.height - 180
    player.health = MAX_HEALTH

    cpu = Cpu()
    cpu.x = SCREEN_WIDTH // 2 + cpu.width // 2 + 100
    cpu.y = SCREEN_HEIGHT - cpu.height - 180
    cpu.health = MAX_HEALTH

    # Particle system for hit sparks
    particles = []

    dominant_action = analyze_moves_on_loss()
    update_cpu_strategy(cpu, dominant_action)

    flore_y = SCREEN_HEIGHT - 180

    try:
        textures = [
            raylibpy.load_texture("D:\\programs\\c++\\games\\game_5\\player movement\\crouch.png"),
            raylibpy.load_texture("D:\\programs\\c++\\games\\game_5\\player movement\\stand.png"),
            raylibpy.load_texture("D:\\programs\\c++\\games\\game_5\\player movement\\move1.png"),
            raylibpy.load_texture("D:\\programs\\c++\\games\\game_5\\player movement\\move2.png"),
            raylibpy.load_texture("D:\\programs\\c++\\games\\game_5\\player movement\\jump.png"),
            raylibpy.load_texture("D:\\programs\\c++\\games\\game_5\\player movement\\kick1.png"),
            raylibpy.load_texture("D:\\programs\\c++\\games\\game_5\\player movement\\kick2.png"),
            raylibpy.load_texture("D:\\programs\\c++\\games\\game_5\\player movement\\kick3.png"),
            raylibpy.load_texture("D:\\programs\\c++\\games\\game_5\\player movement\\kick4.png"),
            raylibpy.load_texture("D:\\programs\\c++\\games\\game_5\\player movement\\kick5.png"),
            raylibpy.load_texture("D:\\programs\\c++\\games\\game_5\\player movement\\punch1.png"),
            raylibpy.load_texture("D:\\programs\\c++\\games\\game_5\\player movement\\punch2.png"),
            raylibpy.load_texture("D:\\programs\\c++\\games\\game_5\\player movement\\punch3.png"),
            raylibpy.load_texture("D:\\programs\\c++\\games\\game_5\\player movement\\punch4.png"),
            raylibpy.load_texture("D:\\programs\\c++\\games\\game_5\\player movement\\punch5.png"),
            raylibpy.load_texture("D:\\programs\\c++\\games\\game_5\\player movement\\block.png"),
            raylibpy.load_texture("D:\\programs\\c++\\games\\game_5\\cpu\\crouch.png"),
            raylibpy.load_texture("D:\\programs\\c++\\games\\game_5\\cpu\\stand.png"),
            raylibpy.load_texture("D:\\programs\\c++\\games\\game_5\\cpu\\move 1.png"),
            raylibpy.load_texture("D:\\programs\\c++\\games\\game_5\\cpu\\move 2.png"),
            raylibpy.load_texture("D:\\programs\\c++\\games\\game_5\\cpu\\jump.png"),
            raylibpy.load_texture("D:\\programs\\c++\\games\\game_5\\cpu\\kick 1.png"),
            raylibpy.load_texture("D:\\programs\\c++\\games\\game_5\\cpu\\kick 2.png"),
            raylibpy.load_texture("D:\\programs\\c++\\games\\game_5\\cpu\\kick 3.png"),
            raylibpy.load_texture("D:\\programs\\c++\\games\\game_5\\cpu\\kick 4.png"),
            raylibpy.load_texture("D:\\programs\\c++\\games\\game_5\\cpu\\kick 5.png"),
            raylibpy.load_texture("D:\\programs\\c++\\games\\game_5\\cpu\\punch 1.png"),
            raylibpy.load_texture("D:\\programs\\c++\\games\\game_5\\cpu\\punch 2.png"),
            raylibpy.load_texture("D:\\programs\\c++\\games\\game_5\\cpu\\punch 3.png"),
            raylibpy.load_texture("D:\\programs\\c++\\games\\game_5\\cpu\\punch 4.png"),
            raylibpy.load_texture("D:\\programs\\c++\\games\\game_5\\cpu\\punch 5.png"),
            raylibpy.load_texture("D:\\programs\\c++\\games\\game_5\\cpu\\block.png"),
           #raylibpy.load_texture("D:\\programs\\c++\\games\\game_5\\cpu\\throw.png"),
           # raylibpy.load_texture("D:\\programs\\c++\\games\\game_5\\cpu\\ball.png"),
            raylibpy.load_texture("D:\\programs\\c++\\games\\game_5\\background.png")
        ]
        flore = raylibpy.load_texture("D:\\programs\\c++\\games\\game_5\\flore.jpg")
    except Exception as e:
        print(f"Error loading textures: {e}")
        raylibpy.close_window()
        return

    IDLE, MOVE, PUNCH, KICK, BLOCK, CROUCH, JUMP = range(7)
    cpu_action_state = IDLE
    cpu_action_duration = 0.0
    cpu_action_cooldown = 0.0
    MIN_ACTION_DURATION = 0.2  # Seconds
    ACTION_COOLDOWN = 0.38  # Seconds
    cpu_jump_cooldown = 0
    cpu_can_jump = True
    player_move_time = raylibpy.get_time()
    cpu_move_time = raylibpy.get_time()

    while not raylibpy.window_should_close():
        current_time = raylibpy.get_time()
        delta_time = raylibpy.get_frame_time()

        # Update music stream
        raylibpy.update_music_stream(music)

        # Check for reset move log
        if raylibpy.is_key_pressed(raylibpy.KEY_R):
            reset_move_log()

        if not match_over:
            distance = cpu.x - player.x
            abs_distance = abs(distance)

            # Check round over
            if not game_over:
                if player.health <= 0:
                    game_over = True
                    hb = 2
                    cpu_rounds_won += 1
                    dominant_action = analyze_moves_on_loss()
                    update_cpu_strategy(cpu, dominant_action)
                    round_end_time = current_time  # Set round end time
                if cpu.health <= 0:
                    game_over = True
                    hb = 1
                    player_rounds_won += 1
                    dominant_action = analyze_moves_on_loss()
                    update_cpu_strategy(cpu, dominant_action)
                    round_end_time = current_time  # Set round end time

            # Check if match is over (3 rounds won)
            if player_rounds_won >= 3 or cpu_rounds_won >= 3:
                match_over = True

            # Reset for next round if game_over but match not over
            if game_over and not match_over:
                if current_time - round_end_time >= 2.0:  # Wait 2 seconds before next round
                    reset_round(player, cpu)
                    current_round += 1
                    game_over = False
                    hb = 0
                    cpu_start_time = current_time  # Reset CPU start delay
                    round_end_time = 0.0  # Reset round end time

            # CPU health regeneration
            if not game_over and current_time - last_regen_time >= 3.0 and not cpu.is_punching and not cpu.is_kicking:
                cpu.health = min(MAX_HEALTH, cpu.health + 2)
                last_regen_time = current_time

            # Update screen shake
            if current_time - shake_time < 0.2:
                screen_shake.x = random.randint(-5, 5)
                screen_shake.y = random.randint(-5, 5)
            else:
                screen_shake.x, screen_shake.y = 0, 0

            # Update particles
            particles[:] = [p for p in particles if p['lifetime'] > 0]
            for p in particles:
                p['pos'].x += p['vel'].x * delta_time
                p['pos'].y += p['vel'].y * delta_time
                p['lifetime'] -= delta_time

            # Player input and movement
            if not game_over:
                if not raylibpy.is_key_down(raylibpy.KEY_S):
                    player.is_crouch = False
                if raylibpy.is_key_pressed(raylibpy.KEY_W) and not player.is_jumping and not player.is_crouch:
                    player.is_jumping = True
                    player.is_moving = False
                    log_player_move("jump")
                if raylibpy.is_key_down(raylibpy.KEY_S) and not player.is_jumping:
                    player.is_crouch = True
                    player.is_moving = False
                    log_player_move("crouch")
                if player.is_jumping:
                    player.y -= MOVE_Y
                    if player.y <= SCREEN_HEIGHT - 180 - player.height - 300:
                        player.is_jumping = False
                if not player.is_jumping and player.y < SCREEN_HEIGHT - 180 - player.height:
                    player.y += MOVE_Y
                if raylibpy.is_key_down(raylibpy.KEY_A):
                    player.x -= MOVE_X
                    player.is_moving = True
                    log_player_move("move")
                if raylibpy.is_key_down(raylibpy.KEY_D):
                    player.x += MOVE_X
                    player.is_moving = True
                    log_player_move("move")
                if not (raylibpy.is_key_down(raylibpy.KEY_A) or raylibpy.is_key_down(raylibpy.KEY_D)):
                    player.is_moving = False
                if player.x < 0:
                    player.x = 0
                if player.x > SCREEN_WIDTH - player.width:
                    player.x = SCREEN_WIDTH - player.width
                if cpu.x < 0:
                    cpu.x = 0
                if cpu.x > SCREEN_WIDTH - cpu.width:
                    cpu.x = SCREEN_WIDTH - cpu.width
                player.is_blocking = raylibpy.is_key_down(raylibpy.KEY_SPACE)
                if raylibpy.is_key_pressed(raylibpy.KEY_SPACE):
                    log_player_move("block")

                # Player kick actions
                if raylibpy.is_key_pressed(raylibpy.KEY_L):
                    if raylibpy.is_key_down(raylibpy.KEY_D):
                        player.kick = 2
                    elif raylibpy.is_key_down(raylibpy.KEY_W):
                        player.kick = 3
                        player.is_jumping = False
                    elif raylibpy.is_key_down(raylibpy.KEY_S):
                        player.kick = 4
                    elif raylibpy.is_key_down(raylibpy.KEY_A):
                        player.kick = 5
                    else:
                        player.kick = 1
                    player.is_kicking = True
                    kick_start_time = current_time
                    cpu.player_kick_count += 1
                    cpu.memory.append("kick")
                    log_player_move("kick")

                # Player punch actions
                if raylibpy.is_key_pressed(raylibpy.KEY_K):
                    if raylibpy.is_key_down(raylibpy.KEY_D):
                        player.punch = 2
                    elif raylibpy.is_key_down(raylibpy.KEY_W):
                        player.punch = 3
                    elif raylibpy.is_key_down(raylibpy.KEY_S):
                        player.punch = 4
                    elif raylibpy.is_key_down(raylibpy.KEY_A):
                        player.punch = 5
                    else:
                        player.punch = 1
                    player.is_punching = True
                    punch_start_time = current_time
                    cpu.player_punch_count += 1
                    cpu.memory.append("punch")
                    log_player_move("punch")

                # End player attacks
                if player.is_kicking and (current_time - kick_start_time >= (SPECIAL_ATTACK_TIME if player.kick in [3, 5] else ATTACK_TIME)):
                    player.kick = 0
                    player.is_kicking = False
                if player.is_punching and (current_time - punch_start_time >= (SPECIAL_ATTACK_TIME if player.punch in [3, 5] else ATTACK_TIME)):
                    player.punch = 0
                    player.is_punching = False

                # Player movement animation
                if player.is_moving and not player.is_jumping and not player.is_kicking and not player.is_punching:
                    if current_time - frame_time >= MOVE_FRAME_TIME:
                        player.move_position = 1 if player.move_position in [0, 2] else 2
                        frame_time = current_time
                else:
                    player.move_position = 0

                # Collision detection
                player_rect = raylibpy.Rectangle(player.x, player.y, player.width, player.height)
                cpu_rect = raylibpy.Rectangle(cpu.x, cpu.y, cpu.width, cpu.height)
                is_colliding = raylibpy.check_collision_recs(player_rect, cpu_rect)

                # Damage system
                if is_colliding and (player.is_punching or player.is_kicking) and (current_time - kick_start_time <= 0.1 or current_time - punch_start_time <= 0.1):
                    damage = 1.5 if player.is_punching and player.punch in [3, 5] else 1 if player.is_punching else 1.5 if player.kick in [3, 5] else 1
                    if cpu.is_blocking:
                        damage = (damage * 3) // 4  # ~25% damage reduction
                    cpu.health -= damage
                    cpu.damage_flash_time = current_time
                    if cpu.health < 0:
                        cpu.health = 0
                    if current_time - player.last_hit_time < 2.0:
                        player.combo_count += 1
                    else:
                        player.combo_count = 1
                    player.last_hit_time = current_time
                    if player.punch in [3, 5] or player.kick in [3, 5]:
                        shake_time = current_time
                    for _ in range(5):
                        particles.append({
                            'pos': raylibpy.Vector2(cpu.x + cpu.width / 2, cpu.y + cpu.height / 2),
                            'vel': raylibpy.Vector2(random.randint(-100, 100), random.randint(-100, 100)),
                            'lifetime': 0.3
                        })
                    raylibpy.update_music_stream(playerhit)

                if is_colliding and (cpu.is_punching or cpu.is_kicking) and (current_time - cpu_punch_start_time <= 0.1 or current_time - cpu_kick_start_time <= 0.1):
                    damage = 3 if cpu.is_punching and cpu.punch in [3, 5] else 1.5 if cpu.is_punching else 2.5 if cpu.kick in [3, 5] else 2
                    if player.is_blocking:
                        damage = (damage * 3) // 4  # ~25% damage reduction
                    player.health -= damage
                    player.damage_flash_time = current_time
                    if player.health < 0:
                        player.health = 0
                    if current_time - cpu.last_hit_time < 2.0:
                        cpu.combo_count += 1
                    else:
                        cpu.combo_count = 1
                    cpu.last_hit_time = current_time
                    if cpu.punch in [3, 5] or cpu.kick in [3, 5]:
                        shake_time = current_time
                    for _ in range(5):
                        particles.append({
                            'pos': raylibpy.Vector2(player.x + player.width / 2, player.y + player.height / 2),
                            'vel': raylibpy.Vector2(random.randint(-100, 100), random.randint(-100, 100)),
                            'lifetime': 0.3
                        })
                    raylibpy.update_music_stream(cpuhit)

                # CPU AI
                cpu_can_move = (current_time - cpu_start_time) >= cpu_start_delay
                if current_time - nemesis_update_time >= 10.0:  # Update every 10 seconds
                    dominant_action = analyze_moves_on_loss()
                    update_cpu_strategy(cpu, dominant_action)
                    nemesis_update_time = current_time

                close_distance = 150.0
                medium_distance = 300.0
                if cpu_jump_cooldown > 0:
                    cpu_jump_cooldown -= delta_time * FPS
                    if cpu_jump_cooldown <= 0:
                        cpu_can_jump = True

                if cpu_can_move:
                    if cpu_action_duration > 0:
                        cpu_action_duration -= delta_time
                    if cpu_action_cooldown > 0:
                        cpu_action_cooldown -= delta_time

                    if cpu_action_duration <= 0 and cpu_action_state != IDLE:
                        cpu.is_moving = False
                        cpu.move_position = 0
                        cpu.is_punching = False
                        cpu.punch = 0
                        cpu.is_kicking = False
                        cpu.kick = 0
                        cpu.is_blocking = False
                        cpu.is_crouch = False
                        cpu.is_jumping = False
                        cpu_action_state = IDLE
                        cpu_action_cooldown = ACTION_COOLDOWN

                    if cpu_action_duration <= 0 and cpu_action_cooldown <= 0:
                        action_choice = random.randint(0, 99)
                        block_probability = 40 + cpu.block_modifier
                        punch_probability = 70 + cpu.punch_modifier
                        kick_probability = 80 + cpu.kick_modifier

                        if is_colliding:
                            if action_choice < block_probability:
                                cpu_action_state = BLOCK
                                cpu.is_blocking = True
                                cpu_action_duration = MIN_ACTION_DURATION
                            elif action_choice < punch_probability:
                                cpu_action_state = PUNCH
                                cpu.is_punching = True
                                cpu.punch = random.randint(1, 5)
                                cpu_punch_start_time = current_time
                                cpu_action_duration = SPECIAL_ATTACK_TIME if cpu.punch in [3, 5] else ATTACK_TIME
                            else:
                                cpu_action_state = KICK
                                cpu.is_kicking = True
                                cpu.kick = random.randint(1, 5)
                                cpu_kick_start_time = current_time
                                cpu_action_duration = SPECIAL_ATTACK_TIME + 0.1 if cpu.kick == 3 else SPECIAL_ATTACK_TIME if cpu.kick == 5 else ATTACK_TIME
                        elif abs_distance < close_distance:
                            if action_choice < 30:
                                cpu_action_state = BLOCK
                                cpu.is_blocking = True
                                cpu_action_duration = MIN_ACTION_DURATION
                            elif action_choice < 50:
                                cpu_action_state = PUNCH
                                cpu.is_punching = True
                                cpu.punch = random.randint(1, 5)
                                cpu_punch_start_time = current_time
                                cpu_action_duration = SPECIAL_ATTACK_TIME if cpu.punch in [3, 5] else ATTACK_TIME
                            elif action_choice < 70:
                                cpu_action_state = KICK
                                cpu.is_kicking = True
                                cpu.kick = random.randint(1, 5)
                                cpu_kick_start_time = current_time
                                cpu_action_duration = SPECIAL_ATTACK_TIME + 0.1 if cpu.kick == 3 else SPECIAL_ATTACK_TIME if cpu.kick == 5 else ATTACK_TIME
                            elif action_choice < 85 and cpu_can_jump:
                                cpu_action_state = JUMP
                                cpu.is_jumping = True
                                cpu_can_jump = False
                                cpu_jump_cooldown = 24
                                cpu_action_duration = JUMP_TIME
                            else:
                                cpu_action_state = CROUCH
                                cpu.is_crouch = True
                                cpu_crouch_start_time = current_time
                                cpu_action_duration = CROUCH_TIME
                        elif abs_distance < medium_distance:
                            if action_choice < 50:
                                cpu_action_state = MOVE
                                cpu.is_moving = True
                                cpu.move_position = 1
                                cpu_action_duration = MIN_ACTION_DURATION + 0.1
                            elif action_choice < 70:
                                cpu_action_state = PUNCH
                                cpu.is_punching = True
                                cpu.punch = random.randint(1, 5)
                                cpu_punch_start_time = current_time
                                cpu_action_duration = SPECIAL_ATTACK_TIME if cpu.punch in [3, 5] else ATTACK_TIME
                            else:
                                cpu_action_state = KICK
                                cpu.is_kicking = True
                                cpu.kick = random.randint(1, 5)
                                cpu_kick_start_time = current_time
                                cpu_action_duration = SPECIAL_ATTACK_TIME + 0.1 if cpu.kick == 3 else SPECIAL_ATTACK_TIME if cpu.kick == 5 else ATTACK_TIME
                        else:
                            if action_choice < 70:
                                cpu_action_state = MOVE
                                cpu.is_moving = True
                                cpu.move_position = 1
                                cpu_action_duration = MIN_ACTION_DURATION + 0.1
                            elif action_choice < 85:
                                cpu_action_state = PUNCH
                                cpu.is_punching = True
                                cpu.punch = random.randint(1, 5)
                                cpu_punch_start_time = current_time
                                cpu_action_duration = SPECIAL_ATTACK_TIME if cpu.punch in [3, 5] else ATTACK_TIME
                            else:
                                cpu_action_state = KICK
                                cpu.is_kicking = True
                                cpu.kick = random.randint(1, 5)
                                cpu_kick_start_time = current_time
                                cpu_action_duration = SPECIAL_ATTACK_TIME + 0.1 if cpu.kick == 3 else SPECIAL_ATTACK_TIME if cpu.kick == 5 else ATTACK_TIME
                else:
                    cpu_action_state = IDLE
                    cpu.is_moving = False
                    cpu.move_position = 0
                    cpu.is_punching = False
                    cpu.punch = 0
                    cpu.is_kicking = False
                    cpu.kick = 0
                    cpu.is_blocking = False
                    cpu.is_crouch = False
                    cpu.is_jumping = False

                # CPU jumping physics
                if cpu.is_jumping:
                    cpu.y -= MOVE_Y
                    if cpu.y <= SCREEN_HEIGHT - 180 - cpu.height - 300:
                        cpu.is_jumping = False
                        cpu.y = SCREEN_HEIGHT - 180 - cpu.height
                if not cpu.is_jumping and cpu.y < SCREEN_HEIGHT - 180 - cpu.height:
                    cpu.y += MOVE_Y

                # CPU movement logic
                cpu_moving_backward = False
                if cpu.is_moving and cpu_action_state == MOVE:
                    if current_time - cpu_move_time >= 0.05:
                        if cpu.x < player.x and not is_colliding and cpu.x < SCREEN_WIDTH - cpu.width:
                            cpu.x += MOVE_X
                        elif cpu.x > player.x and not is_colliding and cpu.x > 0:
                            cpu.x -= MOVE_X
                        cpu_move_time = current_time
                    if current_time - frame_time >= MOVE_FRAME_TIME:
                        cpu.move_position = 2 if cpu.move_position == 1 else 1
                        frame_time = current_time
                    if (cpu.x < player.x and cpu.x > 0 and cpu.x - player.x < 0) or \
                       (cpu.x > player.x and cpu.x < SCREEN_WIDTH - cpu.width and cpu.x - player.x > 0):
                        cpu_moving_backward = True

                # CPU action timers
                if cpu.is_punching and (current_time - cpu_punch_start_time >= (SPECIAL_ATTACK_TIME if cpu.punch in [3, 5] else ATTACK_TIME)):
                    cpu.is_punching = False
                    cpu.punch = 0
                if cpu.is_kicking and (current_time - cpu_kick_start_time >= (SPECIAL_ATTACK_TIME + 0.1 if cpu.kick == 3 else SPECIAL_ATTACK_TIME if cpu.kick == 5 else ATTACK_TIME)):
                    cpu.is_kicking = False
                    cpu.kick = 0
                if cpu.is_crouch and (current_time - cpu_crouch_start_time >= CROUCH_TIME):
                    cpu.is_crouch = False

                # Player movement with collision
                if current_time - player_move_time >= 0.05:
                    if raylibpy.is_key_down(raylibpy.KEY_A) and (not is_colliding or player.x > cpu.x):
                        player.x -= MOVE_X
                    if raylibpy.is_key_down(raylibpy.KEY_D) and (not is_colliding or player.x < cpu.x):
                        player.x += MOVE_X
                    player_move_time = current_time

            # Rendering
            raylibpy.begin_drawing()
            raylibpy.clear_background(raylibpy.RAYWHITE)

            raylibpy.draw_texture(textures[32], screen_shake.x, screen_shake.y, raylibpy.WHITE)
            raylibpy.draw_texture(flore, screen_shake.x, flore_y + screen_shake.y, raylibpy.WHITE)

            # Draw health bars
            raylibpy.draw_rectangle(10, 10, 200, 20, raylibpy.RED)
            raylibpy.draw_rectangle(10, 10, (player.health * 200) // MAX_HEALTH, 20, raylibpy.GREEN)
            raylibpy.draw_text("Player", 10, 35, 20, raylibpy.BLACK)
            raylibpy.draw_rectangle(SCREEN_WIDTH - 210, 10, 200, 20, raylibpy.RED)
            raylibpy.draw_rectangle(SCREEN_WIDTH - 210, 10, (cpu.health * 200) // MAX_HEALTH, 20, raylibpy.GREEN)
            raylibpy.draw_text("CPU", SCREEN_WIDTH - 210, 35, 20, raylibpy.BLACK)

            # Draw round information
            raylibpy.draw_text(f"Round {current_round}", SCREEN_WIDTH // 2 - 100, 10, 50, raylibpy.WHITE)
            raylibpy.draw_text(f"Player Wins: {player_rounds_won}", 10, 60, 20, raylibpy.BLUE)
            raylibpy.draw_text(f"CPU Wins: {cpu_rounds_won}", SCREEN_WIDTH - 150, 60, 20, raylibpy.RED)

            # Draw combo counter
            if player.combo_count > 1:
                raylibpy.draw_text(f"Combo: {player.combo_count}", 10, 85, 20, raylibpy.BLUE)

            # Draw particles
            for p in particles:
                raylibpy.draw_rectangle(int(p['pos'].x), int(p['pos'].y), 5, 5, raylibpy.YELLOW)

            # Draw CPU taunts
            if cpu.memory and random.randint(0, 60) == 0:  # More frequent taunts
                if cpu.preferred_counter == "kick":
                    raylibpy.draw_text("Your kicks won't get past my blocks!", cpu.x, cpu.y - 20, 20, raylibpy.RED)
                elif cpu.preferred_counter == "punch":
                    raylibpy.draw_text("Your punches can't break me!", cpu.x, cpu.y - 20, 20, raylibpy.RED)
                else:
                    raylibpy.draw_text("I'm ready for your next move!", cpu.x, cpu.y - 20, 20, raylibpy.RED)

            # Draw player
            player_color = raylibpy.RED if current_time - player.damage_flash_time < 0.2 else raylibpy.WHITE
            player_texture = get_texture_for_state(player, cpu, textures, False, False)
            player_y_offset = 130 if player.is_crouch or player.kick == 4 or player.punch == 4 else -100 if player.kick == 3 or player.punch == 3 else 0
            raylibpy.draw_texture(player_texture, player.x + screen_shake.x, player.y + player_y_offset + screen_shake.y, player_color)

            # Draw CPU
            cpu_color = raylibpy.RED if current_time - cpu.damage_flash_time < 0.2 else raylibpy.WHITE
            cpu_texture = get_texture_for_state(player, cpu, textures, True, cpu_moving_backward)
            cpu_y_offset = 130 if cpu.is_crouch or cpu.kick == 4 or cpu.punch == 4 else -100 if cpu.kick == 3 or cpu.punch == 3 else 0
            raylibpy.draw_texture(cpu_texture, cpu.x + screen_shake.x, cpu.y + cpu_y_offset + screen_shake.y, cpu_color)

            # Draw round or match result
            if game_over and not match_over and current_time - round_end_time < 2.0:
                if hb == 1:
                    raylibpy.draw_text("Player Wins!", SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 + 20, 80, raylibpy.GREEN)
                elif hb == 2:
                    raylibpy.draw_text("CPU Wins!", SCREEN_WIDTH // 2 - 270, SCREEN_HEIGHT // 2 + 20, 80, raylibpy.RED)
            elif match_over:
                if player_rounds_won >= 3:
                    raylibpy.draw_text("Player Wins the Match!", SCREEN_WIDTH // 2 - 360, SCREEN_HEIGHT // 2 + 20, 80, raylibpy.GREEN)
                else:
                    raylibpy.draw_text("CPU Wins the Match!", SCREEN_WIDTH // 2 - 330, SCREEN_HEIGHT // 2 + 20, 80, raylibpy.RED)

        raylibpy.end_drawing()

    # Unload textures and music
    for texture in textures:
        raylibpy.unload_texture(texture)
    raylibpy.unload_texture(flore)
    raylibpy.unload_music_stream(music)
    raylibpy.unload_music_stream(playerhit)
    raylibpy.unload_music_stream(cpuhit)
    raylibpy.close_audio_device()
    raylibpy.close_window()

if __name__ == "__main__":
    main()