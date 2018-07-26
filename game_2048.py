#!/usr/bin/env python
# coding: utf-8
# CopyRight by heibanke
# 网易云课堂 << 用Python做2048 >> 课程代码

import pyglet
import random
from pyglet.window import key
import copy

WIN_WIDTH = 530
WIN_HEIGHT = 720

# 棋盘起始位置左下角的x，y
STARTX = 15
STARTY = 110

# 每块的宽度和每行的块数（默认是正方形块）
WINDOW_BLOCK_NUM = 4

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
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)
        self.game_init()

    def game_init(self):
        self.main_batch = pyglet.graphics.Batch()
        self.data = [[2 for i in range(WINDOW_BLOCK_NUM)] for j in range(WINDOW_BLOCK_NUM)]
        #self.data[0][:] = [0,0,0,0]
        ##self.data[1][0]= 0
        #self.data[2][0]= 0
        #self.data[3][0]= 0

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
            font_s = 22 if data > 10000 else 28

            a = pyglet.text.Label(text=str(data), bold=True, anchor_x = 'center', anchor_y = 'center',
                    color=(0,0,0, 255), x=x+dx/2, y=y+dy/2,
                    font_size=font_s)

            a.draw()


    def on_key_press(self, symbol, modifiers):

        eq_tile = False
        key_press = False
        score = 0

        if symbol == key.UP:
            self.data, eq_tile, score = self.slideUpDown(True)
            key_press = True
        elif symbol == key.DOWN:
            self.data, eq_tile, score = self.slideUpDown(False)
            key_press = True
        elif symbol == key.LEFT:
            self.data, eq_tile, score = self.slideLeftRight(True)
            key_press = True

        elif symbol == key.RIGHT:
            self.data, eq_tile, score = self.slideLeftRight(False)
            key_press = True
        elif symbol == key.ESCAPE:
            self.close()

        self.score += score

    def merge(self,vlist,direct):
        score = 0
        if direct: #up or left
            i = 1
            while i<len(vlist):
                if vlist[i-1]==vlist[i]:
                    # 当两个块值相等，则删除一个，并让另一个值*2
                    del vlist[i]
                    vlist[i-1] *= 2
                    score += vlist[i-1]
                i += 1
        else:
            i = len(vlist)-1
            while i>0:
                if vlist[i-1]==vlist[i]:
                    del vlist[i]
                    vlist[i-1] *= 2
                    score += vlist[i-1]
                i -= 1      
        return score
        
    def slideUpDown(self,up):
        oldData = copy.deepcopy(self.data)
        score = 0
        for col in range(WINDOW_BLOCK_NUM):
            
            # 抽取一维非零向量
            cvl = [oldData[row][col] for row in range(WINDOW_BLOCK_NUM) if oldData[row][col]!=0]

            # 合并
            if len(cvl)>=2:
                score += self.merge(cvl,up)
            
            # 补零
            for i in range(WINDOW_BLOCK_NUM-len(cvl)):
                if up: cvl.append(0)
                else: cvl.insert(0,0)
            
            # 回填
            for row in range(WINDOW_BLOCK_NUM): oldData[row][col] = cvl[row]
        return oldData, oldData==self.data, score

    def slideLeftRight(self,left):
        oldData = copy.deepcopy(self.data)
        score = 0
        for row in range(WINDOW_BLOCK_NUM):
            rvl = [oldData[row][col] for col in range(WINDOW_BLOCK_NUM) if oldData[row][col]!=0]

            if len(rvl)>=2:           
                score += self.merge(rvl,left)
            for i in range(WINDOW_BLOCK_NUM-len(rvl)):
                if left: rvl.append(0)
                else: rvl.insert(0,0)
            for col in range(WINDOW_BLOCK_NUM): oldData[row][col] = rvl[col]
        return oldData, oldData==self.data, score


# 创建窗口
win = Window(WIN_WIDTH, WIN_HEIGHT)

# 设置图标
icon = pyglet.image.load('icon.ico')
win.set_icon(icon)

pyglet.app.run()