#!/usr/bin/env python
#coding:utf-8

#Team Unware Basketball Robot
#China , Xi'an ,NWPU
#外部发送一个弧度值，使机器人旋转相应的角度

# author = hao , liao-zhihan

#first_debug_date = 2015-07
#first_debug: 第一次测试通过

#second_debug_date = 2016-03-02 author=liao-zhihan
#second_debug:重写代码，对代码进行了规范，测试通过

#################################################
#注意添加坐标获取模块路径到pth!                 #
#################################################
#           tf这边返回的角度 是 -pi 到 pi
#           所以在出现 -pi 越过 pi 时 会十分奇葩
#           所以通过计算角度变化的累加值 避免出现这个情况
#             2016-7-15 这个错误以修复
#append the robot state pkg to the python path
import config
import math
import sys
sys.path.append(config.robot_state_pkg_path)
import robot_state_pkg.get_robot_position as robot_state
import rospy
import geometry_msgs.msg as g_msgs

class turn_an_angular(object):
    def __init__(self):
        rospy.loginfo('[robot_move_pkg]->move_an_angular is initial')
        self.robot_state = robot_state.robot_position_state()
        self.speed = config.high_turn_angular_speed
        self.stop_tolerance = config.high_turn_angular_stop_tolerance
        # self.turn_scale = config.turn_angular_scale
        self.cmd_vel_pub = rospy.Publisher('/cmd_move' , g_msgs.Twist , queue_size=100)

    #发送急停速度，机器人停止
    def brake(self):
        self.cmd_vel_pub.publish(g_msgs.Twist())

    def start_turn(self , goal_angular = 0.0):
        rospy.loginfo('[robot_move_pkg]->move_an_angular will turn %s'%goal_angular)
        rospy.on_shutdown(self.brake) #系统停止时，机器人急停
        current_angular = start_angular = self.robot_state.get_robot_current_w()#获取当前机器人的角度
        is_arrive_goal = False
        r = rospy.Rate(100)
        delta_angular = current_angular - start_angular
        delta_upper_limit = abs(goal_angular) + self.stop_tolerance #误差上限
        delta_lower_limit = abs(goal_angular) - self.stop_tolerance #误差下限
        move_velocity = g_msgs.Twist()
        while not rospy.is_shutdown() and not is_arrive_goal:
            if abs(delta_angular)<=delta_upper_limit and abs(delta_angular) >= delta_lower_limit: #到达目标
                self.brake()
                is_arrive_goal = True
                break
            current_angular = self.robot_state.get_robot_current_w()
            if goal_angular > 0:
                move_velocity.angular.z = self.speed
            else:
                move_velocity.angular.z = -self.speed
            delta_angular += abs(abs(current_angular) - abs(start_angular) )
            start_angular = current_angular
            self.cmd_vel_pub.publish(move_velocity) #发送速度，使机器人旋转
            r.sleep()
        self.brake()

    #使机器转某角度. 单位：弧度
    def turn(self , angular = 0.0):
        self.start_turn(self.normalize_angle(angular))#正规化

    #使机器转到某一角度.范围为：-pi 到 pi .机器的初始位置为0.  单位：弧度
    def turn_to(self,goal_angular):
        current_angular = self.robot_state.get_robot_current_w()
        rospy.loginfo("current = %s",current_angular)
        if current_angular * goal_angular < 0:
            turn_angular = abs(current_angular) + abs(goal_angular)
            if current_angular > 0:
                turn_angular = -turn_angular
        else:
            turn_angular = goal_angular - current_angular

        rospy.loginfo("turn = %s",turn_angular)
        if abs(turn_angular) > math.pi:
            if turn_angular > 0:
                turn_angular = -(2 * math.pi - abs(turn_angular))
            else:
                turn_angular = 2 * math.pi - abs(turn_angular)
        self.turn(turn_angular)


    #将目标角度规范化，取最近的方向进行移动
	#如：发送目标值200
	#此时可正转200,亦可逆转160
	#此时逆转160度
    def normalize_angle(self,angular):
        while angular > math.pi:
            angular -= 2.0 * math.pi
        while angular < -math.pi:
            angular += 2.0 * math.pi
        print('current angular is %s'%angular)
        return angular


if __name__ == '__main__':
    rospy.init_node('turn_angular')
    a = turn_an_angular()
    a.turn_to(-(1.0/4.0) * math.pi)
    # a.turn(math.radians(float(sys.argv[1])))

sys.path.remove(config.robot_state_pkg_path)
