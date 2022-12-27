#-----------------------------------------------------------------------------
# Name:        Hexatron Version 1 (Hexatron v1.py)
# Purpose:     A game of Hexapawn using a basic machine-learning AI [Version 1]
#
# Author:      Ibrahim Haq
# Created:     26-10-2020
# Updated:     26-12-2022
#-----------------------------------------------------------------------------



# Initialization




import pygame


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


TBx = Rect((500,625), (150,100))        # Title button borders
SBx = Rect((290,290), (155,100))        # Start button borders
HBx = Rect((290,440), (155,100))        # Help button borders
OBx = Rect((280,590), (175,100))        # Options button borders

YBx = Rect((240,450), (85,80))          # Yes button borders
NBx = Rect((440,450), (70,80))          # No button borders


gs     = 'title'                        # Gamestate
bu     = 0                              # Mouse button value
po     = 0                              # Mouse position value
pMove  = True                           # Control variable to check if player is moving
cMove  = False                          # Control variable to check if computer is moving
mvdSp  = 0                              # Space a pawn was moved to, for the purpose of updating wp[x]Sp
mvdPos = ()                             # New coordinates of a pawn, for the purpose of updating wp[x]Pos


wp1Pos    = (225,525)                   # Coordinates of wp1
wp2Pos    = (375,525)                   # Coordinates of wp2
wp3Pos    = (525,525)                   # Coordinates of wp3

bp1Pos    = (225,225)                   # Coordinates of bp1
bp2Pos    = (375,225)                   # Coordinates of bp2
bp3Pos    = (525,225)                   # Coordinates of bp3


# Dictionary containing spaces occupy by all pawns
occupy  = {'wp1' : a1, 'wp2' : b1, 'wp3' : c1, 'bp1' : a3, 'bp2' : b3, 'bp3' : c3}

# Dictionaries containins spaces occupy by white team and black team
wo = occupy.copy()
bo = occupy.copy()

# Dictionary checking if a pawn is captured or not
captured = {'wp1' : False, 'wp2' : False, 'wp3' : False, 'bp1' : False, 'bp2' : False, 'bp3' : False}

# Dictionary checking if a space is a valid option to move to
valid = {'a1' : False, 'a2' : False, 'a3' : False,
         'b1' : False, 'b2' : False, 'b3' : False,
         'c1' : False, 'c2' : False, 'c3' : False}

# Dictionary checking if a pawn is selected
selected = {'wp1' : False, 'wp2' : False, 'wp3' : False, 'bp1' : False, 'bp2' : False, 'bp3' : False}


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
    
    global bu
    global po
    global gs
    
    if gs == g and bu == mouse.LEFT:
        
        if b.collidepoint(po):
            return True
        
        else:
            return False
        
    else:
        return False



def inflate(actorIn, xIncrease):
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
        
        
        
def move():
    '''Handles movement of pawns'''
    
    global selected
    global mvdSp
    global mvdPos
    
    if click('play', a2) and valid['a2']:
    
        mvdPos = (225,375)
        mvdSp  = a2
        
    elif click('play', b2) and valid['b2']:
        
        mvdPos = (375,375)
        mvdSp  = b2
    
    elif click('play', c2) and valid['c2']:
        
        mvdPos = (525,375)
        mvdSp  = c2
        
    elif click('play', a3) and valid['a3']:
        
        mvdPos = (225,225)
        mvdSp  = a3
    
    elif click('play', b3) and valid['b3']:
        
        mvdPos = (375,225)
        mvdSp  = b3
        
    elif click('play', c3) and valid['c3']:
        
        mvdPos = (525,225)
        mvdSp  = c3
    
    elif click('play', a1) and valid['a1']:
        
        mvdPos = (225,525)
        mvdSp  = a1
        
    elif click('play', b1) and valid['b1']:
        
        mvdPos = (375,525)
        mvdSp  = b1
        
    elif click('play', c1) and valid['c1']:
        
        mvdPos = (525,525)
        mvdSp = c1
        
    reset()
        
        
        
