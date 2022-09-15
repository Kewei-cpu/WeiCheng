import pygame
import sys
from pygame.locals import *
import time

initRole = initStep = 1
initFlag = 0
cross_pos = circle_pos = []
b = chess_h = chess_v = chess_cross_bfs = []
chess_all = 7
times = 0
isStart = False
win_cross_bfs = win_circle_bfs = []
global_time = 20
clock_ = global_time
clock = pygame.time.Clock()

chess_space = 120
chess_cell_size = 80
chess_cell_num = 7


def matrix(row, column, item):
    matrix_list = []
    for i in range(row):
        matrix_list.append([])
        for j in range(column):
            matrix_list[i].append(item)
    return matrix_list


def time_judge():
    global clock_, initStep, initRole
    if clock_ <= 0:
        if initRole == 1:
            if initStep == 1:
                initRole = 1
                initStep = 2
            elif initStep == 2:
                if cross_pos[1] >= 1:
                    if chess_h[cross_pos[0]][cross_pos[1] - 1] == 0:
                        chess_h[cross_pos[0]][cross_pos[1] - 1] = 1
                if cross_pos[1] <= chess_cell_num - 2:
                    if chess_h[cross_pos[0]][cross_pos[1]] == 0:
                        chess_h[cross_pos[0]][cross_pos[1]] = 1
                if cross_pos[0] >= 1:
                    if chess_v[cross_pos[0] - 1][cross_pos[1]] == 0:
                        chess_v[cross_pos[0] - 1][cross_pos[1]] = 1
                if cross_pos[0] <= chess_cell_num - 2:
                    if chess_v[cross_pos[0]][cross_pos[1]] == 0:
                        chess_v[cross_pos[0]][cross_pos[1]] = 1
                    initRole = 2
                    initStep = 1
        elif initRole == 2:
            if initStep == 1:
                initStep = 2
            elif initStep == 2:
                if cross_pos[1] >= 1:
                    if chess_h[circle_pos[0]][circle_pos[1] - 1] == 0:
                        chess_h[circle_pos[0]][circle_pos[1] - 1] = 1
                if circle_pos[1] <= chess_cell_num - 2:
                    if chess_h[circle_pos[0]][circle_pos[1]] == 0:
                        chess_h[circle_pos[0]][circle_pos[1]] = 1
                if circle_pos[0] >= 1:
                    if chess_v[circle_pos[0] - 1][circle_pos[1]] == 0:
                        chess_v[circle_pos[0] - 1][circle_pos[1]] = 1
                if circle_pos[0] <= chess_cell_num - 2:
                    if chess_v[circle_pos[0]][circle_pos[1]] == 0:
                        chess_v[circle_pos[0]][circle_pos[1]] = 1
                initRole = 1
                initStep = 1
        clock_ = global_time


def bfs(wall_hor, wall_ver, start_point, gone_place, step=50):
    dis_array = []
    gone_place[start_point[0]][start_point[1]] = 1
    x, y = len(gone_place), len(gone_place[0])
    if step != 0:
        step -= 1

        if start_point[1] - 1 >= 0:
            if wall_hor[start_point[0]][start_point[1] - 1] == 0 and gone_place[start_point[0]][
                start_point[1] - 1] == 0:
                dis_array.append([start_point[0], start_point[1] - 1, step])
                
            

        if start_point[1] + 1 <= y - 1:
            if wall_hor[start_point[0]][start_point[1]] == 0 and gone_place[start_point[0]][start_point[1] + 1] == 0:
                dis_array.append([start_point[0], start_point[1] + 1, step])
                


        if start_point[0] - 1 >= 0:
            if wall_ver[start_point[0] - 1][start_point[1]] == 0 and gone_place[start_point[0] - 1][
                start_point[1]] == 0:
                dis_array.append([start_point[0] - 1, start_point[1], step])
                
            

        if start_point[0] + 1 <= x - 1:
            if wall_ver[start_point[0]][start_point[1]] == 0 and gone_place[start_point[0] + 1][start_point[1]] == 0:
                dis_array.append([start_point[0] + 1, start_point[1], step])
                
            

        for i in dis_array:
            gone_place = bfs(wall_hor, wall_ver, [i[0], i[1]], gone_place, i[2])

    return gone_place


