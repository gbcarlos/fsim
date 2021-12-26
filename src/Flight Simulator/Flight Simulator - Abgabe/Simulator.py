# -*- coding: utf-8 -*-
"""
Created on Sun Feb 14 17:55:56 2021

@author: RichR
"""

#Imports
import pygame, sys
from pygame.locals import *
import random, time
import numpy as np
import math as math
import pygame_menu

#Initializing 
pygame.init()
 
#Setting up FPS 
FPS = 60
clock = pygame.time.Clock()
 
#Creating colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 
#Other Variables for use in the program
SCREEN_WIDTH = 2000
SCREEN_HEIGHT =1000
posx=SCREEN_WIDTH /2
#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)
 
#Create a white screen 
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Flight Simulator")

# global variables
#state
x=np.zeros((4,1))
#control
u=np.zeros((2,1))
#altitude
h0=SCREEN_HEIGHT/2;
#Airbus Data
theta0=0
V=264
A=np.array([[-1.54508144736000,	-2.53353514538667,	-0.000163348494222222,	0],
                     [1,	-0.680192330400000,	-0.000281461400000000,	0],
                     [0,-0.000629749821760000,	-0.00501182880000000,	-0.000980665000000000],
                     [0,	0.380192330400000,	0.000281461400000000,	0]])
B=np.array([[0.113751187084520,	-1.80698945152000],
                      [-0.000498802081447004,	-0.811368432000000],
                      [0.00347692307692308,	-0.00195592066560000],
                      [0.000498802081447004,	0.0211368432000000]])
#load airbus picture
      
airbusImg=pygame.image.load('A300.png').convert_alpha()
airbusImg=pygame.transform.scale(airbusImg,(100,40))


#define statespace for cruise flight  
def ss(x,u):    
    #get statespace LB Cruise
    #system matrix
    #control matrix
    x_dot=np.matmul(A,x)+np.matmul(B,u)
    return x_dot
  
    # Runge Kutta 4. Ordnung Integration Statespace
def RK4(x,u,dt):    
      k1=ss(x,u);
      k2=ss(x+k1*dt/2,u);
      k3=ss(x+k2*dt/2,u);
      k4=ss(x+k3*dt,u);
      x_new=x+(dt/6)*(k1+2*k2+2*k3+k4);
      return x_new 
    
def plane_update(x,u,dt,h0):
    xnew=RK4(x,u,dt)
    Vnew=V+xnew[2]
    theta=(theta0+xnew[1]+xnew[3])
    Vx=math.cos(xnew[3]*np.pi/180)*Vnew
    Vy=math.sin(xnew[3]*np.pi/180)*Vnew
    posy=h0-dt*Vy
    return xnew,Vx,Vy,posy,theta
  
def plane_draw(posy,theta):
    rotiert = pygame.transform.rotate(airbusImg, theta)
    # Bestimmen der neuen Abmessungen (nach Rotation ändern sich diese!)
    groesse = rotiert.get_rect()
    # Ausgabe
    DISPLAYSURF.blit(rotiert, (posx - groesse.center[0],posy - groesse.center[1]))
                      
class Background():
      def __init__(self):
            self.bgimage = pygame.image.load('sky.jpg').convert()
            self.bg=pygame.transform.scale(self.bgimage,(2000,1000))
            self.rectBGimg = self.bgimage.get_rect()
 
            self.bgY1 = 0
            self.bgX1 = 0
 
            self.bgY2 = 0
            self.bgX2 = self.rectBGimg.width
         
      def update(self,speed):
        self.bgX1 -= speed
        self.bgX2 -= speed
        if self.bgX1 <= -self.rectBGimg.width:
            self.bgX1 = self.rectBGimg.width
        if self.bgX2 <= -self.rectBGimg.width:
            self.bgX2 = self.rectBGimg.width
             
      def render(self):
         DISPLAYSURF.blit(self.bg, (self.bgX1, self.bgY1))
         DISPLAYSURF.blit(self.bg, (self.bgX2, self.bgY2))  
         

 