def capture(team):
    '''Handles capturing of pawns
       
       Parameters:
       team = the team that is capturing the pawn (white or black)
    '''
    
    global captured
    global occupy
    global wo
    global bo
    
    
    wo = occupy.copy()
    wo.pop('bp1')
    wo.pop('bp2')
    wo.pop('bp3')
    
    if captured['wp1']:
        wo.pop('wp1')
    if captured['wp2']:
        wo.pop('wp2')
    if captured['wp3']:
        wo.pop('wp3')
        
    bo = occupy.copy()
    bo.pop('wp1')
    bo.pop('wp2')
    bo.pop('wp3')

    if captured['bp1']:
        bo.pop('bp1')
    if captured['bp2']:
        bo.pop('bp2')
    if captured['bp3']:
        bo.pop('bp3')
    
    
    if team == 'w':
        
        if occupy['bp1'] in wo.values():
            captured['bp1'] = True
        
        elif occupy['bp2'] in wo.values():
            captured['bp2'] = True
        
        elif occupy['bp3'] in wo.values():
            captured['bp3'] = True
    
    
    elif team == 'b':
        
        if occupy['wp1'] in bo.values():
            captured['wp1'] = True
            
        elif occupy['wp2'] in bo.values():
            captured['wp2'] = True
            
        elif occupy['wp3'] in bo.values():
            captured['wp3'] = True
            
            
            
def turn():
    '''Switches turns'''
    
    global pMove
    global cMove
    
    if pMove:
        pMove = False
        cMove = True
        
    elif cMove:
        pMove = True
        cMove = False
            
            
            
def validate(pwn):
    '''Checks if a move is valid or not
       
       Parameters:
       pwn = Pawn that is being moved
    '''
    
    global occupy
    global valid
    global wo
    global bo
    
    
    # White Pawn
    if pwn in wo:
        
        
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
        
        
        if occupy[pwn] == a1 and b2 in bo.values() and b2 not in wo.values():
            valid['b2'] = True
            
        if occupy[pwn] == b1 and a2 in bo.values() and a2 not in wo.values():
            valid['a2'] = True
        
        if occupy[pwn] == b1 and c2 in bo.values() and c2 not in wo.values():
            valid['c2'] = True
            
        if occupy[pwn] == c1 and b2 in bo.values() and b2 not in wo.values():
            valid['b2'] = True
            
        if occupy[pwn] == a2 and b3 in bo.values() and b3 not in wo.values():
            valid['b3'] = True
            
        if occupy[pwn] == b2 and a3 in bo.values() and a3 not in wo.values():
            valid['a3'] = True
        
        if occupy[pwn] == b2 and c3 in bo.values() and c3 not in wo.values():
            valid['c3'] = True
            
        if occupy[pwn] == c2 and b3 in bo.values() and b3 not in wo.values():
            valid['b3'] = True
            
        
    # Black Pawn
    elif pwn in bo:
        
        
        # Moving to empty spaces
        
        
        if occupy[pwn] == a3 and a2 not in occupy.values():
            valid['a2'] = True
        
        elif occupy[pwn] == b3 and b2 not in occupy.values():
            valid['b2'] = True
            
        elif occupy[pwn] == c3 and c2 not in occupy.values():
            valid['c2'] = True
        
        elif occupy[pwn] == a2 and a1 not in occupy.values():
            valid['a1'] = True
            
        elif occupy[pwn] == b2 and b1 not in occupy.values():
            valid['b1'] = True
            
        elif occupy[pwn] == c2 and c1 not in occupy.values():
            valid['c1'] = True
            
        
        # Capturing Pawns
        
        
        if occupy[pwn] == a3 and b2 in wo.values() and b2 not in bo.values():
            valid['b2'] = True
            
        if occupy[pwn] == b3 and a2 in wo.values() and a2 not in bo.values():
            valid['a2'] = True
        
        if occupy[pwn] == b3 and c2 in wo.values() and c2 not in bo.values():
            valid['c2'] = True
            
        if occupy[pwn] == c3 and b2 in wo.values() and b2 not in bo.values():
            valid['b2'] = True
            
        if occupy[pwn] == a2 and b1 in wo.values() and b1 not in bo.values():
            valid['b1'] = True
            
        if occupy[pwn] == b2 and a1 in wo.values() and a1 not in bo.values():
            valid['a1'] = True
        
        if occupy[pwn] == b2 and c1 in wo.values() and c1 not in bo.values():
            valid['c1'] = True
            
        if occupy[pwn] == c2 and b1 in wo.values() and b1 not in bo.values():
            valid['b1'] = True



