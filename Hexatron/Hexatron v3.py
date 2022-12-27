#-----------------------------------------------------------------------------
# Name:        Hexatron Version 3 (Hexatron v3.py)
# Purpose:     A game of Hexapawn using a basic machine-learning AI [Version 3]
#
# Author:      Ibrahim Haq
# Created:     30-10-2020
# Updated:     26-12-2022
#-----------------------------------------------------------------------------
#
# Index:
#   41-137      Variable and Dictionary initializations
#   141-665     Function initializations
#   670-809     First section of draw
#   812-1402    Analyzing the game board and choosing from all possible moves
#   1407-1484   Later section of draw
#   1489-1685   Mouse up function, including player moving their pawns and pressing buttons
#
#-----------------------------------------------------------------------------
#
# Credits:
#
# Bugs were found and AI trials completed with testing from Evan Birnie
#
# Inflate function is a slightly modified version of a function
# of the same name created by Mr. Brooks
#
# Sprites of pawns:
# https://www.freeiconspng.com/img/22003
#
# Sound of pawn moved:
# https://freesound.org/people/mh2o/sounds/351518/
#
# Diagram of possible moves, as well as inspiration for this project:
# https://youtu.be/sw7UAZNgGg8
#
#-----------------------------------------------------------------------------




# Initialization




import pygame
import random as rn
import time as t


WIDTH = 750
HEIGHT = 750


a1 = Rect((150,450), (150,150))         # Space a1 borders
b1 = Rect((300,450), (150,150))         # Space b1 borders
c1 = Rect((450,450), (150,150))         # Space c1 borders

a2 = Rect((150,300), (150,150))         # Space a2 borders
b2 = Rect((300,300), (150,150))         # Space a2 borders
c2 = Rect((450,300), (150,150))         # Space a2 borders

a3 = Rect((150,150), (150,150))         # Space a3 borders
b3 = Rect((300,150), (150,150))         # Space b3 borders
c3 = Rect((450,150), (150,150))         # Space b3 borders


TitleBx   = Rect((500,625), (150,100))  # Title button borders
StartBx   = Rect((290,290), (155,100))  # Start button borders
HelpBx    = Rect((290,440), (155,100))  # Help button borders
OptionsBx = Rect((280,590), (175,100))  # Options button borders
ResetBx   = Rect((285,245), (185,90))   # Reset AI button borders
LearnBx   = Rect((490,375), (125,80))   # Learning Rate button borders
SoundBx   = Rect((490,500), (85, 80))   # Sound toggle button borders

YesBx     = Rect((240,450), (85,80))    # Yes button borders
NoBx      = Rect((440,450), (70,80))    # No button borders


gs       = 'title'                      # Gamestate
butn     = 0                            # Mouse button value
mPos     = 0                            # Mouse position value
pMove    = True                         # Control variable to check if player is moving
cMove    = False                        # Control variable to check if computer is moving
chosen   = False                        # Control variable to check if computer has chosen a move
misclick = True                         # Control variable to prevent misclick errors
stale    = False                        # Control variable checking for stalemate
snd      = True                         # Control variable for toggling sound
cause    = ''                           # Statement on win or lose screen that describes why player won/lost
mvdSp    = 0                            # Space a pawn was moved to, for the purpose of updating wp[x]Sp
mvdPos   = ()                           # New coordinates of a pawn, for the purpose of updating wp[x]Pos
colour   = ''                           # Colour cooresponding to the move chosen
indx     = 0                            # Index variable
learning = 'fast'                       # AI's learning configuration, between fast or slow



wp1Pos    = (225,525)                   # Coordinates of wp1
wp2Pos    = (375,525)                   # Coordinates of wp2
wp3Pos    = (525,525)                   # Coordinates of wp3

bp1Pos    = (225,225)                   # Coordinates of bp1
bp2Pos    = (375,225)                   # Coordinates of bp2
bp3Pos    = (525,225)                   # Coordinates of bp3


# Dictionary containing spaces occupy by all pawns
occupy  = {'wp1' : a1, 'wp2' : b1, 'wp3' : c1, 'bp1' : a3, 'bp2' : b3, 'bp3' : c3}

# Dictionary containing coordinates of all the grid space (for pawn positioning)
spaces = {'a1' : (225,525), 'b1' : (375,525), 'c1' : (525,525),
          'a2' : (225,375), 'b2' : (375,375), 'c2' : (525,375),
          'a3' : (225,225), 'b3' : (375,225), 'c3' : (525,225)}

# Dictionaries containins spaces occupied by white team and black team
wOcc = occupy.copy()
bOcc = occupy.copy()

# Dictionary checking if a pawn is captured or not
captured = {'wp1' : False, 'wp2' : False, 'wp3' : False, 'bp1' : False, 'bp2' : False, 'bp3' : False}

# Dictionary checking if a space is a valid option to move to
valid = {'a1' : False, 'a2' : False, 'a3' : False,
         'b1' : False, 'b2' : False, 'b3' : False,
         'c1' : False, 'c2' : False, 'c3' : False}

# Dictionary checking if a pawn is selected
selected = {'wp1' : False, 'wp2' : False, 'wp3' : False}


wp1 = Actor('wp', wp1Pos)               # Player's first pawn    (White Pawn 1)
wp2 = Actor('wp', wp2Pos)               # Player's second pawn   (White Pawn 2)
wp3 = Actor('wp', wp3Pos)               # Player's third pawn    (White Pawn 3)

bp1 = Actor('bp', bp1Pos)               # Computer's first pawn  (Black Pawn 1)
bp2 = Actor('bp', bp2Pos)               # Computer's second pawn (Black Pawn 2)
bp3 = Actor('bp', bp3Pos)               # Computer's third pawn  (Black Pawn 3)