def bfs_include_circle(wall_hor, wall_ver, start_point, gone_place, step=50000):
    if step != 0 and start_point != circle_pos:
        dis_array = []
        x, y = len(gone_place), len(gone_place[0])
        gone_place[start_point[0]][start_point[1]] = 1
        step -= 1

        if start_point[1] - 1 >= 0:
            if wall_hor[start_point[0]][start_point[1] - 1] == 0 and gone_place[start_point[0]][
                start_point[1] - 1] == 0 and not (
                    start_point[0] == circle_pos[0] and start_point[1] - 1 == circle_pos[1]):
                dis_array.append([start_point[0], start_point[1] - 1, step])
                
            

        if start_point[1] + 1 <= y - 1:
            if wall_hor[start_point[0]][start_point[1]] == 0 and gone_place[start_point[0]][start_point[1] + 1] == 0 \
                    and not (start_point[0] == circle_pos[0] and start_point[1] + 1 == circle_pos[1]):
                dis_array.append([start_point[0], start_point[1] + 1, step])
                
            

        if start_point[0] - 1 >= 0:
            if wall_ver[start_point[0] - 1][start_point[1]] == 0 and gone_place[start_point[0] - 1][
                start_point[1]] == 0 and not (start_point[0] - 1 == circle_pos[0] and start_point[1] == circle_pos[1]):
                dis_array.append([start_point[0] - 1, start_point[1], step])
                
            

        if start_point[0] + 1 <= x - 1:
            if wall_ver[start_point[0]][start_point[1]] == 0 and gone_place[start_point[0] + 1][start_point[1]] == 0 \
                    and not (start_point[0] + 1 == circle_pos[0] and start_point[1] == circle_pos[1]):
                dis_array.append([start_point[0] + 1, start_point[1], step])
                
            

        for i in dis_array:
            gone_place = bfs(wall_hor, wall_ver, [i[0], i[1]], gone_place, i[2])

    return gone_place


def bfs_include_cross(wall_hor, wall_ver, start_point, gone_place, step=50000):
    if step != 0 and start_point != cross_pos:
        dis_array = []
        x, y = len(gone_place), len(gone_place[0])
        gone_place[start_point[0]][start_point[1]] = 1
        step -= 1

        if start_point[1] - 1 >= 0:
            if wall_hor[start_point[0]][start_point[1] - 1] == 0 and gone_place[start_point[0]][
                start_point[1] - 1] == 0 and not (
                    start_point[0] == cross_pos[0] and start_point[1] - 1 == cross_pos[1]):
                dis_array.append([start_point[0], start_point[1] - 1, step])
                
            

        if start_point[1] + 1 <= y - 1:
            if wall_hor[start_point[0]][start_point[1]] == 0 and gone_place[start_point[0]][start_point[1] + 1] == 0 \
                    and not (start_point[0] == cross_pos[0] and start_point[1] + 1 == cross_pos[1]):
                dis_array.append([start_point[0], start_point[1] + 1, step])
                
            

        if start_point[0] - 1 >= 0:
            if wall_ver[start_point[0] - 1][start_point[1]] == 0 and gone_place[start_point[0] - 1][
                start_point[1]] == 0 and not (start_point[0] - 1 == cross_pos[0] and start_point[1] == cross_pos[1]):
                dis_array.append([start_point[0] - 1, start_point[1], step])
                
            

        if start_point[0] + 1 <= x - 1:
            if wall_ver[start_point[0]][start_point[1]] == 0 and gone_place[start_point[0] + 1][start_point[1]] == 0 \
                    and not (start_point[0] + 1 == cross_pos[0] and start_point[1] == cross_pos[1]):
                dis_array.append([start_point[0] + 1, start_point[1], step])
                
            

        for i in dis_array:
            gone_place = bfs(wall_hor, wall_ver, [i[0], i[1]], gone_place, i[2])

    return gone_place


