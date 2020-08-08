import multiprocessing
import sys
from time import sleep

import cv2
import numpy
import win32gui
import win32ui

from brawl_stars import config
from brawl_stars.battle_thinking import Direction, AttackType
from brawl_stars.hero_attack import HeroAttackProcess
from brawl_stars.hero_move import HeroMoveProcess


class TestHeroAction:

    # 持续运行标识
    def __init__(self):
        # 开辟进程间共享变量
        self.active_flag = multiprocessing.Value('b', False)
        self.process = None

        # 攻击方向
        self.attack_direction = multiprocessing.Value('i', Direction.none.value)
        # 攻击类型
        self.attack_type = multiprocessing.Value('i', AttackType.none.value)

        # 移动方向
        self.move_direction = multiprocessing.Value('i', Direction.none.value)
        # 移动距离
        self.move_distance = multiprocessing.Value('i', 0)

        # 获取后台窗口的句柄，注意后台窗口不能最小化
        # 窗口的类名可以用Visual Studio的SPY++工具获取
        h_wnd = win32gui.FindWindow(config.game_window_class_name, config.game_window_title)

        # 实例化HeroMoveProcess
        self.hero_move_process = HeroMoveProcess(h_wnd)
        # self.hero_move_process.start_process()

        # 实例化HeroAttackProcess
        self.hero_attack_process = HeroAttackProcess(h_wnd)
        # self.hero_attack_process.start_process()

        pass

    def start_process(self):
        # 如果进程已经存在，则先停止进程
        if self.process is not None:
            self.stop_process()
            pass
        pass

        self.active_flag.value = True

        # self.process = multiprocessing.Process(target=self._func_run, args=(0, 1))
        self.process = multiprocessing.Process(target=self._run_battle_observation)
        # self.process.daemon = True
        self.process.start()
        pass

    def stop_process(self):
        self.active_flag.value = False
        print('battle observation process stopping...')

        if self.process is not None:
            # 等待循环退出
            sleep(1)
            self.process.terminate()
            pass
        pass

    def _run_battle_observation(self):
        """
        开始
        :return:
        """
        print('battle observation process starting...')

        # # 获取后台窗口的句柄，注意后台窗口不能最小化
        # # 窗口的类名可以用Visual Studio的SPY++工具获取
        # h_wnd = win32gui.FindWindow(config.game_window_class_name, config.game_window_title)
        #
        # # 实例化HeroMoveProcess
        # self.hero_move_process = HeroMoveProcess(h_wnd)
        self.hero_move_process.start_process()

        # # 实例化HeroAttackProcess
        # self.hero_attack_process = HeroAttackProcess(h_wnd)
        self.hero_attack_process.start_process()

        # 循环 动作
        # self._loop_action()

        # print('TestHeroAction process terminated.')
        pass

    # def _loop_action(self):
    #     # 判断 进程间共享变量 是否为 True
    #     while self.active_flag.value:
    #
    #         result_move_direction = self.move_direction.value
    #         result_move_distance = self.move_distance.value
    #         result_attack_direction = self.attack_direction.value
    #         result_attack_type = self.attack_type.value
    #
    #         # [battle_observation]进程，启动[hero_movement]进程，由[hero_movement]进程，调用[device_control]功能，实现移动功能。
    #         self.hero_move_process.refresh(move_direction=result_move_direction, move_distance=result_move_distance)
    #
    #         # [battle_observation]进程，启动[hero_attack]进程，由[hero_attack]进程，调用[device_control]功能，实现攻击功能。
    #         self.hero_attack_process.refresh(attack_direction=result_attack_direction, attack_type=result_attack_type)
    #     pass


if __name__ == "__main__":
    # 启动 action进程，负责 根据输入的 multiprocessing.Value，移动方向、移动距离、攻击方向、攻击距离，执行相应的动作
    test_action = TestHeroAction()
    test_action.start_process()

    # 主程序持续运行标识
    main_active_flag = True

    while main_active_flag is True:
        # main线程，负责监听按键，输入移动方向、移动距离、攻击方向、攻击距离，使用 multiprocessing.Value 进程间通信
        print('[1+回车] 移动')
        print('[2+回车] 攻击')
        print('[x+回车] 退出')

        key = input()
        if key is 'x':
            # 退出程序
            # 释放资源
            test_action.stop_process()
            main_active_flag = False
            break
        elif key is 'a':
            # 向左 移动 1
            # test_action.move_distance.value = 1
            # test_action.move_direction.value = Direction.west.value
            test_action.hero_move_process.refresh(Direction.north_east.value, 2)

            pass
        elif key is ' ':
            # 空格 向下 攻击
            # test_action.attack_direction.value = Direction.south.value
            # test_action.attack_type.value = AttackType.none.value
            test_action.hero_attack_process.refresh(Direction.south, AttackType.normal_attack)

            pass
        #         # 攻击方向
        #         self.attack_direction = multiprocessing.Value('int', Direction.none.value)
        #         # 攻击类型
        #         self.attack_type = multiprocessing.Value('int', AttackType.none.value)
        #
        #         # 移动方向
        #         self.move_direction = multiprocessing.Value('int', Direction.none.value)
        #         # 移动距离
        #         self.move_distance = multiprocessing.Value('int', 0)
        else:
            test_action.hero_move_process.refresh(int(key), 2)
            # test_action.hero_attack_process.refresh(int(key), 1)
            test_action.hero_attack_process.refresh(10 - int(key), 1)
        pass
    pass