# Functions



def clear():
    '''Clears the screen'''
    screen.fill((255,255,255))



def write(wd, xy, fs):
    '''Prints text on the screen

       Parameters:
       
       wd = string to be typed
       xy = coordinates tuple
       fs = font size
       '''
    screen.draw.text(wd, xy, color = (0), fontsize = fs, fontname = "paper flowers")



def reset():
    '''Resets the grid to default state'''
    
    global valid
    global selected
    
    for x in valid:
        valid[x] = False
    
    for x in selected:
        selected[x] = False



def click(g, b):
    '''Checks to see if a button is clicked during a particular gamestate
        
        Parameters:
        
        g = gamestate during which the button is pressed
        b = button in question
        
        Returns:
        True or false depending on if the button is clicked in the specified gamestate
    '''
    
    global butn
    global mPos
    global gs
    
    if gs == g and butn == mouse.LEFT:
        
        if b.collidepoint(mPos):
            return True
        
        else:
            return False
        
    else:
        return False



def inflate(actorIn, xIncrease): # Original function created by Mr. Brooks, slightly modified version used
    '''Increase the size of an actor by the given amount
    
    Parameters
    ----------
    actorIn - The actor to work with
    xIncrease - The amount (in pixels) to increase the width by, use a negative number to shrink
    yIncrease - The amount (in pixels) to increase the height by, use a negative number to shrink
    
    Returns
    -------
    The modified actor object
    '''
    yIncrease = xIncrease
    oldLocation = actorIn.center
    currentXSize = actorIn.width
    currentYSize = actorIn.height
    actorIn._surf = pygame.transform.scale(actorIn._surf, (currentXSize + xIncrease, currentXSize + xIncrease))
    actorIn._update_pos()
    actorIn.center = oldLocation
    
    return actorIn



def pawn():
    '''Handles display of pawns'''
    
    global wp1Pos
    global wp2Pos
    global wp3Pos
    global bp1Pos
    global bp2Pos
    global bp3Pos
    global captured
    
    wp1 = Actor('wp', wp1Pos)
    wp2 = Actor('wp', wp2Pos)
    wp3 = Actor('wp', wp3Pos)
    bp1 = Actor('bp', bp1Pos)
    bp2 = Actor('bp', bp2Pos)
    bp3 = Actor('bp', bp3Pos)
    
    wp1 = inflate(wp1, -2250)
    wp2 = inflate(wp2, -2250)
    wp3 = inflate(wp3, -2250)
    bp1 = inflate(bp1, -2250)
    bp2 = inflate(bp2, -2250)
    bp3 = inflate(bp3, -2250)
    
    if captured['wp1'] == False:
        wp1.draw()
        
    if captured['wp2'] == False:
        wp2.draw()
    
    if captured['wp3'] == False:
        wp3.draw()
    
    if captured['bp1'] == False:
        bp1.draw()
    
    if captured['bp2'] == False:
        bp2.draw()
    
    if captured['bp3'] == False:
        bp3.draw()



def grid():
    '''Handles display of grid'''
    
    global valid   
    
    if valid['a1'] == False:
        screen.draw.rect(a1, color=(0))
    elif valid['a1']:
        screen.draw.filled_rect(a1, color=(0,160,220))

    if valid['b1'] == False:
        screen.draw.rect(b1, color=(0))
    elif valid['b1']:
        screen.draw.filled_rect(b1, color=(0,160,220))
    
    if valid['c1'] == False:
        screen.draw.rect(c1, color=(0))
    elif valid['c1']:
        screen.draw.filled_rect(c1, color=(0,160,220))
    
    
    if valid['a2'] == False:
        screen.draw.rect(a2, color=(0))
    elif valid['a2']:
        screen.draw.filled_rect(a2, color=(0,160,220))
    
    if valid['b2'] == False:
        screen.draw.rect(b2, color=(0))
    elif valid['b2']:
        screen.draw.filled_rect(b2, color=(0,160,220))
    
    if valid['c2'] == False:
        screen.draw.rect(c2, color=(0))
    elif valid['c2']:
        screen.draw.filled_rect(c2, color=(0,160,220))
    
    
    if valid['a3'] == False:
        screen.draw.rect(a3, color=(0))
    elif valid['a3']:
        screen.draw.filled_rect(a3, color=(0,160,220))
    
    if valid['b3'] == False:
        screen.draw.rect(b3, color=(0))
    elif valid['b3']:
        screen.draw.filled_rect(b3, color=(0,160,220))
        
    if valid['c3'] == False:
        screen.draw.rect(c3, color=(0))
    elif valid['c3']:
        screen.draw.filled_rect(c3, color=(0,160,220))
        
        
        
def moveW():
    '''Handles movement of white pawns'''
    
    global selected
    global mvdSp
    global mvdPos
    global spaces
    global misclick
    global snd
    
    misclick = False
    
    if click('play', a2) and valid['a2']:
    
        mvdPos = spaces['a2']
        mvdSp  = a2
        
    elif click('play', b2) and valid['b2']:
        
        mvdPos = spaces['b2']
        mvdSp  = b2
    
    elif click('play', c2) and valid['c2']:
        
        mvdPos = spaces['c2']
        mvdSp  = c2
        
    elif click('play', a3) and valid['a3']:
        
        mvdPos = spaces['a3']
        mvdSp  = a3
    
    elif click('play', b3) and valid['b3']:
        
        mvdPos = spaces['b3']
        mvdSp  = b3
        
    elif click('play', c3) and valid['c3']:
        
        mvdPos = spaces['c3']
        mvdSp  = c3
    
    else:
        misclick = True
        
    reset()
    if not misclick and snd:
        sounds.pawn.play()
    
    
    
