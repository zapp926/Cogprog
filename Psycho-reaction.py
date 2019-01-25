#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# 导入所需的库
import sys, random, os, time
from psychopy import visual, core, event, gui
import random, glob, os, time

# 被试信息记录
info = {'name':'', 'age':'', 'gender':['M','F'],'num':'1', 'task':['1','2','3','4']}
infoDlg = gui.DlgFromDict(dictionary = info, title = u'基本信息', order = ['num','name','age','gender','task'])
if infoDlg.OK == False:
    core.quit()

#创建空白文档
dataFile = open('/Users/liuxiao/data_oddball/'+ "%s.csv"%(info['num']+'_'+info['name']), 'a')
dataFile.write(info['num']+','+info['name']+','+info['age']+'\n')
dataFile.write('picName, key, RTs\n')

# 创建窗口
scnWidth, scnHeight = [1024, 800]
win = visual.Window((scnWidth, scnHeight), fullscr=False, units='pix', colorSpace='rgb')
win.mouseVisible =False

# 指导语
text_1 = visual.TextStim(win, text=u'', height=48, font='Hei', pos=(0.0,0.0), color='black')
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

pic_list = []
pic_ims = glob.glob("/Users/liuxiao/PycharmProjects/experiment/pic/*.jpg")
for image in pic_ims:
    pic_list.append(image)
random.shuffle(pic_list)

count = 0

list_rest = [10,20,30]

# 呈现图片
for j in pic_list:

    # 十字注视点
    text_1 = visual.TextStim(win, text=u'+', height=72, pos=(0.0, 0.0), color='white')
    text_1.draw()
    win.flip()
    core.wait(random.uniform(0.8, 1.2))  # 随机空屏

    # timer = core.Clock()

    trigger = os.path.split(j)[1].split('.')[0]
    print (trigger)

    k_1 = event.clearEvents()

    timer = core.Clock()

    # 呈现图片

    pic = visual.ImageStim(win)
    pic.image = j
    pic.draw()
    win.flip()
    core.wait(2, hogCPUperiod=2)

    timer.reset()

    k_1 = event.getKeys(keyList=['f', 'j'],timeStamped = timer)

    #if len(k_1) > 0 :


    print (end - start)

    try:

        key_1 = k_1[0][0]
        key_2 = k_1[0][1] + 2.0
        #gotdata = dlist[1]

        # RT = key_2 + 2.0
        dataFile.write(str(trigger) + ', ' + str(key_1) + ',' + str(key_2) + '\n')
    except IndexError:
        #gotdata = 'null'
        key_1 = 'null'
        key_2 = 'null'
        dataFile.write(str(trigger) + ', ' + key_1 + ',' + key_2 + '\n')

    print (key_1)
    print (key_2)
    # c = key_2 + 2.0
    #print (c)

    count = count + 1

    if count in list_rest:
        text_2 = visual.TextStim(win, text=u'休息一下，按任意键继续', pos=(0.0, 0.0), wrapWidth=1.0, color='white', height=48, font='Hei')
        text_2.draw()
        win.flip()
        core.wait(0)
        k_2 = event.waitKeys()

    for key in event.getKeys():  # 在此while循环中如何按键退出
        if key in ['x']:
            core.quit()

    #dataFile.write(str(j) + ', ' + str(k_1[0][0]) + '\n')

# 结束语
text_3 = visual.TextStim(win, text=u'实验全部结束，感谢您的参与。', pos=(0.0, 0.0), wrapWidth=1.0, color='white', height=48, font='Hei')
text_3.draw()
win.flip()
core.wait(3)

# 关闭窗口
win.close()
core.quit()
