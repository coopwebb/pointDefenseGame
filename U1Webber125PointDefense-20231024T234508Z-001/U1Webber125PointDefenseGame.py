#Imports=========================================
import turtle as trtl
import random as rand
import time

#Functions=======================================    
#Movement functions
def fdMove():
    player.fd(5)

def ltTurn():
    player.lt(5)

def rtTurn():
    player.rt(5)

def bdMove():
    player.backward(5)

def dash():
    player.speed(2)
    player.fd(20)
    player.speed(10)

#Launching the projectile
def projLaunch():
    global lvlNum
    global gameOver
#Making sure the game is still running
    if(gameOver == False):
        wn.tracer(0)
#Creating the projectile
        proj = trtl.Turtle(shape = 'circle')
        proj.ht()
        proj.speed(10)
        proj.color('yellow')
        proj.penup()
#Making the projectile have same coords and heading as player
        proj.goto(player.xcor(), player.ycor())
        proj.pencolor('yellow')
        proj.pendown()
        proj.turtlesize(0.2)
        proj.setheading(player.heading())
        proj.st()
#Setting that the projectile has not hit an enemy
        hit = False
#Projectile goes ahead 40 from player
        for k in range(40):
            proj.fd(1)
#If projectile has hit enemy, break out of function
            if(hit == True):
                break
#Checking every enemy for if their coords are within 5 of projectile
            for i in attackerList:
                if(abs(i.xcor() - proj.xcor()) <= 5 and abs(i.ycor() - proj.ycor()) <= 5):
#Making hit enemy visibly different to create lack of confusion for player and removing enemy from active enemies to inactive enemies, finally setting hit to True to make sure the function ends
                    i.color('grey')
                    attackerList.remove(i)
                    inactiveTrtls.append(i)
                    hit = True
#If lvl num is greater than or equal to one, then enemy hitboxes are bigger
                elif(lvlNum >= 1):
                    if(abs(i.xcor() - proj.xcor()) <= 10 and abs(i.ycor() - proj.ycor()) <= 10):
#Doing the same as above excpet enemy shape is now a different photo because it has an actual photo instead of being a green circle
                        i.shape('attackerLvl2Inactive.gif')
                        attackerList.remove(i)
                        inactiveTrtls.append(i)
                        hit = True
#If both list of enemy attackers are empty, then all enemies have been hit so level is over
                if(attackerInBox == [] and attackerList == []):
                    boxHealthWriter.penup()
                    boxHealthWriter.goto(boxHealthWriter.xcor() - 10, boxHealthWriter.ycor() - 16)
                    boxHealthWriter.pendown()
                    endResultWriter.write('Game won', font = ('Arial', 15))
                    gameOver = True
                    lvlNum += 1
                    time.sleep(1)
                    nextLvl(lvlNum)
#Doing the same loop as in lines 51-68 but now checking the active enemies in the box
            for i in attackerInBox:
                if(abs(i.xcor() - proj.xcor()) <= 5 and abs(i.ycor() - proj.ycor()) <= 5):
                    i.color('grey')
                    attackerInBox.remove(i)
                    inactiveTrtls.append(i)
                    hit = True
                elif(lvlNum >= 1):
                    if(abs(i.xcor() - proj.xcor()) <= 10 and abs(i.ycor() - proj.ycor()) <= 10):
                        i.shape('attackerLvl2Inactive.gif')
                        attackerInBox.remove(i)
                        inactiveTrtls.append(i)
                        hit = True
                if(attackerInBox == [] and attackerList == []):
                    boxHealthWriter.penup()
                    boxHealthWriter.goto(boxHealthWriter.xcor() - 10, boxHealthWriter.ycor() - 16)
                    boxHealthWriter.pendown()
                    endResultWriter.write('Game won', font = ('Arial', 15))
                    gameOver = True
                    lvlNum += 1
                    time.sleep(1)
                    nextLvl(lvlNum)                
        wn.tracer(1)
        time.sleep(0.1)
        proj.clear()
        proj.ht()

