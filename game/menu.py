import pygame
import sys

pygame.init()

LARGURA = 600 
ALTURA = 720
FPS = 60

imagem1 = pygame.image.load("game/sprites/botões/play_teste.png")
imagem2 = pygame.image.load("game/sprites/botões/exit_teste.png")

imagem1 = pygame.transform.scale(imagem1, (190, 80))
imagem2 = pygame.transform.scale(imagem2, (190, 80))

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
        self.fundo_menu = pygame.Surface((LARGURA, ALTURA))
        self.fundo_menu.fill((0, 0, 0)) 
    
        mid_x = LARGURA // 2
        start_y = ALTURA // 2 
        gap = 100
        
        BUTTON_LARGURA = 190
        BUTTON_ALTURA = 80

        self.buttons = [ 
            Button(
                rect=pygame.Rect(mid_x - BUTTON_LARGURA // 2, start_y, BUTTON_LARGURA, BUTTON_ALTURA), 
                default_image=imagem1, 
                highlight_image=imagem1, 
                callback=self.start_game
            ),
            Button(
                rect=pygame.Rect(mid_x - BUTTON_LARGURA // 2, start_y + gap, BUTTON_LARGURA, BUTTON_ALTURA),
                default_image=imagem2, 
                highlight_image=imagem2, 
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