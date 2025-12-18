from classes import Jogador, RoboZigueZague, RoboLento, RoboRapido, RoboCiclico, RoboCacador, RoboSaltador, EasterEgg, PowerUp, BossFinal
import pygame
import random
from menu import Menu
from gameover import GameOver
from you_won import YouWon

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
        self.explosoes_ativas = []
        self.sprites_explosao = []
        for i in range(1, 16): 
            img = pygame.image.load(f"game/sprites/Explosão/Explosão.{i}.png")
            self.sprites_explosao.append(pygame.transform.scale(img, (250, 250)))
    
    def rodar(self):
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        self.fundo = pygame.image.load("game/sprites/background.png")
        self.jogador = Jogador(LARGURA // 2, ALTURA - 60)
        self.todos_sprites.add(self.jogador)
        pygame.mixer.music.load("game/sons/Main Theme.mp3")
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)
    
        pygame.display.set_caption("Spaceship Breakthrough")
        rodando = True
        while rodando:
            self.clock.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    rodando = False
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        tiros = self.jogador.atirar()
                        for tiro in tiros:
                            self.todos_sprites.add(tiro)
                            self.tiros.add(tiro)   

            # timer de entrada dos inimigos
            self.spawn_timer += 1

            if self.bossFinal and self.bossFinal.vivo:
                if self.spawn_timer > 30:
                    self.spawnarRobo(300, self.bossFinal.rect.x)


            elif self.spawn_timer > 40:
                self.spawnarRobo(0)

            # colisão tiro x robô
            som_explosao = pygame.mixer.Sound("game/sons/explosao.mp3")
            som_explosao.set_volume(0.5)
            colisao = pygame.sprite.groupcollide(self.inimigos, self.tiros, False, True)
            for inimigo, tiro in colisao.items():
                tiro_som = pygame.mixer.Sound("game/sons/laser1.wav")
                tiro_som.set_volume(0.3)
                tiro_som.play()
                if inimigo.tomarDano() == 'morto':
                    # Ao matar inimigos, chance de dropar powerup
                    self.adicionar_explosao(inimigo.rect.center)
                    som_explosao.play()
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
                    rodando = False
                    GameOver().run()
                
            # colisão jogador x powerup
            coletados = pygame.sprite.spritecollide(self.jogador, self.powerups, True)
            som_upgrade = pygame.mixer.Sound("game/sons/upgrade.mp3")
            som_upgrade.set_volume(0.5)
            for p in coletados:
                # durações em frames (por exemplo 5s para velocidade, 6s para triplo)
                dur_speed = 5 * self.FPS
                dur_triple = 6 * self.FPS
                som_upgrade.play()

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
            self.tela.blit(self.fundo, (0,0))
            self.todos_sprites.draw(self.tela)

            #Painel de pontos e vida
            font = pygame.font.Font("game/Minecraftia-Regular.ttf", 20)
            texto_vida = font.render(f"Vidas: {self.jogador.vida}", True, (255, 255, 255))
            texto_pontos = font.render(f"Pontos: {self.pontos}", True, (255, 255, 255))
            vida_image = pygame.image.load("game/sprites/medalhaVida.png")
            vida_image = pygame.transform.scale(vida_image, (30, 40))
            pontos_image = pygame.image.load("game/sprites/pontuacao.png")
            pontos_image = pygame.transform.scale(pontos_image, (30, 40))
            self.tela.blit(pontos_image, (10, 60))
            self.tela.blit(texto_vida, (50, 20))
            self.tela.blit(texto_pontos, (50, 70))
            self.tela.blit(vida_image, (10, 10))
            
            self.gerenciar_explosoes()

            pygame.display.flip()

        return
    
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

    def adicionar_explosao(self, posicao):
        nova_explosao = {
            'pos': posicao,
            'frame': 0,
            'ultimo_update': pygame.time.get_ticks()
        }
        self.explosoes_ativas.append(nova_explosao)

    def gerenciar_explosoes(self):
        agora = pygame.time.get_ticks()
        tempo_entre_frames = 30 

        for expl in self.explosoes_ativas:
            if agora - expl['ultimo_update'] > tempo_entre_frames:
                expl['frame'] += 1
                expl['ultimo_update'] = agora
            
            if expl['frame'] < len(self.sprites_explosao):
                img_atual = self.sprites_explosao[expl['frame']]
                rect = img_atual.get_rect(center=expl['pos'])
                self.tela.blit(img_atual, rect)
            else:
                self.explosoes_ativas.remove(expl)
            
jogo = Game(LARGURA, ALTURA, FPS)

if __name__ == '__main__':
    while True:
        menu = Menu()
        menu.run()
        if not menu.running:
            jogo = Game(LARGURA, ALTURA, FPS)
            jogo.rodar()
