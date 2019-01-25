#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# 导入所需的库
from psychopy import visual, core, event, gui
import random

# 被试信息记录
info = {'name':'', 'age':'', 'gender':['M','F'],'num':'1', 'task':['1','2','3','4']}
infoDlg = gui.DlgFromDict(dictionary = info, title = u'基本信息', order = ['num','name','age','gender','task'])
if infoDlg.OK == False:
    core.quit()

#创建空白文档
dataFile = open('/Users/liuxiao/data_rate/'+ "%s.csv"%(info['num']+'_'+info['name']), 'a')
dataFile.write(info['num']+','+info['name']+','+info['age']+'\n')
dataFile.write('picName, likeRating, wantRating\n')

# 创建窗口
scnWidth, scnHeight = [1960, 1080]
win = visual.Window((scnWidth, scnHeight), fullscr=True, units='pix', colorSpace='rgb')
win.mouseVisible =False

# 指导语
text_1 = visual.TextStim(win, text=u'', height=48, font='Hei', pos=(0.0,0.0), color='white')
text_1.text = u'欢迎参加心理学实验！'

# 呈现指导语刺激
text_1.draw()
win.flip()
core.wait(0)
k_1 = event.waitKeys()

# 倒计时时钟
dtimer = core.CountdownTimer(4)
while dtimer.getTime()>0:
    text_1.text = str(int(dtimer.getTime()))
    text_1.draw()
    win.flip()

# 量表内容
ratingScale_1 = visual.RatingScale(win, scale=u'不喜欢 <----------->中等喜欢<-----------> 非常喜欢',
                                     stretch=1.8, textColor='white', labels=('1', '5', '9'), lineColor = 'white',
                                     low=1, high=9, leftKeys='left', rightKeys='right', noMouse=True, markerStart=5,textFont='Hei',size=1.0)

ratingScale_2 = visual.RatingScale(win, scale=u'不想要 <----------->中等想要<-----------> 非常想要',
                                       stretch=1.8, textColor='white', labels=('1', '5', '9'), lineColor = 'white',
                                       low=0, high=9, leftKeys='left', rightKeys='right', noMouse=True, markerStart=5,textFont='Hei',size=1.0)

# 随机图片数列
list = []
for i in range(1,11):
   list.append(i)
random.shuffle(list)

# 呈现图片
for j in list:

    # 十字注视点
    text_1 = visual.TextStim(win, text=u'+', height=72, pos=(0.0, 0.0), color='black')
    text_1.draw()
    win.flip()

    # 随机空屏
    core.wait(random.uniform(0.8, 1.2))

    ratingScale_1.reset()
    ratingScale_2.reset()

    # 呈现图片
    pic = visual.ImageStim(win)
    pic.image = 'pic'+ '/'+ str(j) + '.jpg'
    pic.draw()
    win.flip()
    core.wait(2)

    # 评价量表
    item = visual.TextStim(win, text=u'请评价图片中的物品给你的感受。', pos=(0.0, 0.2), wrapWidth=1.0, color='white', height=48, font='Hei')

    while ratingScale_1.noResponse:
        item.draw()
        ratingScale_1.draw()
        win.flip()

    while ratingScale_2.noResponse:
        item.draw()
        ratingScale_2.draw()
        win.flip()

    dataFile.write(str(j) + '.jpg' + ', ' + str(ratingScale_1.getRating()) + ', ' + str(ratingScale_2.getRating())+ '\n')

    for key in event.getKeys():  # 在此while循环中如何按键退出
        if key in ['x']:
            core.quit()

# 结束语
text_2 = visual.TextStim(win, text=u'实验全部结束，感谢您的参与。', pos=(0.0, 0.0), wrapWidth=1.0, color='white', height=48, font='Hei')
text_2.draw()
win.flip()
core.wait(5)

# 关闭窗口
win.close()
core.quit()
