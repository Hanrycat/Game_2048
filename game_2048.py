#!/usr/bin/env python
# coding: utf-8
# CopyRight by heibanke
# 网易云课堂 << 用Python做2048 >> 课程代码

import pyglet
import random


WIN_WIDTH = 530
WIN_HEIGHT = 720

# 棋盘起始位置左下角的x，y
STARTX = 15
STARTY = 110

# 每块的宽度和每行的块数（默认是正方形块）
WINDOW_BLOCK_NUM = 6

BOARD_WIDTH = (WIN_WIDTH - 2* STARTX)
BLOCK_WIDTH = BOARD_WIDTH/WINDOW_BLOCK_NUM


# 每块的颜色
COLORS = {
    0:(204,192,179),2:(238, 228, 218),4:(237, 224, 200),8:(242, 177, 121),
    16:(245, 149, 99),32:(246, 124, 95),64:(246, 94, 59),128:(237, 207, 114),
    256:(233, 170, 7),512:(215, 159, 14),1024:(222, 186, 30),2048:(222, 212, 30),
    4096:(205, 222, 30),8192:(179, 222, 30),16384:(153, 222, 30),32768:(106, 222, 30),
    65536:(69, 222, 30),131072:(237, 207, 114),262144:(237, 207, 114),524288:(237, 207, 114)
}

LABEL_COLOR = (119, 110, 101, 255)
BG_COLOR = (250,248,239,255)
LINE_COLOR = (165,165,165,225)

class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_init()

    def game_init(self):
        self.main_batch = pyglet.graphics.Batch()
        self.data = [[2**(i+j+1) for i in range(WINDOW_BLOCK_NUM)] for j in range(WINDOW_BLOCK_NUM)]



        # 背景spirite
        background_img = pyglet.image.SolidColorImagePattern(color=BG_COLOR)
        self.background = pyglet.sprite.Sprite(
                background_img.create_image(WIN_WIDTH, WIN_HEIGHT), 
                0, 0)

        # Title
        self.title_label = pyglet.text.Label(text="2048", bold=True, 
                color = LABEL_COLOR, x = STARTX, y=BOARD_WIDTH+STARTY+30, 
                font_size=36, batch= self.main_batch)

        # Score
        self.score = 0
        self.score_label = pyglet.text.Label(text="Score = %d"%(self.score), bold=True, 
                color = LABEL_COLOR, x=200, y=BOARD_WIDTH+STARTY+30,
                font_size=36, batch= self.main_batch)
        # Help
        self.help_label = pyglet.text.Label(text="please use up, down, ->, <-, to play!", bold=True, 
                color = LABEL_COLOR, x=STARTX, y=STARTY - 30,
                font_size=18, batch= self.main_batch)


    def on_draw(self):
        self.clear()
        self.score_label.text = "Score = %d"%(self.score)
        self.background.draw()
        self.main_batch.draw()


        for row in range(WINDOW_BLOCK_NUM):
            for col in range(WINDOW_BLOCK_NUM):
                x = STARTX + BLOCK_WIDTH*col
                y = STARTY + BOARD_WIDTH - BLOCK_WIDTH - BLOCK_WIDTH*row
                self.draw_tile((x,y,BLOCK_WIDTH,BLOCK_WIDTH), self.data[row][col])

        self.draw_grid(STARTX, STARTY)


    def draw_grid(self, startx, starty):
        rows = columns = WINDOW_BLOCK_NUM+1
        #水平线
        for i in range(rows):
            pyglet.graphics.draw(
                2, pyglet.gl.GL_LINES, 
                ('v2f', 
                    (
                        startx, i * BLOCK_WIDTH+starty, 
                        WINDOW_BLOCK_NUM * BLOCK_WIDTH+startx, i * BLOCK_WIDTH+starty
                    )
                ),
                ('c4B', LINE_COLOR*2)
            )
        #垂直线
        for j in range(columns):
            pyglet.graphics.draw(
                2, pyglet.gl.GL_LINES, 
                ('v2f', 
                    (
                        j * BLOCK_WIDTH+startx, 
                        starty, 
                        j * BLOCK_WIDTH+startx, 
                        WINDOW_BLOCK_NUM * BLOCK_WIDTH+starty,
                    )
                ),
                ('c4B', LINE_COLOR*2)
            )


    def draw_tile(self, xywh, data):
        x, y, dx, dy = xywh
        color_rgb = COLORS[data]
        corners = [x+dx, y+dy, x, y+dy, x, y, x+dx, y]
        pyglet.graphics.draw(
            4, pyglet.gl.GL_QUADS, ('v2f', corners), ('c3B', color_rgb*4))

        if data != 0:
            a = pyglet.text.Label(text=str(data), bold=True, anchor_x = 'center', anchor_y = 'center',
                    color=(0,0,0, 255), x=x+dx/2, y=y+dy/2,
                    font_size=28)
            a.draw()


# 创建窗口
win = Window(WIN_WIDTH, WIN_HEIGHT)

# 设置图标
icon = pyglet.image.load('logo.ico')
win.set_icon(icon)

pyglet.app.run()