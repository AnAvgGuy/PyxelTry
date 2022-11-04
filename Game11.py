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
        self.vel = 0.1
        self.angle = 0
        self.shoot = 0
        self.hp = 100
        self.kills = 0
        self.vx, self.vy = 0, 0

    def move(self):
        #self.vx, self.vy = 0, 0
        self.vx /= 1.05
        self.vy /= 1.05

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
                hit = 0
                for e in enemies:
                    if abs(pyxel.mouse_x-e.x) < 8 and abs(pyxel.mouse_y-e.y) < 8:

                        for i in range(10):
                            create_particle(e.x,e.y,rn(1,3),rn(0,2)+8,rn(1,8)/5)
                        e.hp -= rn(20,40)
                        if e.hp < 0:
                            enemies.remove(e)
                            for i in range(40):
                                create_particle(e.x,e.y,rn(1,6),rn(0,2)+8,rn(1,20)/5)
                            self.kills += 1
                            pyxel.play(2,rn(0,2)+3)
                        else:
                            pyxel.play(0,1)

                        hit = 1
                        break
                if hit == 0:
                    pyxel.play(1,2)

        else:
            self.shoot = 0

        self.x += int(self.vx*5)/5
        self.y += int(self.vy*5)/5
            

    def draw(self):

        #pyxel.blt(self.x-4,self.y-4,0,0,0,8,8,colkey=0)
        for x in range(8):
            for y in range(8):
                if rn(0,3)==0:
                    if m.sqrt((x-4)**2 + (y-4)**2) < 4:

                        pyxel.pset(self.x-4+x,self.y-4+y,7)

class Enemy():
    def __init__(self,x,y):
        self.x, self.y = x, y
        self.hp = 60
        self.warning = 100

    def draw(self):
        if self.warning:
            self.warning -= 1
            pyxel.blt(self.x-4, self.y-4, 0, 24, 0, 8, 8, colkey=0)
        else:
            pyxel.blt(self.x-4, self.y-4, 0, 8, 0, 8, 8, colkey=0)

    def move(self):
        ag = m.atan2(player.y-self.y, player.x-self.x)
        if rn(0,3): 
            self.x += int(m.cos(ag)*1.5)
            self.y += int(m.sin(ag)*1.5)
    def attack(self):
        global shake   

        if pyxel.frame_count%30 == 0:
            if abs(self.x-player.x) < 8 and abs(self.y-player.y) < 8:
                player.hp -= 8
                shake = 4


player = Player()
enemies = []
enemy_timer = 0     
global shake   
shake = 0

class App:
    def __init__(self):

        pyxel.init(160, 120,title="   something",fps=60)

        self.res = pyxel.load("first.pyxres",tilemap=False,sound=True,music=False)
        self.enemy_timer = 0
        self.timer_speed_inv_og = 400
        self.score = 0
        pyxel.run(self.update, self.draw)

        
    def update(self):


        
        if player.hp <= 0:
           self.score = str(player.kills*100)
        else:

            player.move()
            

            self.timer_speed_inv = self.timer_speed_inv_og - player.kills * 8
            if self.timer_speed_inv < 200:
                self.timer_speed_inv = 120


            self.enemy_timer += 2
            if self.enemy_timer > self.timer_speed_inv:
                self.enemy_timer = 0
                enemy = Enemy(rn(0,160),rn(0,120))
                enemies.append(enemy)

            for e in enemies:
                if not e.warning:
                    e.move()
                    e.attack()

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
        global shake   

        if player.hp <= 0:
            pyxel.cls(0)

            pyxel.text(80,60,"Score: " + str(self.score),7)
        else:
            if shake:
                shake -= 1
                pyxel.camera(rn(-2,2), rn(-1,1))
            else:
                pyxel.camera(0,0)
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
            


            pyxel.circb(150,10,8,3)
            ag = -m.pi/2+m.pi*2/self.timer_speed_inv*self.enemy_timer
            pyxel.line(150,10,150+m.cos(ag)*8,10+m.sin(ag)*8,3)
            pyxel.line(12,6,12+player.hp/5,6,8)
            pyxel.line(12,7,12+player.hp/5,7,8)
            pyxel.line(12,8,12+player.hp/5,8,8)

            for i in range(player.kills):
                pyxel.pset(12+((i*2)%24),10+2*int((i*2)/24),7)

            if self.timer_speed_inv <= 200 and pyxel.frame_count%12 <= 6:
                pyxel.text(60,8,"MADNESS",8)

            pyxel.blt(pyxel.mouse_x-4, pyxel.mouse_y-4, 0, 16, 0, 8, 8, colkey=0)


App()



