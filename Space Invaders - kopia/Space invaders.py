import pygame
from pygame import mixer
from pygame.locals import *
import random

pygame.init()


pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()


clock = pygame.time.Clock()
fps = 60


screen_width = 600
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Space invaders')

font30 = pygame.font.SysFont('constantia', 30)
font40 = pygame.font.SysFont('constantia', 40)


explosion_fx = pygame.mixer.Sound("img/explosion.wav")
explosion_fx.set_volume(0.2)

explosion2_fx = pygame.mixer.Sound("img/explosion2.wav")
explosion2_fx.set_volume(0.2)

laser_fx = pygame.mixer.Sound("img/laser.wav")
laser_fx.set_volume(0.2)

laser2_fx = pygame.mixer.Sound("img/laser2.wav")
laser2_fx.set_volume(0.25)

laser3_fx = pygame.mixer.Sound("img/laser3.wav")
laser3_fx.set_volume(0.1)


rows = 5
cols = 5
alien_cooldown = 1000
last_alien_shot = 800
laser_cooldown = 2500
explode = False
countdown = 3
last_count = pygame.time.get_ticks()
game_over = 0
clicked = False



red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)


bg = pygame.image.load("img/bg.png")
new_icon = pygame.image.load("img/sonja.jpg")

pygame.display.set_icon(new_icon)

def draw_bg():
	screen.blit(bg, (0, 0))


def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))



class Spaceship(pygame.sprite.Sprite):
	def __init__(self, x, y, health):
		self.reset(x, y, health)
	

	def update(self):

		speed = 8
		cooldown = 500 #Millisekunder
		game_over = 0

		key = pygame.key.get_pressed()
		if key[pygame.K_LEFT] and self.rect.left > 0:
			self.rect.x -= speed
		if key[pygame.K_RIGHT] and self.rect.right < screen_width:
			self.rect.x += speed


		time_now = pygame.time.get_ticks()	


		if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
			bullet = Bullets(self.rect.centerx, self.rect.top)
			laser3_fx.play()
			bullet_group.add(bullet)
			self.last_shot = time_now

		self.mask = pygame.mask.from_surface(self.image)			



		pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 15))
		if self.health_remaining > 0:
			pygame.draw.rect(screen, green, (self.rect.x, (self.rect.bottom + 10), int(self.rect.width * (self.health_remaining / self.health_start)), 15))
		elif self.health_remaining <= 0:
			explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
			explosion_group.add(explosion)
			self.rect.centery += 200
			explosion2_fx.play()
			game_over = -1
		return game_over

	def reset(self, x, y, health):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("img/spaceship.png")
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.health_start = health
		self.health_remaining = health
		self.last_shot = pygame.time.get_ticks()
		self.health = health

			

			


class Bullets(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("img/bullet.png")
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]


	def update(self):
		self.rect.y -= 5
		if self.rect.bottom < 0:
			self.kill()
		if pygame.sprite.spritecollide(self, alien_group, True):
			self.kill()
			explosion_fx.play()
			explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
			explosion_group.add(explosion)
		if pygame.sprite.spritecollide(self, saucer_group, False):
			self.kill()
			explosion_fx.play()
			explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
			explosion_group.add(explosion)
			saucer.health -=1
	
				
	
			



class Aliens(pygame.sprite.Sprite):
	def __init__(self, x, y):
		self.reset(x, y)
	
	def update(self):
		self.rect.x += self.move_direction
		self.move_counter += 1
		if abs(self.move_counter) > 75:
			self.move_direction *= -1
			self.move_counter *= self.move_direction

	def reset(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("img/alien" + str(random.randint(1, 8)) + ".png")
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.move_counter = 0
		self.move_direction = 1


			

class Alien_Bullets(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("img/alien_bullet.png")
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]


	def update(self):
		self.rect.y += 3
		if self.rect.top > screen_height:
			self.kill()	
		if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):
			self.kill()
			explosion_fx.play()
			spaceship.health_remaining -= 1
			explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
			explosion_group.add(explosion)
	

class Saucer(pygame.sprite.Sprite):
	def __init__(self, x, y, health):
		self.reset(x, y, health)

	def update(self):
		self.rect.x += self.move_direction
		self.move_counter += 1
		if abs(self.move_counter) > 100:
			self.move_direction *= -1
			self.move_counter *= self.move_direction

	def reset(self, x, y, health):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("img/Saucer.png")
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.move_counter = 0
		self.move_direction = 1
		self.health = health

			


