#!/usr/bin/python3

import math, sys, random, re
import pickle as Pickle

import pygame, eztext
import compute

FPATH_DIKTRVRS = "./dikt_rvrs.pickle"
FPATH_DIKT = "./dikt_word.pickle"
FPATH_EMBEDDINGS = "./embeddings.pickle"

def read_data(fpath):
    """
    args:
        fpath       : str or pathlike object
    return:
        data        : 
    """
    with open(fpath, "rb") as fo:
        dikt = Pickle.load(fo, encoding="bytes")
    return dikt

pygame.init()

size = width, height = 1000, 1000
# speed = [2, 2]
black = 0, 0, 0
white = 255, 255, 255

screen = pygame.display.set_mode(size)


V = read_data(FPATH_EMBEDDINGS)
dikt = read_data(FPATH_DIKT)
dikt_rvrs = read_data(FPATH_DIKTRVRS)


def do_movement(obj):
    obj = obj.move(speed)
    if obj.left < 0 or obj.right > width: speed[0] = -speed[0]
    if obj.top < 0 or obj.bottom > height: speed[1] = -speed[1]

def calculate_cosinesim(vec_entry, vec_target):
    try:
        AB = 0
        A_sqr = 0
        B_sqr = 0
        
        for a,b in zip(vec_entry, vec_target): AB += a*b
        for x in vec_entry: A_sqr += x**2
        for x in vec_target: B_sqr += x**2
        
        similarity = abs(AB/((A_sqr**0.5)*(B_sqr**0.5)))
        return similarity
    except KeyError as e:
        return "ee"


def MyFirst(image, sss):
    sprite = pygame.sprite.Sprite()
    sprite.image = image
    sprite.rect = image.get_rect()
    font = pygame.font.SysFont('Sans', 30)
    text = font.render(sss, True, (255, 0, 0))
    sprite.image.blit(text, sprite.rect)
    group = pygame.sprite.Group()
    group.add(sprite)
    group.draw(screen)

def generate_seq_coord_now(B):
    seq_coord_now = []
    for ballrect in B:
        seq_coord_now.append([ballrect.x, ballrect.y])
    return seq_coord_now

def calculate_speed(seq_coord_now, seq_coord_goal):
    seq_speed = []
    for coord_now, coord_goal in zip(seq_coord_now, seq_coord_goal):
        x_elem = (coord_goal[0] - coord_now[0])
        y_elem = (coord_goal[1] - coord_now[1])
        base = abs(x_elem) + abs(y_elem)
        speed = [(x_elem/base)*4, (y_elem/base)*4]
        seq_speed.append(speed)
    return seq_speed

num_shown = 20

i = 0
A=[]
B=[]

while(i < num_shown):
    # ball = pygame.image.load("bubble2.jpg").convert()
    # ball.fill((255,255,255,128))
    ball = pygame.Surface((200,50), pygame.SRCALPHA)   # per-pixel alpha
    ball.fill((255,255,255,0))
    ballrect = ball.get_rect()
    A.append(ball)
    B.append(ballrect)
    # speed.append([2,2])
    i+=1

level = 1
point = 0
life = 100
msg = ""

txtbx = eztext.Input(maxlength=45, color=(0,255,0), prompt='type here: ', x=300, y=900)
clock = pygame.time.Clock()

# Loading
ips = [(100,100),(100,200),(100,300),(100,400),(100,500),
        (200,100),(200,200),(200,300),(200,400),(200,500),
        (300,100),(300,200),(300,300),(300,400),(300,500),
        (400,100),(400,200),(400,300),(400,400),(400,500)]

seq_index = [random.randint(0,(level)*2000) for i in range(num_shown)]
seq_word_shown = [dikt_rvrs[index] for index in seq_index]
result_pca = compute.get_seq_coordinate(seq_index, 100, V)
seq_coord_goal = [[500 + 75*coord_rel[0], 500 + 75*coord_rel[1]] for coord_rel in result_pca]
speed = calculate_speed(ips, seq_coord_goal)