#Drawing center square that player has to defend
def drawDefZone(defenseZone):
    drawer.goto(-defenseZone, -defenseZone)
    drawer.pendown()
    drawer.begin_fill()
    for i in range(4):
        drawer.forward(defenseZone * 2)
        drawer.lt(90)
    drawer.end_fill()

#Moving all attackers towards the center
def moveAttackers():
    global defenseZone
    for i in (attackerList):
        startX = i.xcor()
        startY = i.ycor()
#Making sure than enemy is not passing the defense zone
        if(startX > defenseZone / 2):
            startX -= attackerSpeed
        elif(startX < (defenseZone / 2) - 5):
            startX += attackerSpeed
        if(startY > defenseZone / 2):
            startY -= attackerSpeed
        elif(startY < (defenseZone / 2) - 5):
            startY += attackerSpeed
        i.goto(startX, startY)
        newX = i.xcor()
        newY = i.ycor()
#Seeing if enemy is now inside of the defense zone
        if(newY < defenseZone and newX < defenseZone and newY > -defenseZone and newX > -defenseZone):
            attackerList.remove(i)
            attackerInBox.append(i)
#Repeating function every 100 milliseconds
    wn.ontimer(moveAttackers, 100)

#Decreasing the box health
def boxHealthDecrease():
    global boxHealth
    wn.tracer(0)
#Checking if list containing attackers in the box is not empty
    if(len(attackerInBox) > 0):
#Removing one health from the box for every attacker inside of it
        for i in attackerInBox:
            boxHealth -= 1
#If the box health is 0, then display end screen
            if(boxHealth == 0):
                boxHealthWriter.clear()
                boxHealthWriter.write('Health: ' + str(boxHealth), font =('Arial', 15))
                boxHealthWriter.penup()
                boxHealthWriter.goto(boxHealthWriter.xcor() - 10, boxHealthWriter.ycor() - 16)
                boxHealthWriter.pendown()
                wn.clear()
                wn.colormode(255)
                wn.bgcolor(181, 166, 126)
                endResultWriter.write('Game over \nEnemies hit: ' + str(len(inactiveTrtls)) + '\nWave reached: ' + str(lvlNum), font = ('Arial', 20))
                return
#Displaying current box health
    boxHealthWriter.penup()
    boxHealthWriter.goto(-50, 100)
    boxHealthWriter.pendown()
    boxHealthWriter.clear()
    boxHealthWriter.write('Health: ' + str(boxHealth), font =('Arial', 15))
    wn.tracer(1)
    wn.ontimer(boxHealthDecrease, 1000)

#Going to the next level
def nextLvl(lvl):
    global inactiveTrtls
    global boxHealth
    global gameOver
    global defenseZone
    global attackerSpeed
#Making sure program will draw the right level
    if(lvl >= 1):
#Reseting variables and clearing turtles
        gameOver = False
        boxHealthWriter.clear()
        endResultWriter.clear()
        drawer.clear()
        wn.tracer(0)
        defenseZone = 75
#Adding current level onto attackerSpeed and attakcerPerQuad defaults as to make this level harder than the last one
        attackerSpeed = 1 + lvl 
        attackerPerQuad = 4 + lvl
        drawDefZone(defenseZone)
        wn.bgpic('lvl2BG.gif')
#Hiding turtles for past levels
        for i in inactiveTrtls:
            i.ht()
        boxHealth = 100
#Setting the plane that the turtles should be spawned in
        xPlane = '+'
        yPlane = '+'
#Spawingin enemies per quadrand and repeating 4 times to get every quadrand
        for k in range(4):
            for i in range(attackerPerQuad):