def moveB(pwn,sp,spR):
    '''Handles movement of black pawns

       Parameters:
       pwn = Pawn to be moved
       sp  = Space pawn is being moved to (String notation)
       spR = Space pawn is being moved to (Rect notation)       
    '''
              
    global spaces
    global occupy
    
    global bp1Pos
    global bp2Pos
    global bp3Pos
    
    
    if pwn == 'bp1':
        bp1Pos = spaces[sp]
        occupy[pwn] = spR
        
    elif pwn == 'bp2':
        bp2Pos = spaces[sp]
        occupy[pwn] = spR
        
    elif pwn == 'bp3':
        bp3Pos = spaces[sp]
        occupy[pwn] = spR



def setOcc():
    '''Updates the wOcc and bOcc dictionaries'''
    
    global wOcc
    global bOcc
    global occupy
    global captured
    
    wOcc = occupy.copy()
    wOcc.pop('bp1')
    wOcc.pop('bp2')
    wOcc.pop('bp3')
    
    if captured['wp1']:
        wOcc.pop('wp1')
    if captured['wp2']:
        wOcc.pop('wp2')
    if captured['wp3']:
        wOcc.pop('wp3')
        
    bOcc = occupy.copy()
    bOcc.pop('wp1')
    bOcc.pop('wp2')
    bOcc.pop('wp3')

    if captured['bp1']:
        bOcc.pop('bp1')
    if captured['bp2']:
        bOcc.pop('bp2')
    if captured['bp3']:
        bOcc.pop('bp3')
    
        
        
def capture(team):
    '''Handles capturing of pawns
       
       Parameters:
       team = the team that is capturing the pawn (white or black)
    '''
    
    global captured
    global occupy
    global wOcc
    global bOcc
    
    setOcc()
    
    if team == 'w':
        
        if occupy['bp1'] in wOcc.values():
            captured['bp1'] = True
        
        if occupy['bp2'] in wOcc.values():
            captured['bp2'] = True
        
        if occupy['bp3'] in wOcc.values():
            captured['bp3'] = True
    
    
    elif team == 'b':
        
        if occupy['wp1'] in bOcc.values():
            captured['wp1'] = True
            
        if occupy['wp2'] in bOcc.values():
            captured['wp2'] = True
            
        if occupy['wp3'] in bOcc.values():
            captured['wp3'] = True
    
    setOcc()
            
            
            
def turn():
    '''Switches turns'''
    
    global pMove
    global cMove
    
    pMove = not pMove
    cMove = not cMove
            
            
            
def validate(pwn):
    '''Checks if a move is valid or not
    
       Parameters:
       pwn = Pawn that is being moved
    '''
    
    global occupy
    global valid
    global wOcc
    global bOcc
    
    setOcc()
        
    # Moving to empty spaces
    
    
    if occupy[pwn] == a1 and a2 not in occupy.values():
        valid['a2'] = True
    
    elif occupy[pwn] == b1 and b2 not in occupy.values():
        valid['b2'] = True
        
    elif occupy[pwn] == c1 and c2 not in occupy.values():
        valid['c2'] = True
    
    elif occupy[pwn] == a2 and a3 not in occupy.values():
        valid['a3'] = True
        
    elif occupy[pwn] == b2 and b3 not in occupy.values():
        valid['b3'] = True
        
    elif occupy[pwn] == c2 and c3 not in occupy.values():
        valid['c3'] = True
        
    
    # Capturing Pawns
    
    
    if occupy[pwn] == a1 and b2 in bOcc.values() and b2 not in wOcc.values():
        valid['b2'] = True
        
    if occupy[pwn] == b1 and a2 in bOcc.values() and a2 not in wOcc.values():
        valid['a2'] = True
    
    if occupy[pwn] == b1 and c2 in bOcc.values() and c2 not in wOcc.values():
        valid['c2'] = True
        
    if occupy[pwn] == c1 and b2 in bOcc.values() and b2 not in wOcc.values():
        valid['b2'] = True
        
    if occupy[pwn] == a2 and b3 in bOcc.values() and b3 not in wOcc.values():
        valid['b3'] = True
        
    if occupy[pwn] == b2 and a3 in bOcc.values() and a3 not in wOcc.values():
        valid['a3'] = True
    
    if occupy[pwn] == b2 and c3 in bOcc.values() and c3 not in wOcc.values():
        valid['c3'] = True
        
    if occupy[pwn] == c2 and b3 in bOcc.values() and b3 not in wOcc.values():
        valid['b3'] = True
        
        
        
def choose(lst):
    '''Chooses a move for the computer AI
       
       Parameters:
       lst = The list containing the moves to choose from (the line # in the AI database)
    '''
    
    global indx
    global colour
    global stale
    global chosen
    
    stale = False
    indx  = lst
    f     = open("AI.txt")
    x     = f.readlines()
    f.close()
    
    colour = x[indx][rn.randint(0, len(x[indx])-1)]
    while not colour.isalpha():
        colour = x[indx][rn.randint(0, len(x[indx])-1)]
    
    chosen = True
        
        
        
def stalemate():
    '''Checks to see if player is in a stalemate'''
    
    global valid
    global stale
    
    if not captured['wp1']:
        validate('wp1')
    if not captured['wp2']:
        validate('wp2')
    if not captured['wp3']:
        validate('wp3')
    
    if True not in valid.values():
        stale = True
        
    reset()
    
    
    
