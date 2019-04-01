#!'E:/python/Python36
'''
@File    :   zheye_test.py
@Time    :   2019/03/14 20:12:03
@Author  :   fan zehua 
@Version :   1.0
@Contact :   316679581@qq.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here put the import lib
from zheye import zheye

z = zheye()
positions = z.Recognize('tools\\zhihu_image\\c.gif')
last_positions = []
if len(positions) == 2:
    if positions[0][1] > positions[1][1]:
        last_positions.append([positions[1][1], positions[1][0]])
        last_positions.append([positions[0][1], positions[0][0]])
    else:
        last_positions.append([positions[0][1], positions[0][0]])
        last_positions.append([positions[1][1], positions[1][0]])
else:
    last_positions.append([positions[0][1], positions[0][0]])
print(last_positions)
