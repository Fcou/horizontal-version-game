# 导入包
# coding:utf-8
import pygame,easygui,os,sys
from pygame.locals import *

#创建游戏窗口
pygame.init()
canvas = pygame.display.set_mode((1200, 700), FULLSCREEN)
canvas.fill([255, 255, 255])
pygame.display.set_caption("简陋横版游戏")

# 资源导入
bg = pygame.image.load('img/bg.png')
heroR1 = pygame.image.load('img/heroR1.png')
heroR2 = pygame.image.load('img/heroR2.png')
heroR1L = pygame.image.load('img/heroR1L.png')
heroR2L = pygame.image.load('img/heroR2L.png')
heroU = pygame.image.load('img/heroU.png')
heroUL = pygame.image.load('img/heroUL.png')
heroD = pygame.image.load('img/heroD.png')
heroS = pygame.image.load('img/heroS.png')
wallLeft = pygame.image.load('img/wall1.png')
wallCenter = pygame.image.load('img/wall2.png')
wallRight = pygame.image.load('img/wall3.png')
water = pygame.image.load('img/water.png')
stone = pygame.image.load('img/stone.png')
boat = pygame.image.load('img/boat1.png')
box1 = pygame.image.load('img/box1.png')
box2 = pygame.image.load('img/box2.png')
start = pygame.image.load('img/start.png')
over = pygame.image.load('img/over.png')
again = pygame.image.load('img/again.png')
top = pygame.image.load('img/top.png')
lifeTop = pygame.image.load('img/lifeTop.png')
foodTop = pygame.image.load('img/foodTop.png')
jadeTop = pygame.image.load('img/jadeTop.png')

# 英雄类
class Hero():
    # 英雄的属性
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 100
        self.height = 150
        self.n = 1    #用于切换图片
        # 控制行走动作切换
        self.flagW = False
        # 控制站立动作切换
        self.flagS = True
        # 控制左右动作切换
        self.flagRight = True
        # 控制跳跃动作切换
        self.flagJ = False
        # 控制跳跃的变量
        self.jumpVel = 0
        self.base = 500
        # 控制碰撞后动作改变
        self.flagHit = False

    # 站立动作方法
    def stand(self):
        if self.flagS:
            canvas.blit(heroS, (self.x, self.y))

    # 自由下落方法
    def down(self):
        if self.flagHit or self.flagJ:
            return
        if self.y < 500:
            self.y = self.y + 15

    def move(self,event):
        if event.type == KEYDOWN:
            if event.key == K_UP:
                if not self.flagJ:
                    self.flagW = False
                    self.flagS = False
                    self.flagJ = True
                    self.flagHit = False
                    self.jumpVel = -20
            # 向右移动
            if event.key == K_RIGHT:
                if not self.flagJ:
                    self.flagW = True
                    self.flagS = False
                    self.flagHit = False
                    self.flagRight = True
                self.x = self.x + 5
                if self.x > 1000:
                    self.x = self.x - 5
            # 向左移动
            elif event.key == K_LEFT:
                if not self.flagJ:
                    self.flagW = True
                    self.flagS = False
                    self.flagRight = False
                    self.flagHit = False
                self.x = self.x - 5
                if self.x <= 0:
                    self.x = self.x + 5
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                if not self.flagJ:
                    self.flagW = False
                    self.flagS = True
                    self.flagHit = False
            if event.key == K_LEFT:
                if not self.flagJ:
                    self.flagW = False
                    self.flagS = True
                    self.flagHit = False

    def out(self):
        if self.x >= 0:
            self.x = 0
        if self.x < -2393:
            self.x = -2393

    def walk(self):
        if self.flagW:
            if self.n % 2 == 0:   #分类，轮流选择
                if self.flagRight:
                    canvas.blit(heroR1, (self.x, self.y))
                else:
                    canvas.blit(heroR1L, (self.x, self.y))
            else:
                if self.flagRight:
                    canvas.blit(heroR2, (self.x, self.y))
                else:
                    canvas.blit(heroR2L, (self.x, self.y))
            self.n = self.n + 1

    # 跳跃动作方法
    def jump(self):
        if self.flagHit:
            self.flagJ = False
            self.flagW = False
            self.flagS = True
            return
        if self.flagJ:
            if self.flagRight:
                canvas.blit(heroU, (self.x, self.y))
            else:
                canvas.blit(heroUL, (self.x, self.y))   #选好跳跃图片
                
            if self.jumpVel < 0:
                self.jumpVel += 3
            elif self.jumpVel >= 0:
                self.jumpVel += 4    
            self.y += self.jumpVel 
            if self.y > self.base:   #已下落到最底部，停止下落，站立
                self.y = self.base
                self.jumpVel = 0.0
                self.flagJ = False
                self.flagW = False
                self.flagS = True