def learn():
    '''Updates the AI database on winning moves'''
    
    global indx
    global colour
    global learning
    
    f = open("AI.txt")
    x = []
    n = 0
    
    while True:
        x.append(list(f.readline()))
        
        if n > 25:
            f.close()
            break
        
        if n == indx:
            i = x[n].index(colour)
            
            if len(x[n]) > 1:
                
                if learning == 'fast':
                    del x[indx][i]
                elif learning == 'slow' and len(x[n]) < 10:
                    x[indx].append(colour)
        
        n += 1
    
    f = open("AI.txt", "w")
    f.write(''.join(x[0]))
    f.close()
    
    f = open("AI.txt", "a")
    for n in x[1:]:
        f.write(''.join(n))
    f.close()
    
    
    
def forget():
    '''Wipes the AI's database'''
    
    f = open("AI Default.txt")
    x = f.readlines()
    f.close()
    
    f = open("AI.txt", "w")
    f.write(''.join(x[0]))
    f.close()
    
    f = open("AI.txt", "a")
    for n in x[1:]:
        f.write(''.join(n))
    f.close()
    
        
    

# Game

    


def draw():
    '''Function that runs continuously while the game is being played'''
    
    
    # Initialization
    
    
    clear()
    
    global wp1Pos
    global wp2Pos
    global wp3Pos
    global bp1Pos
    global bp2Pos
    global bp3Pos
    
    global gs
    global pMove
    global cMove
    global stale
    global chosen
    global cause
    global learning
    global snd
    
    global occupy
    global captured
    global bOcc
    global wOcc
    global spaces
    
    global wp1
    global wp2
    global wp3
    global bp1
    global bp2
    global bp3
    
    global a1
    global a2
    global a3
    global b1
    global b2
    global b3
    global c1
    global c2
    global c3
    
    setOcc()
    
    
    # Title Screen
    
    
    if gs == 'title':
        
        wp1Pos = spaces['a1']  
        wp2Pos = spaces['b1']    
        wp3Pos = spaces['c1']             

        bp1Pos = spaces['a3']
        bp2Pos = spaces['b3']
        bp3Pos = spaces['c3']
        
        reset()
        stale = False
        pMove = True
        cMove = False
        occupy   = {'wp1' : a1, 'wp2' : b1, 'wp3' : c1, 'bp1' : a3, 'bp2' : b3, 'bp3' : c3}
        captured = {'wp1' : False, 'wp2' : False, 'wp3' : False,
                    'bp1' : False, 'bp2' : False, 'bp3' : False}
        
        
        write('Hexatron', (235,100), 110)
        write('Start',    (310,300), 80)
        write('Help',     (320,450), 80)
        write('Options',  (290,600), 80)
        
        screen.draw.rect(StartBx, color=(0))
        screen.draw.rect(HelpBx, color=(0))
        screen.draw.rect(OptionsBx, color=(0))
        
    
    # Help Screen
    
    
    elif gs == 'help':
        
        write('How to Play',                                    (200,50),  110)
        write('You can move pawns to an empty space ahead, or', (50, 250), 50)
        write('diagonally to capture an enemy pawn',            (120,300), 50)
        write('Click to select a pawn, click again to cancel',  (75, 375), 50)
        write('To win, reach the other side, capture all of',   (80, 450), 50)
        write('the opponents pawns, or put them in stalemate',  (60, 500), 50)
        write('Title',                                          (522,635), 80)
        
        screen.draw.rect(TitleBx, color=(0))
        
        
    # Options Screen
    
    
    elif gs == 'options':
        
        write('Options',        (275,50),  110)
        write('Reset AI',       (295,250), 80)
        write('Learning Rate:', (100,375), 80)
        write(learning,         (500,375), 80)
        write('Toggle Sound:',  (120,500), 80)
        
        if snd:
            write('On',         (500,500), 80)
        elif not snd:
            write('Off',        (500,500), 80)
            
        write('Title',          (522,635), 80)
        
        screen.draw.rect(ResetBx, color=(0))
        screen.draw.rect(LearnBx, color=(0))
        screen.draw.rect(SoundBx, color=(0))
        screen.draw.rect(TitleBx, color=(0))
    
    
    # Confirming AI Reset
    
    
    elif gs == 'confirm':
        
        write('Are you sure?',                  (160,100), 130)
        write("This will wipe the AI's memory", (60,300),  80)
        write('Yes',                            (250,450), 80)
        write('No',                             (450,450), 80)
        
        screen.draw.rect(YesBx, color=(0))
        screen.draw.rect(NoBx, color=(0))
    
    
    # Game Screen
    
    
    elif gs == 'play':
        
        
        
        
        # Computer makes its move (refer to diagram of possible moves)
        if cMove:
            
            stale = True
            chosen = False
        
        
            
            
            # Round 2 Move 1
            if b1 in wOcc.values():
                
                # Straight
                if c1 in wOcc.values() and a2 in wOcc.values():
                    choose(0)
                
                    if colour == 'G':
                        moveB('bp2', 'a2', a2)
                    elif colour == 'B':
                        moveB('bp2', 'b2', b2)
                    elif colour == 'P':
                        moveB('bp3', 'c2', c2)
                
                # Inverse
                elif a1 in wOcc.values() and c2 in wOcc.values():
                    choose(0)

                    if colour == 'G':
                        moveB('bp2', 'c2', c2)
                    elif colour == 'B':
                        moveB('bp2', 'b2', b2)
                    elif colour == 'P':
                        moveB('bp1', 'a2', a2)
            
            
            
            # Round 2 Move 2
            if a1 in wOcc.values() and c1 in wOcc.values() and b2 in wOcc.values() and not chosen:
                choose(1)
                
                if colour == 'G':
                    moveB('bp1', 'a2', a2)
                elif colour == 'B':
                    moveB('bp1', 'b2', b2)
                    
                    
                    
            # Round 4 Move 1
            if a1 in wOcc.values() and a2 in bOcc.values() and c2 in wOcc.values() and c3 in bOcc.values() and b2 in wOcc.values() and b3 in bOcc.values() and not chosen:
                choose(2)
            
                if colour == 'P':
                    moveB('bp2', 'c2', c2)
                elif colour == 'G':
                    moveB('bp3', 'b2', b2)
            
            
            
            # Round 4 Move 2
            if b2 in bOcc.values() and b3 in bOcc.values() and captured['wp2'] and not chosen:
                
                # Straight
                if a1 in wOcc.values() and c2 in wOcc.values() and c3 in bOcc.values():
                    choose(3)
                    
                    if colour == 'G':
                        moveB('bp2', 'c2', c2)
                    elif colour == 'B':
                        moveB('bp1', 'a1', a1)
                    elif colour == 'P':
                        moveB('bp1', 'b1', b1)
                    
                # Inverse
                elif c1 in wOcc.values() and a2 in wOcc.values() and a3 in wOcc.values():
                    choose(3)
                    
                    if colour == 'G':
                        moveB('bp2', 'c2', c2)
                    elif colour == 'B':
                        moveB('bp1', 'a1', a1)
                    elif colour == 'P':
                        moveB('bp1', 'b1', b1)                    
            
            
            
            # Round 4 Move 3
            if a2 in wOcc.values() and b3 in bOcc.values() and c2 in wOcc.values() and not chosen:
                
                # Straight 
                if c1 in wOcc.values() and a3 in bOcc.values() and captured['bp3']:
                    choose(4)
                    
                    if colour == 'P':
                        moveB('bp2', 'a2', a2)
                    elif colour == 'G':
                        moveB('bp2', 'b2', b2)
                    elif colour == 'B':
                        moveB('bp2', 'c3', c3)
            
                # Inverse
                elif a1 in wOcc.values() and c3 in bOcc.values() and captured['bp1']:
                    choose(4)
                                        
                    if colour == 'P':
                        moveB('bp2', 'a2', a2)
                    elif colour == 'G':
                        moveB('bp2', 'b2', b2)
                    elif colour == 'B':
                        moveB('bp2', 'c3', c3)
            
            
            
            # Round 4 Move 4
            if a3 in bOcc.values() and c3 in bOcc.values() and captured['bp2'] and not chosen:
                
                # Straight
                if c1 in wOcc.values() and a2 in wOcc.values():
                    choose(5)
                    
                    if colour == 'R':
                        moveB('bp3', 'c2', c2)
                
                elif a1 in wOcc.values() and c2 in wOcc.values():
                    choose(5)
                    
                    if colour == 'R':
                        moveB('bp1', 'a2', a2)
                        
            
            
            # Round 4 Move 5
            if b2 in wOcc.values() and b3 in bOcc.values() and c1 in wOcc.values() and a2 in wOcc.values() and c2 in bOcc.values() and a3 in bOcc.values() and not chosen:
                choose(6)
            
                if colour == 'B':
                    moveB('bp2', 'a2', a2)
                elif colour == 'P':
                    moveB('bp1', 'b2', b2)
                
            
            
            # Round 4 Move 6
            if b1 in wOcc.values() and b2 in wOcc.values() and a3 in bOcc.values() and c3 in bOcc.values() and not chosen:
                
                # Straight
                if a2 in wOcc.values():
                    choose(7)
                    
                    if colour == 'B':
                        moveB('bp1', 'b2', b2)
                    elif colour == 'G':
                        moveB('bp3', 'b2', b2)
                    elif colour == 'P':
                        moveB('bp3', 'c2', c2)
                    
                # Inverse
                elif c2 in wOcc.values():
                    choose(7)
                    
                    if colour == 'B':
                        moveB('bp3', 'b2', b2)
                    elif colour == 'G':
                        moveB('bp1', 'b2', b2)
                    elif colour == 'P':
                        moveB('bp1', 'a2', a2)
                        
                        
                        
            # Round 4 Move 7          
            if b2 in bOcc.values() and b3 in bOcc.values() and captured['wp2'] and not chosen:
                
                # Straight
                if c1 in wOcc.values() and a2 in wOcc.values() and c3 in bOcc.values():
                    choose(8)
                    
                    if colour == 'B':
                        moveB('bp1', 'b1', b1)
                    elif colour == 'R':
                        moveB('bp1', 'c1', c1)
                    elif colour == 'P':
                        moveB('bp2', 'a2', a2)
                    elif colour == 'G':
                        moveB('bp3', 'c2', c2)
                    
                # Inverse
                elif a1 in wOcc.values() and c2 in wOcc.values() and a3 in bOcc.values():
                    choose(8)
                    
                    if colour == 'B':
                        moveB('bp3', 'b1', b1)
                    elif colour == 'R':
                        moveB('bp3', 'a1', a1)
                    elif colour == 'P':
                        moveB('bp2', 'c2', c2)
                    elif colour == 'G':
                        moveB('bp1', 'a2', a2)


            
            # Round 4 Move 8
            if b2 in wOcc.values() and b3 in bOcc.values() and not chosen:
                
                # Straight 1
                if c1 in wOcc.values() and c3 in bOcc.values() and captured['bp1']:
                    choose(9)
                    
                    if colour == 'P':
                        moveB('bp3', 'b2', b2)
                    elif colour == 'G':
                        moveB('bp3', 'c2', c2)
                        
                # Straight 2
                elif a1 in wOcc.values() and c3 in bOcc.values() and captured['bp1']:
                    choose(9)
                    
                    if colour == 'P':
                        moveB('bp3', 'b2', b2)
                    elif colour == 'G':
                        moveB('bp3', 'c2', c2)
                        
                # Inverse 1
                elif a1 in wOcc.values() and a3 in bOcc.values() and captured['bp3']:
                    choose(9)
                    
                    if colour == 'P':
                        moveB('bp1', 'b2', b2)
                    elif colour == 'G':
                        moveB('bp1', 'a2', a2)
                
                # Inverse 2
                elif c1 in wOcc.values() and a3 in bOcc.values() and captured['bp3']:
                    choose(9)
                    
                    if colour == 'P':
                        moveB('bp1', 'b2', b2)
                    elif colour == 'G':
                        moveB('bp1', 'a2', a2)
            
            
            
            # Round 4 Move 9
            if b2 in wOcc.values() and a3 in bOcc.values() and c3 in bOcc.values() and not chosen:
                
                # Straight
                if c1 in wOcc.values() and a2 in bOcc.values() and captured['wp1']:
                    choose(10)
                    
                    if colour == 'R':
                        moveB('bp2', 'a1', a1)
                    elif colour == 'G':
                        moveB('bp1', 'b2', b2)
                    elif colour == 'B':
                        moveB('bp3', 'b2', b2)
                    elif colour == 'P':
                        moveB('bp3', 'c2', c2)
                        
                # Inverse
                elif a1 in wOcc.values() and c2 in bOcc.values() and captured['wp3']:
                    choose(10)
                    
                    if colour == 'R':
                        moveB('bp2', 'c1', c1)
                    elif colour == 'G':
                        moveB('bp3', 'b2', b2)
                    elif colour == 'B':
                        moveB('bp1', 'b2', b2)
                    elif colour == 'P':
                        moveB('bp1', 'a2', a2)
                        
                        
                        
            # Round 4 Move 10
            if b1 in wOcc.values() and a3 in bOcc.values() and c3 in bOcc.values() and not chosen:
                
                # Straight
                if a2 in bOcc.values() and c2 in wOcc.values() and captured['wp1']:
                    choose (11)
                    
                    if colour == 'G':
                        moveB('bp2', 'a1', a1)
                    elif colour == 'B':
                        moveB('bp2', 'b1', b1)
                
                # Inverse
                elif c2 in bOcc.values() and a2 in wOcc.values() and captured['wp3']:
                    choose(11)
                    
                    if colour == 'G':
                        moveB('bp2', 'c1', c1)
                    elif colour == 'B':
                        moveB('bp2', 'b1', b1)
                        
                        
                        
            # Round 4 Move 11
            if 2 in wOcc.values() and b3 in bOcc.values() and not chosen:
                
                # Straight
                if a1 in wOcc.values() and c3 in bOcc.values() and captured['wp2'] and captured['bp1']:
                    choose(12)
                    
                    if colour == 'R':
                        moveB('bp3', 'b2', b2)
                    elif colour == 'P':
                        moveB('bp3', 'c2', c2)
                    
                # Inverse
                elif c1 in wOcc.values() and a3 in bOcc.values() and captured['wp2'] and captured ['bp3']:
                    choose(12)
                    
                    if colour == 'R':
                        moveB('bp1', 'b2', b2)
                    elif colour == 'P':
                        moveB('bp1', 'a2', a2)
                        
                        
                        
            # Round 6 Move 1
            if b2 in wOcc.values() and b3 in bOcc.values() and not chosen:
                
                # Straight
                if a2 in bOcc.values() and c2 in wOcc.values():
                    choose(13)
                    
                    if colour == 'R':
                        moveB('bp2', 'c2', c2)
                    elif colour == 'P':
                        moveB('bp1', 'a1', a1)
                
                # Inverse
                elif c2 in bOcc.values() and a2 in wOcc.values():
                    choose(13)
                    
                    if colour == 'R':
                        moveB('bp2', 'a2', a2)
                    elif colour == 'P':
                        moveB('bp3', 'c1', c1)
                        
                        
                        
            # Round 6 Move 2
            if b2 in wOcc.values() and a2 in bOcc.values() and a3 in bOcc.values() and not chosen:
                choose(14)
                
                if colour == 'P':
                    moveB('bp1', 'b2', b2)
                elif colour == 'R':
                    moveB('bp2', 'a1', a1)
    
            
            
            # Round 6 Move 3
            if b2 in bOcc.values() and not chosen:
                
                # Straight
                if a2 in bOcc.values() and c2 in wOcc.values() and a3 in bOcc.values():
                    choose(15)
                    
                    if colour == 'B':
                        moveB('bp2', 'a1', a1)
                    elif colour == 'P':
                        moveB('bp3', 'b1', b1)
                        
                # Inverse
                elif c2 in bOcc.values() and a2 in wOcc.values() and c3 in bOcc.values():
                    choose(15)
                    
                    if colour == 'B':
                        moveB('bp2', 'c1', c1)
                    elif colour == 'P':
                        moveB('bp1', 'b1', b1)
                
            
            
            # Round 6 Move 4
            if a2 in wOcc.values() and b2 in wOcc.values() and c2 in wOcc.values() and not chosen:
                
                # Straight
                if a3 in bOcc.values() and captured['bp2'] and captured['bp3']:
                    choose(16)
                    
                    if colour == 'B':
                        moveB('bp1', 'b2', b2)
                
                # Inverse
                elif c3 in bOcc.values() and captured['bp2'] and captured ['bp1']:
                    choose(16)
                    
                    if colour == 'B':
                        moveB('bp3', 'b2', b2)
                        
            
            
            # Round 6 Move 5
            if b2 in bOcc.values() and not chosen:
                
                # Straight
                if a2 in wOcc.values() and c2 in bOcc.values() and c3 in bOcc.values():
                    choose(17)
                    
                    if colour == 'R':
                        moveB('bp1', 'b1', b1)
                    elif colour == 'G':
                        moveB('bp2', 'c1', c1)
                
                # Inverse
                elif c2 in wOcc.values() and a2 in bOcc.values() and a3 in bOcc.values():
                    choose(17)
                    
                    if colour == 'R':
                        moveB('bp3', 'b1', b1)
                    elif colour == 'G':
                        moveB('bp2', 'a1', a1)
                
            
            
            # Round 6 Move 6
            if b2 in bOcc.values() and b3 in bOcc.values() and not chosen:
                
                # Straight
                if a2 in wOcc.values() and captured['wp3']:
                    choose(18)
                    
                    if colour == 'G':
                        moveB('bp2', 'a2', a2)
                    elif colour == 'P':
                        if not captured['bp1']:
                            moveB('bp1', 'b2', b2)
                        elif not captured['bp3']:
                            moveB('bp3', 'b2', b2)
                    
                # Inverse
                elif c2 in wOcc.values() and captured['wp1']:
                    choose(18)
                    
                    if colour == 'G':
                        moveB('bp2', 'c2', c2)
                    elif colour == 'P':
                        if not captured['bp3']:
                            moveB('bp3', 'b2', b2)
                        elif not captured['bp1']:
                            moveB('bp1', 'b2', b2)
                
                
                
            # Round 6 Move 7
            if b2 in wOcc.values() and not chosen:
                
                # Straight
                if a2 in bOcc.values() and c3 in bOcc.values():
                    choose(19)
                    
                    if colour == 'P':
                        if not captured['bp1']:
                            moveB('bp1', 'a1', a1)
                        elif not captured['bp2']:
                            moveB('bp2', 'a1', a1)
                    
                    elif colour == 'R':
                        moveB('bp3', 'b2', b2)
                    elif colour == 'G':
                        moveB('bp3', 'c2', c2)
                
                # Inverse
                if c2 in bOcc.values() and a3 in bOcc.values():
                    choose(19)
                    
                    if colour == 'P':
                        if not captured['bp3']:
                            moveB('bp3', 'c1', c1)
                        elif not captured['bp2']:
                            moveB('bp2', 'c1', c1)
                    
                    elif colour == 'R':
                        moveB('bp1', 'b2', b2)
                    elif colour == 'G':
                        moveB('bp1', 'a2', a2)
                        
                        
                        
            # Round 6 Move 8
            if b2 in wOcc.values() and c2 in bOcc.values() and c3 in bOcc.values() and not chosen:
                choose(20)
                
                if colour == 'G':
                    moveB('bp3', 'b2', b2)
                elif colour == 'B':
                    moveB('bp2', 'c1', c1)
            
            
            
            # Round 6 Move 9
            if b2 in wOcc.values() and b3 in bOcc.values() and not chosen:
                
                # Straight
                if a2 in wOcc.values() and c2 in bOcc.values() and captured['bp1']:
                    choose(21)
                    
                    if colour == 'R':
                        moveB('bp2', 'a2', a2)
                    elif colour == 'P':
                        moveB('bp3', 'c1', c1)
                        
                # Inverse
                elif c2 in wOcc.values() and a2 in bOcc.values() and captured['bp3']:
                    choose(21)
                    
                    if colour == 'R':
                        moveB('bp2', 'c2', c2)
                    elif colour == 'P':
                        moveB('bp1', 'a1', a1)
            
            
            
            # Round 6 Move 10
            if b2 in bOcc.values() and not chosen:
                
                # Straight
                if a2 in bOcc.values() and c2 in wOcc.values() and c3 in bOcc.values() and captured['wp1']:
                    choose(22)
                    
                    if colour == 'P':
                        moveB('bp2', 'a1', a1)
                    elif colour == 'R':
                        moveB('bp1', 'b1', b1)
                
                # Inverse
                elif c2 in bOcc.values() and a2 in wOcc.values() and a3 in bOcc.values() and captured['wp3']:
                    choose(22)
                    
                    if colour == 'P':
                        moveB('bp2', 'c1', c1)
                    elif colour == 'R':
                        moveB('bp3', 'b1', b1)
            
            
            
            # Round 6 Move 11
            if b2 in bOcc.values() and b3 in bOcc.values() and not chosen:
                
                # Straight
                if c2 in wOcc.values() and captured['wp1']:
                    choose(23)
                    
                    if colour == 'P':
                        moveB('bp2', 'c2', c2)
                    elif colour == 'B':
                        if not captured['bp1']:
                            moveB('bp1', 'b1', b1)
                        elif not captured['bp3']:
                            moveB('bp3', 'b1', b1)
                    
                # Inverse
                elif a2 in wOcc.values() and captured['wp3']:
                    choose(23)
                    
                    if colour == 'P':
                        moveB('bp2', 'a2', a2)
                    elif colour == 'B':
                        if not captured['bp3']:
                            moveB('bp3', 'b1', b1)
                        elif not captured['bp1']:
                            moveB('bp1', 'b1', b1)
                
            
            
            
            # Computer is put in stalemate
            if stale:
                gs = 'win'
                cause = '''AI is in stalemate'''
            
            
            capture('b')
            turn()
            stalemate()
        
        
        
        # Player is put in stalemate
        if pMove and stale and gs == 'play':
            gs = 'lose'
            cause = '''you are in stalemate'''
        
        
        
        
        # Board is updated
        
        
        write('1', (100,475), 100)
        write('2', (100,325), 100)
        write('3', (100,175), 100)
        
        write('A', (210,50),  100)
        write('B', (360,50),  100)
        write('C', (510,50),  100)
        
        write('Title', (522,635), 80)
        screen.draw.rect(TitleBx, color=(0))
        
        setOcc()
        grid()
        pawn()
        
                  
        
        
        # Checking for victory or defeat
    
        if len(bOcc) == 0:
            gs = 'win'
            cause = 'all pawns captured'
            
        elif a3 in wOcc.values() or b3 in wOcc.values() or c3 in wOcc.values():
            gs = 'win'
            cause = 'you reached other side'
        
            
        elif len(wOcc) == 0:
            gs = 'lose'
            cause = 'all pawns captured'
        
        elif a1 in bOcc.values() or b1 in bOcc.values() or c1 in bOcc.values():
            gs = 'lose'
            cause = 'AI reached other side'
            
    
    
    
    # Win Screen
    
    
    if gs == 'win':
        
        clear()
        
        write('YOU WIN',          (220,100), 150)
        write('Update Database?', (190,350), 80)
        write('Yes',              (250,450), 80)
        write('No',               (450,450), 80)
        write(cause,              (210,600), 60)
        
        screen.draw.rect(YesBx, color=(0))
        screen.draw.rect(NoBx, color=(0))
    
    
    # Lose Screen
    
    
    if gs == 'lose':
        
        clear()
        
        write('YOU LOSE',         (210,100), 150)
        write('Update Database?', (190,350), 80)
        write('Yes',              (250,450), 80)
        write('No',               (450,450), 80)
        write(cause,              (210,600), 65)
        
        screen.draw.rect(YesBx, color=(0))
        screen.draw.rect(NoBx, color=(0))
    
    
    setOcc()
        



