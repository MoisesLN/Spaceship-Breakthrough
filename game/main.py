from classes import Jogador, RoboZigueZague, RoboLento, RoboRapido, RoboCiclico, RoboCacador, RoboSaltador, EasterEgg, PowerUp, BossFinal
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
        self.powerups = pygame.sprite.Group()
        self.jogador = None # só inicializa quando começar o jogo
        self.pontos = 0
        self.spawn_timer = 0
        self.easter_egg = EasterEgg() 
        self.bossFinal = None
    
    def rodar(self):
        TELA = pygame.display.set_mode((LARGURA, ALTURA))
        self.fundo = pygame.image.load("game/sprites/background.png")
        self.jogador = Jogador(LARGURA // 2, ALTURA - 60)
        self.todos_sprites.add(self.jogador)
        pygame.mixer.music.load("game/sons/Main Theme.mp3")
        pygame.mixer.music.set_volume(0.6)
        pygame.mixer.music.play(-1)
    
        pygame.display.set_caption("Robot Defense - Template")
        rodando = True
        while rodando:
            self.clock.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    rodando = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        tiros = self.jogador.atirar()
                        for tiro in tiros:
                            self.todos_sprites.add(tiro)
                            self.tiros.add(tiro)   

            # timer de entrada dos inimigos
            self.spawn_timer += 1

            if self.bossFinal:
                if self.spawn_timer > 30:
                    self.spawnarRobo(300, self.bossFinal.rect.x)


            elif self.spawn_timer > 40:
                self.spawnarRobo(0)

            # colisão tiro x robô
            colisao = pygame.sprite.groupcollide(self.inimigos, self.tiros, False, True)
            for inimigo, tiro in colisao.items():
                if inimigo.tomarDano() == 'morto':
                    # Ao matar inimigos, chance de dropar powerup
                    self.spawnarPowerUp(inimigo)
                    self.pontos += 1
            
            if self.pontos == 1:
                self.spawnarBoss()

            # colisão robô x robô
            colisoes = pygame.sprite.groupcollide(self.inimigos, self.inimigos, False, False)
            for inimigo, lista_colididos in colisoes.items():
                for collided in lista_colididos:
                    if inimigo is not collided:
                        inimigo.tomarDano()
                        collided.tomarDano()

            # colisão robô x jogador
            if pygame.sprite.spritecollide(self.jogador, self.inimigos, True):
                self.jogador.vida -= 1
                if self.jogador.vida <= 0:
                    print("GAME OVER!")
                    rodando = False

            # colisão jogador x powerup
            coletados = pygame.sprite.spritecollide(self.jogador, self.powerups, True)
            for p in coletados:
                # durações em frames (por exemplo 5s para velocidade, 6s para triplo)
                dur_speed = 5 * self.FPS
                dur_triple = 6 * self.FPS
                if p.tipo == 'vida':
                    self.jogador.aplicar_powerup('vida')
                elif p.tipo == 'velocidade':
                    self.jogador.aplicar_powerup('velocidade', duracao_frames=dur_speed)
                elif p.tipo == 'tiro_triplo':
                    self.jogador.aplicar_powerup('tiro_triplo', duracao_frames=dur_triple)

            # atualizar
            self.todos_sprites.update()
            
            if self.jogador.rect.bottom >= ALTURA:
                self.jogador.rect.bottom = ALTURA
                self.easter_egg.adicionar_colisao("baixo")

            if self.jogador.rect.right >= LARGURA and self.jogador.rect.centery < ALTURA // 2:
                self.jogador.rect.right = LARGURA
                self.easter_egg.adicionar_colisao("direita")

            if self.jogador.rect.left <= 0 and self.jogador.rect.centery < ALTURA // 2:
                self.jogador.rect.left = 0
                self.easter_egg.adicionar_colisao("esquerda")

            if self.easter_egg.ativo:
                self.easter_egg.invocar_chuva_de_balas(self.tiros, self.todos_sprites)
                self.easter_egg.ativo = False

            # desenhar
            TELA.blit(self.fundo, (0,0))
            self.todos_sprites.draw(TELA)

            #Painel de pontos e vida
            font = pygame.font.Font("game/Minecraftia-Regular.ttf", 20)
            texto = font.render(f"Vida: {self.jogador.vida}  |  Pontos: {self.pontos}", True, (255, 255, 255))
            TELA.blit(texto, (10, 10))

            pygame.display.flip()

        pygame.quit()

    def spawnarPowerUp(self, inimigo):
        if random.random() < 0.1:
            tipo = random.choice(['vida', 'velocidade', 'tiro_triplo'])
            px, py = inimigo.rect.centerx, inimigo.rect.centery
            power = PowerUp(px, py, tipo)
            self.todos_sprites.add(power)
            self.powerups.add(power)

    def spawnarRobo(self, altura_base, coordY=None):
        # PESOS:
        # RoboZigueZague: 4
        # RoboLento: 2
        # RoboRapido: 2
        # RoboCiclico: 1
        # RoboCacador: 1
        # RoboSaltador: 1
        print(coordY)

        num = random.randint(1, 11)
        if num <= 4:
            robo = RoboZigueZague(random.randint(40, LARGURA - 60), altura_base)
        elif num <= 6:
            robo = RoboLento(random.randint(40, LARGURA - 40), altura_base)
        elif num <= 8:
            robo = RoboRapido(random.randint(40, LARGURA - 40), altura_base)
        elif num == 9:
            robo = RoboCiclico(random.randint(90, LARGURA - 90), altura_base)
        elif num == 10:
            robo = RoboCacador(random.randint(40, LARGURA - 40), altura_base, self.jogador)
        elif num == 11:
            robo = RoboSaltador(random.randint(40, LARGURA - 40), altura_base)
        self.todos_sprites.add(robo) 
        self.inimigos.add(robo)
        self.spawn_timer = 0

    def spawnarBoss(self):
        if self.bossFinal is None or self.bossFinal.vivo == False:
            self.bossFinal = BossFinal(LARGURA // 2, 125, 3, 240)
            self.todos_sprites.add(self.bossFinal)
            self.inimigos.add(self.bossFinal)


jogo = Game(LARGURA, ALTURA, FPS)

if __name__ == '__main__':
    menu = Menu()
    menu.run()
    if not menu.running:
        jogo.rodar()