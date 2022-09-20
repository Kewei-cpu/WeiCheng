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
        pygame.draw.rect(
            surface=scr,
            color=(255, 255, 255),
            rect=(game.border_size + self.pos[1] * game.grid_size + game.padding_size // 2 + 3,
                  game.border_size + self.pos[0] * game.grid_size + game.padding_size // 2 + 3,
                  game.grid_size - game.padding_size - 6,
                  game.grid_size - game.padding_size - 6),
            border_radius=0
        )

    def draw_wall(self, scr):
        """
        显示墙（人放的）
        只需显示left top（墙重复保存）
        :param scr:
        :return:
        """
        if self.pos[1] >= 1 and self.left:
            Player.draw_left_wall(scr, self.left.color, self.pos[0], self.pos[1])

        if self.pos[0] >= 1 and self.top:
            Player.draw_top_wall(scr, self.top.color, self.pos[0], self.pos[1])

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
        for i, player in enumerate(cls.all_players):
            player.draw(scr)
            if game.player_flag == i:
                player.draw_outline(scr)
                if game.step_flag == 0:
                    player.draw_available(scr)
                    player.draw_preview(scr)
                else:
                    player.draw_wall_preview(scr)

    def draw_preview(self, scr):
        """
        显示玩家可能的位置
        :param scr:
        :return:
        """
        if game.mouse_pos in self.available and game.mouse_pos != self.pos:
            pygame.draw.circle(
                surface=scr,
                color=[255 - (255 - i) * 0.5 for i in self.color],
                center=(game.border_size + (game.mouse_pos[1] + 0.5) * game.grid_size,
                        game.border_size + (game.mouse_pos[0] + 0.5) * game.grid_size),
                radius=game.grid_size * 0.3,
            )

    @staticmethod
    def draw_left_wall(scr, color, pos_x, pos_y, width=0):
        pygame.draw.polygon(
            surface=scr,
            color=color,
            points=((game.border_size + pos_y * game.grid_size,
                     game.border_size + pos_x * game.grid_size),
                    (game.border_size + pos_y * game.grid_size + game.padding_size // 3,
                     game.border_size + pos_x * game.grid_size + game.padding_size // 3),
                    (game.border_size + pos_y * game.grid_size + game.padding_size // 3,
                     game.border_size + (pos_x + 1) * game.grid_size - game.padding_size // 3),
                    (game.border_size + pos_y * game.grid_size,
                     game.border_size + (pos_x + 1) * game.grid_size),
                    (game.border_size + pos_y * game.grid_size - game.padding_size // 3,
                     game.border_size + (pos_x + 1) * game.grid_size - game.padding_size // 3),
                    (game.border_size + pos_y * game.grid_size - game.padding_size // 3,
                     game.border_size + pos_x * game.grid_size + game.padding_size // 3),
                    ),
            width=width)

    @staticmethod
    def draw_top_wall(scr, color, pos_x, pos_y, width=0):
        pygame.draw.polygon(
            surface=scr,
            color=color,
            points=((game.border_size + pos_y * game.grid_size,
                     game.border_size + pos_x * game.grid_size),
                    (game.border_size + pos_y * game.grid_size + game.padding_size // 3,
                     game.border_size + pos_x * game.grid_size + game.padding_size // 3),
                    (game.border_size + (pos_y + 1) * game.grid_size - game.padding_size // 3,
                     game.border_size + pos_x * game.grid_size + game.padding_size // 3),
                    (game.border_size + (pos_y + 1) * game.grid_size,
                     game.border_size + pos_x * game.grid_size),
                    (game.border_size + (pos_y + 1) * game.grid_size - game.padding_size // 3,
                     game.border_size + pos_x * game.grid_size - game.padding_size // 3),
                    (game.border_size + pos_y * game.grid_size + game.padding_size // 3,
                     game.border_size + pos_x * game.grid_size - game.padding_size // 3),
                    ),
            width=width
        )

    def draw_wall_preview(self, scr):
        """
        0=left 1=top 2=right 3=bottom
        :param scr:
        :return:
        """
        if pygame.mouse.get_pos()[0] < game.border_size + (self.pos[1] + 0.5) * game.grid_size and \
                abs(pygame.mouse.get_pos()[1] - (game.border_size + (self.pos[0] + 0.5) * game.grid_size)) < \
                abs(game.border_size + (self.pos[1] + 0.5) * game.grid_size - pygame.mouse.get_pos()[0]) and \
                Cell.all_cells_2d[self.pos].left is None and self.pos[1] > 0:
            self.draw_left_wall(scr, self.color, self.pos[0], self.pos[1])
            self.draw_left_wall(scr, [color * 0.7 for color in self.color], self.pos[0], self.pos[1], width=5)
            game.mouse_wall_pos = 0


        elif pygame.mouse.get_pos()[1] < game.border_size + (self.pos[0] + 0.5) * game.grid_size and \
                abs(pygame.mouse.get_pos()[0] - (game.border_size + (self.pos[1] + 0.5) * game.grid_size)) < \
                abs(game.border_size + (self.pos[0] + 0.5) * game.grid_size - pygame.mouse.get_pos()[1]) and \
                Cell.all_cells_2d[self.pos].top is None and self.pos[0] > 0:
            self.draw_top_wall(scr, self.color, self.pos[0], self.pos[1])
            self.draw_top_wall(scr, [color * 0.7 for color in self.color], self.pos[0], self.pos[1], width=5)
            game.mouse_wall_pos = 1

        elif pygame.mouse.get_pos()[0] > game.border_size + (self.pos[1] + 0.5) * game.grid_size and \
                abs(pygame.mouse.get_pos()[1] - (game.border_size + (self.pos[0] + 0.5) * game.grid_size)) < \
                abs(game.border_size + (self.pos[1] + 0.5) * game.grid_size - pygame.mouse.get_pos()[0]) and \
                Cell.all_cells_2d[self.pos].right is None and self.pos[1] < game.grid_num - 1:
            self.draw_left_wall(scr, self.color, self.pos[0], self.pos[1] + 1)
            self.draw_left_wall(scr, [color * 0.7 for color in self.color], self.pos[0], self.pos[1] + 1, width=5)
            game.mouse_wall_pos = 2

        elif pygame.mouse.get_pos()[1] > game.border_size + (self.pos[0] + 0.5) * game.grid_size and \
                abs(pygame.mouse.get_pos()[0] - (game.border_size + (self.pos[1] + 0.5) * game.grid_size)) < \
                abs(game.border_size + (self.pos[0] + 0.5) * game.grid_size - pygame.mouse.get_pos()[1]) and \
                Cell.all_cells_2d[self.pos].bottom is None and self.pos[0] < game.grid_num - 1:
            self.draw_top_wall(scr, self.color, self.pos[0] + 1, self.pos[1])
            self.draw_top_wall(scr, [color * 0.7 for color in self.color], self.pos[0] + 1, self.pos[1], width=5)
            game.mouse_wall_pos = 3

    def draw_outline(self, scr):
        """
        显示选中的玩家
        :param scr: 屏幕
        :return:
        """
        pygame.draw.circle(
            surface=scr,
            color=[color * 0.7 for color in self.color],
            center=(game.border_size + (self.pos[1] + 0.5) * game.grid_size,
                    game.border_size + (self.pos[0] + 0.5) * game.grid_size),
            width=5,
            radius=game.grid_size * 0.3,
        )

    def draw_available(self, scr):
        """
        显示提示
        :param scr: 屏幕
1        """
        for pos in self.available:
            pygame.draw.rect(
                surface=scr,
                color=[color * 0.7 for color in self.color],
                rect=(game.border_size + pos[1] * game.grid_size + game.padding_size // 2,
                      game.border_size + pos[0] * game.grid_size + game.padding_size // 2,
                      game.grid_size - game.padding_size,
                      game.grid_size - game.padding_size),
                width=6,
                border_radius=0
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
            radius=game.grid_size * 0.3,
        )

    def move_to_mouse(self):
        if game.mouse_pos in self.available:
            Cell.all_cells_2d[self.pos].content = None
            self.pos = game.mouse_pos
            Cell.all_cells_2d[game.mouse_pos].content = self
            return True

    def place_at_mouse(self):
        if game.mouse_wall_pos == 0 and Cell.all_cells_2d[self.pos].left is None and self.pos[1] > 0 or \
                game.mouse_wall_pos == 1 and Cell.all_cells_2d[self.pos].top is None and self.pos[0] > 0 or \
                game.mouse_wall_pos == 2 and Cell.all_cells_2d[self.pos].right is None and self.pos[
            1] < game.grid_num - 1 or \
                game.mouse_wall_pos == 3 and Cell.all_cells_2d[self.pos].bottom is None and self.pos[
            0] < game.grid_num - 1:
            Wall(self.pos, game.mouse_wall_pos, [color * 0.7 for color in self.color])
            return True


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
        self.window_size = 0
        self.padding_size = padding_size
        self.player_num = 0
        self.player_flag = 0  # 玩家编号
        self.step_flag = 0  # 0为移动，1为放置
        self.mouse_pos = (0, 0)
        self.mouse_wall_pos = 0

    def event_handler(self):
        events = pygame.event.get()
        for event in events:
            # 退出
            if event.type == QUIT:
                pygame.display.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                if self.step_flag == 0:
                    res = Player.all_players[self.player_flag].move_to_mouse()
                    if res:
                        self.next_step()
                elif self.step_flag == 1:
                    res = Player.all_players[self.player_flag].place_at_mouse()
                    if res:
                        self.next_step()

    def get_player_num(self):
        self.player_num = len(Player.all_players)

    def next_step(self):
        if self.step_flag == 0:
            self.step_flag += 1
        elif self.player_flag < self.player_num - 1:
            self.step_flag = 0
            self.player_flag += 1
        else:
            self.step_flag = 0
            self.player_flag = 0

    def pos_2_grid(self, pos):
        """
        讲鼠标坐标转化为再网格中的位置
        :param pos:
        :return:
        """
        x = (pos[1] - self.border_size) // self.grid_size
        y = (pos[0] - self.border_size) // self.grid_size
        return x, y

    def move_mouse_handler(self):
        gd = self.pos_2_grid(pygame.mouse.get_pos())
        if 0 <= gd[0] <= self.grid_num - 1 and 0 <= gd[1] <= self.grid_num - 1:
            self.mouse_pos = gd

    def draw_background(self, scr):
        for i in range(self.window_size):
            pygame.draw.line(
                scr,
                color=(round(173 - 29 * i / self.window_size, 0),
                       round(124 + 13 * i / self.window_size, 0),
                       round(170 + 1 * i / self.window_size, 0),),
                start_pos=(0, i),
                end_pos=(i, 0),
                width=1,
            )

        for i in range(self.window_size):
            pygame.draw.line(
                scr,
                color=(round(144 - 29 * i / self.window_size, 0),
                       round(137 + 13 * i / self.window_size, 0),
                       round(171 + 1 * i / self.window_size, 0),),
                start_pos=(self.window_size - 1, i),
                end_pos=(i, self.window_size - 1),
                width=1,
            )

    def init_screen(self):
        """
        初始化屏幕
        """
        self.window_size = self.grid_num * self.grid_size + self.border_size * 2
        screen = pygame.display.set_mode((self.window_size, self.window_size))
        ico = pygame.image.load('./resources/icon/xo.png')
        pygame.display.set_icon(ico)
        pygame.display.set_caption('围城')
        return screen

    def main(self):
        pygame.init()
        screen = self.init_screen()
        Cell.init_grid(self.grid_num, self.grid_num)
        Player((0, 0), (130, 175, 214))
        # Player((1, 2), (192, 141, 117))
        Player((6, 6), (80, 181, 142))
        game.get_player_num()

        while True:
            self.event_handler()
            self.move_mouse_handler()
            Player.refresh_available()
            self.draw_background(screen)
            Cell.display(screen)
            Player.display(screen)
            pygame.display.update()


if __name__ == '__main__':
    game = Game(7, 100, 50, 20)
    game.main()