class Laser(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("img/Laser.png")
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]


	def update(self):
		self.rect.y += 2
		if self.rect.top > screen_height:
			self.kill()	
		if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):
			self.kill()
			spaceship.health_remaining -= 1
			explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
			explosion_group.add(explosion)			




						
		
class Explosion(pygame.sprite.Sprite):
	def __init__(self, x, y, size):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		for num in range(1, 6):
			img = pygame.image.load(f"img/exp{num}.png")
			if size == 1:
				img = pygame.transform.scale(img, (20, 20))
			if size == 2:
				img = pygame.transform.scale(img, (40, 40))
			if size == 3:
				img = pygame.transform.scale(img, (200, 200))
			if size == 4:
				img = pygame.transform.scale(img, (400, 400))	

			self.images.append(img)	
		self.index = 0	
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.counter = 0

	def update(self):
		explosion_speed = 3
		self.counter += 1

		if self.counter >= explosion_speed and self.index < len(self.images) - 1:
			self.counter = 0
			self.index += 1
			self.image = self.images[self.index]

		if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
			self.kill()
		



spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
alien_bullet_group = pygame.sprite.Group()
saucer_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()

def create_aliens():

	for row in range(rows):
		for item in range(cols):
			alien = Aliens(100 + item * 100, 100 + row * 70)
			alien_group.add(alien)


create_aliens()			


saucer = Saucer(screen_width // 2, -100, 25)
saucer_group.add(saucer)
spaceship = Spaceship(int(screen_width / 2), screen_height - 100, 3)
spaceship_group.add(spaceship)		




run = True
while run:

	clock.tick(fps)


	draw_bg()

	if countdown == 0:


		time_now = pygame.time.get_ticks()

		if time_now - last_alien_shot > alien_cooldown and len(alien_group) > 0 and spaceship.health > 0:
			attacking_alien = random.choice(alien_group.sprites())
			laser_fx.play()
			alien_bullet = Alien_Bullets(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
			alien_bullet_group.add(alien_bullet)
			last_alien_shot = time_now

		if len(alien_group) == 0 and saucer.health > 0:
			saucer_group.update()
			saucer_group.draw(screen)


		if len(alien_group) == 0 and saucer.rect.centery < 200:
			saucer.rect.centery += 2
		if saucer.health <= 0 and explode == False:
			explosion2_fx.play()
			explosion = Explosion(saucer.rect.centerx, saucer.rect.centery, 4)
			explosion_group.add(explosion)
			explode = True			

				

		if time_now - last_alien_shot > laser_cooldown and len(alien_group) == 0 and saucer.health > 0  and spaceship.health > 0:
			attacking_alien = random.choice(saucer_group.sprites())
			laser2_fx.play()
			laser = Laser(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
			alien_bullet_group.add(laser)
			last_alien_shot = time_now

		if len(alien_group) == 0 and saucer.health <= 0:
			game_over = 1

		if game_over == 0:	
				
			
			game_over = spaceship.update()

			bullet_group.update()
			alien_group.update()
			alien_bullet_group.update()
		else:
			if game_over == -1:
				draw_text('GAME OVER!!', font40, white, int(screen_width / 2 - 100), int(screen_height / 2 + 50))
			if game_over == 1:
				draw_text('YOU WIN!! :)', font40, white, int(screen_width / 2 - 100), int(screen_height / 2 + 50))
			alien_bullet.kill()
			Laser(attacking_alien.rect.centerx, attacking_alien.rect.bottom).kill()	

				
	if countdown > 0:
		draw_text('GET READY!!', font40, white, int(screen_width / 2 - 110), int(screen_height / 2 + 50))
		draw_text(str(countdown), font40, white, int(screen_width / 2 - 10), int(screen_height / 2 + 100))
		count_timer = pygame.time.get_ticks()
		if count_timer - last_count > 1000:
			countdown -= 1
			last_count = count_timer



	explosion_group.update()	

	spaceship_group.draw(screen)
	bullet_group.draw(screen)
	alien_group.draw(screen)
	alien_bullet_group.draw(screen)
	explosion_group.draw(screen)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONDOWN and game_over == -1 or game_over == 1:
			game_over = 0
			spaceship.reset(int(screen_width / 2), screen_height - 100, 3)

				


	pygame.display.update()		

pygame.quit()			