#     # 是否碰撞到其他物品
#     def hit(self, other):
#         if self.x + self.width >= other.x and self.x < other.x + other.width:
#             #如果从上到下碰撞,英雄的改变
#             if self.y + self.height - 10  <= other.y:  
#                 self.y = other.y    
#                 self.flagS = True
#                 self.stand()
#             #如果从下到上碰撞,英雄的改变
#             if self.y >=  other.y + other.height:
#                 self.flagJ = True
#                 self.jumpVel = 0
#                 self.jump()
#                 
#             return True
#         return False
                
# 背景类
class Sence():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        self.y = -hero.y - 100   # 与英雄上下移动方向相反，上面留100像素空间，防止英雄上挑超出背景
        canvas.blit(bg, (self.x, self.y))
    def move(self,event):        # 侧重于左右移动
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                self.x = self.x - 10
            elif event.key == K_LEFT:
                if self.x != 0:
                    self.x = self.x + 10
    def out(self):
        if self.x >= 0:    #若大于0，则窗口会出现没有背景的区域
            self.x = 0
        if self.x < -2393: #若小于-2400，则窗口会出现没有背景的区域
            self.x = -2393

# 其他物品类
class Obj():
    def __init__(self, x, y, width, height, img, box='boom'):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.img = img
        self.bgX = x
        self.bgY = y
        self.box = box

    def draw(self):
        self.y = sence.y + self.bgY
        canvas.blit(self.img, (self.x, self.y))

    def move(self):
        self.x = sence.x + self.bgX
        self.y = sence.y + self.bgY

    def hit(self, c):  #这个方法太蠢了
        return c.x > self.x - c.width + 50 and c.x < self.x + self.width - 50 

# 英雄碰撞检测
# def checkHitOther():
#     global hero,state,life
#     hero.hit(wallA)
#     for obj in objs:
#         hero.hit(obj)
#     if hero.hit(wallW):
#         life = life - 1
#         state = 'AGAIN'
#     for box in boxes:
#         if hero.hit(box):
#             box.img = box2
#             if k.box == 'get':
#                     jade = jade + 1
#                     box.box = 'null'
#             elif box.box == 'null':
#                 pass
#             else:
#                 life = life - 1
#                 k.box = 'null'
#                 state = 'AGAIN'
            
           
# 碰撞检测（蠢）
def checkHit():
	global state, life, jade
	if wallA.hit(hero):
		if hero.y + hero.height >= wallA.y  and hero.y < wallA.y:
			hero.flagHit = True
			hero.y = hero.y - 10
		if hero.y >= wallA.y and hero.x <= wallA.width:
			hero.flagHit = True
			hero.x = hero.x + 20
	for j in objs:
		if j.hit(hero):
			if hero.y + hero.height >= j.y and hero.y + hero.height <= j.y + 50:
				hero.flagHit = True
				hero.y = hero.y - 10
				print(216, hero.flagHit)
			if j == wallB:
				if hero.x + hero.width >= j.x and hero.y + hero.height >= j.y + 50 and hero.y <= j.y + j.height - 50:
					hero.x = hero.x - 20
	# 碰撞水
	if wallW.hit(hero):
		if hero.y + hero.height >= wallW.y + 100 and hero.y + hero.height <= wallW.y + 200:
			life = life - 1
			state = 'AGAIN'
	# 碰撞箱子
	for k in boxes:
		if k.hit(hero):
			if hero.y >= 500:
				k.img = box2
				if k.box == 'get':
					jade = jade + 1
					k.box = 'null'
				elif k.box == 'null':
					pass
				else:
					life = life - 1
					k.box = 'null'
					state = 'AGAIN'

# 组件绘制
def comPaint():
	wallA.draw()
	wallW.draw()
	for o in objs:
		o.draw()
	for b in boxes:
		b.draw()


# 组件移动
def comMove():
	wallA.move()
	wallW.move()
	for o in objs:
		o.move()
	for b in boxes:
		b.move()


