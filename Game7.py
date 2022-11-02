import pyxel
from random import randint as rn
import math as m





particles = []

def create_particle(x,y,size,color,speed):
    p = [x, y, m.cos(rn(0,640)/100)*speed, m.sin(rn(0,640)/100)*speed, size, color]
    particles.append(p)

class Player():
    def __init__(self):
        self.x, self.y = 0, 0
        self.vel = 1
        self.angle = 0
        self.shoot = 0
    def move(self):
        self.vx, self.vy = 0, 0


        if pyxel.btn(pyxel.KEY_D):
            self.vx += self.vel
        if pyxel.btn(pyxel.KEY_A):
            self.vx -= self.vel

        if pyxel.btn(pyxel.KEY_S):
            self.vy += self.vel
        if pyxel.btn(pyxel.KEY_W):
            self.vy -= self.vel
        
        if pyxel.btn(pyxel.KEY_E):
            if self.shoot == 0:
                self.shoot = 1
                for e in enemies:
                    if abs(pyxel.mouse_x-e.x) < 4 and abs(pyxel.mouse_y-e.y) < 4:
                        enemies.remove(e)
                        for i in range(40):
                            create_particle(e.x,e.y,rn(1,6),rn(0,2)+8,rn(1,20)/5)
        else:
            self.shoot = 0

        self.x += self.vx
        self.y += self.vy
            

    def draw(self):

        pyxel.blt(self.x-4,self.y-4,0,0,0,8,8,colkey=0)

class Enemy():
    def __init__(self,x,y):
        self.x, self.y = x, y

    def draw(self):
        pyxel.blt(self.x-4, self.y-4, 0, 8, 0, 8, 8, colkey=0)

    def move(self):
        ag = m.atan2(player.y-self.y, player.x-self.x)
        if rn(0,3): 
            self.x += int(m.cos(ag)*1.5)
            self.y += int(m.sin(ag)*1.5)

player = Player()
enemies = []
enemy_timer = 0        

class App:
    def __init__(self):
        pyxel.init(160, 120,title="   something",fps=60)

        self.res = pyxel.load("first.pyxres",tilemap=False,sound=False,music=False)
        self.enemy_timer = 0

        pyxel.run(self.update, self.draw)

        
    def update(self):


        player.move()

        self.enemy_timer += 2
        if self.enemy_timer > 600:
            self.enemy_timer = 0
            enemy = Enemy(rn(0,160),rn(0,120))
            enemies.append(enemy)

        for e in enemies:
            e.move()

        for p in particles:
            p[0] += p[2]
            p[1] += p[3]
            if p[2]>0.05:
                p[2] /= 1.01
            if p[3]>0.05:
                p[3] /= 1.01

            p[4] -= 0.05
            if p[1] > 120 or p[4] < 1:
                particles.remove(p)
        
        
        
    def draw(self):

        pyxel.cls(0)

        player.draw()

        '''for x in range(160):
            for y in range(120):
                if abs(pyxel.mouse_x-x) < 4 and abs(pyxel.mouse_y-y) < 4:
                    pyxel.pset(x,y,2)'''


        for e in enemies:
            e.draw()

        for p in particles:
            pyxel.circ(p[0],p[1],p[4],p[5])
            #pyxel.circb(p[0],p[1],p[4],4)
        

        pyxel.circ(150,10,8,6)

        pyxel.circb(150,10,8,3)
        ag = -m.pi/2+m.pi*2/600*self.enemy_timer
        pyxel.line(150,10,150+m.cos(ag)*8,10+m.sin(ag)*8,3)

        pyxel.blt(pyxel.mouse_x-4, pyxel.mouse_y-4, 0, 16, 0, 8, 8, colkey=0)


App()

