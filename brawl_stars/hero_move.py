import multiprocessing
from time import sleep
import win32api, win32gui, win32con

from brawl_stars import device_control
from brawl_stars.battle_thinking import Direction


class HeroMoveProcess:

    def __init__(self, h_wnd):
        # 开辟进程间共享变量
        # 持续运行标识
        self.active_flag = multiprocessing.Value('b', False)
        # result_move_direction, result_move_distance, result_attack_direction, result_attack_type
        # 移动方向
        self.move_direction = multiprocessing.Value('int', Direction.center.value)
        # 移动距离
        self.move_distance = multiprocessing.Value('int', 0)

        self.process = None

        self.h_wnd = h_wnd
        pass

    def refresh(self, move_direction, move_distance):
        self.move_direction = multiprocessing.Value('int', Direction[move_direction.name].value)
        self.move_distance = multiprocessing.Value('int', move_distance)
        pass

    def start_process(self):
        # 如果进程已经存在，则先停止进程
        if self.process is not None:
            self.stop_process()
            pass
        pass

        self.active_flag.value = True

        # self.process = multiprocesmultiprocessing.Processsing.Process(target=self._func_run, args=(0, 1))
        self.process = multiprocessing.Process(target=self._run_hero_move, args=self.h_wnd)
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
            if self.move_distance != 0 and self.move_direction.value != Direction.center.value:
                sleep_sec = 1.0 * self.move_distance.value

                if self.move_direction.value == Direction.north.value:
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYDOWN, win32con.VK_UP, 0)
                    sleep(sleep_sec)
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYUP, win32con.VK_UP, 0)
                    pass
                elif self.move_direction.value == Direction.south.value:
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYDOWN, win32con.VK_DOWN, 0)
                    sleep(sleep_sec)
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYUP, win32con.VK_DOWN, 0)
                    pass
                elif self.move_direction.value == Direction.west.value:
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYDOWN, win32con.VK_LEFT, 0)
                    sleep(sleep_sec)
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYUP, win32con.VK_LEFT, 0)
                    pass
                elif self.move_direction.value == Direction.east.value:
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYDOWN, win32con.VK_RIGHT, 0)
                    sleep(sleep_sec)
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYUP, win32con.VK_RIGHT, 0)
                    pass
                elif self.move_direction.value == Direction.north_west.value:
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYDOWN, win32con.VK_LEFT, 0)
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYDOWN, win32con.VK_UP, 0)
                    sleep(sleep_sec)
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYUP, win32con.VK_LEFT, 0)
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYUP, win32con.VK_UP, 0)
                    pass
                elif self.move_direction.value == Direction.south_west.value:
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYDOWN, win32con.VK_LEFT, 0)
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYDOWN, win32con.VK_DOWN, 0)
                    sleep(sleep_sec)
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYUP, win32con.VK_LEFT, 0)
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYUP, win32con.VK_DOWN, 0)
                    pass
                elif self.move_direction.value == Direction.north_east.value:
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYDOWN, win32con.VK_RIGHT, 0)
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYDOWN, win32con.VK_UP, 0)
                    sleep(sleep_sec)
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYUP, win32con.VK_RIGHT, 0)
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYUP, win32con.VK_UP, 0)
                    pass
                elif self.move_direction.value == Direction.south_east.value:
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYDOWN, win32con.VK_RIGHT, 0)
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYDOWN, win32con.VK_DOWN, 0)
                    sleep(sleep_sec)
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYUP, win32con.VK_RIGHT, 0)
                    win32gui.PostMessage(h_wnd, win32con.WM_KEYUP, win32con.VK_DOWN, 0)
                    pass
                pass

                # 重置
                # 移动距离
                self.move_distance = multiprocessing.Value('int', 0)
                # 移动方向
                self.move_direction = multiprocessing.Value('int', Direction.center.value)
            pass
        pass

    pass
