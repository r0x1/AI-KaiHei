import time
import cv2
import numpy
import win32con
import win32gui
import win32ui

from brawl_stars import config
# from brawl_stars.object_detection import ObjectDetection

active_flag = False


def run_battle_observation():
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
    _loop_screen(save_dc, save_bitmap, width, height, mfc_dc)

    # 释放cv2
    cv2.destroyWindow(config.cv2_window_title)

    # 释放资源
    mfc_dc.DeleteDC()
    save_dc.DeleteDC()
    win32gui.ReleaseDC(h_wnd, h_wnd_dc)
    win32gui.DeleteObject(save_bitmap.GetHandle())

    print('battle observation process terminated.')
    pass


def _loop_screen(save_dc, save_bitmap, width, height, mfc_dc):
    # 实例化ObjectDetection
    global active_flag
    # obj_detect = ObjectDetection(weights='..\\..\\weights\\brawl_stars_enemy_and_teammate.pt', imgsz=1920,
    #                              confidence=0.4)

    # 判断 进程间共享变量 是否为 True
    while active_flag:
        # 将截图保存到saveBitMap中
        save_dc.SelectObject(save_bitmap)
        # 保存bitmap到内存设备描述表
        save_dc.BitBlt((0, 0), (width, height), mfc_dc, (0, 0), win32con.SRCCOPY)

        signed_ints_array = save_bitmap.GetBitmapBits(True)
        img = numpy.fromstring(signed_ints_array, dtype='uint8')
        img.shape = (height, width, 4)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        # [battle_observation]进程，调用object_detection功能，对图片进行检测，返回物体信息list，
        # list_detect, img = obj_detect.detect(img, draw_box=True)
        #
        # if len(list_detect) > 0:
        #     print(list_detect)
        # pass

        # 画框
        # 显示预览
        cv2.namedWindow(config.cv2_window_title, flags=cv2.WND_PROP_FULLSCREEN)
        # cv2.moveWindow(config.cv2_window_title, screen.x - 1, screen.y - 1)
        cv2.setWindowProperty(config.cv2_window_title, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        cv2.imshow(config.cv2_window_title, img)  # 第一个参数是窗口名称，是字符串。第二个参数是我们的图片
        key = cv2.waitKey(1)  # 0 表示程序会无限制的等待用户的按键事件

        if key is not -1:
            print(key)

            if key is 32:
                # 空格键
                cv2.imwrite('./capture_images/' + str(time.time()) + '.png', img)
                pass
            elif key is 113:
                # q 键 退出
                active_flag = False
                pass
            pass
        pass
    pass


if __name__ == "__main__":
    active_flag = True
    run_battle_observation()

    pass