def init_chess(screen, hor, ver, cross_bfs, circle_bfs, cell_num, cell_size, space, normal_width=1,
               abnormal_width=3):
    if initFlag == 0:
        for i in range(len(cross_bfs)):
            for j in range(len(cross_bfs[0])):
                if cross_bfs[i][j] == 1:
                    pygame.draw.rect(screen, (139, 164, 196), (
                        space + i * cell_size, space + j * cell_size, cell_size / 4, cell_size / 4),
                                     0)

        for i in range(len(circle_bfs)):
            for j in range(len(circle_bfs[0])):
                if circle_bfs[i][j] == 1:
                    pygame.draw.rect(screen, (234, 96, 130), (
                        space + (i + 0.75) * cell_size, space + (j + 0.75) * cell_size, cell_size / 4, cell_size / 4),
                                     0)

    else:
        for i in range(len(win_cross_bfs)):
            for j in range(len(win_cross_bfs[0])):
                if win_cross_bfs[i][j] == 1:
                    pygame.draw.rect(screen, (139, 164, 196), (
                        space + i * cell_size, space + j * cell_size, cell_size, cell_size), 0)

        for i in range(len(win_circle_bfs)):
            for j in range(len(win_circle_bfs[0])):
                if win_circle_bfs[i][j] == 1:
                    pygame.draw.rect(screen, (255, 90, 120), (
                        space + i * cell_size, space + j * cell_size, cell_size, cell_size), 0)

    for x in range(0, cell_size * cell_num - 1, cell_size):
        pygame.draw.line(screen, (0, 0, 0), (x + space, 0 + space),
                         (x + space, cell_size * cell_num + space), normal_width)

    for y in range(0, cell_size * cell_num - 1, cell_size):
        pygame.draw.line(screen, (0, 0, 0), (0 + space, y + space),
                         (cell_size * cell_num + space, y + space), normal_width)

    pygame.draw.line(screen, (0, 0, 0), (space, space),
                     (space, space + cell_size * cell_num), abnormal_width)
    pygame.draw.line(screen, (0, 0, 0), (space, space),
                     (space + cell_size * cell_num, space), abnormal_width)
    pygame.draw.line(screen, (0, 0, 0), (space + cell_size * cell_num, space + cell_size * cell_num),
                     (space, space + cell_size * cell_num), abnormal_width)
    pygame.draw.line(screen, (0, 0, 0), (space + cell_size * cell_num, space + cell_size * cell_num),
                     (space + cell_size * cell_num, space), abnormal_width)

    for i in range(len(hor)):
        for j in range(len(hor[0])):
            if hor[i][j] == 1:
                pygame.draw.line(screen, (80, 100, 196),
                                 (space + i * cell_size, space + (j + 1) * cell_size),
                                 (space + (i + 1) * cell_size, space + (j + 1) * cell_size), abnormal_width)
            if hor[i][j] == 2:
                pygame.draw.line(screen, (170, 50, 80),
                                 (space + i * cell_size, space + (j + 1) * cell_size),
                                 (space + (i + 1) * cell_size, space + (j + 1) * cell_size), abnormal_width)

    for i in range(len(ver)):
        for j in range(len(ver[0])):
            if ver[i][j] == 1:
                pygame.draw.line(screen, (80, 100, 196),
                                 (space + (i + 1) * cell_size, space + j * cell_size),
                                 (space + (i + 1) * cell_size, space + (j + 1) * cell_size), abnormal_width)

            if ver[i][j] == 2:
                pygame.draw.line(screen, (170, 50, 80),
                                 (space + (i + 1) * cell_size, space + j * cell_size),
                                 (space + (i + 1) * cell_size, space + (j + 1) * cell_size), abnormal_width)

    screen.blit(cross, (space + cross_pos[0] * cell_size, space + cross_pos[1] * cell_size))
    screen.blit(circle, (space + circle_pos[0] * cell_size, space + circle_pos[1] * cell_size))


