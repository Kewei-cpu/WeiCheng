import random
import sys
import time

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

        for i, cell in np.ndenumerate(cls.all_cells_2d):
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
            Player.draw_left_wall(scr, [color * 0.5 for color in self.left.color], self.pos[0], self.pos[1], width=3)

        if self.pos[0] >= 1 and self.top:
            Player.draw_top_wall(scr, self.top.color, self.pos[0], self.pos[1])
            Player.draw_top_wall(scr, [color * 0.5 for color in self.top.color], self.pos[0], self.pos[1], width=3)

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
    def bfs(cls, pos, board, step=3, ignore_player=False, return_num=False):
        """
        广度优先搜索，考虑墙，可以添加步数限制
        :param board:
        :param return_num: 是否返回步数列表
        :param ignore_player: 是否忽略玩家
        :param step:步数限制
        :param pos:
        :return:
        """
        visited = np.zeros_like(board) > 0
        length = np.zeros_like(board)
        queue = [(pos, 1)]
        visited[pos] = True
        while queue:
            s = queue.pop(0)
            if s[1] <= step:  # 步数限制
                if s[0][1] >= 1 and not board[s[0]].left and \
                        (not board[s[0][0], s[0][1] - 1].content or ignore_player):
                    if not visited[s[0][0], s[0][1] - 1]:
                        queue.append(((s[0][0], s[0][1] - 1), s[1] + 1))
                        visited[s[0][0], s[0][1] - 1] = True
                        length[s[0][0], s[0][1] - 1] = s[1]
                if s[0][0] >= 1 and not board[s[0]].top and \
                        (not board[s[0][0] - 1, s[0][1]].content or ignore_player):
                    if not visited[s[0][0] - 1, s[0][1]]:
                        queue.append(((s[0][0] - 1, s[0][1]), s[1] + 1))
                        visited[s[0][0] - 1, s[0][1]] = True
                        length[s[0][0] - 1, s[0][1]] = s[1]
                if s[0][1] <= game.grid_num - 2 and not board[s[0]].right and \
                        (not board[s[0][0], s[0][1] + 1].content or ignore_player):
                    if not visited[s[0][0], s[0][1] + 1]:
                        queue.append(((s[0][0], s[0][1] + 1), s[1] + 1))
                        visited[s[0][0], s[0][1] + 1] = True
                        length[s[0][0], s[0][1] + 1] = s[1]
                if s[0][0] <= game.grid_num - 2 and not board[s[0]].bottom and \
                        (not board[s[0][0] + 1, s[0][1]].content or ignore_player):
                    if not visited[s[0][0] + 1, s[0][1]]:
                        queue.append(((s[0][0] + 1, s[0][1]), s[1] + 1))
                        visited[s[0][0] + 1, s[0][1]] = True
                        length[s[0][0] + 1, s[0][1]] = s[1]
        if return_num:
            return length
        return visited

    @classmethod
    def is_isolated(cls, pos, step=3, ):
        """
        判断玩家是否呗隔离，考虑墙，可以添加步数限制
        :param step:步数限制
        :param pos:
        :return:
        """
        visited = np.zeros_like(Cell.all_cells_2d) > 0
        queue = [(pos, 1)]
        visited[pos] = True
        while queue:
            s = queue.pop(0)
            if s[1] <= step:  # 步数限制
                # bfs
                if s[0][1] >= 1 and not Cell.all_cells_2d[s[0]].left:
                    if not visited[s[0][0], s[0][1] - 1]:
                        if Cell.all_cells_2d[s[0][0], s[0][1] - 1].content and (s[0][0], s[0][1] - 1) != pos:  # 检测玩家
                            return False
                        queue.append(((s[0][0], s[0][1] - 1), s[1] + 1))
                        visited[s[0][0], s[0][1] - 1] = True
                if s[0][0] >= 1 and not Cell.all_cells_2d[s[0]].top:
                    if not visited[s[0][0] - 1, s[0][1]]:
                        if Cell.all_cells_2d[s[0][0] - 1, s[0][1]].content and (s[0][0] - 1, s[0][1]) != pos:  # 检测玩家
                            return False
                        queue.append(((s[0][0] - 1, s[0][1]), s[1] + 1))
                        visited[s[0][0] - 1, s[0][1]] = True
                if s[0][1] <= game.grid_num - 2 and not Cell.all_cells_2d[s[0]].right:
                    if not visited[s[0][0], s[0][1] + 1]:
                        if Cell.all_cells_2d[s[0][0], s[0][1] + 1].content and (s[0][0], s[0][1] + 1) != pos:  # 检测玩家
                            return False
                        queue.append(((s[0][0], s[0][1] + 1), s[1] + 1))
                        visited[s[0][0], s[0][1] + 1] = True
                if s[0][0] <= game.grid_num - 2 and not Cell.all_cells_2d[s[0]].bottom:
                    if not visited[s[0][0] + 1, s[0][1]]:
                        if Cell.all_cells_2d[s[0][0] + 1, s[0][1]].content and (s[0][0] + 1, s[0][1]) != pos:  # 检测玩家
                            return False
                        queue.append(((s[0][0] + 1, s[0][1]), s[1] + 1))
                        visited[s[0][0] + 1, s[0][1]] = True
        return True