# Display Text on Screen Object    
def displayMSG(value,ttext,posx,posy):
    myFont = pygame.font.SysFont("Verdana", 12)
    Label = myFont.render(ttext, 1, BLACK)
    Value = myFont.render(str(value), 1, BLACK)
    DISPLAYSURF.blit(Label, (posx, posy))
    DISPLAYSURF.blit(Value, (posx + 100, posy))

def game_loop():
  global A,B,x,u,h0
  #set up bg and game loop
  back_ground = Background()
  run=True
  #init
  dt=0.016;  
  #Game Loop
  while run:
      #Event Checker (Keyboard, Mouse, etc.)
      for event in pygame.event.get():  
          if event.type == pygame.QUIT: 
              run = False    
              pygame.quit() 
              quit()
          if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
              u[0]=u[0]-0.02
            if event.key == pygame.K_RIGHT:
              u[0]=u[0]+0.02
            if event.key == pygame.K_UP:
              u[1]=u[1]+0.5
            if event.key == pygame.K_DOWN:
              u[1]=u[1]-0.5
      #check input steuervariablen
      # Schub Vorgaben
      if u[0]<=-0.8:
        u=-0.8
      if u[0]>=0.2:
        u[0]=0.2
      # Elevator vorgaben
      if u[1]<=-10.0:
        u[1]=-10.0
      if u[1]>=10.0:
        u[1]=10.0
      #calculate physics       
      xnew,Vx,Vy,posy,theta=plane_update(x,u,dt,h0)
      #move background
      speed=Vx*dt
      back_ground.update(speed)
      back_ground.render()
      plane_draw(posy,theta)
      #update the state 
      x=xnew;
      h0=posy
      #Calculate 
        
      #Display Text Messages on Screen
      displayMSG(u[0],'thrust',20,30)
      displayMSG(u[1],'elevator in °',20,45)
      displayMSG(dt,'Frametime',20,60)
      displayMSG(theta*180/np.pi,'theta',20,75)
      displayMSG(x[1],'alpha',20,90)
      displayMSG(Vx,'Vx',20,105)
      displayMSG(h0,'höhe',20,120)
      displayMSG(Vy,'Vy',20,135)
      pygame.display.flip()
      pygame.display.update()
      dt = clock.tick_busy_loop(60)/1000
#create menu
def choose_aircraft(value, Aircraft):
    global A,B,V,theta0,airbusImg
    if value==1:
      print('A300 ready for flight')
    else:
      
      #Airbus Data
      theta0=4.67
      V=570
      A=np.array([[-1.54508144736000,	-2.53353514538667,	-0.000163348494222222,	0],
                           [1,	-0.680192330400000,	-0.000281461400000000,	0],
                           [0,-0.000629749821760000,	-0.00501182880000000,	-0.000980665000000000],
                           [0,	0.380192330400000,	0.000281461400000000,	0]])
      B=np.array([[0.113751187084520,	-1.80698945152000],
                            [-0.000498802081447004,	-0.811368432000000],
                            [0.00347692307692308,	-0.00195592066560000],
                            [0.000498802081447004,	0.0211368432000000]])
      #load airbus picture
      
      airbusImg=pygame.image.load('concorde.png').convert_alpha()
      airbusImg=pygame.transform.scale(airbusImg,(160,25)) 
      print('Concorde ready for flight')
    pass

def start_the_game():
    game_loop()
    pass
#menu loop
menu = pygame_menu.Menu(300, 400, 'Welcome',
                       theme=pygame_menu.themes.THEME_BLUE)

menu.add_text_input('Name :', default='John Doe')
menu.add_selector('Difficulty :', [('Airbus A300', 1), ('Concorde', 2)], onchange=choose_aircraft)
menu.add_button('Play', start_the_game)
menu.add_button('Quit', pygame_menu.events.EXIT)

menu.mainloop(DISPLAYSURF)