# Game
    
    


def draw():
    
    
    # Initialization
    
    
    clear()
    
    global TBx
    global SBx
    global HBx
    global OBx
    global YBx
    global NBx
    
    global wp1Pos
    global wp2Pos
    global wp3Pos
    global bp1Pos
    global bp2Pos
    global bp3Pos
    
    global gs
    global pMove
    global cMove
    
    global occupy
    global captured
    global bo
    global wo
    
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
    
    
    # Title Screen
    
    
    if gs == 'title':
        
        wp1Pos    = (225,525)   
        wp2Pos    = (375,525)     
        wp3Pos    = (525,525)              

        bp1Pos    = (225,225)
        bp2Pos    = (375,225)
        bp3Pos    = (525,225)
        
        reset()
        pMove = True
        cMove = False
        occupy   = {'wp1' : a1, 'wp2' : b1, 'wp3' : c1, 'bp1' : a3, 'bp2' : b3, 'bp3' : c3}
        captured = {'wp1' : False, 'wp2' : False, 'wp3' : False,
                    'bp1' : False, 'bp2' : False, 'bp3' : False}
        
        
        write('Hexatron', (235,100), 110)
        write('Start',    (310,300), 80)
        write('Help',     (320,450), 80)
        write('Options',  (290,600), 80)
        
        screen.draw.rect(SBx, color=(0))
        screen.draw.rect(HBx, color=(0))
        screen.draw.rect(OBx, color=(0))
        
    
    # Help Screen
    
    
    elif gs == 'help':
        
        write('How to Play',                                    (200,50),  110)
        write('You can move pawns to an empty space ahead, or', (50, 250), 50)
        write('diagonally to capture an enemy pawn',            (120,300), 50)
        write('Click to select a pawn, click again to cancel',  (75, 375), 50)
        write('To win, reach the other side, capture all of',   (80, 450), 50)
        write('the opponents pawns, or put them in stalemate',  (60, 500), 50)
        write('Title',                                          (522,635), 80)
        
        screen.draw.rect(TBx, color=(0))
    
    
    # Game Screen
    
    
    elif gs == 'play':        
        
        write('1', (100,475), 100)
        write('2', (100,325), 100)
        write('3', (100,175), 100)
        
        write('A', (210,50),  100)
        write('B', (360,50),  100)
        write('C', (510,50),  100)
        
        write('Title', (522,635), 80)
        screen.draw.rect(TBx, color=(0))

        grid()
        pawn()
    
    
    # Win Screen
    
    
    elif gs == 'win':
        
        write('YOU WIN',          (220,100), 150)
        write('Update Database?', (190,350), 80)
        write('Yes',              (250,450), 80)
        write('No',               (450,450), 80)
        
        screen.draw.rect(YBx, color=(0))
        screen.draw.rect(NBx, color=(0))
    
    
    # Lose Screen
    
    
    elif gs == 'lose':
        
        write('YOU LOSE',         (210,100), 150)
        write('Update Database?', (190,350), 80)
        write('Yes',              (250,450), 80)
        write('No',               (450,450), 80)
        
        screen.draw.rect(YBx, color=(0))
        screen.draw.rect(NBx, color=(0))
    
    
    wo = occupy.copy()
    wo.pop('bp1')
    wo.pop('bp2')
    wo.pop('bp3')
    
    if captured['wp1']:
        wo.pop('wp1')
    if captured['wp2']:
        wo.pop('wp2')
    if captured['wp3']:
        wo.pop('wp3')
        
    bo = occupy.copy()
    bo.pop('wp1')
    bo.pop('wp2')
    bo.pop('wp3')

    if captured['bp1']:
        bo.pop('bp1')
    if captured['bp2']:
        bo.pop('bp2')
    if captured['bp3']:
        bo.pop('bp3')
        
        


# Input Functions




