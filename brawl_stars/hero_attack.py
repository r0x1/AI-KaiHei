import multiprocessing
from time import sleep
import win32gui, win32con

from brawl_stars.battle_thinking import Direction, AttackType


class HeroAttackProcess:

    def __init__(self, h_wnd):
        # 用 w/a/s/d 进行移动，用 方向箭头 进行攻击
        # 'w':0x57,'a':0x41,'s':0x53,'d':0x44
        # 开辟进程间共享变量
        # 持续运行标识
        self.active_flag = multiprocessing.Value('b', False)
        # result_move_direction, result_move_distance, result_attack_direction, result_attack_type
        # 攻击方向
        self.attack_direction = multiprocessing.Value('i', Direction.none.value)
        # 攻击类型
        self.attack_type = multiprocessing.Value('i', AttackType.none.value)

        self.process = None

        self.h_wnd = h_wnd
        pass

    def refresh(self, attack_direction, attack_type):
        self.attack_direction.value = attack_direction
        self.attack_type.value = attack_type
        pass

    def start_process(self):
        # 如果进程已经存在，则先停止进程
        if self.process is not None:
            self.stop_process()
            pass
        pass

        self.active_flag.value = True

        # self.process = multiprocesmultiprocessing.Processsing.Process(target=self._func_run, args=(0, 1))
        self.process = multiprocessing.Process(target=self._run_hero_attack, args=(self.h_wnd,))
        # self.process.daemon = True
        self.process.start()
        pass

    def stop_process(self):
        self.active_flag.value = False
        print('hero move process stopping...')

        if self.process is not None:
            # 等待循环退出
            sleep(1)
            self.process.terminate()
            pass
        pass

    def _run_hero_attack(self, h_wnd):
        while self.active_flag.value:
            if self.attack_type.value != AttackType.none.value and self.attack_direction.value != Direction.none.value:
                sleep_sec = 0.5
                # 用 方向箭头 进行攻击
                if self.attack_direction.value == Direction.north.value:
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYDOWN, win32con.VK_UP, 0)
                    sleep(sleep_sec)
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYUP, win32con.VK_UP, 0)
                    pass
                elif self.attack_direction.value == Direction.south.value:
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYDOWN, win32con.VK_DOWN, 0)
                    sleep(sleep_sec)
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYUP, win32con.VK_DOWN, 0)
                    pass
                elif self.attack_direction.value == Direction.west.value:
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYDOWN, win32con.VK_LEFT, 0)
                    sleep(sleep_sec)
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYUP, win32con.VK_LEFT, 0)
                    pass
                elif self.attack_direction.value == Direction.east.value:
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYDOWN, win32con.VK_RIGHT, 0)
                    sleep(sleep_sec)
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYUP, win32con.VK_RIGHT, 0)
                    pass
                elif self.attack_direction.value == Direction.north_west.value:
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYDOWN, win32con.VK_LEFT, 0)
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYDOWN, win32con.VK_UP, 0)
                    sleep(sleep_sec)
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYUP, win32con.VK_LEFT, 0)
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYUP, win32con.VK_UP, 0)
                    pass
                elif self.attack_direction.value == Direction.south_west.value:
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYDOWN, win32con.VK_LEFT, 0)
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYDOWN, win32con.VK_DOWN, 0)
                    sleep(sleep_sec)
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYUP, win32con.VK_LEFT, 0)
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYUP, win32con.VK_DOWN, 0)
                    pass
                elif self.attack_direction.value == Direction.north_east.value:
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYDOWN, win32con.VK_RIGHT, 0)
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYDOWN, win32con.VK_UP, 0)
                    sleep(sleep_sec)
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYUP, win32con.VK_RIGHT, 0)
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYUP, win32con.VK_UP, 0)
                    pass
                elif self.attack_direction.value == Direction.south_east.value:
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYDOWN, win32con.VK_RIGHT, 0)
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYDOWN, win32con.VK_DOWN, 0)
                    sleep(sleep_sec)
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYUP, win32con.VK_RIGHT, 0)
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYUP, win32con.VK_DOWN, 0)
                    pass
                pass

                # 重置
                # 攻击类型
                self.attack_type.value = AttackType.none.value
                # 攻击方向
                self.attack_direction.value = Direction.none.value
            pass
        pass

    pass
