import pygame
import sys
from pygame.locals import *
import time


class Cell:
    # 实例列表
    all_cells = []

    def __init__(self, pos, border=(0, 0, 0, 0), content=0):
        """
        :param pos:位置
        :param border: 边界，（上，左，下，右），0为无墙，1为蓝，2为红
        :param content:内容物，0为无，1为蓝，2为红
        :return:
        """
        self.pos = pos
        self.border = border
        self.content = content

        Cell.all_cells.append(self)

    def show(self, scr, grid_size=80, border_size=120):
        """
        显示
        :param scr: 屏幕
        :param grid_size: 棋盘格大小
        :param border_size: 棋盘边缘空白大小
        :return:
        """
        BLACK = (0, 0, 0)


        # 画棋盘格
        pygame.draw.rect(
            scr,
            BLACK,
            (
                border_size + self.pos[0] * grid_size,
                border_size + self.pos[1] * grid_size,
                grid_size,
                grid_size),
            5
        )


def eventHandler():
    events = pygame.event.get()
    for event in events:

        # 退出
        if event.type == QUIT:
            pygame.display.quit()
            sys.exit()


def init_screen(*, grid_num, grid_size, border_size):
    """
    初始化屏幕
    """

    width = height = grid_num * grid_size + border_size * 2
    screen = pygame.display.set_mode((width, height))
    ico = pygame.image.load('./resources/icon/xo.png')

    pygame.display.set_icon(ico)
    pygame.display.set_caption('围城')
    return screen


def main():
    pygame.init()
    screen = init_screen(grid_size=80, grid_num=7, border_size=120)
    for i in range(7):
        for j in range(7):
            a = Cell((i, j))
    while True:
        eventHandler()
        screen.fill((255, 255, 255))
        for cell in Cell.all_cells:
            cell.show(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
