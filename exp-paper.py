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


# 创建窗口
scnWidth, scnHeight = [1920, 1080]
win = visual.Window((scnWidth, scnHeight), fullscr=False, units='pix', color = (-1,-1,-1))
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

# 随机刺激材料
pic_list = []
pic_ims = glob.glob("/Users/zapp/Downloads/daily-download.ZAPP.com/exp/*.jpg")
for image in pic_ims:
    pic_list.append(image)
random.shuffle(pic_list)

Word_list = ['幽雅','无私','正义','端庄','学叔','富丽','苦闷','郁闷','自卑','偏见','新颖','天使','虚伪','乞丐','疾病','宽厚','高贵','焦躁','疲倦','细菌','雅致','坦诚','压力','精品','懒惰']
random.shuffle(Word_list)


# 呈现图片
for j,i in zip(pic_list,Word_list):

    # 十字注视点
    text_1 = visual.TextStim(win, text=u'+', height=72, pos=(0.0, 0.0), color='white',font='Hei')
    text_1.draw()
    win.flip()
    core.wait(0.4)

    # 呈现图片

    pic = visual.ImageStim(win)
    pic.image = j
    pic.draw()
    win.flip()
    core.wait(0.1)

    # 呈现空屏幕

    pic = visual.ImageStim(win)
    pic.image = '/Users/zapp/Downloads/daily-download.ZAPP.com/pic1.jpg'
    pic.draw()
    win.flip()
    core.wait(0.1)

    # 呈现词语

    text_1 = visual.TextStim(win, text=i, height=72, pos=(0.0, 0.0), color='white',font='Hei',wrapWidth=1.0)
    text_1.draw()
    win.flip()
    core.wait(1.5)

# 结束语
text_3 = visual.TextStim(win, text=u'实验结束，感谢「学叔」的参与。', pos=(0.0, 0.0), wrapWidth=1.0, color='white', height=48, font='Hei')
text_3.draw()
win.flip()
core.wait(3)

# 关闭窗口
win.close()
core.quit()