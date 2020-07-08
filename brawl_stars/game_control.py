import multiprocessing
from time import sleep

from brawl_stars.battle_observation import BattleObservationProcess


class GameControlProcess:

    def __init__(self):
        # 开辟进程间共享变量
        # 持续运行标识
        self.active_flag = multiprocessing.Value('b', False)
        self.process = None
        self.battle_observation_process = BattleObservationProcess()
        pass

    def start_process(self):
        # 如果进程已经存在，则先停止进程
        if self.process is not None:
            self.stop_process()
            pass
        pass

        self.active_flag.value = True

        # self.process = multiprocessing.Process(target=self._func_run, args=(0, 1))
        self.process = multiprocessing.Process(target=self._run_game_control)
        # self.process.daemon = True
        self.process.start()
        pass

    def stop_process(self):
        self.active_flag.value = False
        print('game control process stopping...')

        # 停止[battle_observation]进程
        if self.battle_observation_process is not None:
            self.battle_observation_process.stop_process()
            pass

        # 停止[game_control]进程
        if self.process is not None:
            # 等待循环退出
            sleep(1)
            self.process.terminate()
            pass
        pass

    def _run_game_control(self):
        """
        开始
        :return:
        """
        # [battle_observation]：战斗观察，负责从屏幕"截取图片"、调用[object_detection]、[battle_thinking]、[hero_movement]、[hero_attack]。
        # 停止[battle_observation]进程
        if self.battle_observation_process is not None:
            self.battle_observation_process.stop_process()
            pass

        # 由[游戏控制]进程，启动[战斗观察]进程。
        self.battle_observation_process.start_process()
        pass
