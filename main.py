import random
import sys

import numpy as np
import pygame
from pygame.locals import *


class Cell:
    # 实例列表
    all_cells = []
    all_cells_2d = None

    def __init__(self, pos):
        """
        :param pos:位置
        :return:
        """
        self.pos = pos
        self.content = None

        # 网格四周墙壁情况 0为无 -1为边界 1为放置的墙
        self.left = None
        self.top = None
        self.right = None
        self.bottom = None

        self.all_cells.append(self)
        self.all_cells_2d[pos[0], pos[1]] = self

    @classmethod
    def display(cls, scr):
        """
        显示所有网格
        :param scr: 屏幕
        :return:
        """

        for cell in cls.all_cells:
            cell.draw(scr)
            cell.draw_wall(scr)

    def draw(self, scr):
        """
        显示单个网格
        :param scr: 屏幕
        :return:
        """
        # 画棋盘格
        pygame.draw.rect(
            surface=scr,
            color=(0, 0, 0),
            rect=(game.border_size + self.pos[1] * game.grid_size + game.padding_size // 2,
                  game.border_size + self.pos[0] * game.grid_size + game.padding_size // 2,
                  game.grid_size - game.padding_size,
                  game.grid_size - game.padding_size),
            width=3,
            border_radius=10
        )

    def draw_wall(self, scr):
        """
        显示墙（人放的）
        只需显示left top（墙重复保存）
        :param scr:
        :return:
        """
        if self.pos[1] >= 1 and self.left:
            pygame.draw.polygon(
                surface=scr,
                color=self.left.color,
                points=((game.border_size + self.pos[1] * game.grid_size,
                         game.border_size + self.pos[0] * game.grid_size),
                        (game.border_size + self.pos[1] * game.grid_size + game.padding_size // 2 - 1,
                         game.border_size + self.pos[0] * game.grid_size + game.padding_size // 2),
                        (game.border_size + self.pos[1] * game.grid_size + game.padding_size // 2 - 1,
                         game.border_size + (self.pos[0] + 1) * game.grid_size - game.padding_size // 2),
                        (game.border_size + self.pos[1] * game.grid_size,
                         game.border_size + (self.pos[0] + 1) * game.grid_size),
                        (game.border_size + self.pos[1] * game.grid_size - game.padding_size // 2,
                         game.border_size + (self.pos[0] + 1) * game.grid_size - game.padding_size // 2),
                        (game.border_size + self.pos[1] * game.grid_size - game.padding_size // 2,
                         game.border_size + self.pos[0] * game.grid_size + game.padding_size // 2),
                        )
            )
        if self.pos[0] >= 1 and self.top:
            pygame.draw.polygon(
                surface=scr,
                color=self.top.color,
                points=((game.border_size + self.pos[1] * game.grid_size,
                         game.border_size + self.pos[0] * game.grid_size),
                        (game.border_size + self.pos[1] * game.grid_size + game.padding_size // 2,
                         game.border_size + self.pos[0] * game.grid_size + game.padding_size // 2 - 1),
                        (game.border_size + (self.pos[1] + 1) * game.grid_size - game.padding_size // 2,
                         game.border_size + self.pos[0] * game.grid_size + game.padding_size // 2 - 1),
                        (game.border_size + (self.pos[1] + 1) * game.grid_size,
                         game.border_size + self.pos[0] * game.grid_size),
                        (game.border_size + (self.pos[1] + 1) * game.grid_size - game.padding_size // 2,
                         game.border_size + self.pos[0] * game.grid_size - game.padding_size // 2),
                        (game.border_size + self.pos[1] * game.grid_size + game.padding_size // 2,
                         game.border_size + self.pos[0] * game.grid_size - game.padding_size // 2),
                        )
            )

    @classmethod
    def init_grid(cls, width, height):
        """
        生成网格对象
        :param width: 几列
        :param height: 几行
        :return:
        """
        if not cls.all_cells_2d:
            cls.all_cells_2d = np.empty((game.grid_num, game.grid_num), dtype='object')
        for i in range(width):
            for j in range(height):
                Cell((i, j))

    @classmethod
    def bfs(cls, pos, step=3):
        """
        广度优先搜索，考虑墙，可以添加步数限制
        :param step:步数限制，-1为不限制
        :param pos:
        :return:
        """
        visited = np.zeros_like(Cell.all_cells_2d) > 0
        queue = [(pos, 1)]
        visited[pos] = True
        while queue:
            s = queue.pop(0)
            if s[1] <= step:  # 步数限制
                if s[0][1] >= 1 and not Cell.all_cells_2d[s[0]].left and \
                        not Cell.all_cells_2d[s[0][0], s[0][1] - 1].content:
                    if not visited[s[0][0], s[0][1] - 1]:
                        queue.append(((s[0][0], s[0][1] - 1), s[1] + 1))
                        visited[s[0][0], s[0][1] - 1] = True
                if s[0][0] >= 1 and not Cell.all_cells_2d[s[0]].top and \
                        not Cell.all_cells_2d[s[0][0] - 1, s[0][1]].content:
                    if not visited[s[0][0] - 1, s[0][1]]:
                        queue.append(((s[0][0] - 1, s[0][1]), s[1] + 1))
                        visited[s[0][0] - 1, s[0][1]] = True
                if s[0][1] <= game.grid_num - 2 and not Cell.all_cells_2d[s[0]].right and \
                        not Cell.all_cells_2d[s[0][0], s[0][1] + 1].content:
                    if not visited[s[0][0], s[0][1] + 1]:
                        queue.append(((s[0][0], s[0][1] + 1), s[1] + 1))
                        visited[s[0][0], s[0][1] + 1] = True
                if s[0][0] <= game.grid_num - 2 and not Cell.all_cells_2d[s[0]].bottom and \
                        not Cell.all_cells_2d[s[0][0] + 1, s[0][1]].content:
                    if not visited[s[0][0] + 1, s[0][1]]:
                        queue.append(((s[0][0] + 1, s[0][1]), s[1] + 1))
                        visited[s[0][0] + 1, s[0][1]] = True
        return visited


class Wall:
    all_walls = []

    def __init__(self, pos, location, color):
        """
        向期盼边界添加墙会报错
        :param pos:
        :param location: 0=left 1=top 2=right 3=bottom
        :param color: 颜色
        """
        self.color = color
        if location == 0:
            Cell.all_cells_2d[pos].left = self
            Cell.all_cells_2d[pos[0], pos[1] - 1].right = self
        elif location == 1:
            Cell.all_cells_2d[pos].top = self
            Cell.all_cells_2d[pos[0] - 1, pos[1]].bottom = self
        elif location == 2:
            Cell.all_cells_2d[pos].right = self
            Cell.all_cells_2d[pos[0], pos[1] + 1].left = self
        elif location == 3:
            Cell.all_cells_2d[pos].bottom = self
            Cell.all_cells_2d[pos[0] + 1, pos[1]].top = self
        self.all_walls.append(self)


class Player:
    all_players = []

    def __init__(self, pos, color, name=""):
        """
        玩家
        :param start_pos: 位置，二元组
        :param color: 颜色， 三元组
        :param name: 名字
        """
        self.pos = pos
        self.color = color
        self.name = name
        self.available = []

        # 将玩家添加到网格中
        Cell.all_cells_2d[pos].content = self
        self.all_players.append(self)

    @classmethod
    def refresh_available(cls):
        for player in cls.all_players:
            player.get_available()

    def get_available(self):
        self.available = []
        for pos, i in np.ndenumerate(Cell.bfs(self.pos)):
            if i:
                self.available.append(pos)

    @classmethod
    def display(cls, scr):
        """
        显示所有玩家
        :param scr: 屏幕
        :return:
        """
        cls.all_players[0].draw_available(scr)
        for player in cls.all_players:
            player.draw(scr)

    def draw_available(self, scr):
        """
        显示提示
        :param scr: 屏幕
        :return:
        """
        for pos in self.available:
            pygame.draw.rect(
                surface=scr,
                color=[255 - (255 - i) * 0.5 for i in self.color],
                rect=(game.border_size + pos[1] * game.grid_size + game.padding_size // 2 + 3,
                      game.border_size + pos[0] * game.grid_size + game.padding_size // 2 + 3,
                      game.grid_size * 0.3,
                      game.grid_size * 0.3),
                border_top_left_radius=7
            )
            pygame.draw.polygon(
                surface=scr,
                color=(255, 255, 255),
                points=((game.border_size + (pos[1] + 0.3) * game.grid_size + game.padding_size // 2 + 3,
                         game.border_size + (pos[0] + 0.3) * game.grid_size + game.padding_size // 2 + 3),
                        (game.border_size + (pos[1]) * game.grid_size + game.padding_size // 2 + 3,
                         game.border_size + (pos[0] + 0.3) * game.grid_size + game.padding_size // 2 + 3),
                        (game.border_size + (pos[1] + 0.3) * game.grid_size + game.padding_size // 2 + 3,
                         game.border_size + (pos[0]) * game.grid_size + game.padding_size // 2 + 3),)
            )

    def draw(self, scr):
        """
        显示单个玩家
        :param scr: 屏幕
        :return:
        """
        pygame.draw.circle(
            surface=scr,
            color=self.color,
            center=(game.border_size + (self.pos[1] + 0.5) * game.grid_size,
                    game.border_size + (self.pos[0] + 0.5) * game.grid_size),
            width=0,
            radius=game.grid_size * 0.3,
        )


class Game:
    def __init__(self, grid_num, grid_size, border_size, padding_size):
        """
        :param padding_size: 每个棋盘格的间距
        :param grid_num: 棋盘格数量
        :param grid_size: 棋盘格大小
        :param border_size: 棋盘边缘空白大小
        """
        self.border_size = border_size
        self.grid_size = grid_size
        self.grid_num = grid_num
        self.padding_size = padding_size

    @staticmethod
    def event_handler():
        events = pygame.event.get()
        for event in events:
            # 退出
            if event.type == QUIT:
                pygame.display.quit()
                sys.exit()

    def init_screen(self):
        """
        初始化屏幕
        """
        width = height = self.grid_num * self.grid_size + self.border_size * 2
        screen = pygame.display.set_mode((width, height))
        ico = pygame.image.load('./resources/icon/xo.png')

        pygame.display.set_icon(ico)
        pygame.display.set_caption('围城')
        return screen

    def main(self):
        pygame.init()
        screen = self.init_screen()
        Cell.init_grid(self.grid_num, self.grid_num)
        Wall((1, 1), 0, [random.randint(0, 255) for i in range(3)])
        Wall((2, 1), 0, [random.randint(0, 255) for i in range(3)])
        Wall((1, 2), 0, [random.randint(0, 255) for i in range(3)])
        Wall((1, 1), 3, [random.randint(0, 255) for i in range(3)])
        Wall((2, 1), 3, [random.randint(0, 255) for i in range(3)])
        Wall((1, 2), 3, [random.randint(0, 255) for i in range(3)])
        Player((1, 3), (34, 232, 193), 'acb')
        Player((1, 2), (34, 32, 193), 'acb')
        Player((0, 3), (244, 232, 193), 'acb')
        Player.refresh_available()

        while True:
            self.event_handler()
            screen.fill((255, 255, 255))
            Cell.display(screen)
            Player.display(screen)
            pygame.display.update()


if __name__ == '__main__':
    game = Game(7, 100, 50, 10)
    game.main()
