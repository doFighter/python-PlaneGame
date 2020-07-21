import random
import pygame

# 定义屏幕大小的常量
SCREEN_RECT = pygame.Rect(0,0,380,600)
# 定义刷新的频率
FRAME_PER_SEC = 60
# 定义敌机出现的定时器常量
CREATE_ENEMY_EVENT = pygame.USEREVENT
# 定义英雄发射子弹事件
HERO_FIRE_EVENT = pygame.USEREVENT + 1
# 定义碰撞事件定时器
COLLIDE_EVENT = pygame.USEREVENT + 2
# 击毁普通飞机分数
DESTROY_COMMONPLANE = 5

class GameSprite(pygame.sprite.Sprite):
	"""飞机大战游戏精灵"""

	def __init__(self,image_name,speed = 1):
		# 调用父类的初始化方法
		super().__init__()

		# 定义对象的属性
		self.image = pygame.image.load(image_name)
		self.rect = self.image.get_rect()
		self.speed = speed


	def update(self):
		# 在屏幕的垂直方向上移动
		self.rect.y += self.speed

class Background(GameSprite):
	""""背景图片精灵"""
	def __init__(self,is_alt=False):
		# 创建背景精灵
		super(Background, self).__init__("./images/background.png")
		if is_alt:
			self.rect.y = -self.rect.height
	# 重写父类的 update 方法
	def update(self):
		# 1.调用父类的update方法，使其进行上下移动
		super(Background, self).update()
		# 2.判断是否移出屏幕
		if self.rect.y >= SCREEN_RECT.height:
			self.rect.y = -self.rect.y

class Enemy(GameSprite):
	"""敌机类"""
	def __init__(self):
		# 1.使用父类方法，选取特定图片，创建敌机类
		super(Enemy, self).__init__("./images/enemy1.png")
		# 2.设置敌机初始速度
		self.speed = random.randint(1,3)
		# 3.设置敌机随机出现的位置
		self.rect.bottom = 0
		MAX_X = SCREEN_RECT.width - self.rect.width
		self.rect.x = random.randint(0,MAX_X)

	def update(self):
		# 1.设置敌机在屏幕上移动
		super(Enemy, self).update()
		# 2.判断敌机是否飞出屏幕，
		if self.rect.y >= SCREEN_RECT.height:
			# print("敌机飞出了窗口，需要销毁。。。")
			self.kill()

	def __del__(self):
		# print("敌机销毁 %s" % self.rect)
		pass

class Hero(GameSprite):
	"""英雄精灵类"""
	def __init__(self,flag = True):
		# 1.调用父类的方法，初始化image和speed
		if flag:
			super(Hero, self).__init__("./images/me1.png",0)
		else:
			super(Hero, self).__init__("./images/me_destroy_2.png",0)
		# 2.设置英雄战机的初始位置
		self.rect.centerx = SCREEN_RECT.centerx
		self.rect.bottom = SCREEN_RECT.bottom - 120
		self.bullets = pygame.sprite.Group()

	def update(self):
		# 英雄精灵水平移动
		self.rect.x += self.speed
		# 设置英雄精灵的边界
		if self.rect.x < 0:
			self.rect.x = 0
		elif self.rect.right > SCREEN_RECT.right:
			self.rect.right = SCREEN_RECT.right

	def fire(self):
		for i in (0,1,2):
			bullet = Bullet()
			bullet.rect.bottom = self.rect.y - i * 20
			bullet.rect.centerx = self.rect.centerx
			self.bullets.add(bullet)

	def destroy(self):
		self.__init__(False)

class Bullet(GameSprite):
	"""子弹精灵类"""
	def __init__(self):
		# 设置子弹图片和初始速度
		super(Bullet, self).__init__("./images/bullet1.png",-2)

	def update(self):
		super(Bullet, self).update()
		# 子弹飞出屏幕需要销毁
		if self.rect.bottom <= 0:
			self.kill()

	def __del__(self):
		# print("子弹被销毁。。。")
		pass

class Blast(GameSprite):
	"""战机爆炸类"""
	def __init__(self):
		super(Blast, self).__init__("./images/enemy1_down2.png",0)
		pygame.time.set_timer(COLLIDE_EVENT,50)

	def update(self):
		super(Blast, self).update()
		for even in pygame.event.get():
			if even.type == COLLIDE_EVENT:
				self.kill()

class Imageshow(pygame.sprite.Sprite):
	"""展示暂停或者死亡后应该显示的图片"""
	def __init__(self,flag = 1):
		self.flag = flag
		super().__init__()
		if flag == 1:
			self.image = pygame.image.load("./images/resume_nor.png")
			self.rect = self.image.get_rect()
		elif flag == 2:
			self.image = pygame.image.load("./images/gameover.png")
			self.image = pygame.transform.scale(self.image,(150,20))
			self.rect = self.image.get_rect()
		elif flag == 3:
			self.image = pygame.image.load("./images/again.png")
			self.image = pygame.transform.scale(self.image,(150,20))
			self.rect = self.image.get_rect()

	def update(self):
		if self.flag == 1:
			self.rect.centerx = SCREEN_RECT.centerx
			self.rect.centery = SCREEN_RECT.centery
		elif self.flag == 2:
			self.rect.centerx = SCREEN_RECT.centerx - 100
			self.rect.centery = SCREEN_RECT.centery
		elif self.flag == 3:
			self.rect.centerx = SCREEN_RECT.centerx + 100
			self.rect.centery = SCREEN_RECT.centery