def on_mouse_up(pos, button):
    
    global gs
    global bu
    global po
    global pMove
    global cMove
    global mvdPos
    global mvdSp
    
    global occupy
    global valid
    global selected
    
    global wp1Pos
    global wp2Pos
    global wp3Pos
    
    global bp1Pos
    global bp2Pos
    global bp3Pos
    
    global OBx
    global TBx
    global SBx
    global HBx
    
    
    bu = button
    po = pos
    
    
    print(po)
    

    
    
    # Player move
    if pMove:
    
    
    
    
        # All possible moves for Pawn 1    
        if click('play', occupy['wp1']) and captured['wp1'] == False and True not in selected.values():
                        
            selected['wp1'] = True
            validate('wp1')
        
        
        # Pawn 1 movement is cancelled
        elif click('play', occupy['wp1']):
            reset()


        # Pawn 1 is selected to move
        elif selected['wp1']:
            move()
            
            if True not in selected.values():
                
                occupy['wp1'] = mvdSp
                wp1Pos = mvdPos
                capture('w')
                turn()
        
        
        
        # All possible moves for Pawn 2  
        elif click('play', occupy['wp2']) and captured['wp2'] == False and True not in selected.values():
            
            selected['wp2'] = True
            validate('wp2')
                
        
        # Pawn 2 movement is cancelled
        elif click('play', occupy['wp2']):
            reset()
        
        
        # Pawn 2 is selected to move
        elif selected['wp2']:
            move()
            
            if True not in selected.values():
                
                occupy['wp2'] = mvdSp
                wp2Pos = mvdPos
                capture('w')
                turn()
            
            
            
        # All possible moves for Pawn 3
        elif click('play', occupy['wp3']) and captured['wp3'] == False and True not in selected.values():
            
            selected['wp3'] = True
            validate('wp3')


        # Pawn 3 movement is cancelled
        elif click('play', occupy['wp3']):
            reset()

        
        # Pawn 3 is selected to move
        elif selected['wp3']:
            move()
            
            if True not in selected.values():
                
                occupy['wp3'] = mvdSp
                wp3Pos = mvdPos
                capture('w')
                turn()

    
    
    
    # Computer move
    elif cMove:
        
        
        
        
        # All possible moves for Pawn 1    
        if click('play', occupy['bp1']) and captured['bp1'] == False and True not in selected.values():
                        
            selected['bp1'] = True
            validate('bp1')
        
        
        # Pawn 1 movement is cancelled
        elif click('play', occupy['bp1']):
            reset()
        
        
        # Pawn 1 is selected to move
        elif selected['bp1']:
            move()
            
            if True not in selected.values():
                
                occupy['bp1'] = mvdSp
                bp1Pos = mvdPos
                capture('b')
                turn()
                
                
        
        # All possible moves for Pawn 2  
        elif click('play', occupy['bp2']) and captured['bp2'] == False and True not in selected.values():
            
            selected['bp2'] = True
            validate('bp2')
                
        
        # Pawn 2 movement is cancelled
        elif click('play', occupy['bp2']):
            reset()
        
        
        # Pawn 2 is selected to move
        elif selected['bp2']:
            move()
            
            if True not in selected.values():
                
                occupy['bp2'] = mvdSp
                bp2Pos = mvdPos
                capture('b')
                turn()
        
        
        
        # All possible moves for Pawn 3
        elif click('play', occupy['bp3']) and captured['bp3'] == False and True not in selected.values():
            
            selected['bp3'] = True
            validate('bp3')


        # Pawn 3 movement is cancelled
        elif click('play', occupy['bp3']):
            reset()

        
        # Pawn 3 is selected to move
        elif selected['bp3']:
            move()
            
            if True not in selected.values():
                
                occupy['bp3'] = mvdSp
                bp3Pos = mvdPos
                capture('b')
                turn()

    
    # Checking for victory or defeat
    
    
    if gs == 'play' and len(bo) == 0 or a3 in wo.values() or b3 in wo.values() or c3 in wo.values():
        gs = 'win'
        
    elif gs == 'play' and len(wo) == 0 or a1 in bo.values() or b1 in bo.values() or c1 in bo.values():
        gs = 'lose'
        
        
        
        
    # Buttons

    


    # Start the game
    if click('title', SBx):
        gs = 'play'
    
    # Go to help screen
    elif click('title', HBx):
        gs = 'help'
    
    # Go to title screen
    elif click('help', TBx) or click('options', TBx) or click('play', TBx):
        gs = 'title'
        
    # Win: update database
    elif click('win', YBx):
        gs = 'title'
    
    # Lose: update database
    elif click('lose', YBx):
        gs = 'title'
    
    # Don't update database
    elif click('win', NBx) or click('lose', NBx):
        gs = 'title'