#Spawning turtles in positive positive quad
                if(xPlane == '+'  and yPlane == '+'):
                    spawnX = rand.randint(150, 250)
                    spawnY = rand.randint(150, 250)
                    i = trtl.Turtle()
                    i.penup()
                    i.goto(spawnX, spawnY)
                    attackerList.append(i)
                    yPlane = '-'
#Spawning turtles in positive negative quad
                elif(xPlane == '+' and yPlane == '-'):
                    spawnX = rand.randint(150, 250)
                    spawnY = rand.randint(-250, -150)
                    i = trtl.Turtle()
                    i.penup()
                    i.goto(spawnX, spawnY)
                    attackerList.append(i)
                    xPlane = '-'
#Spawning turtles in negative negative quad
                elif(xPlane == '-' and yPlane == '-'):
                    spawnX = rand.randint(-250, -150)
                    spawnY = rand.randint(-250, -150)
                    i = trtl.Turtle()
                    i.penup()
                    i.goto(spawnX, spawnY)
                    attackerList.append(i)
                    yPlane = '+'
#Spawning turtles in negative positive quad
                elif(xPlane == '-' and yPlane == '+'):
                    spawnX = rand.randint(-250, -150)
                    spawnY = rand.randint(150, 250)
                    i = trtl.Turtle()
                    i.penup()
                    i.goto(spawnX, spawnY)
                    attackerList.append(i)
                    xPlane = '+'
                    yPlane = '+'
#Setting turtles shape to that of the attacker
                i.shape('attackerLvl2.gif')
        wn.tracer(1)

#Hiding all inactive turtles mid round every 5 seconds
def destroyTrtls():
    for i in inactiveTrtls:
        i.ht()
    wn.ontimer(destroyTrtls, 5000)


#Variables=======================================
player = trtl.Turtle()
attackerList = []
drawer = trtl.Turtle()
wn = trtl.Screen()
defenseZone = 50
attackerNum = 15
attackerInBox = []
boxHealthWriter = trtl.Turtle()
endResultWriter = trtl.Turtle()
boxHealth = 100
attackerSpeed = 6
lvlNum = 0
gameOver = False
inactiveTrtls = []

#Methods=========================================
wn.tracer(0)
endResultWriter.penup()
endResultWriter.goto(-290, 0)
endResultWriter.pendown()
drawer.ht()
boxHealthWriter.ht()
wn.addshape('attackerLvl2.gif')
wn.addshape('attackerLvl2Inactive.gif')
wn.addshape('lvl1BG.gif')
wn.addshape('lvl2BG.gif')
wn.addshape('introTitleScreenAttackers.gif')
wn.setup(width = 600, height = 300, startx = 0, starty = 0)
wn.tracer(1)
#Showing title screen
wn.bgpic('introTitleScreenAttackers.gif')
endResultWriter.ht()
player.ht()
ready = ''
while(ready != 'y'): 
    ready = input('Are you ready to play?(y for yes, n for no): ')
#Initiating first level
wn.bgpic('lvl1BG.gif')
wn.colormode(255)

wn.tracer(0)
drawer.color(100, 100, 255)
drawer.penup()
drawDefZone(defenseZone)

player.st()
#Spawing first level turtles
for i in range(attackerNum):
    spawnX = rand.randint(150, 250)
    spawnY = rand.randint(100, 150)
    i = trtl.Turtle()
    i.shape('circle')
    i.color('dark green')
    i.penup()
    i.goto(spawnX, spawnY)
    attackerList.append(i)

wn.tracer(1)


#Events and function calls=======================
player.penup()
player.speed(10)
moveAttackers()
boxHealthDecrease()
destroyTrtls()
wn.onkeypress(projLaunch, 'q')
wn.onkeypress(dash, 'space')
wn.onkeypress(fdMove, 'w')
wn.onkeypress(ltTurn, 'a')
wn.onkeypress(bdMove, 's')
wn.onkeypress(rtTurn, 'd')

wn.listen()
wn.mainloop()