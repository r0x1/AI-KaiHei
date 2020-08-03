import multiprocessing
from time import sleep


class HeroMoveProcess:

    # 持续运行标识
    def __init__(self):
        # 开辟进程间共享变量
        self.active_flag = multiprocessing.Value('b', False)
        # result_move_direction, result_move_distance, result_attack_direction, result_attack_type
        # 移动方向
        self.move_direction = multiprocessing.Value('int', 5)
        # 移动距离
        self.move_distance = multiprocessing.Value('int', 0)

        self.process = None
        pass

    def start_process(self):
        # 如果进程已经存在，则先停止进程
        if self.process is not None:
            self.stop_process()
            pass
        pass

        self.active_flag.value = True

        # self.process = multiprocessing.Process(target=self._func_run, args=(0, 1))
        self.process = multiprocessing.Process(target=self._run_hero_move)
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

    def _run_hero_move(self):
        """
        开始
        :return:
        """
        while self.active_flag.value:
            pass
        pass

    pass