# 写文字
def fillText(text, position, size, view=canvas):
	my_font = pygame.font.Font("my_font/font1.ttf", size)
	text = my_font.render(str(text), True, (255, 255, 255))
	view.blit(text, position)


# 开城门
def open():
	global food
	if food >= 50:
		food = 0
		easygui.msgbox('成功进入良渚内城')
	else:
		easygui.msgbox('您的余粮不够，请使用古玉去粮仓置换')

# 用宝石买粮草
def buy():
	global food, jade
	easygui.msgbox('欢迎来到粮仓，此处可以使用玉石置换粮食')
	f = easygui.enterbox('请输入您的玉石数量进行粮食换购(一块玉石可以换购30斤粮食)')
	if (f == '3' or f == '2' or f == '1') and int(f) <= jade:
		food = food + 30 * int(f)
		jade = jade - int(f)
		easygui.msgbox('换购成功')
	else:
		easygui.msgbox('换购失败')


# 创建变量，变量初始化
# 场景绘制
sence = Sence(0, -100)
hero = Hero(10, 0)
wallA = Obj(0, 330, 461, 968, wallLeft)
wallB = Obj(1000, 400, 280, 439, wallCenter)
wallW = Obj(1280, 380, 1192, 465, water)
wallC = Obj(2472, 400, 1183, 437, wallRight)
stoneA = Obj(480, 350, 142, 103, stone)
stoneB = Obj(700, 500, 142, 103, stone)
stoneC = Obj(900, 350, 142, 103, stone)
stoneD = Obj(600, 700, 142, 103, stone)
stoneE = Obj(800, 700, 142, 103, stone)
stoneF = Obj(480, 900, 142, 103, stone)
stoneG = Obj(700, 1100, 142, 103, stone)
boatA = Obj(1450, 400, 310, 158, boat)
boatB = Obj(1950, 400, 310, 158, boat)
# 物品列表
objs = [wallB, wallC, stoneA, stoneB, stoneC, stoneD, stoneE, stoneF, stoneG, boatA, boatB]     
# 创建箱子对象， 箱子不需要重置
boxA = Obj(1300, 1230, 105, 77, box1)
boxB = Obj(1800, 1230, 105, 77, box1, 'get')
boxC = Obj(2300, 1230, 105, 77, box1)
boxD = Obj(2800, 1230, 105, 77, box1, 'get')
boxE = Obj(3000, 1230, 105, 77, box1, 'get')
# 箱子列表
boxes = [boxA, boxB, boxC, boxD, boxE]

# 变量初始化
state = 'START'  #游戏状态
life = 3         #玩家生命值
food = 0         #粮食超过50才能过关
jade = 0         #收集的宝石数量

#对应状态写对应组件逻辑
def controlStates():
    global state
    if state == 'START':
        canvas.blit(start, (0, 0))
    elif state == 'RUNNING':
        sence.draw()   #背景绘制
        sence.out()    #背景越界限制 
        comPaint()     #绘制其他组件
        hero.stand()   #通过flag标志来确定英雄目前的状态（唯一）
        hero.down()
        hero.walk()
        hero.jump()
        checkHit()
#         checkHitOther()
        canvas.blit(top, (640, 0))    #绘制生命值，宝石数，粮食数量
        fillText(life, (860, 0), 40)
        fillText(jade, (1010, 0), 40)
        fillText(food, (1140, 0), 40)
        if life <= 0:
            state = 'OVER'
    elif state == 'AGAIN':
        canvas.blit(again, (0, 0))
        fillText(life, (290, 300), 200)
    elif state == 'OVER':
        canvas.blit(over, (0, 0))
        
#处理交互事件        
def handleEvent():
    global state,hero,sence
    for event in pygame.event.get():
        #退出监听
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            sys.exit() 
        if state == 'RUNNING':
            hero.move(event)
            sence.move(event)
            comMove()
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if state == 'START':
                state = 'RUNNING'
            if state == 'AGAIN':
                state = 'RUNNING'
            pos = pygame.mouse.get_pos()
            if sence.x <= -2300 and sence.y <= -600 and pos[0] > 800 and pos[1] >= 500:
                open()
            if sence.x <= -2300 and sence.y >= -200 and pos[0] >= 800 and pos[1] <= 200:
                buy()
                
while True:
    controlStates()           #分为四种状态，各自处理
    handleEvent()             #处理交互事件
    pygame.display.update()   #界面更新 
    pygame.time.delay(1)     #将暂停一段给定的毫秒数