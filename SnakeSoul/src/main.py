import os
import pygame
import random
import colors
from grid import Grid
from snake import Snake
from button import Button
from hawk import Hawk
from bar import Bar

# pygame setup
pygame.init()
WIDTH, HEIGHT = 720, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SnakeSoul")
clock = pygame.time.Clock()

def timer(t):
    min = t//60
    sec = t%60
    return f"{(min//10)%10}{min%10}:{(sec//10)%10}{sec%10}"

def gaussian_blur(surface, radius):
    scaled_surface = pygame.transform.smoothscale(surface, (surface.get_width() // radius, surface.get_height() // radius))
    scaled_surface = pygame.transform.smoothscale(scaled_surface, (surface.get_width(), surface.get_height()))
    return scaled_surface

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/vinque.otf", size)

def display_text(surface, text, pos, font, color):
    collection = [word.split(' ') for word in text.splitlines()]
    space = font.size(' ')[0]
    x,y = pos
    for lines in collection:
        for words in lines:
            word_surface = font.render(words, True, color)
            word_width , word_height = word_surface.get_size()
            if x + word_width >= WIDTH:
                x = pos[0]
                y += word_height
            surface.blit(word_surface, (x,y))
            x += word_width + space
        x = pos[0]
        y += word_height

def tutorial():
    TUTORIAL_TEXT = "Welcome to SnakeSoul!\n\n"\
                    "Your goal is to defeat the Magic Hawk before it defeats you!\n\n"\
                    "How to play:\n"\
                    "- Use WASD to move the snake\n"\
                    "- There are 3 types of apples:\n"\
                    "   + NormalApples(Red): Gain length and damage the Magic Hawk\n"\
                    "   + GoldenApples(Yellow): Gain length, lives and cause severe damage to the Magic Hawk\n"\
                    "   + PoisonApples(Gray): Shorten the snake and heal the Magic Hawk\n\n"\
                    "Sometimes the Magic Hawk will shoot Fireball(Purple). If they touch you, you will decay and the Magic Hawk will heal up.\n\n"\
                    "At night, there will be more Fireballs and there are no GoldenApples.\n\n"\
                    "You have 3 lives. You will lose a live if you run into a Fireball, run out of border or run into yourself.\n"\
                    "If you are out of lives, the game will be over.\n"
    font = get_font(30)

    QUIT_BUTTON = Button(pos=(WIDTH//2, 1000), text_input="MAIN MENU", font=get_font(75), base_color=colors.white, hovering_color=colors.gray)
    
    instruction = 3
    running = True
    while running:
        screen.fill(colors.black)

        display_text(screen, TUTORIAL_TEXT, (20, 20), font, colors.white)

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        QUIT_BUTTON.changeColor(MENU_MOUSE_POS)
        QUIT_BUTTON.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    instruction = 0
                    running = False

        pygame.display.update()

    return instruction



def victory(game_time):
    MENU_TEXT = get_font(50).render("VICTORY", True, colors.dark_yellow)
    MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH//2, 400))

    TIME_TEXT = get_font(50).render(f"Time taken: {game_time}", True, colors.white)
    TIME_RECT = TIME_TEXT.get_rect(center=(WIDTH//2, 600))

    QUIT_BUTTON = Button(pos=(WIDTH//2, 800), text_input="MAIN MENU", font=get_font(75), base_color=colors.white, hovering_color=colors.dark_green)

    instruction = 2
    running = True
    while running:
        screen.fill(colors.black)

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        screen.blit(MENU_TEXT, MENU_RECT)
        screen.blit(TIME_TEXT, TIME_RECT)

        QUIT_BUTTON.changeColor(MENU_MOUSE_POS)
        QUIT_BUTTON.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    instruction = 0
                    running = False
        pygame.display.update()

    return instruction

def game_over():
    MENU_TEXT = get_font(80).render("GAME OVER", True, colors.dark_yellow)
    MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH//2, 400))

    QUIT_BUTTON = Button(pos=(WIDTH//2, 600), text_input="MAIN MENU", font=get_font(75), base_color=colors.white, hovering_color=colors.dark_green)

    instruction = 2
    running = True
    while running:
        screen.fill(colors.black)

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        screen.blit(MENU_TEXT, MENU_RECT)

        QUIT_BUTTON.changeColor(MENU_MOUSE_POS)
        QUIT_BUTTON.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    instruction = 0
                    running = False
        pygame.display.update()

    return instruction

def pause():
    MENU_TEXT = get_font(80).render("SnakeSoul", True, colors.dark_yellow)
    MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH//2, 400))

    RESUME_BUTTON = Button(pos=(WIDTH//2, 600), text_input="RESUME", font=get_font(75), base_color=colors.white, hovering_color=colors.gray)
    QUIT_BUTTON = Button(pos=(WIDTH//2, 800), text_input="MAIN MENU", font=get_font(75), base_color=colors.white, hovering_color=colors.gray)

    instruction = 0
    running = True
    while running:
        screen.fill(colors.black)

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [RESUME_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if RESUME_BUTTON.checkForInput(MENU_MOUSE_POS):
                    instruction = 0
                    running = False
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    instruction = 1
                    running = False
        pygame.display.update()

    return instruction

def menu():
    imgFile = f"bg{random.randint(1,3)}.jpg"
    bg = pygame.transform.scale(pygame.image.load(os.path.join("assets", imgFile)), (WIDTH, HEIGHT))

    instruction = 0
    running = True
    while running:
        screen.fill(colors.black)

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(80).render("SnakeSoul", True, colors.dark_yellow)
        MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH//2, 200))

        PLAY_BUTTON = Button(pos=(WIDTH//2, 400), text_input="PLAY", font=get_font(75), base_color=colors.white, hovering_color=colors.gray)
        OPTIONS_BUTTON = Button(pos=(WIDTH//2, 600), text_input="TUTORIAL", font=get_font(75), base_color=colors.white, hovering_color=colors.gray)
        QUIT_BUTTON = Button(pos=(WIDTH//2, 800), text_input="QUIT", font=get_font(75), base_color=colors.white, hovering_color=colors.gray)

        screen.blit(gaussian_blur(bg, 5), (0, 0))
        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    instruction = 1
                    running = False
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    instruction = 3
                    running = False
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    instruction = -1
                    running = False
        pygame.display.update()
    return instruction


def play():
    dt = 0
    prev_game_time = 0
    game_time = 0
    updated_time = 0
    clock.tick(60)

    DAYTIME = 60
    is_day = True

    day = pygame.transform.scale(pygame.image.load(os.path.join("assets", "day_sky.jpg")), (WIDTH, 360))
    night = pygame.transform.scale(pygame.image.load(os.path.join("assets", "night_sky.jpg")), (WIDTH, 360))
    grass = pygame.transform.scale(pygame.image.load(os.path.join("assets", "grass.jpg")), (WIDTH, HEIGHT-360))
    grass2 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "grass2.jpg")), (WIDTH, HEIGHT-360))
    hawk_img = pygame.transform.scale(pygame.image.load(os.path.join("assets", "hawk.png")).convert_alpha(), (200, 210))
    full_heart = pygame.transform.scale(pygame.image.load(os.path.join("assets", "full_heart.png")).convert_alpha(), (50, 50))
    empty_heart = pygame.transform.scale(pygame.image.load(os.path.join("assets", "empty_heart.png")).convert_alpha(), (50, 50))


    font = get_font(60)
    game_title = font.render("SnakeSoul", True, colors.dark_yellow)
    title_rect = game_title.get_rect(center=(150, 50))

    SHAPE = [18, 18]
    grid = Grid(0, 360, WIDTH, HEIGHT, SHAPE, get_font(30))

    snake = Snake(SHAPE[0]//2, SHAPE[1]//2, 3)
    dir = snake.getDirection()
    isDirUpdated = False

    hawk = Hawk(grid.getShape())
    hawk.spawn_apple("apple", snake.get_segments_pos(), game_time)
    
    health_bar = Bar(200, 300, 500, 30, colors.red, colors.gray, hawk.MAX_HEALTH)

    instruction = 1
    while True:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            response = pause()
            if response:
                instruction = 0
                break
            clock.tick(60)

        if not isDirUpdated:
            newDir = dir
            if keys[pygame.K_w]:
                newDir = -2
            elif keys[pygame.K_s]:
                newDir = 2
            elif keys[pygame.K_a]:
                newDir = -1
            elif keys[pygame.K_d]:
                newDir = 1
            if newDir != dir:
                isDirUpdated = True
                dir = newDir

        # Day-time switch
        if int(game_time) % DAYTIME == 0 and updated_time:
            is_day = not is_day

        # Game events
        if updated_time:
            if is_day:
                if game_time >= 15 and int(game_time) % 15 in range(5):
                    hawk.spawn_fireball()
                if game_time >= 30 and int(game_time) % 30 == 0:
                    hawk.spawn_apple("golden_apple", snake.get_segments_pos(), game_time)
            else:
                if game_time >= 15 and int(game_time) % 15 in range(10):
                    hawk.spawn_fireball()
            if game_time >= 20 and int(game_time) % 20 in range(10):
                hawk.spawn_apple("poison_apple", snake.get_segments_pos(), game_time)
            for apple in hawk.get_apples():
                if apple.get_type() in ["golden_apple", "poison_apple"]:
                    if apple.is_timeup(game_time):
                        hawk.remove_apple(apple)

        # Snake movement
        if snake.is_move(dt):
            snake.update_pos(dir)
            index = snake.collide(hawk.get_apple_pos())
            if index != -1:
                type = hawk.pop_apple(index)
                if type == "apple":
                    snake.grow()
                    hawk.damage(100)
                    hawk.spawn_apple("apple", snake.get_segments_pos(), game_time)
                elif type == "golden_apple":
                    snake.gain_live()
                    hawk.damage(500)
                    snake.move()
                else:
                    hawk.heal(20)
                    snake.decay(-1)
                    snake.move()
            elif grid.checkBounderies(snake.get_head()):
                snake = Snake(SHAPE[0]//2, SHAPE[1]//2, snake.get_lives()-1)
                hawk.reset_mob()
            elif snake.self_collide():
                snake.lose_live()
            else:
                snake.move()
            isDirUpdated = False


        # Mobs movement
        hawk.update(dt)
        for mob in hawk.get_mobs():
            if grid.checkBounderies(mob.get_pos()):
                hawk.remove_mob(mob)
            index = mob.collide(snake.get_segments_pos())
            if index != -1:
                l = snake.decay(index)
                hawk.heal(50*l)
                hawk.remove_mob(mob)

        # End game
        if snake.is_dead():
            instruction = 2
            break
        if hawk.is_dead():
            victory(timer(int(game_time)))
            instruction = 0
            break

        # Adding to grid
        grid.reset()
        for s in snake.getSegments():
            grid.addObject(s.get_x(), s.get_y(), s.get_type(), s.get_color())
        for a in hawk.get_apples():
            grid.addObject(a.get_x(), a.get_y(), a.get_type(), a.get_color(), a.get_time(game_time))
        for mob in hawk.get_mobs():
            grid.addObject(mob.get_x(), mob.get_y(), mob.get_type(), mob.get_color())

        # Updating UI
        timer_str = font.render(timer(int(game_time)), True, colors.white)
        timer_rect = timer_str.get_rect(center=(WIDTH-100, 50))

        health_bar.set_val(hawk.get_health())

        # Drawing
        screen.fill(colors.black)
        if is_day:
            screen.blit(day, (0, 0))
            screen.blit(grass, (0, 360))
        else:
            screen.blit(night, (0, 0))
            screen.blit(grass2, (0, 360))
        grid.draw(screen)
        screen.blit(game_title, title_rect)
        screen.blit(timer_str, timer_rect)
        screen.blit(hawk_img, (0, 160))

        health_bar.draw(screen)

        for i in range(3, 0, -1):
            screen.blit((full_heart if i <= snake.get_lives() else empty_heart), (WIDTH-20-50*i, 100))

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-independent physics.
        dt = clock.tick(60) / 1000
        print(dt)
        game_time += dt
        updated_time = int(game_time) - int(prev_game_time)
        prev_game_time = game_time

    return instruction

def main():
    if __name__ == "__main__":
        instruction = 0
        while instruction != -1:
            if instruction == 0:
                instruction = menu()
            elif instruction == 1:
                instruction = play()
            elif instruction == 2:
                instruction = game_over()
            elif instruction == 3:
                instruction = tutorial()
        pygame.quit()

main()
