# -*- coding: utf-8 -*-.
import os, sys
title_a = '!['
title_b = ')'
title_c = ']('


count = 0

with open('/Users/anren/Desktop/pic.txt', 'r') as f:
    while True:
        line = f.readline()     # 逐行读取
        if not line:
            break

        count = count + 1  # 用数字定位

        line = line.strip('\n')

        f1 = str (count) +  '\n' +  title_a +  str(count) + title_c + line + title_b + '\n'  # 加字符和数字

        with open('/Users/anren/Desktop/pic1.txt', 'a') as p:
            p.write(f1)  # 写入

        print (f1)
