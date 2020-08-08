import multiprocessing
import random
from time import sleep
import win32gui, win32con

from brawl_stars.battle_thinking import Direction


class HeroMoveProcess:

    def __init__(self, h_wnd):
        # 用 w/a/s/d 进行移动，用 方向箭头 进行攻击
        # 'w':0x57,'a':0x41,'s':0x53,'d':0x44
        # 开辟进程间共享变量
        # 持续运行标识
        self.active_flag = multiprocessing.Value('b', False)
        # result_move_direction, result_move_distance, result_attack_direction, result_attack_type
        # 移动方向
        self.move_direction = multiprocessing.Value('i', Direction.none.value)
        # 移动距离
        self.move_distance = multiprocessing.Value('i', 0)

        self.process = None

        self.h_wnd = h_wnd
        pass

    def refresh(self, move_direction, move_distance):
        if move_direction != 0 and move_distance != 0:
            self.move_direction.value = move_direction
            self.move_distance.value = move_distance
        pass

    def start_process(self):
        # 如果进程已经存在，则先停止进程
        if self.process is not None:
            self.stop_process()
            pass
        pass

        self.active_flag.value = True

        # self.process = multiprocesmultiprocessing.Processsing.Process(target=self._func_run, args=(0, 1))
        self.process = multiprocessing.Process(target=self._run_hero_move, args=(self.h_wnd,))
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

    def _run_hero_move(self, h_wnd):
        while self.active_flag.value:
            if self.move_distance.value != 0 and self.move_direction.value != Direction.none.value:
                sleep_sec = 1.0 * self.move_distance.value

                #  'w':0x57,'a':0x41,'s':0x53,'d':0x44,
                if self.move_direction.value == Direction.north.value:
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYDOWN, 0x57, 0)
                    sleep(sleep_sec)
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYUP, 0x57, 0)
                    pass
                elif self.move_direction.value == Direction.south.value:
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYDOWN, 0x53, 0)
                    sleep(sleep_sec)
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYUP, 0x53, 0)
                    pass
                elif self.move_direction.value == Direction.west.value:
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYDOWN, 0x41, 0)
                    sleep(sleep_sec)
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYUP, 0x41, 0)
                    pass
                elif self.move_direction.value == Direction.east.value:
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYDOWN, 0x44, 0)
                    sleep(sleep_sec)
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYUP, 0x44, 0)
                    pass
                elif self.move_direction.value == Direction.north_west.value:
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYDOWN, 0x41, 0)
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYDOWN, 0x57, 0)
                    sleep(sleep_sec)
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYUP, 0x41, 0)
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYUP, 0x57, 0)
                    pass
                elif self.move_direction.value == Direction.south_west.value:
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYDOWN, 0x41, 0)
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYDOWN, 0x53, 0)
                    sleep(sleep_sec)
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYUP, 0x41, 0)
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYUP, 0x53, 0)
                    pass
                elif self.move_direction.value == Direction.north_east.value:
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYDOWN, 0x44, 0)
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYDOWN, 0x57, 0)
                    sleep(sleep_sec)
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYUP, 0x44, 0)
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYUP, 0x57, 0)
                    pass
                elif self.move_direction.value == Direction.south_east.value:
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYDOWN, 0x44, 0)
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYDOWN, 0x53, 0)
                    sleep(sleep_sec)
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYUP, 0x44, 0)
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYUP, 0x53, 0)
                    pass
                pass

                # 重置
                # 移动距离
                self.move_distance.value = 0
                # 移动方向
                self.move_direction.value = Direction.none.value
            else:
                # 左右摇摆
                randow_sleep = random.uniform(0.201, 0.599)

                win32gui.PostMessage(h_wnd, win32con.WM_KEYDOWN, 0x44, 0)
                win32gui.PostMessage(h_wnd, win32con.WM_KEYUP, 0x44, 0)
                sleep(randow_sleep)

                win32gui.PostMessage(h_wnd, win32con.WM_KEYDOWN, 0x41, 0)
                win32gui.PostMessage(h_wnd, win32con.WM_KEYUP, 0x41, 0)
                sleep(randow_sleep)
                pass
            pass
        pass

    pass
