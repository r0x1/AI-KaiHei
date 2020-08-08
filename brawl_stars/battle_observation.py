import cv2
import numpy
import win32con
import win32gui
import win32ui
import multiprocessing
from time import sleep

from brawl_stars import config
from brawl_stars.battle_thinking import BattleThinking
from brawl_stars.hero_attack import HeroAttackProcess
from brawl_stars.hero_move import HeroMoveProcess
from brawl_stars.object_detection import ObjectDetection


class BattleObservationProcess:

    # 持续运行标识
    def __init__(self):
        # 开辟进程间共享变量
        self.active_flag = multiprocessing.Value('b', False)
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

        # 获取后台窗口的句柄，注意后台窗口不能最小化
        # 窗口的类名可以用Visual Studio的SPY++工具获取
        h_wnd = win32gui.FindWindow(config.game_window_class_name, config.game_window_title)

        # 获取句柄窗口的大小信息
        left, top, right, bottom = win32gui.GetWindowRect(h_wnd)
        width = right - left
        height = bottom - top

        # 返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
        h_wnd_dc = win32gui.GetWindowDC(h_wnd)
        # 创建设备描述表
        mfc_dc = win32ui.CreateDCFromHandle(h_wnd_dc)
        # 创建内存设备描述表
        save_dc = mfc_dc.CreateCompatibleDC()
        # 创建位图对象准备保存图片
        save_bitmap = win32ui.CreateBitmap()
        # 为bitmap开辟存储空间
        save_bitmap.CreateCompatibleBitmap(mfc_dc, width, height)

        # 循环截图
        # self._loop_screen(save_dc, save_bitmap, width, height, mfc_dc, h_wnd)

        # 实例化ObjectDetection
        obj_detect = ObjectDetection(weights='..\\weights\\brawl_stars_enemy_and_teammate.pt', imgsz=1920,
                                     confidence=0.4)

        # 实例化BattleThinking
        battle_think = BattleThinking()

        # 实例化HeroMoveProcess
        hero_move_process = HeroMoveProcess(h_wnd)
        hero_move_process.start_process()

        # 实例化HeroAttackProcess
        hero_attack_process = HeroAttackProcess(h_wnd)
        hero_attack_process.start_process()

        # 判断 进程间共享变量 是否为 True
        while self.active_flag.value:
            # 将截图保存到saveBitMap中
            save_dc.SelectObject(save_bitmap)
            # 保存bitmap到内存设备描述表
            save_dc.BitBlt((0, 0), (width, height), mfc_dc, (0, 0), win32con.SRCCOPY)

            signed_ints_array = save_bitmap.GetBitmapBits(True)
            img = numpy.fromstring(signed_ints_array, dtype='uint8')
            img.shape = (height, width, 4)
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

            # [battle_observation]进程，调用object_detection功能，对图片进行检测，返回物体信息list，
            # 如果显示预览窗体，则 画框
            list_detect, img = obj_detect.detect(img, draw_box=config.display_preview_screen)

            if len(list_detect) > 0:
                print(list_detect)
            pass

            # 是否显示游戏预览
            if config.display_preview_screen:
                # 全屏显示游戏画面
                if config.preview_full_screen:
                    cv2.namedWindow(config.cv2_window_title, flags=cv2.WND_PROP_FULLSCREEN)
                    # cv2.moveWindow(config.cv2_window_title, screen.x - 1, screen.y - 1)
                    cv2.setWindowProperty(config.cv2_window_title, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                pass

                # 在指定窗口中，显示图片
                cv2.imshow(config.cv2_window_title, img)
                # 0 表示程序会无限制的等待用户的按键事件
                key = cv2.waitKey(1)

                if key is not -1:
                    print(key)

                    if key is 113:
                        # q 键 退出
                        self.active_flag.value = False
                        pass
                    pass
                pass
            pass

            # [battle_observation]进程，调用battle_thinking功能，对物体信息list进行分析
            # 清空数据
            battle_think.clear_data()
            # 处理物体列表
            result_move_direction, result_move_distance, result_attack_direction, result_attack_type = \
                battle_think.process_all(objects_list=list_detect)

            # [battle_observation]进程，启动[hero_movement]进程，由[hero_movement]进程，调用[device_control]功能，实现移动功能。
            hero_move_process.refresh(move_direction=result_move_direction, move_distance=result_move_distance)

            # [battle_observation]进程，启动[hero_attack]进程，由[hero_attack]进程，调用[device_control]功能，实现攻击功能。
            hero_attack_process.refresh(attack_direction=result_attack_direction, attack_type=result_attack_type)

        pass

        # 释放cv2
        cv2.destroyWindow(config.cv2_window_title)

        # 释放资源
        mfc_dc.DeleteDC()
        save_dc.DeleteDC()
        win32gui.ReleaseDC(h_wnd, h_wnd_dc)
        win32gui.DeleteObject(save_bitmap.GetHandle())

        print('battle observation process terminated.')
        pass

    # def _loop_screen(self, save_dc, save_bitmap, width, height, mfc_dc, h_wnd):
        # # 实例化ObjectDetection
        # obj_detect = ObjectDetection(weights='..\\weights\\brawl_stars_enemy_and_teammate.pt', imgsz=1920,
        #                              confidence=0.4)
        #
        # # 实例化BattleThinking
        # battle_think = BattleThinking()
        #
        # # 实例化HeroMoveProcess
        # hero_move_process = HeroMoveProcess(h_wnd)
        # hero_move_process.start_process()
        #
        # # 实例化HeroAttackProcess
        # hero_attack_process = HeroAttackProcess(h_wnd)
        # hero_attack_process.start_process()
        #
        # # 判断 进程间共享变量 是否为 True
        # while self.active_flag.value:
        #     # 将截图保存到saveBitMap中
        #     save_dc.SelectObject(save_bitmap)
        #     # 保存bitmap到内存设备描述表
        #     save_dc.BitBlt((0, 0), (width, height), mfc_dc, (0, 0), win32con.SRCCOPY)
        #
        #     signed_ints_array = save_bitmap.GetBitmapBits(True)
        #     img = numpy.fromstring(signed_ints_array, dtype='uint8')
        #     img.shape = (height, width, 4)
        #     img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        #
        #     # [battle_observation]进程，调用object_detection功能，对图片进行检测，返回物体信息list，
        #     # 如果显示预览窗体，则 画框
        #     list_detect, img = obj_detect.detect(img, draw_box=config.display_preview_screen)
        #
        #     if len(list_detect) > 0:
        #         print(list_detect)
        #     pass
        #
        #     # 是否显示游戏预览
        #     if config.display_preview_screen:
        #         # 全屏显示游戏画面
        #         if config.preview_full_screen:
        #             cv2.namedWindow(config.cv2_window_title, flags=cv2.WND_PROP_FULLSCREEN)
        #             # cv2.moveWindow(config.cv2_window_title, screen.x - 1, screen.y - 1)
        #             cv2.setWindowProperty(config.cv2_window_title, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        #         pass
        #
        #         # 在指定窗口中，显示图片
        #         cv2.imshow(config.cv2_window_title, img)
        #         # 0 表示程序会无限制的等待用户的按键事件
        #         key = cv2.waitKey(1)
        #
        #         if key is not -1:
        #             print(key)
        #
        #             if key is 113:
        #                 # q 键 退出
        #                 self.active_flag.value = False
        #                 pass
        #             pass
        #         pass
        #     pass
        #
        #     # if key is 32:
        #     #     cv2.imwrite(str(time.time()) + '.png', img)
        #     #     pass
        #     # pass
        #
        #     # if key is not -1:
        #     #     print(key)
        #
        #     # [battle_observation]进程，调用battle_thinking功能，对物体信息list进行分析
        #     # 清空数据
        #     battle_think.clear_data()
        #     # 处理物体列表
        #     result_move_direction, result_move_distance, result_attack_direction, result_attack_type = \
        #         battle_think.process_all(objects_list=list_detect)
        #
        #     # [battle_observation]进程，启动[hero_movement]进程，由[hero_movement]进程，调用[device_control]功能，实现移动功能。
        #     hero_move_process.refresh(move_direction=result_move_direction, move_distance=result_move_distance)
        #
        #     # [battle_observation]进程，启动[hero_attack]进程，由[hero_attack]进程，调用[device_control]功能，实现攻击功能。
        #     hero_attack_process.refresh(attack_direction=result_attack_direction, attack_type=result_attack_type)
        # pass
