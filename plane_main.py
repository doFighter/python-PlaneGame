import pygame
from plane_sprites import *

class PlaneGame(object):
	"""飞机大战主游戏"""

	def __init__(self):
		# print("游戏初始化")
	# 	创建一个标识符，用于作为暂停或者死亡用
		self.flag = True
		self.pause = False
		self.score = 0
	# 	1.创建游戏的窗口
		self.screen = pygame.display.set_mode(SCREEN_RECT.size)
	# 	2.创建游戏的时钟
		self.clock = pygame.time.Clock()
	# 	3.调用私有方法，创建精灵和精灵组
		self.__create_sprites()
	# 	4.设置定时器，产生敌机
		pygame.time.set_timer(CREATE_ENEMY_EVENT,1000)
	# 	5.设置英雄发射子弹定时器
		pygame.time.set_timer(HERO_FIRE_EVENT,500)
		# 设置字体
		pygame.init()
		self.game_font = pygame.font.SysFont('华文行楷', 16, True)

	def __create_sprites(self):
		# 创建背景精灵
		bg1 = Background()
		bg2 = Background(True)
		self.back_group = pygame.sprite.Group(bg1,bg2)
		self.enemy_group = pygame.sprite.Group()
		# 创建英雄的精灵和精灵组
		self.hero = Hero()
		self.hero_group = pygame.sprite.Group(self.hero)
		# 创建敌机爆炸精灵
		self.enemy_collide_group = pygame.sprite.Group()
		# 创建暂停精灵
		self.imageShow = Imageshow()
		# 创建结束图片精灵
		self.restart = Imageshow(3)
		self.gameOver = Imageshow(2)
		self.restartAndOver_group = pygame.sprite.Group(self.restart,self.gameOver)


	def start_game(self):
		print("游戏开始")
		while True:
			# 1.设置刷新频率
			self.clock.tick(FRAME_PER_SEC)
			#2.事件监听
			self.__event_handler()
			#3.碰撞检测
			self.__check_collide()
			#4.更新/绘制精灵组
			self.__update_sprites()
			#5.更新显示
			pygame.display.update()

	# 写一个函数判断鼠标点击是否在指定范围内
	def __is_rect(self, pos, rect):
		x, y = pos
		rx, ry, rw, rh = rect
		if (rx <= x <= rx + rw) and (ry <= y <= ry + rh):
			return True
		return False

	# 事件监听方法
	def __event_handler(self):
		for event in pygame.event.get():
			#判断是否是 pygame 中的退出方法
			if event.type == pygame.QUIT:
				PlaneGame.__game_over()
			elif event.type == CREATE_ENEMY_EVENT:
				enemy = Enemy()
				self.enemy_group.add(enemy)
			elif event.type == HERO_FIRE_EVENT and self.flag:
				self.hero.fire()
			elif self.flag and (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE or event.type == pygame.MOUSEBUTTONDOWN):
				self.showImage_group = pygame.sprite.Group(self.imageShow)
				self.pause = not self.pause
			elif not self.flag and event.type == pygame.MOUSEBUTTONDOWN:
				if self.__is_rect(event.pos,self.restart.rect):
					game = PlaneGame()
					game.start_game()
				if self.__is_rect(event.pos,self.gameOver.rect):
					self.__game_over()
		key_group = pygame.key.get_pressed()
		if self.flag and key_group[pygame.K_RIGHT]:
			self.hero.speed = 2
		elif self.flag and key_group[pygame.K_LEFT]:
			self.hero.speed = -2
		else:
			self.hero.speed = 0

	# 碰撞检测方法
	def __check_collide(self):
		# 1.子弹摧毁敌机
		enemy_collide = pygame.sprite.groupcollide(self.enemy_group, self.hero.bullets, True, True)
		if enemy_collide:
			for balst_enemy in enemy_collide:
				self.score += DESTROY_COMMONPLANE
				rect = balst_enemy.rect
				blast = Blast()
				blast.rect.centerx = rect.centerx
				blast.rect.centery = rect.centery
				self.enemy_collide_group.add(blast)
		if self.flag:
			# 2.敌机碰撞英雄机
			hero_collide = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)
			if len(hero_collide) > 0:
				self.hero.destroy()
				self.flag = False

			# PlaneGame.__game_over()


	# 更新绘制精灵组方法
	def __update_sprites(self):
		if not self.pause:
			self.back_group.update()
			self.back_group.draw(self.screen)
		# 	更新敌机
			self.enemy_group.update()
			self.enemy_group.draw(self.screen)
			# 更新英雄精灵
			self.hero_group.update()
			self.hero_group.draw(self.screen)
			# 更新子弹精灵
			self.hero.bullets.update()
			self.hero.bullets.draw(self.screen)
			# 更新爆炸精灵
			self.enemy_collide_group.update()
			self.enemy_collide_group.draw(self.screen)
			# 绘制游戏得分
			self.screen.blit(self.game_font.render(u'当前得分：%d' % self.score, True, [255, 0, 0]), [20, 20])
			# 更新重新开始以及结束按钮
			if not self.flag:
				self.restartAndOver_group.update()
				self.restartAndOver_group.draw(self.screen)
		elif self.pause:
			self.showImage_group.update()
			self.showImage_group.draw(self.screen)
	# 游戏结束   由于不需要使用其他的对象，所以可以将该方法写成静态方法
	@staticmethod
	def __game_over():
		print("游戏结束")
		pygame.quit()
		exit()

if __name__ == '__main__':
	# 创建游戏对象
	game = PlaneGame()
	# 启动游戏
	game.start_game()
	# print(pygame.font.get_fonts())