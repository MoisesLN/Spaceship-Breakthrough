import pygame
import sys

pygame.init()

LARGURA = 600 
ALTURA = 720
FPS = 60

play_button = pygame.image.load("game/sprites/botões/play.png")
exit_button = pygame.image.load("game/sprites/botões/exit.png")
play_button_hover = pygame.image.load("game/sprites/botões/play-hover.png")
exit_button_hover = pygame.image.load("game/sprites/botões/exit-hover.png")

play_button = pygame.transform.scale(play_button, (190, 80))
exit_button = pygame.transform.scale(exit_button, (190, 80))
play_button_hover = pygame.transform.scale(play_button_hover, (190, 80))
exit_button_hover = pygame.transform.scale(exit_button_hover, (190, 80))

pygame.display.set_caption("Robot Defense - Template")

class Button:
    def __init__(self, rect, default_image, highlight_image, callback):
        self.rect = rect
        self.default_image = default_image
        self.highlight_image = highlight_image
        self.callback = callback     
        
    def draw(self, surface, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            surface.blit(self.highlight_image, self.rect)
        else:
            surface.blit(self.default_image, self.rect)

    def check_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.callback()


class Menu:
    def __init__(self):
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        self.fundo_menu = pygame.image.load("game/sprites/background_menu.png")
    
        mid_x = LARGURA // 2
        start_y = ALTURA // 2 
        gap = 100
        
        BUTTON_LARGURA = 190
        BUTTON_ALTURA = 80

        self.buttons = [ 
            Button(
                rect=pygame.Rect(mid_x - BUTTON_LARGURA // 2, start_y + 60, BUTTON_LARGURA, BUTTON_ALTURA), 
                default_image=play_button, 
                highlight_image=play_button_hover, 
                callback=self.start_game
            ),
            Button(
                rect=pygame.Rect(mid_x - BUTTON_LARGURA // 2, start_y + gap + 60, BUTTON_LARGURA, BUTTON_ALTURA),
                default_image=exit_button, 
                highlight_image=exit_button_hover, 
                callback=self.exit_game
            ),
        ]
        self.running = True

    def start_game(self):
        self.running = False

    def exit_game(self):
        pygame.quit()
        sys.exit()

    def run(self):
        clock = pygame.time.Clock()
        self.tela.blit(self.fundo_menu, (0,0))
        while self.running:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for btn in self.buttons:
                        btn.check_click(mouse_pos)

            self.tela.blit(self.fundo_menu, (0,0))
            for btn in self.buttons:
                btn.draw(self.tela, mouse_pos)

            pygame.display.flip()
            clock.tick(FPS)