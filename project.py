import turtle
import random

# constants
STYLE = ('fixedsys', 18)

WIDTH = 1200
HEIGHT = 600

TOP = HEIGHT/2
BOTTOM = -HEIGHT/2
LEFT = -WIDTH/2
RIGHT = WIDTH/2

BASELINE = -HEIGHT/4
HEART_LINE = 4*HEIGHT/10
SPREAD = 15

TRACER_OFF = 1000
TRACER_ON = 1

GOOD_BACTERIA_NUM = 50
BAD_BACTERIA_NUM = 50

FULL_LIVES = 3
LIVES = FULL_LIVES
SCORE = 0
GAIN = 50
STEP = 1
PLAYER_MOVE = 5

PLAY = True

# images
BACKGROUND = "bg_large.gif"
PLAYER_IMG = "cup_small.gif"
PLAYER_WIDTH = 113
PLAYER_HEIGHT = 126
GOOD_BACTERIA_IMG = "good_bacteria_small.gif"
GOOD_WIDTH = 52
GOOD_HEIGHT = 52
BAD_BACTERIA_IMG = "bad_bacteria_small.gif"
BAD_WIDTH = 64
BAD_HEIGHT = 49
GAME_OVER = "go.gif"
WINNER = "winner.gif"
HEART = "heart_small.gif"
HEART_WIDTH = 40
HEART_HEIGHT = 40

# lists
GOOD_BACTERIA = []
BAD_BACTERIA = []
HEARTS = []

# score turtle
SCORE_TURTLE = turtle.Turtle()
SCORE_TURTLE.penup()
SCORE_TURTLE.hideturtle()
SCORE_TURTLE.goto(-WIDTH/2+HEART_WIDTH, HEART_LINE)
SCORE_TURTLE.write('SCORE: '+str(SCORE), font = STYLE)

# helper functions
def create_heart(x_pos):
    ''' creates a heart sign for lives '''
    heart = turtle.Turtle()
    heart.penup()
    heart.shape(HEART)
    heart.goto(x_pos, HEART_LINE)

    return heart
def remove_heart():
    '''removes hearts from the bar'''
    global PLAY
    if HEARTS:
        heart = HEARTS.pop(-1)
        heart.hideturtle()
    else:
        PLAY = False
def create_bacteria(bacteria_type):
    '''
    creates a bacteria turtle
    bacteria_type: good --> 0 , bad --> 1
    '''
    bacteria = turtle.Turtle()
    bacteria.penup()

    #randomize coordinates
    x = random.randint(LEFT,RIGHT)
    y = random.randint(TOP+max(BAD_HEIGHT, GOOD_HEIGHT)/2, TOP*SPREAD)
    
    bacteria.goto(x, y)
    
    if bacteria_type == 0:
        bacteria.shape(GOOD_BACTERIA_IMG)
    else:
        bacteria.shape(BAD_BACTERIA_IMG)

    return bacteria

def reset_lives(reset_to = FULL_LIVES):
    '''
    refills lives
    '''
    global LIVES
    LIVES = reset_to

def lose_life():
    '''
    -1 lives
    ends game when out of lives
    '''
    
    global LIVES
    global PLAY
    LIVES -= 1
    remove_heart()

    # end game if out of lives
    if LIVES <= 0:
        PLAY = False

def update_score(gain):
    '''
    add gain to score
    '''
    
    global SCORE
    SCORE += gain
    SCORE_TURTLE.clear()
    SCORE_TURTLE.write('SCORE: '+str(SCORE), font = STYLE)
    turtle.update()
    
# set background
turtle.setup(WIDTH, HEIGHT)
turtle.bgpic(BACKGROUND)

#turn off tracer
turtle.tracer(TRACER_OFF)

# register shapes
turtle.register_shape(PLAYER_IMG)
turtle.register_shape(GOOD_BACTERIA_IMG)
turtle.register_shape(BAD_BACTERIA_IMG)
turtle.register_shape(GAME_OVER)
turtle.register_shape(HEART)
turtle.register_shape(WINNER)

# create yogurt cup
player = turtle.Turtle()
player.shape(PLAYER_IMG)
player.penup()
player.goto(0, BASELINE-PLAYER_WIDTH/2)

# update window
turtle.update()

# create bacteria

for _ in range(GOOD_BACTERIA_NUM):
    bacteria = create_bacteria(0)
    GOOD_BACTERIA.append(bacteria)

for _ in range(BAD_BACTERIA_NUM):
    bacteria = create_bacteria(1)
    BAD_BACTERIA.append(bacteria)

# create hearts
HEARTS_START = (-(FULL_LIVES-1)/2)*HEART_WIDTH
for life in range(FULL_LIVES):
    heart = create_heart(HEARTS_START+(HEART_WIDTH*life))
    HEARTS.append(heart)


# set listeners
def left():
    global player
    if player.xcor() > -(WIDTH-PLAYER_WIDTH)/2:
        player.goto(player.xcor()-PLAYER_MOVE, player.ycor())
        turtle.update()

def right():
    global player
    if player.xcor() < (WIDTH-PLAYER_WIDTH)/2:
        player.goto(player.xcor()+PLAYER_MOVE, player.ycor())
        turtle.update()

turtle.onkeypress(right,"Right")
turtle.onkeypress(left,"Left")
turtle.listen()

# the game
while PLAY and (BAD_BACTERIA or GOOD_BACTERIA):
    # go over good bacteria
    NEXT_GOOD = []
    for bacteria in GOOD_BACTERIA:
        bacteria.goto(bacteria.xcor(), bacteria.ycor()-STEP)
        if bacteria.ycor() <= BASELINE+GOOD_HEIGHT/2:
            if player.xcor()-(PLAYER_WIDTH/2)-(GOOD_WIDTH/2) <= bacteria.xcor() <= player.xcor()+(PLAYER_WIDTH/2)+(GOOD_WIDTH/2):
                update_score(GAIN)
            bacteria.hideturtle()
        else:
            NEXT_GOOD.append(bacteria)

    # go over bad bacteria
    NEXT_BAD = []
    for bacteria in BAD_BACTERIA:
        bacteria.goto(bacteria.xcor(), bacteria.ycor()-STEP)
        if bacteria.ycor() <= BASELINE+BAD_HEIGHT/2:
            if player.xcor()-(PLAYER_WIDTH/2)-(BAD_WIDTH/2) <= bacteria.xcor() <= player.xcor()+(PLAYER_WIDTH/2)+(BAD_WIDTH/2):
                lose_life()
            bacteria.hideturtle()
        else:
            NEXT_BAD.append(bacteria)

    GOOD_BACTERIA = NEXT_GOOD
    BAD_BACTERIA = NEXT_BAD

    turtle.update()

if LIVES <= 0:
    game_over = turtle.Turtle()
    game_over.shape(GAME_OVER)
    turtle.update()
else:
    winner = turtle.Turtle()
    winner.shape(WINNER)
    turtle.update()              
# update window
turtle.update()
    

