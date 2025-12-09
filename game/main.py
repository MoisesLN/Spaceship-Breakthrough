from classes import Jogador, RoboZigueZague, RoboLento, RoboRapido, RoboCiclico, RoboCacador, RoboSaltador
import pygame
import random
from menu import Menu

pygame.init()

LARGURA = 600 
ALTURA = 720
FPS = 60

class Game():
    def __init__(self, largura, altura, FPS):
        self.largura = largura
        self.altura = altura
        self.clock = pygame.time.Clock()
        self.FPS = FPS
        self.todos_sprites = pygame.sprite.Group()
        self.inimigos = pygame.sprite.Group()
        self.tiros = pygame.sprite.Group()
        self.jogador = Jogador(LARGURA // 2, ALTURA - 60)
        self.todos_sprites.add(self.jogador)
        self.pontos = 0
        self.spawn_timer = 0
    
    def rodar(self):
        TELA = pygame.display.set_mode((LARGURA, ALTURA))
        self.fundo = pygame.image.load("game/sprites/background.png")
    
        pygame.display.set_caption("Robot Defense - Template")
        rodando = True
        while rodando:
            self.clock.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    rodando = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        tiro = self.jogador.atirar()
                        self.todos_sprites.add(tiro)
                        self.tiros.add(tiro)

            # timer de entrada dos inimigos
            self.spawn_timer += 1
            if self.spawn_timer > 40:
                # PESOS:
                # RoboZigueZague: 4
                # RoboLento: 2
                # RoboRapido: 2
                # RoboCiclico: 1
                # RoboCacador: 1
                # RoboSaltador: 1

                num = random.randint(1, 11)
                if num <= 4:
                    robo = RoboZigueZague(random.randint(40, LARGURA - 40), -40)
                elif num <= 6:
                    robo = RoboLento(random.randint(40, LARGURA - 40), -40)
                elif num <= 8:
                    robo = RoboRapido(random.randint(40, LARGURA - 40), -40)
                elif num == 9:
                    robo = RoboCiclico(random.randint(90, LARGURA - 90), -40)
                elif num == 10:
                    robo = RoboCacador(random.randint(40, LARGURA - 40), -40, self.jogador)
                elif num == 11:
                    robo = RoboSaltador(random.randint(40, LARGURA - 40), -40)
                self.todos_sprites.add(robo) 
                self.inimigos.add(robo)
                self.spawn_timer = 0

            # colisão tiro x robô
            colisao = pygame.sprite.groupcollide(self.inimigos, self.tiros, True, True)
            self.pontos += len(colisao) 

            # colisão robô x robô
            colisoes = pygame.sprite.groupcollide(self.inimigos, self.inimigos, False, False)
            for inimigo, lista_colididos in colisoes.items():
                for collided in lista_colididos:
                    if inimigo is not collided:
                        inimigo.kill()
                        collided.kill()

            # colisão robô x jogador
            if pygame.sprite.spritecollide(self.jogador, self.inimigos, True):
                self.jogador.vida -= 1
                if self.jogador.vida <= 0:
                    print("GAME OVER!")
                    rodando = False

            # atualizar
            self.todos_sprites.update()

            # desenhar
            TELA.blit(self.fundo, (0,0))
            self.todos_sprites.draw(TELA)

            #Painel de pontos e vida
            font = pygame.font.Font("game/Minecraftia-Regular.ttf", 20)
            texto = font.render(f"Vida: {self.jogador.vida}  |  Pontos: {self.pontos}", True, (255, 255, 255))
            TELA.blit(texto, (10, 10))

            pygame.display.flip()

        pygame.quit()

jogo = Game(LARGURA, ALTURA, FPS)

if __name__ == '__main__':
    menu = Menu()
    menu.run()
    if not menu.running:
        jogo.rodar()