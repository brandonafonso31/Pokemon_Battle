import os,sys,pygame
from config import *
from button_test import Button_test

#------|Init pygame
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
dt = 0

#------|Resolution
res_scene = (1050,540)
window = pygame.display.set_mode(res_scene)
pygame.display.set_caption(project_name)
pygame.display.set_icon(pygame.image.load(os.path.join(img_dir_path,"sys/logo.png")))

#------|Fonts
font = pygame.font.SysFont("arialblack",40)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    window.blit(img, (x, y))

def create_button(text,x,y):
    button_img_path = os.path.join(img_dir_path,f"battle_ui/move_button.png")
    button_img = pygame.image.load(button_img_path).convert_alpha()
    return Button_test(x, y, button_img, 1, text)

def fps_counter():
    fps = str(int(clock.get_fps()))
    fps_t = font.render(f"{fps} fps" , 1, pygame.Color("RED"))
    window.blit(fps_t,(0,0))
    
#------|Button
PLAY_BUTTON = create_button("Play", 200 ,200)
OPTIONS_BUTTON = create_button("Options", 200,300)
BACK_BUTTON = create_button("Back", 200,400)
QUIT_BUTTON = create_button("Quit", 200,400)

#------|Var
y_menu = res_scene[1] + 50
x_menu = 50
BACKGROUND_INTRO = pygame.image.load(os.path.join(sys_dir_path,"intro.jpg"))
BACKGROUND_LENTH,BACKGROUND_HEIGHT = BACKGROUND_INTRO.get_size()
ratio = res_scene[1] / BACKGROUND_HEIGHT
scale = (BACKGROUND_LENTH*ratio,BACKGROUND_HEIGHT*ratio)
BACKGROUND_INTRO = pygame.transform.scale(BACKGROUND_INTRO,scale)

#------|function
def play():
    run = True
    while run :
        dt = clock.tick(30)
        window.fill(BLACK)        
        window.blit(BACKGROUND_INTRO,(0,0))
        fps_counter()
        
        pos = pygame.mouse.get_pos()
        draw_text("PLAY", font, "#b68f40", res_scene[0]//2 + 200, res_scene[1]//2)

        for button in [BACK_BUTTON]:
            button.draw(window)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if BACK_BUTTON.handle_event(event):
                run = False

        pygame.display.flip()

def options():
    run = True
    while run :
        dt = clock.tick(30)
        window.fill(BLACK)        
        window.blit(BACKGROUND_INTRO,(0,0))
        fps_counter()
        
        pos = pygame.mouse.get_pos()
        draw_text("OPTIONS", font, "#b68f40", res_scene[0]//2 + 200, res_scene[1]//2)

        for button in [BACK_BUTTON]:
            button.draw(window)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if BACK_BUTTON.handle_event(event):
                run = False

        pygame.display.flip()

def main_menu():
    run = True
    while run :
        dt = clock.tick(30)
        window.fill(BLACK)        
        window.blit(BACKGROUND_INTRO,(0,0))
        fps_counter()
        
        draw_text(project_name, font, "#b68f40", res_scene[0]//2 + 200, res_scene[1]//2 - 100)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.draw(window)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if PLAY_BUTTON.handle_event(event):
                play()
            if OPTIONS_BUTTON.handle_event(event):
                options()
            if QUIT_BUTTON.handle_event(event):
                pygame.quit()
                sys.exit()

        pygame.display.flip()

main_menu()