# Input Functions




def on_mouse_up(pos, button):
    '''Function that runs when the mouse button is released'''
    
    global gs
    global butn
    global mPos
    global pMove
    global cMove
    global mvdPos
    global mvdSp
    global misclick
    global cause
    global learning
    global snd
    
    global occupy
    global valid
    global selected
    
    global wp1Pos
    global wp2Pos
    global wp3Pos
    
    global bp1Pos
    global bp2Pos
    global bp3Pos
    
    
    butn = button
    mPos = pos
    
    

    
    # Player move
    if pMove:
    
    
    
    
        # Pawn 1 is selected
        if click('play', occupy['wp1']) and captured['wp1'] == False and True not in selected.values():
                        
            selected['wp1'] = True
            validate('wp1')
        
        
        # Pawn 1 movement is cancelled
        elif click('play', occupy['wp1']) and not captured['wp1']:
            reset()


        # Pawn 1 is moved
        elif selected['wp1']:
            moveW()
            
            if True not in selected.values() and not misclick:
                
                occupy['wp1'] = mvdSp
                wp1Pos = mvdPos
                capture('w')
                turn()
        
        
        
        # Pawn 2 is selected
        elif click('play', occupy['wp2']) and captured['wp2'] == False and True not in selected.values():
            
            selected['wp2'] = True
            validate('wp2')
                
        
        # Pawn 2 movement is cancelled
        elif click('play', occupy['wp2']) and not captured['wp2']:
            reset()
        
        
        # Pawn 2 is moved
        elif selected['wp2']:
            moveW()
            
            if True not in selected.values() and not misclick:
                
                occupy['wp2'] = mvdSp
                wp2Pos = mvdPos
                capture('w')
                turn()
            
            
            
        # Pawn 3 is selected
        elif click('play', occupy['wp3']) and captured['wp3'] == False and True not in selected.values():
            
            selected['wp3'] = True
            validate('wp3')


        # Pawn 3 movement is cancelled
        elif click('play', occupy['wp3']) and not captured['wp3']:
            reset()

        
        # Pawn 3 is moved
        elif selected['wp3']:
            moveW()
            
            if True not in selected.values() and not misclick:
                
                occupy['wp3'] = mvdSp
                wp3Pos = mvdPos
                capture('w')
                turn()
        
        
        
        
    # Buttons

    


    # Start the game
    if click('title', StartBx):
        gs = 'play'
    
    # Go to help screen
    elif click('title', HelpBx):
        gs = 'help'
    
    # Go to options screen
    elif click('title', OptionsBx):
        gs = 'options'
    
    
    
    # Learning rate
    elif click('options', LearnBx):
        if learning == 'fast':
            learning = 'slow'
        else:
            learning = 'fast'
        
    # Toggle Sound
    elif click('options', SoundBx):
        snd = not snd

    # Reset AI database confirmation screen
    elif click('options', ResetBx):
        gs = 'confirm'
    
    # Confirm AI reset
    elif click('confirm', YesBx):
        forget()
        gs = 'options'
    
    # Cancel AI reset
    elif click('confirm', NoBx):
        gs = 'options'
        
    
    
    # Go to title screen
    elif click('help', TitleBx) or click('options', TitleBx) or click('play', TitleBx):
        gs = 'title'
        
        
        
    # Win: update database
    elif click('win', YesBx):
        if learning == 'fast':
            learn()
        gs = 'title'
    
    # Lose: update database
    elif click('lose', YesBx):
        if learning == 'slow':
            learn()
        gs = 'title'
    
    # Don't update database
    elif click('win', NoBx) or click('lose', NoBx):
        gs = 'title'