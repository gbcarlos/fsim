# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 19:17:08 2020

@author: TUB ILR F3 - FLUGSIMULATIONSTECHNIK - CodeSnipetCollection by C.Berth and M.Bormann
BSP: Nummerische Integration, Bewegungsgleichungen, Punktmassemodell, 3 DOF, Multidrone



"""

import pygame
import pygame.gfxdraw
import time
import random
import sys
import math
import random as rd




pygame.init()

Time = 0.0

display_width = 1000
display_height = 800

# Define some colors
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

drone_width = 73
drone_height = 70
gravity_earth = 9.81  #in m/s²
drone_mass = 0.1      #in kg
Weight = drone_mass* gravity_earth


Xdd0 = 0.0          #Initial Acceleration in X Direction in m/s²    - "d" means dot here 
Ydd0 = 0.0          #Initial Acceleration in Y Direction in m/s²
Zdd0 = 0.0          #Initial Acceleration in Z Direction in m/s²

Xd0 = 0.0           #Initial Velocity in X Direction in m/s
Yd0 = 0.0           #Initial Velocity in Y Direction in m/s
Zd0 = 0.0           #Initial Velocity in Z Direction in m/s

X0 = 0.0            #Initial Position in X Direction in m
Y0 = 400.0            #Initial Position in Y Direction in m
Z0 = 47.0            #Initial Position in Z Direction in m


X = 0.0
Xd = 0.0
Xdd = 0.0

Y = 0.0
Yd = 0.0
Ydd = 0.0

Z = 0.0
Zd = 0.0
Zdd = 0.0

#Forces
FThrustX = 0.0      #Initial Thrust in X Direction in N
FThrustY = 0.0      #Initial Thrust in Y Direction in N
FThrustZ = 0.0      #Initial Thrust in Z Direction in N


Fx = 0.0            #Combined Force in X Direction
Fy = 0.0            #Combined Force in Y Direction
Fz = 0.0            #Combined Force in Z Direction

#random number generation
#roll = random.randrange(20,60)

#Init Pygame Display, WindowText, Clock
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Find Home')
clock = pygame.time.Clock()

#Drone Sprite Image Load Function
droneImg = pygame.image.load('DJI.png')

#pos2 = (300, 731)
pause = False

#waypoints



wp = [(880,16),(780,16),(780,716),(680,716),(680,16),(580,16),(580,716),(480,716),(480,16),(380,16),(380,716),(280,716),(280,16)]



# =============================================================================
# Class for other drones
# =============================================================================

class dronesim:
    def __init__(self,Self,dX,dY,ddX,ddY,X1,Y1,wp):
        self.Xself = wp[Self][0]
        self.Yself = wp[Self][1]  
        self.oself = Self
        self.dX = dX
        self.dY = dY
        self.ddX = ddX
        self.ddY = ddY
        self.Vel = (dX,dY)
        self.Acc = (ddX,ddY)
        self.X1 = X1          #PosX of Masterdrone
        self.Y1 = Y1          #PosX of Masterdrone



#==============================================================================
# Direction finding and Pyhsics
# =============================================================================        
        
        
       
    def Thrust(self,Self, Weight, wp, dtime):
        drone_mass = 0.1
        

        Ri = 1
        if self.oself > (len(wp)/2):
            Ri = -1   
        l = Self + Ri
        
        
        FXThrust = 0
        FYThrust = 0
        
       
        if  self.Xself > wp[l][0]:
            FXThrust = -35
            
        elif self.Xself < wp[l][0]:
            FXThrust = 35  
            
        
        if self.Yself > wp[l][1]:
            FYThrust = Weight + 35
            
        if self.Yself < wp[l][1]:
            FYThrust = Weight - 35 
        

		# Physics


        FDragX = self.dX * 0.5
        FDragY = self.dY * 0.5
        
            
            
        Fx = FXThrust - FDragX
        Fy = -FYThrust  + Weight - FDragY
        

    
        self.ddX = Fx/drone_mass  
        self.ddY = Fy/drone_mass     
        
        self.dX = self.dX + (self.ddX * dtime)
        self.dY = self.dY + (self.ddY * dtime) 
        
        self.Xself  = self.Xself  + (self.dX *  dtime)  
        self.Yself  = self.Yself  + (self.dY *  dtime)
        
        Pos = (self.Xself,self.Yself,Ri)
        
        return Pos
        
        
        



#######
def things(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])
#######


def drone(x,y):
    gameDisplay.blit(droneImg,(x,y))
 

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text, PosX, PosY):
    largeText = pygame.font.Font('freesansbold.ttf',30)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((PosX),(PosY))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

    time.sleep(2)

    game_loop()

#Draw Vectors to Screen Object    
def draw2DVectors(posx,posy,vvaluex,vvaluey):
    pygame.draw.line(gameDisplay, BLACK, [posx, posy], [posx, posy-vvaluey], 1)
    pygame.draw.line(gameDisplay, BLACK, [posx, posy], [posx + vvaluex, posy], 1)
    
def drawSpeedVectors(posx,posy,vvaluex,vvaluey):
    pygame.gfxdraw.line(gameDisplay, posx,posy,posx+vvaluex,posy+vvaluey,RED)

#Indicate Crash on Screen Object
def crash():
    message_display('You Crashed', 200 , 100)

# Display Text on Screen Object    
def displayMSG(value,ttext,posx,posy):
    myFont = pygame.font.SysFont("Verdana", 12)
    Label = myFont.render(ttext, 1, black)
    Value = myFont.render(str(value), 1, black)
    gameDisplay.blit(Label, (posx, posy))
    gameDisplay.blit(Value, (posx + 100, posy))

#First Iteration Calculation (Start Values)

#Integration Function Object (Rect Rule)
def Integration_Rect(IntVal, deltaTime):
    Integral = IntVal * deltaTime
    return Integral



#Equation of Motion Object
def EqoM(dTime):
    global X, Y, Z, Xd, Yd, Zd, Xdd, Ydd, Zdd, Xd0, Yd0, Zd0, X0, Y0 ,Z0
    
    Xd = Xd + Integration_Rect(Xdd, dTime) 
    X  = X  + Integration_Rect(Xd, dTime)  + X0
    Yd = Yd + Integration_Rect(Ydd, dTime) 
    Y  = Y  + Integration_Rect(Yd, dTime)  + Y0
    Zd = Zd + Integration_Rect(Zdd, dTime)
    Z  = Z  + Integration_Rect(Zd, dTime)  + Z0
    
    #Min and Max Height of Drone
    if Z < 47:
        Z = 47
        Zd = 0
    if Z > 100:
        Z = 100
        Zd = 0
        
       
    
    
    X0 = 0.0
    Y0 = 0.0
    Z0 = 0.0
    Xd0 = 0.0
    Yd0 = 0.0
    Zd0 = 0.0
 
def CalcXForces():
    global Fx, Fy,Fz,Xd,Yd,Zd, Xdd, Ydd, Zdd, Xdd0, Ydd0,Zdd0, FThrustX, FThrustY, FThrustZ, Weight
    
    FDragX = Xd* 0.5
    FDragY = Yd* 0.5 
    FDragZ = Zd* 0.5
    
    
    
    
    Fx = FThrustX - FDragX


    Fy = -FThrustY - FDragY + Weight


    Fz = FThrustZ - FDragZ
        
    
    
    Xdd = Fx/drone_mass + Xdd0
    Ydd = Fy/drone_mass + Ydd0
    Zdd = Fz/drone_mass + Zdd0
    
    
    
    Xdd0 = 0.0
    Ydd0 = 0.0
    Zdd0 = 0.0
    




# Erstelle ein Haus
def Haus():
    hpx = rd.  randint(320,980)  
    hpy = rd.  randint(20,800)
    h= (hpx,hpy,10,10)
    return h


# Euler Abstand
def Abstand(h,X,Y):
    Abx =((X+70)-(h[0]+5))**2
    Aby =((Y+35)-(h[1]+5))**2
    Abstand = math.sqrt((Abx)+(Aby))
    return Abstand

# Unpause game
def unpause():
    global pause
    pause = False
 

# Game Pause    
def paused():

    largeText = pygame.font.SysFont("comicsansms",15)
    TextSurf, TextRect = text_objects(" Found Home Press C to continue and try again", largeText)
    TextRect.center = ((display_width/2),(display_height/4))
    gameDisplay.blit(TextSurf, TextRect)
    

    while pause:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        #gameDisplay.fill(white)
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    pygame.draw.rect(gameDisplay, WHITE,[302,0,700,800])
                    unpause()
        

        pygame.display.update()
        clock.tick(15)          




#Main Loop Object    
def game_loop():
    global X, Y, Z, FThrustX, FThrustY,FThrustZ, FDragY,Weight, Time,pause
    
    
# ==========================================================================================================================================================
# Set Starting Positions
# ==========================================================================================================================================================
    
    #Start Masterdrone
    X = (display_width * 0.88)
    Y = (display_height * 0.395)
    
    #Startingpoint drone 2
    #d2 = 12
    
    #drone2 = dronesim(d2, Xd0, Yd0, Xdd0, Ydd0, X, Y,wp)
    
    
    
    #Startingpoint drone 3
    #d3 = 7
    
    #drone3 = dronesim(d3, Xd0, Yd0, Xdd0, Ydd0, X, Y,wp)
    
    
    i = 0
    j = i+1
    
# ==========================================================================================================================================================
#Main game Loop
# ==========================================================================================================================================================
    
    #Display Background Fill
        
    gameDisplay.fill(white)

    FThrustY =  Weight
    
    gameExit = False
    
    while not gameExit:
        dt = clock.tick(60)
        Time = (Time + dt)
        #Event Checker (Keyboard, Mouse, etc.)
        for event in pygame.event.get():
            pressed = pygame.key.get_pressed()
           

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            
# =============================================================================
# Flight  and Game Controls            
# =============================================================================
            if pressed[pygame.K_w]:
                    FThrustZ = 35
            elif pressed[pygame.K_s]:
                    FThrustZ = -35
            if pressed[pygame.K_r]:
                #Display Background Fill
                gameDisplay.fill(white)
            if pressed[pygame.K_p]:
                pause = True
                paused()
                
            if pressed[pygame.K_h]:
                 h = Haus()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()    
            
            
# =============================================================================
# Calculation of Forces                    
# =============================================================================
        
        j = i+1
        
        
        wayp = wp[i][0]
        wayn = wp[j][0]
        Last = 0
        
        if Z > 47 :
            
            
            Zp = Z -47
            
            Sight_zp = Zp/ math.cos(math.radians(20))

            if i == 0 :
                wayp = wp[i][0] - Sight_zp
            #print (wp[i][0]-wp[j][0])
            #elif i == 1:
             #   wayp = wp[i][0] - Sight_zp*(i+2)+10
            elif (wayp-wayn)==0:
                Last = Sight_zp*(i+2)
                wayp = wp[i][0]- Last
            elif (wayp-wayn)!=0:
                wayp = wp[i][0]- Sight_zp*(i+1)
                
                

        if X < wayp:
            FThrustX = 35
        elif X > wayp:
            FThrustX = -35
        if Y < wp[i][1]:
            FThrustY = -35 + Weight
        elif Y > wp[i][1]:
            FThrustY = 35 + Weight
            
        if (X - wayp)**2 < 0.2 :
            X = wayp
            
        if (Y - wp[i][1])**2 < 0.2 :
            Y = wp[i][1]
            
        if X == wayp and Y == wp[i][1]:
            i = i+1
            
            
            
            
        
        CalcXForces()
        EqoM(dt/1000)
        
        #Resesting the Thrust        
        
        FThrustX = 0
        FThrustY = Weight
        FThrustZ = 0
        
        
        # =============================================================================
        # Move Masterdrone 
        # =============================================================================
        
        #Sight Masterdrone
        Sight_r = Z / math.cos(math.radians(20))
        pygame.draw.circle(gameDisplay, GREEN ,(X+70,Y+35), radius = Sight_r ,width= 1000)
        if Zd < 0 and Xd < 0.01 and Yd < 0.01:
            pygame.draw.circle(gameDisplay, WHITE ,(X+70,Y+35), radius = Sight_r+1 ,width= 2)
        Sight = (Sight_r*Sight_r)* math.pi
        
        
        #Draw Drone 
        pygame.draw.line(gameDisplay,BLACK,(X+60,Y+25),(X+80,Y+45),width =2)
        pygame.draw.line(gameDisplay,BLACK,(X+60,Y+45),(X+80,Y+25),width =2)
        
        
        
        #Draw Home if Exists
        try:
            
          pygame.draw.rect(gameDisplay,WHITE,h,width = 1)
          pygame.draw.line(gameDisplay,WHITE,(h[0],h[1]),(h[0]+9,h[1]+9),width = 1)
          pygame.draw.line(gameDisplay,WHITE,(h[0],h[1]+9),(h[0]+9,h[1]),width = 1)
          Gef=Abstand(h,X,Y)
          
        except:
            pass
        
        # =============================================================================
        # Move other drones               
        # =============================================================================
                
        try:
            #Move Drone 2
            Pos = drone2.Thrust(d2,Weight,wp,dt/1000) 
            # Pos[0] X-Position
            # Pos[1] Y-Position
            # Pos[2] Direction the drone is flying
           
            
            pygame.draw.circle(gameDisplay, GREEN ,(Pos[0]+70,Pos[1]+35), radius = Sight_r ,width= 1000)
            pygame.draw.line(gameDisplay,BLACK,(Pos[0]+60,Pos[1]+25),(Pos[0]+80,Pos[1]+45),width =2)
            pygame.draw.line(gameDisplay,BLACK,(Pos[0]+60,Pos[1]+45),(Pos[0]+80,Pos[1]+25),width =2)
            
            
            if ((Pos[0] - wp[d2+ Pos[2]][0] )**2 < 1) and ((Pos[1] -wp[d2+ Pos[2]][1])**2 < 1) :
                d2 = d2 + Pos[2]
        except:
            pass




        #Move Drone 3
        try:
            Pos2 = drone3.Thrust(d3,Weight,wp,dt/1000)
            
            pygame.draw.circle(gameDisplay, GREEN ,(Pos2[0]+70,Pos2[1]+35), radius = Sight_r ,width= 1000)
            pygame.draw.line(gameDisplay,BLACK,(Pos2[0]+60,Pos2[1]+25),(Pos2[0]+80,Pos2[1]+45),width =2)
            pygame.draw.line(gameDisplay,BLACK,(Pos2[0]+60,Pos2[1]+45),(Pos2[0]+80,Pos2[1]+25),width =2)
            
            
            if ((Pos2[0] - wp[d3+ Pos2[2]][0] )**2 < 1) and ((Pos2[1] -wp[d3+ Pos2[2]][1])**2 < 1) :
                d3 = d3 + Pos2[2]
        except:
            pass
        
        try:
            pygame.draw.circle(gameDisplay, RED ,(wayp+70,wp[i][1]+35), radius = 20 )
            pygame.draw.circle(gameDisplay, WHITE ,(wayp+70,wp[i][1]+35), radius = 21,width= 2 )
        except:
            pass


        #Draw Home if Exists
        try:
            
          pygame.draw.rect(gameDisplay,WHITE,h,width = 1)
          pygame.draw.line(gameDisplay,WHITE,(h[0],h[1]),(h[0]+9,h[1]+9),width = 1)
          pygame.draw.line(gameDisplay,WHITE,(h[0],h[1]+9),(h[0]+9,h[1]),width = 1)
          Gef=Abstand(h,X,Y)
          Gef2 = Abstand(h,Pos[0],Pos[1])
          
        except:
            pass
        
        
        
# =============================================================================
# Interface Section       
# =============================================================================
        
        
        pygame.draw.rect(gameDisplay, (211,211,211),[0,0,300,800])
        pygame.draw.rect(gameDisplay, BLACK,[0,0,300,800],width= 3)
        
        
        #Position and Speed Messages on Screen
        displayMSG(' ','Position and Speed', 20, 20)
        displayMSG(X,'XPos',20,40)
        displayMSG(Y,'YPos',20,50)
        displayMSG(Z,'Height',20,60)
        
        displayMSG(Xd,'Vx',20,70)
        displayMSG(Yd,'Vy',20,80)
        displayMSG(Zd,'Vz',20,90)
        try:
            if h[0]> 0:
                displayMSG('','Created Home',20,460)
        except:
            pass
        
        
        
        #Performance Messages
        #displayMSG(' ','Performance Messages Masterdrone',20,110)
        displayMSG(Sight,'Sight in pix',20,130)
        displayMSG(Sight_r,'Radius of Sight',20,140)
        displayMSG(display_height,'dp_height',20,150)
        displayMSG(display_width,'dp_width',20,160)
        if Z == 100:
            displayMSG('','Max. Height reached',20,500)
        if Z == 50:
            displayMSG('','You can not fly lower ',20,540)
        
        
        # How to fly
        displayMSG(' ','Move Drone with arrow keys',20,300)
        displayMSG(' ','Rise Drone with W',20,320)
        displayMSG(' ','Lower Drone with S',20,340)
        displayMSG(' ','Create a new home with H ',20,360)
        displayMSG(' ','Display reset with R  ',20,380)
        displayMSG(' ','Pause with P  ',20,400)
        
        
        
        

        # Pause if Home is found
        try:
            if Sight_r > Gef or Sight_r > Gef2:
                displayMSG(' ','Found Home',20,420)
                displayMSG(Time/1000.0,'Time',20,700)
                pause = True
                paused()
                h = Haus()
                Time = 0.0
                
        except:
            pass
        
        
        #Time Messages
        
        displayMSG(dt,'Frametime',20,690)
        displayMSG(Time/1000.0,'Time',20,700)
        
        
       
        
        #Draw Drone Object Vectors
        draw2DVectors(X + 70,Y + 35,(Xd/2), -(Yd/2))
        
        
        x = int(X)
        y = int(Y)
        xd = int(Xd/2)
        yd = int(Yd/2)
        
        
        drawSpeedVectors(x + 70,y + 35,xd,yd)
        #drawSpeedVectors(70,70,300,300)
    
        
            
        
            
        
        pygame.display.update()
        


#MAIN
game_loop()
pygame.quit()
sys.exit()