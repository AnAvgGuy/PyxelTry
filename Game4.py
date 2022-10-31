import pyxel
#from random import randint as rn
#import math as m

MY_PI = 180

class Player():
    def __init__(self):
        self.x, self.y = 0, 0
        self.vel = 1.5
        self.angle = 0
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
        if not (self.vx == 0 and self.vy == 0):
            ag = pyxel.atan2(self.vy,self.vx)
            self.x += int(self.vel * pyxel.cos(ag))
            self.y += int(self.vel * pyxel.sin(ag))
    def draw(self):

        #pyxel.rect(self.x, self.y, 4, 4, 2)
        self.angle += 2
        a, b = self.x + 8*pyxel.cos(self.angle), self.y + 8*pyxel.sin(self.angle)
        c, d = self.x + 8*pyxel.cos(self.angle+MY_PI/3*2), self.y + 8*pyxel.sin(self.angle+MY_PI/3*2)
        e, f = self.x + 8*pyxel.cos(self.angle+MY_PI/3*4), self.y + 8*pyxel.sin(self.angle+MY_PI/3*4)

        pyxel.tri(a, b, c, d, e, f, 1)

class App:
    def __init__(self):
        pyxel.init(160, 120,title="   something",fps=60)
        
        self.player = Player()
        pyxel.run(self.update, self.draw)

    def update(self):
        self.player.move()


    def draw(self):
        pyxel.cls(0)
        self.player.draw()

App()