def isWin():
    global times, initFlag, win_cross_bfs, win_circle_bfs, w_circle, w_cross
    win_cross_bfs = bfs(chess_h, chess_v, cross_pos, matrix(chess_all, chess_all, 0), 5000)
    win_circle_bfs = bfs(chess_h, chess_v, circle_pos, matrix(chess_all, chess_all, 0), 5000)
    if win_cross_bfs[circle_pos[0]][circle_pos[1]] == 0:
        w_cross = 0
        w_circle = 0
        for i in range(len(win_cross_bfs)):
            for j in range(len(win_cross_bfs[0])):
                if win_cross_bfs[i][j] == 1:
                    w_cross += 1

        for i in range(len(win_circle_bfs)):
            for j in range(len(win_circle_bfs[0])):
                if win_circle_bfs[i][j] == 1:
                    w_circle += 1
        print(w_cross, ':', w_circle)
        if w_cross > w_circle:
            initFlag = 1
        elif w_cross < w_circle:
            initFlag = 2
        else:
            initFlag = 3

        chess_cross_bfs = bfs_include_circle(chess_h, chess_v, cross_pos, matrix(chess_all, chess_all, 0), 3)
        chess_cross_bfs[circle_pos[0]][circle_pos[1]] = 0
        chess_circle_bfs = bfs_include_cross(chess_h, chess_v, circle_pos, matrix(chess_all, chess_all, 0), 3)
        chess_circle_bfs[cross_pos[0]][cross_pos[1]] = 0
        init_chess(screen, chess_h, chess_v, chess_cross_bfs, chess_circle_bfs, chess_cell_num, chess_cell_size,
                   chess_space, 1, 10)
        textRend()
        pygame.display.update()
        time.sleep(5)
        initMat()


