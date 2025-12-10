import pygame
import random
import math

# TODO: som de colisão robôs, sistema de VIDA dos robôs, sprites dos robôs
LARGURA = 600 
ALTURA = 720

# CLASSE BASE
class Entidade(pygame.sprite.Sprite):
    def __init__(self, x, y, velocidade):
        super().__init__()
        self.velocidade = velocidade
        self.image = pygame.Surface((40, 40))
        self.rect = self.image.get_rect(center=(x, y))

    def mover(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy


# TIRO (DO JOGADOR)
class Tiro(Entidade):
    def __init__(self, x, y):
        super().__init__(x, y, 10)
        self.image = pygame.image.load('game/sprites/tiro.png')
        self.image = pygame.transform.scale(self.image, (20, 60))

    def update(self):
        self.rect.y -= self.velocidade
        if self.rect.y < 0:
            self.kill()

# JOGADOR
class Jogador(Entidade):
    def __init__(self, x, y):
        super().__init__(x, y, 5)
        # self.image.fill((0, 255, 0))  # verde
        self.imagesArray = ['game/sprites/nave/nave_base1.png', 'game/sprites/nave/nave_base2.png', 'game/sprites/nave/nave_base3.png', 'game/sprites/nave/nave_base4.png']
        self.indexImg = 0
        self.image = pygame.image.load(self.imagesArray[self.indexImg])
        self.image = pygame.transform.scale(self.image, (64, 80))
        self.vida = 5
        self.ticks = 0

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.mover(0, -self.velocidade)
        if keys[pygame.K_s]:
            self.mover(0, self.velocidade)
        if keys[pygame.K_a]:
            self.mover(-self.velocidade, 0)
        if keys[pygame.K_d]:
            self.mover(self.velocidade, 0)

        # limites de tela
        self.rect.x = max(0, min(self.rect.x, LARGURA - 64))
        self.rect.y = max(0, min(self.rect.y, ALTURA - 80))

        # Animação das sprites
        if self.ticks % 4 == 0: # atualizar a cada 4 ticks
            self.image = pygame.image.load(self.imagesArray[self.indexImg])
            self.image = pygame.transform.scale(self.image, (64, 80))
            if self.indexImg == len(self.imagesArray) - 1:
                self.indexImg = 0
            else:
                self.indexImg += 1
        
        self.ticks += 1

    def atirar(self):
        Tiro(self.rect.centerx, self.rect.centery)
        return Tiro(self.rect.centerx, self.rect.centery)

# ROBO BASE
class Robo(Entidade):
    def __init__(self, x, y, velocidade):
        super().__init__(x, y, velocidade)
        self.image.fill((255, 0, 0))  # vermelho

    def atualizar_posicao(self):
        raise NotImplementedError


# ROBO EXEMPLO — ZigueZague
class RoboZigueZague(Robo):
    def __init__(self, x, y):
        super().__init__(x, y, velocidade=3)
        self.image = pygame.image.load('game/sprites/naveZigZag.png')
        self.image = pygame.transform.scale(self.image, (75, 75))
        self.direcao = 1
        self.ticks = 0
        self.timeToRevert = random.randint(75, 150)

    def atualizar_posicao(self):
        if self.ticks == self.timeToRevert:
            # Inverter a direção a cada X ticks entre 100 e 200
            self.direcao *= -1
            self.timeToRevert = random.randint(75, 150)
            self.ticks = 0

        self.rect.y += self.velocidade
        self.rect.x += self.direcao * 3
        if self.rect.x <= 0 or self.rect.x >= LARGURA - 75:
            self.direcao *= -1

    def update(self):
        self.atualizar_posicao()
        self.ticks += 1
        if self.rect.y > ALTURA:
            self.kill()

# Robô Lento
class RoboLento(Robo):
    def __init__(self, x, y):
        super().__init__(x, y, velocidade=2)
        self.imagesArray = ['game/sprites/naveLenta/naveLenta1.png', 'game/sprites/naveLenta/naveLenta2.png', 'game/sprites/naveLenta/naveLenta3.png', 'game/sprites/naveLenta/naveLenta4.png']
        self.indexImg = 0
        self.image = pygame.image.load(self.imagesArray[self.indexImg])
        self.image = pygame.transform.scale(self.image, (75, 80))
        self.ticks = 0
        # self.image.fill((255, 0, 255))  # roxo

    def atualizar_posicao(self):
        self.rect.y += self.velocidade

    def update(self):
        self.atualizar_posicao()
        if self.rect.y > ALTURA:
            self.kill()
            
        if self.ticks % 4 == 0:
            self.image = pygame.image.load(self.imagesArray[self.indexImg])
            self.image = pygame.transform.scale(self.image, (64, 80))
            if self.indexImg == len(self.imagesArray) - 1:
                self.indexImg = 0
            else:
                self.indexImg += 1
                
        self.ticks += 1
            
# Robô Rápido
class RoboRapido(Robo):
    def __init__(self, x, y):
        super().__init__(x, y, velocidade=6)
        self.imagesArray = ['game/sprites/naveRapida/naveRapida1.png', 'game/sprites/naveRapida/naveRapida2.png', 'game/sprites/naveRapida/naveRapida3.png', 'game/sprites/naveRapida/naveRapida4.png']
        self.indexImg = 0
        self.image = pygame.image.load(self.imagesArray[self.indexImg])
        self.image = pygame.transform.scale(self.image, (69, 80))
        self.ticks = 0
        self.direcao = 1
        self.num = random.randint(1, 2)

    def atualizar_posicao(self):
        if self.num == 1:
            self.rect.y += self.velocidade
            self.rect.x += self.direcao * 3
            if self.rect.x <= 0 or self.rect.x >= LARGURA - 69:
                self.direcao *= -1
                
        elif self.num == 2:
            self.rect.y += self.velocidade

    def update(self):
        self.atualizar_posicao()
        if self.rect.y > ALTURA:
            self.kill()
            
        if self.ticks % 4 == 0:
            self.image = pygame.image.load(self.imagesArray[self.indexImg])
            self.image = pygame.transform.scale(self.image, (64, 80))
            if self.indexImg == len(self.imagesArray) - 1:
                self.indexImg = 0
            else:
                self.indexImg += 1
                
        self.ticks += 1

# Robô Cíclico
class RoboCiclico(Robo):
    # Para fazer o círculo:
    # x = Xcentro + raio * cos(angulo)
    # y = ycentro + raio * sin(angulo)

    def __init__(self, x, y):
        super().__init__(x, y, velocidade=2)
        self.imagesArray = ['game/sprites/naveCiclica/naveCiclica1.png', 'game/sprites/naveCiclica/naveCiclica2.png', 'game/sprites/naveCiclica/naveCiclica3.png', 'game/sprites/naveCiclica/naveCiclica4.png']
        self.indexImg = 0
        self.image = pygame.image.load(self.imagesArray[self.indexImg])
        self.image = pygame.transform.scale(self.image, (75, 80))
        self.direcao = 1
        self.num = random.randint(1, 2)
        self.ticksToRotate = 80
        self.ticks = 0
        self.x = self.rect.x
        self.y = self.rect.y
        self.radius = random.randint(30,70)

    def atualizar_posicao(self):
        angle = (2 * math.pi / self.ticksToRotate) * self.ticks
        self.y += self.velocidade
        self.rect.x = self.x + (self.radius * math.cos(angle))
        self.rect.y = self.y + (self.radius * math.sin(angle))

    def update(self):
        self.atualizar_posicao()
        self.ticks += 1
        if self.rect.y > ALTURA:
            self.kill()
            
        if self.ticks % 4 == 0:
            self.image = pygame.image.load(self.imagesArray[self.indexImg])
            self.image = pygame.transform.scale(self.image, (64, 80))
            if self.indexImg == len(self.imagesArray) - 1:
                self.indexImg = 0
            else:
                self.indexImg += 1
            
class RoboCacador(Robo):

    def __init__(self, x, y, jogador):
        super().__init__(x, y, velocidade=3)
        self.imagesArray = ['game/sprites/naveCacador/naveCacador1.png', 'game/sprites/naveCacador/naveCacador2.png', 'game/sprites/naveCacador/naveCacador3.png', 'game/sprites/naveCacador/naveCacador4.png']
        self.indexImg = 0
        self.image = pygame.image.load(self.imagesArray[self.indexImg])
        self.image = pygame.transform.scale(self.image, (75, 80))
        self.ticks = 0
        self.direcao = 1
        self.jogador = jogador
        
    def atualizar_posicao(self):
        if self.rect.x > self.jogador.rect.x:
            self.rect.y += self.velocidade
            self.rect.x -= self.direcao * 3
        else: 
            self.rect.y += self.velocidade
            self.rect.x += self.direcao * 3
            
    def update(self):
        self.atualizar_posicao()
        if self.rect.y > ALTURA:
            self.kill()
            
        if self.ticks % 4 == 0: 
            self.image = pygame.image.load(self.imagesArray[self.indexImg])
            self.image = pygame.transform.scale(self.image, (64, 80))
            if self.indexImg == len(self.imagesArray) - 1:
                self.indexImg = 0
            else:
                self.indexImg += 1
                
        self.ticks += 1
            
class RoboSaltador(Robo):
    def __init__(self, x, y):
        super().__init__(x, y, velocidade=3)
        self.direcao = random.choice([-1, 1])
        self.image.fill((0, 0, 100))  # azul
        self.ticks = 0
        self.timeToRevert = random.randint(30, 75)
        self.num = random.randint(1,2)
        self.direcao_salto = random.randint(1,2)
        self.mudanca_x = random.randint(50, 100)

    def atualizar_posicao(self):
        # Teleportar e inverter direção após teleporte
        if self.ticks == self.timeToRevert:
            self.timeToRevert = random.randint(100, 150)
            # Teleporte para a direita
            if self.direcao_salto == 1:
                # Não passar da largura da tela
                if self.rect.x + self.mudanca_x >= LARGURA - 40:
                    self.rect.x = LARGURA - 45
                else:
                    self.rect.x += self.mudanca_x
            # Teleporte para a esquerda
            else:
                # Não passar da largura da tela
                if self.rect.x - self.mudanca_x <= 0:
                    self.rect.x = 5
                else:
                    self.rect.x -= self.mudanca_x  
            
            self.direcao *= -1
        
        # Se bater numa parede, inverter direção
        elif self.rect.x >= LARGURA - 40 or self.rect.x <= 0:
            self.direcao *= -1

        self.rect.x += self.direcao * 3
        self.rect.y += self.velocidade

    def update(self):
        self.atualizar_posicao()
        self.ticks += 1
        if self.rect.y > ALTURA:
            self.kill()