import pygame
import random
import math

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
        self.image.fill((255, 255, 0))  # amarelo

    def update(self):
        self.rect.y -= self.velocidade
        if self.rect.y < 0:
            self.kill()

# JOGADOR
class Jogador(Entidade):
    def __init__(self, x, y):
        super().__init__(x, y, 5)
        self.image.fill((0, 255, 0))  # verde
        self.vida = 5

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
        self.rect.x = max(0, min(self.rect.x, LARGURA - 40))
        self.rect.y = max(0, min(self.rect.y, ALTURA - 40))

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
        if self.rect.x <= 0 or self.rect.x >= LARGURA - 40:
            self.direcao *= -1

    def update(self):
        self.atualizar_posicao()
        self.ticks += 1
        if self.rect.y > ALTURA:
            self.kill()

# Robô Lento
class RoboLento(Robo):
    def __init__(self, x, y):
        super().__init__(x, y, velocidade=1)
        self.image.fill((255, 0, 255))  # roxo

    def atualizar_posicao(self):
        self.rect.y += self.velocidade

    def update(self):
        self.atualizar_posicao()
        if self.rect.y > ALTURA:
            self.kill()
            
# Robô Rápido
class RoboRapido(Robo):
    def __init__(self, x, y):
        super().__init__(x, y, velocidade=6)
        self.image.fill((0, 0, 255))  # azul
        self.direcao = 1
        self.num = random.randint(1, 2)

    def atualizar_posicao(self):
        if self.num == 1:
            self.rect.y += self.velocidade
            self.rect.x += self.direcao * 3
            if self.rect.x <= 0 or self.rect.x >= LARGURA - 40:
                self.direcao *= -1
                
        elif self.num == 2:
            self.rect.y += self.velocidade

    def update(self):
        self.atualizar_posicao()
        if self.rect.y > ALTURA:
            self.kill()

# Robô Cíclico
class RoboCiclico(Robo):
    # Para fazer o círculo:
    # x = Xcentro + raio * cos(angulo)
    # y = ycentro + raio * sin(angulo)

    def __init__(self, x, y):
        super().__init__(x, y, velocidade=2)
        self.image.fill((0, 0, 255))  # azul
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