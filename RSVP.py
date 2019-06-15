#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 导入所需的库
import sys, random, os, time
from psychopy import visual, core, event, gui
import random, glob, os, time

# from ctypes import windll
#
# p = windll.inpoutx64
# def send_code(code):
#     p.Out32(0x378, code)
#     time.sleep(0.006)
#     p.Out32(0x378, 0)
#     time.sleep(0.01)

# 被试信息记录
info = {'name':'', 'age':'', 'gender':['M','F'],'num':'1', 'task':['1','2','3','4']}
infoDlg = gui.DlgFromDict(dictionary = info, title = u'基本信息', order = ['num','name','age','gender','task'])
if infoDlg.OK == False:
    core.quit()

#创建空白文档
dataFile = open('/Users/zapp/Documents/neurhythm/'+ "%s.csv"%(info['num']+'_'+info['name']), 'a')
dataFile.write(info['num']+','+info['name']+','+info['age']+'\n')
dataFile.write('k_3, key, RTs\n')

# 创建窗口
scnWidth, scnHeight = [1920, 1080]
win = visual.Window((scnWidth, scnHeight), fullscr=True, units='pix', colorSpace='rgb')
win.mouseVisible =False

# 指导语
text_1 = visual.TextStim(win, text=u'', height=40,color='white')
text_1.text = u'Welcome to the psychological experiment'

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

T2 = 'x'

Condition_list = [chr(i) for i in range(97,123)]
random.shuffle(Condition_list)
Condition_list.remove(T2)

# 十字注视点
text_1 = visual.TextStim(win, text=u'+', height=72, pos=(0.0, 0.0), color='white')
text_1.draw()
win.flip()
core.wait(random.uniform(1.0, 1.5)) # 随机呈现注视点

# x = random.shuffle([4,7])
# x= x[0]

count = 0

block = 0

y = [1, 2, 7, -1] * 16
random.shuffle(y)

while block <= 10:

    T3 = -1

    x = [4, 7]
    random.shuffle(x)

    for j in Condition_list[0:18]:# 呈现字母流

        j= j.upper()

        text_2 = visual.TextStim(win, text= j, pos=(0.0, 0.0), wrapWidth=1.0, color='white', height=48,font='Hei')
        text_2.draw()
        win.flip()
        core.wait(0.2)

        count = count + 1

        if count == x[0]:

            # print (count)

            text_T1 = visual.TextStim(win, text=j, pos=(0.0, 0.0), wrapWidth=1.0, color='green', height=48, font='Hei')
            text_T1.draw()
            win.flip()
            core.wait(0.2)

            T3 = y[block] + x[0]

        T2 = T2.upper()
        if count == T3:
            text_T1 = visual.TextStim(win, text= T2, pos=(0.0, 0.0), wrapWidth=1.0, color='white', height=48, font='Hei')
            text_T1.draw()
            win.flip()
            core.wait(0.2)
            # send_code(11)

        # print(count)

        for key in event.getKeys():  # 在此while循环中如何按键退出
            if key in ['q']:
                core.quit()

    text_4 = visual.TextStim(win, text=u'If the word X appear?',  height= 40, color='white')
    text_4.draw()
    win.flip()
    core.wait(0)

    count = 0
    #k_3 = event.waitKeys() #等待按键反应
    #k_3 = event.getKeys(keyList=['y', 'n']
    k_3 = event.waitKeys(keyList=['f', 'j'])
    # if k_3[0] == 'f':
    #     send_code == 12
    # else:
    #     send_code == 13

    block = block + 1

    if block % 5 == 0:
        text_rest = visual.TextStim(win, text=u'Have a rest\n\nPress spacebar to continue', color='white', height=40)
        text_rest.draw()
        win.flip()
        core.wait(0)
        k_rest = event.waitKeys()

# 结束语
text_5 = visual.TextStim(win, text=u'Thank you for your participation', color='white', height=40)
text_5.draw()
win.flip()
core.wait(3)

# 关闭窗口
win.close()
core.quit()