def eventHerder():
    for event in pygame.event.get():
        global initRole, initStep, initFlag, clock_
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if chess_space <= x <= chess_space + chess_cell_size * chess_cell_num and chess_space <= y <= chess_space + \
                    chess_cell_size * chess_cell_num:

                chess_cross_bfs_3 = bfs(chess_h, chess_v, cross_pos, matrix(chess_all, chess_all, 0), 3)
                chess_circle_bfs_3 = bfs(chess_h, chess_v, circle_pos, matrix(chess_all, chess_all, 0), 3)
                chess_cross_bfs_3[circle_pos[0]][circle_pos[1]] = 0
                chess_circle_bfs_3[cross_pos[0]][cross_pos[1]] = 0

                if initRole == 1 and initStep == 1:
                    if chess_cross_bfs_3[(x - chess_space) // chess_cell_size][
                        (y - chess_space) // chess_cell_size] == 1:
                        cross_pos[0] = (x - chess_space) // chess_cell_size
                        cross_pos[1] = (y - chess_space) // chess_cell_size
                        initStep = 2
                        clock_ = global_time

                if initRole == 2 and initStep == 1:
                    if chess_circle_bfs_3[(x - chess_space) // chess_cell_size][
                        (y - chess_space) // chess_cell_size] == 1:
                        circle_pos[0] = (x - chess_space) // chess_cell_size
                        circle_pos[1] = (y - chess_space) // chess_cell_size
                        initStep = 2
                        clock_ = global_time

        if event.type == KEYDOWN:
            if initRole == 1 and initStep == 2:
                if event.key == pygame.K_UP:
                    if cross_pos[1] >= 1:
                        if chess_h[cross_pos[0]][cross_pos[1] - 1] == 0:
                            chess_h[cross_pos[0]][cross_pos[1] - 1] = 1
                            initRole = 2
                            initStep = 1
                            clock_ = global_time

                if event.key == pygame.K_DOWN:
                    if cross_pos[1] <= chess_cell_num - 2:
                        if chess_h[cross_pos[0]][cross_pos[1]] == 0:
                            chess_h[cross_pos[0]][cross_pos[1]] = 1
                            initRole = 2
                            initStep = 1
                            clock_ = global_time

                if event.key == pygame.K_LEFT:
                    if cross_pos[0] >= 1:
                        if chess_v[cross_pos[0] - 1][cross_pos[1]] == 0:
                            chess_v[cross_pos[0] - 1][cross_pos[1]] = 1
                            initRole = 2
                            initStep = 1
                            clock_ = global_time

                if event.key == pygame.K_RIGHT:
                    if cross_pos[0] <= chess_cell_num - 2:
                        if chess_v[cross_pos[0]][cross_pos[1]] == 0:
                            chess_v[cross_pos[0]][cross_pos[1]] = 1
                            initRole = 2
                            initStep = 1
                            clock_ = global_time

            if initRole == 2 and initStep == 2:
                if event.key == pygame.K_UP:
                    if circle_pos[1] >= 1:
                        if chess_h[circle_pos[0]][circle_pos[1] - 1] == 0:
                            chess_h[circle_pos[0]][circle_pos[1] - 1] = 2
                            initRole = 1
                            initStep = 1
                            clock_ = global_time

                if event.key == pygame.K_DOWN:
                    if circle_pos[1] <= chess_cell_num - 2:
                        if chess_h[circle_pos[0]][circle_pos[1]] == 0:
                            chess_h[circle_pos[0]][circle_pos[1]] = 2
                            initRole = 1
                            initStep = 1
                            clock_ = global_time

                if event.key == pygame.K_LEFT:
                    if circle_pos[0] >= 1:
                        if chess_v[circle_pos[0] - 1][circle_pos[1]] == 0:
                            chess_v[circle_pos[0] - 1][circle_pos[1]] = 2
                            initRole = 1
                            initStep = 1
                            clock_ = global_time

                if event.key == pygame.K_RIGHT:
                    if circle_pos[0] <= chess_cell_num - 2:
                        if chess_v[circle_pos[0]][circle_pos[1]] == 0:
                            chess_v[circle_pos[0]][circle_pos[1]] = 2
                            initRole = 1
                            initStep = 1
                            clock_ = global_time
            if event.key == K_SPACE:
                initMat()


def game_clock():
    global clock_
    pygame.time.get_ticks()
    if pygame.time.get_ticks() % 1 == 0:
        screen.fill((220, 220, 220))
        clock_ -= 0.1
        clock_ = round(clock_, 2)
    clock.tick(10)
    clock_g = str(clock_)
    largeText = pygame.font.Font('./resources/ali-font.ttf', 30)
    TextSurf, TextRect = text_objects(clock_g, largeText)
    TextRect.topleft = (25, 25)
    screen.blit(TextSurf, TextRect)


def text_objects(text, font):
    textSurface = font.render(text, True, (0, 0, 0))
    return textSurface, textSurface.get_rect()


def text_objects_complex(text, font, isBold, color):
    textSurface = font.render(text, isBold, color)
    return textSurface, textSurface.get_rect()


def textRend():
    global initRole, initStep
    blue = (100, 130, 170)
    red = (200, 70, 100)
    if initFlag == 0:
        myfont = pygame.font.Font('./resources/ali-font.ttf', 60)
        if initRole == 1:
            if initStep == 1:
                textImage, textRect = text_objects_complex("蓝方  移动", myfont, True, blue)
            else:
                textImage, textRect = text_objects_complex("蓝方  放置", myfont, True, blue)
        else:
            if initStep == 1:
                textImage, textRect = text_objects_complex("红方  移动", myfont, True, red)
            else:
                textImage, textRect = text_objects_complex("红方  放置", myfont, True, red)

        textRect.midtop = 400, 20
        screen.blit(textImage, textRect)

    else:
        font = pygame.font.Font('./resources/ali-font.ttf', 80)
        if initFlag == 1:
            textImage, textRect = text_objects("蓝方  获胜", font)
            textImage_2, textRect_2 = text_objects('%d : %d' % (w_cross, w_circle), font)
        elif initFlag == 2:
            textImage, textRect = text_objects("红方  获胜", font)
            textImage_2, textRect_2 = text_objects('%d : %d' % (w_cross, w_circle), font)
        else:
            textImage, textRect = text_objects("平局", font)
            textImage_2, textRect_2 = text_objects('%d : %d' % (w_cross, w_circle), font)

        textRect.midtop, textRect_2.midbottom = (400, 20), (400, 780)

        screen.blit(textImage, textRect)
        screen.blit(textImage_2, textRect_2)


def initMat():
    global b, chess_h, chess_v, chess_cross_bfs, cross_pos, circle_pos, initRole, initStep, initFlag, times, clock_
    initRole = initStep = 1
    initFlag = 0
    b = matrix(chess_all, chess_all, 0)
    chess_v = matrix(chess_all - 1, chess_all, 0)
    chess_h = matrix(chess_all, chess_all - 1, 0)
    cross_pos = [0, 0]
    circle_pos = [chess_all - 1, chess_all - 1]
    times = 0
    clock_ = global_time


dots = 1


def pre_init():
    global dots
    screen.fill((220, 220, 220))

    font = pygame.font.Font('./resources/ali-font.ttf', 80)
    text_surface, text_rect = text_objects('围   城', font)
    text_rect.center = (400, 100)
    screen.blit(text_surface, text_rect)

    font_1 = pygame.font.Font('./resources/ali-font.ttf', 20)
    text_1_surface, text_1_rect = text_objects('作者：C191337  赵科为', font_1)
    text_1_rect.center = (400, 170)
    screen.blit(text_1_surface, text_1_rect)

    pygame.draw.line(screen, (0, 0, 0), (50, 225), (750, 225))

    font_2 = pygame.font.Font('./resources/ali-font.ttf', 60)
    text_2_surface, text_2_rect = text_objects('游戏规则', font_2)
    text_2_rect.center = (400, 300)
    screen.blit(text_2_surface, text_2_rect)

    font_3 = pygame.font.Font('./resources/ali-font.ttf', 20)
    text_3_1_surface, text_3_1_rect = text_objects('7 X 7 棋盘，两名玩家位于对角', font_3)
    text_3_1_rect.center = (400, 380)
    screen.blit(text_3_1_surface, text_3_1_rect)

    text_3_2_surface, text_3_2_rect = text_objects('两名玩家轮流进行0~3步移动（对应颜色的小点表示可到达的位置，点击格子来移动）', font_3)
    text_3_2_rect.center = (400, 420)
    screen.blit(text_3_2_surface, text_3_2_rect)

    text_3_3_surface, text_3_3_rect = text_objects('移动之后，放置一堵也当前位置相邻的墙（必须放置，按上下左右键）', font_3)
    text_3_3_rect.center = (400, 460)
    screen.blit(text_3_3_surface, text_3_3_rect)

    text_3_4_surface, text_3_4_rect = text_objects('当两人完全被墙分开至不同区域时，游戏结束', font_3)
    text_3_4_rect.center = (400, 500)
    screen.blit(text_3_4_surface, text_3_4_rect)

    text_3_5_surface, text_3_5_rect = text_objects('按所占的区域大小判断胜负，格数多者胜。如果有一些格两人都不拥有，则不计入', font_3)
    text_3_5_rect.center = (400, 540)
    screen.blit(text_3_5_surface, text_3_5_rect)

    pygame.draw.line(screen, (0, 0, 0), (50, 635), (750, 635))

    font_2 = pygame.font.Font('./resources/ali-font.ttf', 40)
    if 1 <= dots <= 50:
        text_2_surface, text_2_rect = text_objects('按任意键开始游戏.  ', font_2)
        dots += 1
    elif 51 <= dots <= 100:
        text_2_surface, text_2_rect = text_objects('按任意键开始游戏.. ', font_2)
        dots += 1
    elif 101 <= dots <= 150:
        text_2_surface, text_2_rect = text_objects('按任意键开始游戏...', font_2)
        dots += 1
    else:
        text_2_surface, text_2_rect = text_objects('按任意键开始游戏...', font_2)
        dots = 1

    text_2_rect.center = (400, 700)
    screen.blit(text_2_surface, text_2_rect)


def pre_eventHearder():
    global isStart
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
            isStart = True


pygame.init()

initMat()

grid_size = chess_cell_size * chess_cell_num + chess_space * 2  # 棋盘的大小
pygame.display.set_caption('围城 by 科为')
screen = pygame.display.set_mode((grid_size, grid_size))  # 设置窗口长宽

cross = pygame.image.load('./resources/cross.png')
cross = pygame.transform.scale(cross, (chess_cell_size, chess_cell_size))
circle = pygame.image.load('./resources/circle.png')
circle = pygame.transform.scale(circle, (chess_cell_size, chess_cell_size))

while True:
    if not isStart:
        pre_init()
        pre_eventHearder()
    else:
        eventHerder()
        game_clock()
        chess_cross_bfs = bfs_include_circle(chess_h, chess_v, cross_pos, matrix(chess_all, chess_all, 0), 3)
        chess_cross_bfs[circle_pos[0]][circle_pos[1]] = 0
        chess_circle_bfs = bfs_include_cross(chess_h, chess_v, circle_pos, matrix(chess_all, chess_all, 0), 3)
        chess_circle_bfs[cross_pos[0]][cross_pos[1]] = 0
        init_chess(screen, chess_h, chess_v, chess_cross_bfs, chess_circle_bfs, chess_cell_num, chess_cell_size,
                   chess_space, 1, 5)
        time_judge()
        isWin()
        textRend()

    pygame.display.update()
