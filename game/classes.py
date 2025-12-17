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
        self.image = pygame.image.load('game/sprites/tiro.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (20, 60))
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y -= self.velocidade
        if self.rect.y < 0:
            self.kill()

class TiroInclinado(Tiro):
    def __init__(self, x, y, direcao):
        super().__init__(x, y)
        self.direcao = direcao

    def update(self):
        self.rect.y -= self.velocidade
        self.rect.x += self.direcao * 3
        if self.rect.y < 0:
            self.kill()

# JOGADOR
class Jogador(Entidade):
    def __init__(self, x, y):
        self.base_speed = 5
        super().__init__(x, y, self.base_speed)

        self.imagesArray = [
            pygame.transform.scale(pygame.image.load('game/sprites/nave/nave_base1.png').convert_alpha(), (64, 80)),
            pygame.transform.scale(pygame.image.load('game/sprites/nave/nave_base2.png').convert_alpha(), (64, 80)),
            pygame.transform.scale(pygame.image.load('game/sprites/nave/nave_base3.png').convert_alpha(), (64, 80)),
            pygame.transform.scale(pygame.image.load('game/sprites/nave/nave_base4.png').convert_alpha(), (64, 80)),
        ]
        self.indexImg = 0
        self.image = self.imagesArray[self.indexImg]
        self.rect = self.image.get_rect(center=(x, y))

        self.vida = 5
        self.ticks = 0

        self.power_timers = {
            'velocidade': 0,
            'tiro_triplo': 0
        }
        self.tiro_triplo = False
        self.velocidade = self.base_speed

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
        self.rect.x = max(-5, min(self.rect.x, LARGURA - 59))
        self.rect.y = max(-5, min(self.rect.y, ALTURA - 75))

        # Animação das sprites
        if self.ticks % 4 == 0:  # atualizar a cada 4 ticks
            old_center = self.rect.center
            self.image = self.imagesArray[self.indexImg]
            self.rect = self.image.get_rect(center=old_center)
            self.indexImg = (self.indexImg + 1) % len(self.imagesArray)

        self.ticks += 1

        # reduzir timers de powerups (1 frame por update)
        if self.power_timers['velocidade'] > 0:
            self.power_timers['velocidade'] -= 1
            if self.power_timers['velocidade'] == 0:
                self.velocidade = self.base_speed

        if self.power_timers['tiro_triplo'] > 0:
            self.power_timers['tiro_triplo'] -= 1
            if self.power_timers['tiro_triplo'] == 0:
                self.tiro_triplo = False

    def atirar(self):
        tiros = []
        tiros.append(Tiro(self.rect.centerx, self.rect.centery))

        if self.tiro_triplo:
            tiros.append(TiroInclinado(self.rect.centerx, self.rect.centery, -1))
            tiros.append(TiroInclinado(self.rect.centerx, self.rect.centery, 1))

        return tiros

    def aplicar_powerup(self, tipo, duracao_frames=0):

        if tipo == 'vida':
            self.vida += 1
        elif tipo == 'velocidade':

            self.velocidade = self.base_speed + 3  # ajuste se quiser menos/mais
            self.power_timers['velocidade'] = duracao_frames
        elif tipo == 'tiro_triplo':
            self.tiro_triplo = True
            self.power_timers['tiro_triplo'] = duracao_frames



# ROBO BASE
class Robo(Entidade):
    def __init__(self, x, y, velocidade):
        super().__init__(x, y, velocidade)
        self.image.fill((255, 0, 0))  # vermelho

    def atualizar_posicao(self):
        raise NotImplementedError
    
    def tomarDano(self):
        self.vida -= 1
        if self.vida <=0:
            self.kill()
            return 'morto'


# ROBO EXEMPLO — ZigueZague
class RoboZigueZague(Robo):
    def __init__(self, x, y):
        super().__init__(x, y, velocidade=3)
        self.image = pygame.image.load('game/sprites/naveZigZag.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (75, 75))
        self.rect = self.image.get_rect(center=(x, y))
        self.direcao = 1
        self.ticks = 0
        self.timeToRevert = random.randint(75, 150)
        self.vida = 1

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
        self.imagesArray = [
            pygame.transform.scale(pygame.image.load('game/sprites/naveLenta/naveLenta1.png').convert_alpha(), (64, 80)),
            pygame.transform.scale(pygame.image.load('game/sprites/naveLenta/naveLenta2.png').convert_alpha(), (64, 80)),
            pygame.transform.scale(pygame.image.load('game/sprites/naveLenta/naveLenta3.png').convert_alpha(), (64, 80)),
            pygame.transform.scale(pygame.image.load('game/sprites/naveLenta/naveLenta4.png').convert_alpha(), (64, 80)),
            ]
        self.indexImg = 0
        self.image = self.imagesArray[self.indexImg]
        self.ticks = 0
        self.vida = 1
        # self.image.fill((255, 0, 255))  # roxo

    def atualizar_posicao(self):
        self.rect.y += self.velocidade

    def update(self):
        self.atualizar_posicao()
        if self.rect.y > ALTURA:
            self.kill()
            
        if self.ticks % 4 == 0:
            old_center = self.rect.center
            self.image = self.imagesArray[self.indexImg]
            self.rect = self.image.get_rect(center=old_center)
            self.indexImg = (self.indexImg + 1) % len (self.imagesArray)

                
        self.ticks += 1
            
# Robô Rápido
class RoboRapido(Robo):
    def __init__(self, x, y):
        super().__init__(x, y, velocidade=6)
        self.imagesArray = [
            pygame.transform.scale(pygame.image.load('game/sprites/naveRapida/naveRapida1.png').convert_alpha(), (64, 80)),
            pygame.transform.scale(pygame.image.load('game/sprites/naveRapida/naveRapida2.png').convert_alpha(), (64, 80)),
            pygame.transform.scale(pygame.image.load('game/sprites/naveRapida/naveRapida3.png').convert_alpha(), (64, 80)),
            pygame.transform.scale(pygame.image.load('game/sprites/naveRapida/naveRapida4.png').convert_alpha(), (64, 80)),
            ]
        self.indexImg = 0
        self.image = self.imagesArray[self.indexImg]
        self.ticks = 0
        self.direcao = 1
        self.num = random.randint(1, 2)
        self.vida = 2

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
            old_center = self.rect.center
            self.image = self.imagesArray[self.indexImg]
            self.rect = self.image.get_rect(center=old_center)
            self.indexImg = (self.indexImg + 1) % len (self.imagesArray)

                
        self.ticks += 1

# Robô Cíclico
class RoboCiclico(Robo):
    # Para fazer o círculo:
    # x = Xcentro + raio * cos(angulo)
    # y = ycentro + raio * sin(angulo)

    def __init__(self, x, y):
        super().__init__(x, y, velocidade=2)
        self.imagesArray = [
            pygame.transform.scale(pygame.image.load('game/sprites/naveCiclica/naveCiclica1.png').convert_alpha(), (64, 80)),
            pygame.transform.scale(pygame.image.load('game/sprites/naveCiclica/naveCiclica2.png').convert_alpha(), (64, 80)),
            pygame.transform.scale(pygame.image.load('game/sprites/naveCiclica/naveCiclica3.png').convert_alpha(), (64, 80)),
            pygame.transform.scale(pygame.image.load('game/sprites/naveCiclica/naveCiclica4.png').convert_alpha(), (64, 80)),
            ]
        self.indexImg = 0
        self.image = self.imagesArray[self.indexImg]
        self.direcao = 1
        self.num = random.randint(1, 2)
        self.ticksToRotate = 80
        self.ticks = 0
        self.x = self.rect.x
        self.y = self.rect.y
        self.radius = random.randint(30,70)
        self.vida = 3

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
            old_center = self.rect.center
            self.image = self.imagesArray[self.indexImg]
            self.rect = self.image.get_rect(center=old_center)
            self.indexImg = (self.indexImg + 1) % len (self.imagesArray)
            
class RoboCacador(Robo):

    def __init__(self, x, y, jogador):
        super().__init__(x, y, velocidade=3)
        self.imagesArray = [
            pygame.transform.scale(pygame.image.load('game/sprites/naveCacador/naveCacador1.png').convert_alpha(), (64, 80)),
            pygame.transform.scale(pygame.image.load('game/sprites/naveCacador/naveCacador2.png').convert_alpha(), (64, 80)),
            pygame.transform.scale(pygame.image.load('game/sprites/naveCacador/naveCacador3.png').convert_alpha(), (64, 80)),
            pygame.transform.scale(pygame.image.load('game/sprites/naveCacador/naveCacador4.png').convert_alpha(), (64, 80)),
            ]
        self.indexImg = 0
        self.image = self.imagesArray[self.indexImg]
        self.ticks = 0
        self.direcao = 1
        self.jogador = jogador
        self.vida = 3
        
    def atualizar_posicao(self):
        self.rect.y += self.velocidade
        if self.rect.x > self.jogador.rect.x:
            self.rect.x -= self.direcao * 3
        else: 
            self.rect.x += self.direcao * 3
            
    def update(self):
        self.atualizar_posicao()
        if self.rect.y > ALTURA:
            self.kill()
            
        if self.ticks % 4 == 0: 
            old_center = self.rect.center
            self.image = self.imagesArray[self.indexImg]
            self.rect = self.image.get_rect(center=old_center)
            self.indexImg = (self.indexImg + 1) % len (self.imagesArray)

                
        self.ticks += 1
            
class RoboSaltador(Robo):
    def __init__(self, x, y):
        super().__init__(x, y, velocidade=3)
        self.direcao = random.choice([-1, 1])
        self.image = pygame.image.load('game/sprites/naveGlitch.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (75, 75))
        self.rect = self.image.get_rect(center=(x, y))
        self.ticks = 0
        self.timeToRevert = random.randint(30, 75)
        self.num = random.randint(1,2)
        self.direcao_salto = random.randint(1,2)
        self.mudanca_x = random.randint(50, 100)
        self.vida = 3

    def atualizar_posicao(self):
        # Teleportar e inverter direção após teleporte
        if self.ticks == self.timeToRevert:
            self.timeToRevert = random.randint(100, 150)
            # Teleporte para a direita
            if self.direcao_salto == 1:
                # Não passar da largura da tela
                if self.rect.x + self.mudanca_x >= LARGURA - 75:
                    self.rect.x = LARGURA - 80
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
        if self.rect.x <= 0 or self.rect.x >= LARGURA - 75:
            self.direcao *= -1

        self.rect.x += self.direcao * 3
        self.rect.y += self.velocidade

    def update(self):
        self.atualizar_posicao()
        self.ticks += 1
        if self.rect.y > ALTURA:
            self.kill()

class BossFinal(Robo):
    def __init__(self, x, y, velocidade, tamanho):
        super().__init__(x, y, velocidade)
        self.tamanho = tamanho
        self.image = pygame.image.load('game/sprites/naveBoss.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.tamanho, self.tamanho))
        self.rect = self.image.get_rect(center=(x, y))
        self.ticks = 0
        self.vida = 50
        self.vivo = True
        self.direcao = 1

    def update(self):
        self.rect.x += self.direcao * self.velocidade
        if (self.rect.x + 240) >= LARGURA or self.rect.x  <= 0:
            self.direcao *= -1

    def tomarDano(self):
        self.vida -= 1
        print(self.vida)
        if self.vida <= 0:
            self.kill()

class PowerUp(Entidade):
    def __init__(self, x, y, tipo):
        super().__init__(x, y, velocidade=2)
        self.tipo = tipo

        if tipo == 'vida':
            self.image = pygame.image.load(
                'game/sprites/upgradeVida.png'
            ).convert_alpha()

        elif tipo == 'velocidade':
            self.image = pygame.image.load(
                'game/sprites/upgradeVelocidade.png'
            ).convert_alpha()

        elif tipo == 'tiro_triplo':
            self.image = pygame.image.load(
                'game/sprites/upgradeTiro_triplo.png'
            ).convert_alpha()

        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y += self.velocidade

        if self.rect.top > ALTURA:
            self.kill()

class EasterEgg:
    def __init__(self):
        self.colisoes = []
        self.ativo = False
        self.ultima_colisao = None

    def adicionar_colisao(self, parede):
        if self.ativo:
            return

        if parede == self.ultima_colisao:
            return

        self.ultima_colisao = parede
        self.colisoes.append(parede)

        if len(self.colisoes) > 3:
            self.colisoes.pop(0)

        if self.colisoes == ["baixo", "direita", "esquerda"]:
            self.ativo = True

    def invocar_chuva_de_balas(self, grupo_tiros, todos_sprites):
        for x in range(0, LARGURA, 40):
            tiro = Tiro(x, ALTURA - 20)
            grupo_tiros.add(tiro)
            todos_sprites.add(tiro)