class Wall:
    all_walls = []

    def __init__(self, pos, location, color=(128, 128, 128)):
        """
        向期盼边界添加墙会报错
        :param pos:
        :param location: 0=left 1=top 2=right 3=bottom
        :param color: 颜色
        """
        self.pos = pos
        self.color = color
        self.location = location
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

    def __del__(self):
        if self.location == 0:
            Cell.all_cells_2d[self.pos].left = None
            Cell.all_cells_2d[self.pos[0], self.pos[1] - 1].right = None
        elif self.location == 1:
            Cell.all_cells_2d[self.pos].top = None
            Cell.all_cells_2d[self.pos[0] - 1, self.pos[1]].bottom = None
        elif self.location == 2:
            Cell.all_cells_2d[self.pos].right = None
            Cell.all_cells_2d[self.pos[0], self.pos[1] + 1].left = None
        elif self.location == 3:
            Cell.all_cells_2d[self.pos].bottom = None
            Cell.all_cells_2d[self.pos[0] + 1, self.pos[1]].top = None
        if self in self.all_walls:
            self.all_walls.remove(self)


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
        self.territory = None
        self.isolated = False

        # 将玩家添加到网格中
        Cell.all_cells_2d[pos].content = self
        self.all_players.append(self)

    @classmethod
    def refresh_available(cls):
        for player in cls.all_players:
            player.get_available()

    @classmethod
    def refresh_territory(cls):
        for player in cls.all_players:
            player.territory = Cell.bfs(player.pos, Cell.all_cells_2d, step=100, ignore_player=True, return_num=True)

    def get_available(self):
        self.available = []
        for pos, i in np.ndenumerate(Cell.bfs(self.pos, Cell.all_cells_2d)):
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
            if not player.isolated:
                player.draw_territory(scr)
                player.draw(scr)
            else:
                player.draw_end(scr, Cell.bfs(player.pos, Cell.all_cells_2d, 100))
                player.draw_dead(scr)
                if game.player_flag == i:
                    game.next_player()
        for i, player in enumerate(cls.all_players):
            if game.player_flag == i and not player.isolated:
                player.draw_outline(scr)
                if game.step_flag == 0:
                    player.draw_available(scr)
                    player.draw_preview(scr)
                else:
                    player.draw_wall_preview(scr)

    def draw_territory(self, scr):
        for pos, i in np.ndenumerate(self.territory):
            terr = True
            for player in self.all_players:
                if player is not self and player.territory[pos] <= i:
                    terr = False
            if terr:
                pygame.draw.rect(
                    surface=scr,
                    color=[255 - (255 - i) * 0.4 for i in self.color],
                    rect=(game.border_size + pos[1] * game.grid_size + game.padding_size // 2 + 3,
                          game.border_size + pos[0] * game.grid_size + game.padding_size // 2 + 3,
                          game.grid_size - game.padding_size - 6,
                          game.grid_size - game.padding_size - 6),
                    width=10
                )

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
            self.draw_left_wall(scr, [255 - (255 - i) * 0.5 for i in self.color], self.pos[0], self.pos[1])
            game.mouse_wall_pos = 0


        elif pygame.mouse.get_pos()[1] < game.border_size + (self.pos[0] + 0.5) * game.grid_size and \
                abs(pygame.mouse.get_pos()[0] - (game.border_size + (self.pos[1] + 0.5) * game.grid_size)) < \
                abs(game.border_size + (self.pos[0] + 0.5) * game.grid_size - pygame.mouse.get_pos()[1]) and \
                Cell.all_cells_2d[self.pos].top is None and self.pos[0] > 0:
            self.draw_top_wall(scr, [255 - (255 - i) * 0.5 for i in self.color], self.pos[0], self.pos[1])
            game.mouse_wall_pos = 1

        elif pygame.mouse.get_pos()[0] > game.border_size + (self.pos[1] + 0.5) * game.grid_size and \
                abs(pygame.mouse.get_pos()[1] - (game.border_size + (self.pos[0] + 0.5) * game.grid_size)) < \
                abs(game.border_size + (self.pos[1] + 0.5) * game.grid_size - pygame.mouse.get_pos()[0]) and \
                Cell.all_cells_2d[self.pos].right is None and self.pos[1] < game.grid_num - 1:
            self.draw_left_wall(scr, [255 - (255 - i) * 0.5 for i in self.color], self.pos[0], self.pos[1] + 1)
            game.mouse_wall_pos = 2

        elif pygame.mouse.get_pos()[1] > game.border_size + (self.pos[0] + 0.5) * game.grid_size and \
                abs(pygame.mouse.get_pos()[0] - (game.border_size + (self.pos[1] + 0.5) * game.grid_size)) < \
                abs(game.border_size + (self.pos[0] + 0.5) * game.grid_size - pygame.mouse.get_pos()[1]) and \
                Cell.all_cells_2d[self.pos].bottom is None and self.pos[0] < game.grid_num - 1:
            self.draw_top_wall(scr, [255 - (255 - i) * 0.5 for i in self.color], self.pos[0] + 1, self.pos[1])
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
                color=[color * 1 for color in self.color],
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

    def draw_end(self, scr, can_go):
        for pos, i in np.ndenumerate(can_go):
            if i:
                pygame.draw.rect(
                    surface=scr,
                    color=[255 - (255 - i) * 0.4 for i in self.color],
                    rect=(game.border_size + pos[1] * game.grid_size + game.padding_size // 2 + 3,
                          game.border_size + pos[0] * game.grid_size + game.padding_size // 2 + 3,
                          game.grid_size - game.padding_size - 6,
                          game.grid_size - game.padding_size - 6),
                )

    def draw_dead(self, scr):
        """
        显示单个玩家
        :param scr: 屏幕
        :return:
        """
        pygame.draw.circle(
            surface=scr,
            color=[color * 0.5 for color in self.color],
            center=(game.border_size + (self.pos[1] + 0.5) * game.grid_size,
                    game.border_size + (self.pos[0] + 0.5) * game.grid_size),
            radius=game.grid_size * 0.3,
            width=5
        )

    def move_to_mouse(self):
        if game.mouse_pos in self.available:
            Cell.all_cells_2d[self.pos].content = None
            self.pos = game.mouse_pos
            Cell.all_cells_2d[game.mouse_pos].content = self
            game.record['moves'][self.name].append([self.pos])
            return True

    def place_at_mouse(self):
        if game.mouse_wall_pos == 0 and Cell.all_cells_2d[self.pos].left is None and self.pos[1] > 0 or \
                game.mouse_wall_pos == 1 and Cell.all_cells_2d[self.pos].top is None and self.pos[0] > 0 or \
                game.mouse_wall_pos == 2 and Cell.all_cells_2d[self.pos].right is None and self.pos[
            1] < game.grid_num - 1 or \
                game.mouse_wall_pos == 3 and Cell.all_cells_2d[self.pos].bottom is None and self.pos[
            0] < game.grid_num - 1:
            Wall(self.pos, game.mouse_wall_pos, [255 - (255 - i) * 0.5 for i in self.color])
            game.record['moves'][self.name][-1].append(game.mouse_wall_pos)
            game.record['steps'] += 1
            if game.test_end():
                return None
            return True

    def max_territory_strategy(self):
        """
        单步最优化策略
        :return:
        """
        choices = []
        for pos in self.available:  # 遍历每一个个能位置
            if (abs(pos[0] - self.pos[0]) + abs(pos[1] - self.pos[1])) < 2:
                # continue
                pass
            if int(Cell.all_cells_2d[pos].left is not None) + int(Cell.all_cells_2d[pos].top is not None) + \
                    int(Cell.all_cells_2d[pos].right is not None) + int(Cell.all_cells_2d[pos].bottom is not None) > 1:
                continue
                # pass
            new_board = Cell.all_cells_2d.copy()
            new_board[self.pos].content = None
            new_board[pos].content = self
            for loc in range(4):
                # 检测边缘
                if pos[0] == 0 and loc == 1 or pos[1] == 0 and loc == 0 or \
                        pos[0] == game.grid_num - 1 and loc == 3 or pos[1] == game.grid_num - 1 and loc == 2:
                    continue

                # 已有墙的位置
                if loc == 0 and Cell.all_cells_2d[pos].left or loc == 1 and Cell.all_cells_2d[pos].top or \
                        loc == 2 and Cell.all_cells_2d[pos].right or loc == 3 and Cell.all_cells_2d[pos].bottom:
                    continue

                a = Wall(pos, loc)
                # 移动放置后进行模拟
                terr = Cell.bfs(pos, new_board, step=100, return_num=True)
                a.__del__()
                new_board[pos].content = None
                new_board[self.pos].content = self

                # 计算当前领地大小
                terr_num = 0
                for pos_go, i in np.ndenumerate(terr):
                    is_my_terr = True
                    for player in self.all_players:
                        if player is not self and i > player.territory[pos_go] > 0 or i <= 0:
                            is_my_terr = False
                        if i == player.territory[pos_go] and player is not self and player.territory[pos_go] > 0:
                            terr_num -= 0.5
                    if is_my_terr:
                        terr_num += 1
                choices.append((pos, loc, terr_num))


        choices.sort(key=lambda x: x[2], reverse=True)
        max_terr = choices[0][2]
        max_terr_choices = [c for c in choices if c[2] >= max_terr - 1]
        print(max_terr_choices)

        max_terr_choices.sort(key=lambda x: (abs(x[0][0] - self.pos[0]) + abs(x[0][1] - self.pos[1])))
        min_dis = abs(max_terr_choices[0][0][0] - self.pos[0]) + abs(max_terr_choices[0][0][1] - self.pos[1])
        min_distance_choices = [c for c in max_terr_choices if abs(c[0][0] - self.pos[0]) + abs(c[0][1] - self.pos[1]) <= min_dis + 1]
        print(min_distance_choices)

        return random.choice(min_distance_choices)


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
        self.running = True
        self.record = {
            'time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            'steps': 0,
            'moves': dict(),
            'result': dict()
        }

    def event_handler(self):
        events = pygame.event.get()
        for event in events:
            # 退出
            if event.type == QUIT:
                pygame.display.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                if self.running:
                    if self.step_flag == 0:
                        res = Player.all_players[self.player_flag].move_to_mouse()
                        if res:
                            self.next_step()
                    elif self.step_flag == 1:
                        res = Player.all_players[self.player_flag].place_at_mouse()
                        if res:
                            self.next_step()

    def get_players(self):
        self.player_num = len(Player.all_players)
        for player in Player.all_players:
            self.record['moves'][player.name] = []

    def test_end(self):
        """
        判断游戏是否结束
        :return:
        """
        for player in Player.all_players:
            isolated = Cell.is_isolated(player.pos, step=100)
            if isolated and not player.isolated:
                print(f'{player.name} Dies!')
                player.isolated = True
                all_die = True
                for player_ in Player.all_players:
                    if player_.isolated is False:
                        all_die = False
                if all_die:
                    self.running = False
                    self.score_calculator()
                    return True

    def score_calculator(self):
        """
        结算
        :return:
        """
        print('=' * 20)
        print('GAME\t\tOVER')
        print('=' * 20)
        print('NAME\t\tSCORE')
        # 计算每个玩家的占地面积
        for player in Player.all_players:
            score = np.sum(Cell.bfs(player.pos, Cell.all_cells_2d, step=100))
            self.record['result'][player.name] = score
            print(player.name, score, sep='\t\t\t')
        self.write_log()
        print(self.record)

    def write_log(self):
        with open(f"./log/{self.record['time'].split(' ')[0]}.txt", 'a') as f:
            f.write(str(self.record))
            f.write('\n')

    def robot_handler(self):
        if 'Robot' in Player.all_players[self.player_flag].name:
            if self.running:
                act = Player.all_players[self.player_flag].max_territory_strategy()
                if act:
                    Cell.all_cells_2d[Player.all_players[self.player_flag].pos].content = None
                    Player.all_players[self.player_flag].pos = act[0]
                    Cell.all_cells_2d[act[0]].content = Player.all_players[self.player_flag]
                    Wall(act[0], act[1], Player.all_players[self.player_flag].color)
                    self.test_end()
                    self.record['steps'] += 1
                    self.record['moves'][Player.all_players[self.player_flag].name].append([act[0], act[1]])
                    self.next_player()

    def next_step(self):
        if self.step_flag == 0:
            self.step_flag += 1
        elif self.player_flag < self.player_num - 1:
            self.step_flag = 0
            self.player_flag += 1
        else:
            self.step_flag = 0
            self.player_flag = 0

    def next_player(self):
        if self.player_flag < self.player_num - 1:
            self.player_flag += 1
        else:
            self.player_flag = 0
        self.step_flag = 0

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
        Player((0, 0), (130, 175, 214), 'Blue Player')
        # Player((0, 6), (192, 141, 117), 'Brown Robot')
        # Player((6, 0), (207, 155, 176), 'Pink Robot')
        Player((6, 6), (80, 181, 142), 'Green Robot')
        game.get_players()

        while True:
            Player.refresh_available()
            Player.refresh_territory()
            self.robot_handler()
            self.event_handler()
            self.move_mouse_handler()
            self.draw_background(screen)
            Cell.display(screen)
            Player.display(screen)
            pygame.display.update()


if __name__ == '__main__':
    game = Game(7, 100, 50, 20)
    game.main()