is_init = True
while 1:
    # make sure the program is running at 30 fps
    clock.tick(30)

    # events for txtbx
    events = pygame.event.get()
    # process other events
    for event in events:
        # close it x button si pressed
        if event.type == pygame.QUIT: sys.exit()


    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT: sys.exit()
    # events = pygame.event.get()

    screen.fill(black)
    screen = pygame.display.get_surface()

    for i in range(num_shown):
        if is_init: B[i].move_ip(*ips[i])
        B[i] = B[i].move(speed[i])
        if B[i].left < 0  or B[i].right > width: speed[i][0] = -speed[i][0]
        if B[i].top < 0  or B[i].bottom > height: speed[i][1] = -speed[i][1]
        screen.blit(A[i], B[i])
        MyFirst(A[i], dikt_rvrs[seq_index[i]])

    # Level board
    # ball_level = pygame.Surface((200,50), pygame.SRCALPHA)   # per-pixel alpha
    # ball_level.fill((0,0,255,255))
    # ballrect_level = ball_level.get_rect()
    # ballrect_level.move_ip(500,0)
    # screen.blit(ball_level, ballrect_level)
    # MyFirst(ball_level, "Current Level: {0}".format(level))

    # Point board
    ball_point = pygame.Surface((1000,50), pygame.SRCALPHA)   # per-pixel alpha
    ball_point.fill((0,0,255,255))
    ballrect_point = ball_point.get_rect()
    screen.blit(ball_point, ballrect_point)
    MyFirst(ball_point, "Current Level: {0}   Score: {1:6f}   Life: {2:6f}    {3}".format(level, point, life, msg))

    # textbox operations
    txtbx.update(events)
    # blit txtbx on the sceen
    txtbx.draw(screen)

    if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_RETURN) and (len(txtbx.value) > 0):
        entry = txtbx.value
        txtbx.value=""
        # print(txtbx.value)
        

        seq_coord_now =generate_seq_coord_now(B)
        try:
            # print(len(entry.split(" ")))
            # seq_parse = entry.split(" ")
            # if len(seq_parse) > 0:
            #     vec_entry = V[dikt[seq_parse[0]]] + V[dikt[seq_parse[1]]]
            
            entry_split = re.split('([+|-])', entry)
            if len(entry_split)>1:
                vec_entry = V[dikt[entry_split[0]]]
                for i in range(int(len(entry_split[1:])/2)):

                    if entry_split[(i+1)*2 -1] =="+":
                        vec_entry = vec_entry + V[dikt[entry_split[(i+1)*2]]]
                    elif entry_split[(i+1)*2 -1] =="-":
                        vec_entry = vec_entry - V[dikt[entry_split[(i+1)*2]]]
            else:
                vec_entry = V[dikt[entry]]
            
            seq_possim = []
            for pos, word_shown in enumerate(seq_word_shown):
                # vec_entry = V[index]
                vec_target = V[dikt[word_shown]]
                similarity = calculate_cosinesim(vec_entry, vec_target)
                # print(similarity)
                if 0.3 < similarity:
                    seq_possim.append([pos, similarity])
                
                
            seq_possim = sorted(seq_possim, key=lambda l:l[1], reverse=True)
            print(seq_possim)

            # for i in range(num_shown):
            #     if is_init: B[i].move_ip(*ips[i])
            #     B[i] = B[i].move(speed[i])
            #     if B[i].left < 0  or B[i].right > width: speed[i][0] = -speed[i][0]
            #     if B[i].top < 0  or B[i].bottom > height: speed[i][1] = -speed[i][1]
            #     ball = pygame.Surface((200,50), pygame.SRCALPHA)   # per-pixel alpha
            #     A[i].fill((255,255,255,0))
            #     screen.blit(A[i], B[i])

            # Delete target object(s)
            for possim in seq_possim[:1]:
                # word_shot = possim[0]
                # pos_word_shot = seq_word_shown.index(word_shot)
                pos_word_shot = possim[0]
                print(possim[1])
                if possim[1] > 0.99:
                    msg = "SAME WORD!"
                else:
                    msg = ""
                    point += possim[1]
                    life += 10*possim[1]**2
                # print(pos_word_shot)
                index_newgen = dikt_rvrs[random.randint(0,(level)*2000)]
                seq_word_shown[pos_word_shot] = index_newgen


                A[pos_word_shot]
                B[pos_word_shot]

                # Boom Effect
                ball_boom = pygame.image.load("boom.jpg").convert()
                # ball_boom = pygame.Surface((200,50), pygame.SRCALPHA)   # per-pixel alpha
                # ball_boom.fill((0,255,0,127))
                ballrect_boom = ball_boom.get_rect()
                screen.blit(ball_boom, B[pos_word_shot])
                
                # Regenenrate Object
                ball = pygame.Surface((200,50), pygame.SRCALPHA)   # per-pixel alpha
                ball.fill((255,255,255,0))
                ballrect = ball.get_rect()
                ballrect.move_ip(*seq_coord_now[pos_word_shot])
                

                A[pos_word_shot] = ball
                B[pos_word_shot] = ballrect
            msg = entry
        except KeyError:
            msg = "NOT REAL WORD!"
            pass

        print(seq_word_shown)
        

        # Update goal position
        seq_index = [dikt[word_shown] for word_shown in seq_word_shown]
        result_pca = compute.get_seq_coordinate(seq_index, 100, V)

        seq_coord_goal = [[500 + 75*coord_rel[0], 500 + 75*coord_rel[1]] for coord_rel in result_pca]
        speed = calculate_speed(seq_coord_now, seq_coord_goal)

        # Update level state
        if point > level*4:
            level += 1
    life -= 0.01

    is_init = False

    if life <=0:
        print("Your Final Level: {0}".format(level))
        print("Your Final Point: {0}".format(point))
        print("Your seem to know {0} words".format(int(point*400)))
        print(msg)
        sys.exit()

    pygame.display.flip()
