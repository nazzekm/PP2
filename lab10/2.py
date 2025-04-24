import pygame
import sys
import random
import psycopg2

conn = psycopg2.connect(
    host="localhost", dbname="lab10", user="postgres", password="12345678", port="5432"
)
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL
    );
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS user_score (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        score INTEGER,
        level INTEGER
    )
""")
conn.commit()

# пользователь
def get_or_create_user():
    username = input("Enter your username: ").strip()

    # существует?
    cur.execute("SELECT id FROM users WHERE username = %s", (username,))
    user = cur.fetchone()

    if user:
        print(f"Welcome back, {username}!")
        return user[0]  
    else:
        cur.execute("INSERT INTO users (username) VALUES (%s) RETURNING id", (username,))
        user_id = cur.fetchone()[0]
        conn.commit()
        print(f"Hello, {username}! You have been registered.")
        return user_id

def insert_score(user_id, score, level):
    cur.execute("INSERT INTO user_score (user_id, score, level) VALUES (%s, %s, %s)", (user_id, score, level))
    conn.commit()

def show_scores():
    cur.execute("SELECT username, score, level FROM user_score "
                "JOIN users ON users.id = user_score.user_id ORDER BY score DESC LIMIT 10")
    rows = cur.fetchall()
    print("\n=== Top 10 Scores ===")
    for row in rows:
        print(f"{row[0]} - Score: {row[1]} | Level: {row[2]}")

def play_game():
    pygame.init()
    SCREEN_WIDTH, SCREEN_HEIGHT = 600, 400
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)

    snake_pos = [[100, 50], [90, 50], [80, 50]]
    snake_speed = [10, 0]
    food = {'pos': [0, 0], 'weight': 1}
    food_spawn = True
    score = 0
    level = 1
    speed_increase = 0.5
    food_counter = 0
    fps = pygame.time.Clock()
    paused = False

    user_id = get_or_create_user()

    def check_collision(pos):
        if pos[0] < 0 or pos[0] >= SCREEN_WIDTH:
            return True
        if pos in snake_pos[1:]:
            return True
        return False

    def get_random_food():
        nonlocal food_counter
        while True:
            pos = [random.randrange(1, (SCREEN_WIDTH // 10)) * 10,
                   random.randrange(1, (SCREEN_HEIGHT // 10)) * 10]
            if pos not in snake_pos:
                weight = 2 if food_counter >= 2 else 1
                food_counter = 0 if weight == 2 else food_counter + 1
                return {'pos': pos, 'weight': weight}

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_speed[1] == 0:
                    snake_speed = [0, -10]
                elif event.key == pygame.K_DOWN and snake_speed[1] == 0:
                    snake_speed = [0, 10]
                elif event.key == pygame.K_LEFT and snake_speed[0] == 0:
                    snake_speed = [-10, 0]
                elif event.key == pygame.K_RIGHT and snake_speed[0] == 0:
                    snake_speed = [10, 0]
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_s and paused:  
                    insert_score(user_id, score, level)
                    print(f"[✔] Score saved: {score} (Level {level})")

        if not paused:
            snake_pos.insert(0, [snake_pos[0][0] + snake_speed[0], snake_pos[0][1] + snake_speed[1]])
            if check_collision(snake_pos[0]):
                insert_score(user_id, score, level)

                screen.fill(BLACK)
                font_big = pygame.font.SysFont('arial', 50)
                game_over_text = font_big.render("GAME OVER", True, RED)
                screen.blit(game_over_text, [SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 - 25])
                pygame.display.flip()
                pygame.time.delay(2000)
                pygame.quit()

                print("\n===== GAME OVER =====")
                print(f"Player: {user_id} | Score: {score} | Level: {level}\n")
                show_scores() 
                return

            if snake_pos[0] == food['pos']:
                score += food['weight']
                if score % 3 == 0:
                    level += 1
                food_spawn = True
            else:
                snake_pos.pop()

            if food_spawn:
                food = get_random_food()
                food_spawn = False

        screen.fill(BLACK)
        for pos in snake_pos:
            pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))

        pygame.draw.rect(screen, RED, pygame.Rect(food['pos'][0], food['pos'][1], 10, 10))

        font = pygame.font.SysFont('arial', 20)
        score_text = font.render(f"Score: {score} Level: {level}", True, (255, 255, 255))
        screen.blit(score_text, [0, 0])

        if paused:
            pause_text = font.render("Paused", True, (255, 255, 255))
            screen.blit(pause_text, [SCREEN_WIDTH // 2 - 30, SCREEN_HEIGHT // 2])

        pygame.display.flip()
        fps.tick(10 + level * speed_increase)

def menu():
    while True:
        print("""
        === SNAKE GAME MENU ===
        [p] Play Game
        [r] Show Top Ratings
        [f] Finish
        """)
        cmd = input("Choose command: ").lower()

        if cmd == "p":
            play_game()
        elif cmd == "r":
            show_scores() 
        elif cmd == "f":
            break

menu()
cur.close()
conn.close()
