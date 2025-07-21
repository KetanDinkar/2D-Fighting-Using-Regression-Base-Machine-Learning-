#include <iostream>
#include <raylib.h>
#include <vector>
#include <string>
#include <ctime>

using namespace std;

#define move_x 6
#define move_y 15
#define MAX_HEALTH 100 // Maximum health for both player and CPU

class Player {
public:
    int x, y, width, height, health;
    bool isJumping, ismoving, iskicking, ispunching, isblocking, iscrouch;
    int movepossion, kick, punch;
};

class Cpu : public Player {};

int main() {

    bool gameover = false;
    int hb=0;

    const int width = 16 * 100;
    const int height = 9 * 100;
    int distance = 0;

    Player player;
    player.width = 221;
    player.height = 363;
    player.x = width / 2 - player.width / 2 - 300;
    player.y = height - player.height - 180;
    player.health = MAX_HEALTH;
    player.isJumping = false;
    player.ismoving = false;
    player.movepossion = 0;
    player.iskicking = false;
    player.kick = 0;
    player.ispunching = false;
    player.punch = 0;
    player.isblocking = false;
    player.iscrouch = false;

    Cpu cpu;
    cpu.width = 221;
    cpu.height = 363;
    cpu.x = width / 2 + cpu.width / 2 + 100;
    cpu.y = height - cpu.height - 180;
    cpu.health = MAX_HEALTH;
    cpu.isJumping = false;
    cpu.ismoving = false;
    cpu.movepossion = 0;
    cpu.iskicking = false;
    cpu.kick = 0;
    cpu.ispunching = false;
    cpu.punch = 0;
    cpu.isblocking = false;
    cpu.iscrouch = false;

    int flore_y = height - 180;

    InitWindow(width, height, "3D");
    SetTargetFPS(60);

    // Texture loading
    Texture2D playercrouch = LoadTexture("D:\\programs\\c++\\games\\game_5\\player movement\\crouch.png");
    Texture2D playerstand = LoadTexture("D:\\programs\\c++\\games\\game_5\\player movement\\stand.png");
    Texture2D playermove1 = LoadTexture("D:\\programs\\c++\\games\\game_5\\player movement\\move1.png");
    Texture2D playermove2 = LoadTexture("D:\\programs\\c++\\games\\game_5\\player movement\\move2.png");
    Texture2D playerjump = LoadTexture("D:\\programs\\c++\\games\\game_5\\player movement\\jump.png");
    Texture2D playerkick1 = LoadTexture("D:\\programs\\c++\\games\\game_5\\player movement\\kick1.png");
    Texture2D playerkick2 = LoadTexture("D:\\programs\\c++\\games\\game_5\\player movement\\kick2.png");
    Texture2D playerkick3 = LoadTexture("D:\\programs\\c++\\games\\game_5\\player movement\\kick3.png");
    Texture2D playerkick4 = LoadTexture("D:\\programs\\c++\\games\\game_5\\player movement\\kick4.png");
    Texture2D playerkick5 = LoadTexture("D:\\programs\\c++\\games\\game_5\\player movement\\kick5.png");
    Texture2D playerpunch1 = LoadTexture("D:\\programs\\c++\\games\\game_5\\player movement\\punch1.png");
    Texture2D playerpunch2 = LoadTexture("D:\\programs\\c++\\games\\game_5\\player movement\\punch2.png");
    Texture2D playerpunch3 = LoadTexture("D:\\programs\\c++\\games\\game_5\\player movement\\punch3.png");
    Texture2D playerpunch4 = LoadTexture("D:\\programs\\c++\\games\\game_5\\player movement\\punch4.png");
    Texture2D playerpunch5 = LoadTexture("D:\\programs\\c++\\games\\game_5\\player movement\\punch5.png");
    Texture2D playerblock = LoadTexture("D:\\programs\\c++\\games\\game_5\\player movement\\block.png");

    Texture2D cpucrouch = LoadTexture("D:\\programs\\c++\\games\\game_5\\cpu\\crouch.png");
    Texture2D cpustand = LoadTexture("D:\\programs\\c++\\games\\game_5\\cpu\\stand.png");
    Texture2D cpumove1 = LoadTexture("D:\\programs\\c++\\games\\game_5\\cpu\\move 1.png");
    Texture2D cpumove2 = LoadTexture("D:\\programs\\c++\\games\\game_5\\cpu\\move 2.png");
    Texture2D cpujump = LoadTexture("D:\\programs\\c++\\games\\game_5\\cpu\\jump.png");
    Texture2D cpukick1 = LoadTexture("D:\\programs\\c++\\games\\game_5\\cpu\\kick 1.png");
    Texture2D cpukick2 = LoadTexture("D:\\programs\\c++\\games\\game_5\\cpu\\kick 2.png");
    Texture2D cpukick3 = LoadTexture("D:\\programs\\c++\\games\\game_5\\cpu\\kick 3.png");
    Texture2D cpukick4 = LoadTexture("D:\\programs\\c++\\games\\game_5\\cpu\\kick 4.png");
    Texture2D cpukick5 = LoadTexture("D:\\programs\\c++\\games\\game_5\\cpu\\kick 5.png");
    Texture2D cpupunch1 = LoadTexture("D:\\programs\\c++\\games\\game_5\\cpu\\punch 1.png");
    Texture2D cpupunch2 = LoadTexture("D:\\programs\\c++\\games\\game_5\\cpu\\punch 2.png");
    Texture2D cpupunch3 = LoadTexture("D:\\programs\\c++\\games\\game_5\\cpu\\punch 3.png");
    Texture2D cpupunch4 = LoadTexture("D:\\programs\\c++\\games\\game_5\\cpu\\punch 4.png");
    Texture2D cpupunch5 = LoadTexture("D:\\programs\\c++\\games\\game_5\\cpu\\punch 5.png");
    Texture2D cpublock = LoadTexture("D:\\programs\\c++\\games\\game_5\\cpu\\block.png");

    Texture2D background = LoadTexture("D:\\programs\\c++\\games\\game_5\\background.png"); 

    Texture2D flore = LoadTexture("D:\\programs\\c++\\games\\game_5\\flore.jpg"); 

    int frame_counter = 0;
    int kick_frame_counter = 0;
    int punch_frame_counter = 0;
    double cpu_start_delay = 5.0;
    double cpu_start_time = GetTime();

    // CPU AI variables
    enum CpuAction { IDLE, MOVE, PUNCH, KICK, BLOCK, CROUCH, JUMP };
    CpuAction cpu_action_state = IDLE;
    static int cpu_action_duration = 0;
    static int cpu_action_cooldown = 0;
    const int MIN_ACTION_DURATION = 12; // 0.2 seconds at 60 FPS
    const int ACTION_COOLDOWN = 18;    // 0.3 seconds at 60 FPS

    while (!WindowShouldClose()) {
        if (!gameover) {
            distance = cpu.x - player.x;
            float abs_distance = abs(distance);

            if(player.health<=0){
                gameover=true;
                hb=2;
            }
            if(cpu.health<=0){
                gameover=true;
                hb=1;
            }

            frame_counter++;
            if (player.iskicking) kick_frame_counter++;
            if (player.ispunching) punch_frame_counter++;

            // Player input and movement
            if (!IsKeyDown(KEY_S)) player.iscrouch = false;
            if (IsKeyDown(KEY_W) && !player.isJumping && !player.iscrouch) {
                player.isJumping = true;
                player.ismoving = false;
            }
            if (IsKeyDown(KEY_S) && !player.isJumping) {
                player.iscrouch = true;
                player.ismoving = false;
            }
            if (player.isJumping) {
                player.y -= move_y;
                if (player.y <= height - 180 - player.height - 300) {
                    player.isJumping = false;
                }
            }
            if (!player.isJumping && player.y < height - 180 - player.height) {
                player.y += move_y;
            }
            if (IsKeyDown(KEY_A)) {
                player.x -= move_x;
                player.ismoving = true;
            }
            if (IsKeyDown(KEY_D)) {
                player.x += move_x;
                player.ismoving = true;
            }
            if (!IsKeyDown(KEY_A) && !IsKeyDown(KEY_D)) {
                player.ismoving = false;
            }
            if (player.x < 0) player.x = 0;
            if (player.x > width - player.width) player.x = width - player.width;
            if (cpu.x < 0) cpu.x = 0;
            if (cpu.x > width - cpu.width) cpu.x = width - cpu.width;
            if (IsKeyDown(KEY_SPACE)) player.isblocking = true;
            else player.isblocking = false;

            // Player kick actions
            if (IsKeyPressed(KEY_L) && IsKeyDown(KEY_D)) {
                player.kick = 2;
                player.iskicking = true;
                kick_frame_counter = 0;
            } else if (IsKeyPressed(KEY_L) && IsKeyDown(KEY_W)) {
                player.isJumping = false;
                player.kick = 3;
                player.iskicking = true;
                kick_frame_counter = 0;
            } else if (IsKeyPressed(KEY_L) && IsKeyDown(KEY_S)) {
                player.kick = 4;
                player.iskicking = true;
                kick_frame_counter = 0;
            } else if (IsKeyPressed(KEY_L) && IsKeyDown(KEY_A)) {
                player.kick = 5;
                player.iskicking = true;
                kick_frame_counter = 0;
            } else if (IsKeyPressed(KEY_L) && !IsKeyDown(KEY_D)) {
                player.kick = 1;
                player.iskicking = true;
                kick_frame_counter = 0;
            }
            if (kick_frame_counter >= 15) {
                player.kick = 0;
                player.iskicking = false;
                kick_frame_counter = 0;
            }

            // Player punch actions
            if (IsKeyPressed(KEY_K) && IsKeyDown(KEY_D)) {
                player.punch = 2;
                player.ispunching = true;
            } else if (IsKeyPressed(KEY_K) && IsKeyDown(KEY_W)) {
                player.punch = 3;
                player.ispunching = true;
            } else if (IsKeyPressed(KEY_K) && IsKeyDown(KEY_S)) {
                player.punch = 4;
                player.ispunching = true;
            } else if (IsKeyPressed(KEY_K) && IsKeyDown(KEY_A)) {
                player.punch = 5;
                player.ispunching = true;
            } else if (IsKeyPressed(KEY_K) && !IsKeyDown(KEY_D)) {
                player.punch = 1;
                player.ispunching = true;
            }
            if (punch_frame_counter >= 15) {
                player.punch = 0;
                player.ispunching = false;
                punch_frame_counter = 0;
            }

            // Player movement animation
            if (player.ismoving) {
                if (frame_counter >= 13) {
                    if (player.movepossion == 0) player.movepossion = 1;
                    else if (player.movepossion == 1) player.movepossion = 2;
                    else if (player.movepossion == 2) player.movepossion = 1;
                    frame_counter = 0;
                }
                if (IsKeyDown(KEY_A) && !IsKeyDown(KEY_D)) {
                    player.movepossion = player.movepossion == 1 ? 2 : 1;
                }
            }

            // Collision detection
            Rectangle playerRect = { (float)player.x, (float)player.y, (float)player.width, (float)player.height };
            Rectangle cpuRect = { (float)cpu.x, (float)cpu.y, (float)cpu.width, (float)cpu.height };
            bool isColliding = CheckCollisionRecs(playerRect, cpuRect);

            // Damage system
            // Player attacks CPU
            if (isColliding && (player.ispunching || player.iskicking) && (punch_frame_counter == 1 || kick_frame_counter == 1)) {
                int damage = 0;
                if (player.ispunching) {
                    damage = (player.punch == 3 || player.punch == 5) ? 8 : 5; // Special punch: 8, basic punch: 5
                } else if (player.iskicking) {
                    damage = (player.kick == 3 || player.kick == 5) ? 10 : 7; // Special kick: 10, basic kick: 7
                }
                if (cpu.isblocking) {
                    damage = (damage + 1) / 2; // Reduce damage by 50% if CPU is blocking
                }
                cpu.health -= damage;
                if (cpu.health < 0) cpu.health = 0;
            }

            // CPU attacks player
            static int cpu_punch_frame_counter = 0;
            static int cpu_kick_frame_counter = 0;
            if (isColliding && (cpu.ispunching || cpu.iskicking) && (cpu_punch_frame_counter == 1 || cpu_kick_frame_counter == 1)) {
                int damage = 0;
                if (cpu.ispunching) {
                    damage = (cpu.punch == 3 || cpu.punch == 5) ? 8 : 5; // Special punch: 8, basic punch: 5
                } else if (cpu.iskicking) {
                    damage = (cpu.kick == 3 || cpu.kick == 5) ? 10 : 7; // Special kick: 10, basic kick: 7
                }
                if (player.isblocking) {
                    damage = (damage + 1) / 2; // Reduce damage by 50% if player is blocking
                }
                player.health -= damage;
                if (player.health < 0) player.health = 0;
            }

            // CPU can move after delay
            bool cpu_can_move = (GetTime() - cpu_start_time) >= cpu_start_delay;

            // CPU AI: Single action at a time
            float close_distance = 150.0f;
            float medium_distance = 300.0f;

            static int cpu_jump_cooldown = 0;
            static bool cpu_can_jump = true;
            static bool initialized_jump = false;
            if (!initialized_jump) {
                cpu_jump_cooldown = 0;
                cpu_can_jump = true;
                initialized_jump = true;
            }
            if (cpu_jump_cooldown > 0) {
                cpu_jump_cooldown--;
                if (cpu_jump_cooldown == 0) cpu_can_jump = true;
            }

            static int cpu_crouch_frame_counter = 0;

            // Update CPU action
            if (cpu_can_move) {
                // Update action duration and cooldown
                if (cpu_action_duration > 0) {
                    cpu_action_duration--;
                }
                if (cpu_action_cooldown > 0) {
                    cpu_action_cooldown--;
                }

                // Reset to idle when action duration ends
                if (cpu_action_duration == 0 && cpu_action_state != IDLE) {
                    cpu.ismoving = false;
                    cpu.movepossion = 0;
                    cpu.ispunching = false;
                    cpu.punch = 0;
                    cpu.iskicking = false;
                    cpu.kick = 0;
                    cpu.isblocking = false;
                    cpu.iscrouch = false;
                    cpu.isJumping = false;
                    cpu_action_state = IDLE;
                    cpu_action_cooldown = ACTION_COOLDOWN;
                }

                // Select new action when cooldown and duration are zero
                if (cpu_action_duration == 0 && cpu_action_cooldown == 0) {
                    int action_choice = GetRandomValue(0, 99);
                    if (isColliding) {
                        // Close-range actions when colliding
                        if (action_choice < 40) { // 40% block
                            cpu_action_state = BLOCK;
                            cpu.isblocking = true;
                            cpu_action_duration = MIN_ACTION_DURATION;
                        } else if (action_choice < 70) { // 30% punch
                            cpu_action_state = PUNCH;
                            cpu.ispunching = true;
                            cpu.punch = GetRandomValue(1, 5);
                            cpu_action_duration = MIN_ACTION_DURATION + (cpu.punch == 3 || cpu.punch == 5 ? 4 : 0);
                        } else { // 30% kick
                            cpu_action_state = KICK;
                            cpu.iskicking = true;
                            cpu.kick = GetRandomValue(1, 5);
                            cpu_action_duration = MIN_ACTION_DURATION + (cpu.kick == 3 ? 6 : cpu.kick == 5 ? 4 : 2);
                        }
                    } else if (abs_distance < close_distance) {
                        // Close range: mix of attacks and defensive moves
                        if (action_choice < 20) { // 20% block
                            cpu_action_state = BLOCK;
                            cpu.isblocking = true;
                            cpu_action_duration = MIN_ACTION_DURATION;
                        } else if (action_choice < 40) { // 20% punch
                            cpu_action_state = PUNCH;
                            cpu.ispunching = true;
                            cpu.punch = GetRandomValue(1, 5);
                            cpu_action_duration = MIN_ACTION_DURATION + (cpu.punch == 3 || cpu.punch == 5 ? 4 : 0);
                        } else if (action_choice < 60) { // 20% kick
                            cpu_action_state = KICK;
                            cpu.iskicking = true;
                            cpu.kick = GetRandomValue(1, 5);
                            cpu_action_duration = MIN_ACTION_DURATION + (cpu.kick == 3 ? 6 : cpu.kick == 5 ? 4 : 2);
                        } else if (action_choice < 80 && cpu_can_jump) { // 20% jump
                            cpu_action_state = JUMP;
                            cpu.isJumping = true;
                            cpu_can_jump = false;
                            cpu_jump_cooldown = 24;
                            cpu_action_duration = MIN_ACTION_DURATION + 6;
                        } else { // 20% crouch
                            cpu_action_state = CROUCH;
                            cpu.iscrouch = true;
                            cpu_action_duration = MIN_ACTION_DURATION;
                        }
                    } else if (abs_distance < medium_distance) {
                        // Medium range: move or attack
                        if (action_choice < 60) { // 60% move
                            cpu_action_state = MOVE;
                            cpu.ismoving = true;
                            cpu.movepossion = 1;
                            cpu_action_duration = MIN_ACTION_DURATION + 6;
                        } else if (action_choice < 80) { // 20% punch
                            cpu_action_state = PUNCH;
                            cpu.ispunching = true;
                            cpu.punch = GetRandomValue(1, 5);
                            cpu_action_duration = MIN_ACTION_DURATION + (cpu.punch == 3 || cpu.punch == 5 ? 4 : 0);
                        } else { // 20% kick
                            cpu_action_state = KICK;
                            cpu.iskicking = true;
                            cpu.kick = GetRandomValue(1, 5);
                            cpu_action_duration = MIN_ACTION_DURATION + (cpu.kick == 3 ? 6 : cpu.kick == 5 ? 4 : 2);
                        }
                    } else {
                        // Far range: mostly move
                        if (action_choice < 80) { // 80% move
                            cpu_action_state = MOVE;
                            cpu.ismoving = true;
                            cpu.movepossion = 1;
                            cpu_action_duration = MIN_ACTION_DURATION + 6;
                        } else if (action_choice < 90) { // 10% punch
                            cpu_action_state = PUNCH;
                            cpu.ispunching = true;
                            cpu.punch = GetRandomValue(1, 5);
                            cpu_action_duration = MIN_ACTION_DURATION + (cpu.punch == 3 || cpu.punch == 5 ? 4 : 0);
                        } else { // 10% kick
                            cpu_action_state = KICK;
                            cpu.iskicking = true;
                            cpu.kick = GetRandomValue(1, 5);
                            cpu_action_duration = MIN_ACTION_DURATION + (cpu.kick == 3 ? 6 : cpu.kick == 5 ? 4 : 2);
                        }
                    }
                }
            } else {
                // Before CPU can move, remain idle
                cpu_action_state = IDLE;
                cpu.ismoving = false;
                cpu.movepossion = 0;
                cpu.ispunching = false;
                cpu.punch = 0;
                cpu.iskicking = false;
                cpu.kick = 0;
                cpu.isblocking = false;
                cpu.iscrouch = false;
                cpu.isJumping = false;
            }

            // CPU jumping physics
            if (cpu.isJumping) {
                cpu.y -= move_y;
                if (cpu.y <= height - 180 - cpu.height - 300) {
                    cpu.isJumping = false;
                    cpu.y = height - 180 - cpu.height;
                }
            }
            if (!cpu.isJumping && cpu.y < height - 180 - cpu.height) {
                cpu.y += move_y;
            }

            // CPU movement logic
            bool cpu_moving_backward = false;
            if (cpu.ismoving && cpu_action_state == MOVE) {
                static int cpu_move_delay = 0;
                cpu_move_delay++;
                if (cpu_move_delay >= 2) {
                    if (cpu.x < player.x && !isColliding && cpu.x < width - cpu.width) {
                        cpu.x += move_x; // Move right towards player
                    } else if (cpu.x > player.x && !isColliding && cpu.x > 0) {
                        cpu.x -= move_x; // Move left towards player
                    }
                    cpu_move_delay = 0;
                }
                if (frame_counter >= 13) {
                    if (cpu.movepossion == 1) cpu.movepossion = 2;
                    else cpu.movepossion = 1;
                    frame_counter = 0;
                }
                // Set cpu_moving_backward
                if ((cpu.x < player.x && cpu.x > 0 && cpu.x - player.x < 0) || 
                    (cpu.x > player.x && cpu.x < width - cpu.width && cpu.x - player.x > 0)) {
                    cpu_moving_backward = true;
                }
            }

            // CPU punch animation timer
            if (cpu.ispunching) {
                cpu_punch_frame_counter++;
                if (cpu_punch_frame_counter >= (cpu.punch == 3 || cpu.punch == 5 ? 16 : 10)) {
                    cpu.ispunching = false;
                    cpu.punch = 0;
                    cpu_punch_frame_counter = 0;
                }
            }

            // CPU kick animation timer
            if (cpu.iskicking) {
                cpu_kick_frame_counter++;
                int kick_duration = (cpu.kick == 3 ? 12 : cpu.kick == 5 ? 10 : 8);
                if (cpu_kick_frame_counter >= kick_duration) {
                    cpu.iskicking = false;
                    cpu.kick = 0;
                    cpu_kick_frame_counter = 0;
                }
            }

            // CPU crouch timer
            if (cpu.iscrouch) {
                cpu_crouch_frame_counter++;
                int crouch_duration = (cpu.ispunching || cpu.iskicking) ? 18 : 12;
                if (cpu_crouch_frame_counter >= crouch_duration) {
                    cpu.iscrouch = false;
                    cpu_crouch_frame_counter = 0;
                }
            } else {
                cpu_crouch_frame_counter = 0;
            }

            // Player movement with collision
            static int player_move_delay = 0;
            player_move_delay++;
            bool can_move_player = (player_move_delay >= 2);
            if (can_move_player) {
                if (IsKeyDown(KEY_A) && (!isColliding || player.x > cpu.x)) {
                    player.x -= move_x;
                }
                if (IsKeyDown(KEY_D) && (!isColliding || player.x < cpu.x)) {
                    player.x += move_x;
                }
                player_move_delay = 0;
            }

            // Rendering
            BeginDrawing();
            ClearBackground(RAYWHITE);

            DrawTexture(background, 0, 0, WHITE);
            DrawTexture(flore, 0, flore_y, WHITE);

            // Draw health bars
            // Player health bar (top-left)
            DrawRectangle(10, 10, 200, 20, RED); // Background
            DrawRectangle(10, 10, (player.health * 200) / MAX_HEALTH, 20, GREEN); // Health
            DrawText("Player", 10, 35, 20, BLACK);
            // CPU health bar (top-right)
            DrawRectangle(width - 210, 10, 200, 20, RED); // Background
            DrawRectangle(width - 210, 10, (cpu.health * 200) / MAX_HEALTH, 20, GREEN); // Health
            DrawText("CPU", width - 210, 35, 20, BLACK);

            if (player.iscrouch) {
                DrawTexture(playercrouch, player.x, player.y + 130, WHITE);
            } else if (player.isJumping) {
                DrawTexture(playerjump, player.x, player.y, WHITE);
            } else {
                if (player.kick == 1) {
                    DrawTexture(playerkick1, player.x, player.y, WHITE);
                } else if (player.kick == 2) {
                    DrawTexture(playerkick2, player.x, player.y, WHITE);
                } else if (player.kick == 3) {
                    DrawTexture(playerkick3, player.x, player.y - 100, WHITE);
                } else if (player.kick == 4) {
                    DrawTexture(playerkick4, player.x, player.y + 100, WHITE);
                } else if (player.kick == 5) {
                    DrawTexture(playerkick5, player.x, player.y, WHITE);
                } else if (player.isblocking) {
                    DrawTexture(playerblock, player.x, player.y, WHITE);
                } else if (player.ispunching) {
                    if (player.punch == 1) {
                        DrawTexture(playerpunch1, player.x, player.y, WHITE);
                    } else if (player.punch == 2) {
                        DrawTexture(playerpunch2, player.x, player.y, WHITE);
                    } else if (player.punch == 3) {
                        DrawTexture(playerpunch3, player.x, player.y - 100, WHITE);
                    } else if (player.punch == 4) {
                        DrawTexture(playerpunch4, player.x, player.y + 100, WHITE);
                    } else if (player.punch == 5) {
                        DrawTexture(playerpunch5, player.x, player.y, WHITE);
                    }
                } else {
                    if (player.ismoving && !player.isJumping) {
                        if (IsKeyDown(KEY_A) && !IsKeyDown(KEY_D)) {
                            if (player.movepossion == 1) {
                                DrawTexture(playermove2, player.x, player.y, WHITE);
                            } else {
                                DrawTexture(playermove1, player.x, player.y, WHITE);
                            }
                        } else {
                            if (player.movepossion == 1) {
                                DrawTexture(playermove1, player.x, player.y, WHITE);
                            } else if (player.movepossion == 2) {
                                DrawTexture(playermove2, player.x, player.y, WHITE);
                            }
                        }
                    } else if (IsKeyDown(KEY_S)) {
                        DrawTexture(playercrouch, player.x, player.y + 130, WHITE);
                    } else {
                        DrawTexture(playerstand, player.x, player.y, WHITE);
                    }
                }
            }

            if (cpu.isJumping) {
                DrawTexture(cpujump, cpu.x, cpu.y, WHITE);
            } else if (cpu.ismoving && !cpu.isJumping) {
                if (cpu_moving_backward) {
                    if (cpu.movepossion == 1) {
                        DrawTexture(cpumove2, cpu.x, cpu.y, WHITE);
                    } else {
                        DrawTexture(cpumove1, cpu.x, cpu.y, WHITE);
                    }
                } else {
                    if (cpu.movepossion == 1) {
                        DrawTexture(cpumove1, cpu.x, cpu.y, WHITE);
                    } else if (cpu.movepossion == 2) {
                        DrawTexture(cpumove2, cpu.x, cpu.y, WHITE);
                    }
                }
            } else if (cpu.isblocking) {
                DrawTexture(cpublock, cpu.x, cpu.y, WHITE);
            } else if (cpu.ispunching) {
                if (cpu.punch == 1) {
                    DrawTexture(cpupunch1, cpu.x, cpu.y, WHITE);
                } else if (cpu.punch == 2) {
                    DrawTexture(cpupunch2, cpu.x, cpu.y, WHITE);
                } else if (cpu.punch == 3) {
                    DrawTexture(cpupunch3, cpu.x, cpu.y - 100, WHITE);
                } else if (cpu.punch == 4) {
                    DrawTexture(cpupunch4, cpu.x, cpu.y + 100, WHITE);
                } else if (cpu.punch == 5) {
                    DrawTexture(cpupunch5, cpu.x, cpu.y, WHITE);
                }
            } else if (cpu.iskicking) {
                if (cpu.kick == 1) {
                    DrawTexture(cpukick1, cpu.x, cpu.y, WHITE);
                } else if (cpu.kick == 2) {
                    DrawTexture(cpukick2, cpu.x, cpu.y, WHITE);
                } else if (cpu.kick == 3) {
                    DrawTexture(cpukick3, cpu.x, cpu.y - 100, WHITE);
                } else if (cpu.kick == 4) {
                    DrawTexture(cpukick4, cpu.x, cpu.y + 100, WHITE);
                } else if (cpu.kick == 5) {
                    DrawTexture(cpukick5, cpu.x, cpu.y, WHITE);
                }
            } else if (cpu.iscrouch) {
                DrawTexture(cpucrouch, cpu.x, cpu.y + 130, WHITE);
            } else {
                DrawTexture(cpustand, cpu.x, cpu.y, WHITE);
            }
        }
        else if(gameover) {
            if (hb == 1) {
                DrawText("You Wins!", width / 2 - 200, height / 2 - 20, 100,GREEN);
            } else if (hb == 2) {
                DrawText("CPU Wins!", width / 2 - 200, height / 2 - 20, 100,RED);
        }
    }
        EndDrawing();
    }

    // Unload textures
    UnloadTexture(playerstand);
    UnloadTexture(playermove1);
    UnloadTexture(playermove2);
    UnloadTexture(playerjump);
    UnloadTexture(playerkick1);
    UnloadTexture(playerkick2);
    UnloadTexture(playerkick3);
    UnloadTexture(playerkick4);
    UnloadTexture(playerkick5);
    UnloadTexture(playerpunch1);
    UnloadTexture(playerpunch2);
    UnloadTexture(playerpunch3);
    UnloadTexture(playerpunch4);
    UnloadTexture(playerpunch5);
    UnloadTexture(playerblock);
    UnloadTexture(playercrouch);
    UnloadTexture(cpustand);
    UnloadTexture(cpumove1);
    UnloadTexture(cpumove2);
    UnloadTexture(cpujump);
    UnloadTexture(cpukick1);
    UnloadTexture(cpukick2);
    UnloadTexture(cpukick3);
    UnloadTexture(cpukick4);
    UnloadTexture(cpukick5);
    UnloadTexture(cpupunch1);
    UnloadTexture(cpupunch2);
    UnloadTexture(cpupunch3);
    UnloadTexture(cpupunch4);
    UnloadTexture(cpupunch5);
    UnloadTexture(cpublock);
    UnloadTexture(cpucrouch);

    UnloadTexture(background);

    UnloadTexture(flore);

    CloseWindow();
    return 0;
}