# -*- coding:utf-8 -*-

#2016-7-16
###############  经过几天的测试 发现基于时间的三次样条插值效果并不好,容易出问题,所以这个方案就pass了
###############  所以现在用的 基于位移的细菌生长曲线插值
#机器人移动速度最大值
velocity_max = 1.0
#机器人移动加速度最大值
acceleration_max = 0.75
#机器人移动加速度变化率最大值
rate_of_acceleration__max = 1.0
#小于此距离按照第一种模式插值，两个加速阶段，两个减速阶段
first_mode_dis = 0.5
#大于第一种小于这个距离按照第二种模式插值，三个加速阶段，三个减速阶段
second_mode_dis = 1.2

#基于细生长曲线插值的相关参数
#直线移动的参数
#启动时的参数
# gamma 影响插值曲线上的最大速度
GAMMA = velocity_max
#插值起始速度等于 gamma/(1+beta）
START_BETA =   24
# alpha 影响达到最大速度的自变量的值 alpha越大,越快达到最大速度
START_ALPHA =22
#结束时的参数
END_BETA = 27
END_ALPHA = 18
