# -*- coding:utf-8 -*-

#2016-7-16
###############  经过几天的测试 发现基于时间的三次样条插值效果并不好,容易出问题,所以这个方案就pass了
###############  所以现在用的 基于位移的细菌生长曲线插值
#机器人移动速度最大值
velocity_max = 0.5


#基于细生长曲线插值的相关参数
#直线移动的参数
#启动时的参数
# gamma 影响插值曲线上的最大速度
GAMMA = velocity_max
#插值起始速度等于 gamma/(1+beta）
START_BETA =   22
# alpha 影响达到最大速度的自变量的值 alpha越大,越快达到最大速度
START_ALPHA =27
#结束时的参数
END_BETA = 15
END_ALPHA = 10
