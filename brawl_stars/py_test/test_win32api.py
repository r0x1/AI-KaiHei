import random
import time
from time import sleep

import win32api
import win32con
import win32gui

from brawl_stars import config


if __name__ == "__main__":
    h_wnd = win32gui.FindWindow(config.game_window_class_name, config.game_window_title)

    #  'w':0x57,'a':0x41,'s':0x53,'d':0x44,

    while True:
        randow_sleep = random.uniform(0.1, 0.8)

        win32api.PostMessage(h_wnd, win32con.WM_KEYDOWN, 0x41, 0)
        win32api.PostMessage(h_wnd, win32con.WM_KEYUP, 0x41, 0)
        sleep(randow_sleep)

        win32api.PostMessage(h_wnd, win32con.WM_KEYDOWN, 0x44, 0)
        win32api.PostMessage(h_wnd, win32con.WM_KEYUP, 0x44, 0)
        sleep(randow_sleep)
    pass

# while True:
#     win32api.SendMessage(h_wnd, win32con.WM_KEYDOWN, win32con.VK_SPACE, 0)
#     sleep(1)
#     win32api.SendMessage(h_wnd, win32con.WM_KEYUP, win32con.VK_SPACE, 0)
#     sleep(1)
#     print('1')

# # h_wnd = win32gui.FindWindow('Notepad', '*无标题 - 记事本')
# # win32gui.PostMessage(h_wnd, win32con.WM_KEYDOWN, win32con.VK_LEFT, 0)
# # sleep(2)
# # win32gui.PostMessage(h_wnd, win32con.WM_KEYUP, win32con.VK_LEFT, 0)
#
# # 获取句柄窗口的大小信息
# # left, top, right, bottom = win32gui.GetWindowRect(h_wnd)
# # width = right - left
# # height = bottom - top
#
# # 返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
# # h_wnd_dc = win32gui.GetWindowDC(h_wnd)
# # 创建设备描述表
# # mfc_dc = win32ui.CreateDCFromHandle(h_wnd_dc)
# # # 创建内存设备描述表
# # save_dc = mfc_dc.CreateCompatibleDC()
# # # 创建位图对象准备保存图片
# # save_bitmap = win32ui.CreateBitmap()
# # # 为bitmap开辟存储空间
# # save_bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
#
# # 循环截图
# # self._loop_screen(save_dc, save_bitmap, width, height, mfc_dc, h_wnd)
#
# # save_dc.SelectObject(save_bitmap)
# # # 保存bitmap到内存设备描述表
# # save_dc.BitBlt((0, 0), (width, height), mfc_dc, (0, 0), win32con.SRCCOPY)
# #
# # signed_ints_array = save_bitmap.GetBitmapBits(True)
# # img = numpy.fromstring(signed_ints_array, dtype='uint8')
# # img.shape = (height, width, 4)
# # img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
#
# # # 在指定窗口中，显示图片
# # cv2.imshow(config.cv2_window_title, img)
# # # 0 表示程序会无限制的等待用户的按键事件
# # key = cv2.waitKey(0)
#
# # 释放cv2
# # cv2.destroyWindow(config.cv2_window_title)
#

#
# # win32api.PostMessage(h_wnd, win32con.WM_KEYDOWN, win32con.VK_SPACE, 0)
# # win32api.PostMessage(h_wnd, win32con.WM_KEYUP, win32con.VK_SPACE, 0)
#
# # win32gui.PostMessage(h_wnd, win32con.WM_CLOSE, 0, 0)
#
# # 释放资源
# # mfc_dc.DeleteDC()
# # save_dc.DeleteDC()
# # win32gui.ReleaseDC(h_wnd, h_wnd_dc)
# # win32gui.DeleteObject(save_bitmap.GetHandle())


# 获取前景窗口标题
# title = win32gui.GetWindowText(h_wnd)
# print(title)

# if win32api.LoadKeyboardLayout('0x0409', win32con.KLF_ACTIVATE) == None:
#     print('加载键盘失败')
# else:
#     print('加载键盘成功')

# hwndex = win32gui.FindWindowEx(h_wnd, None, 'Qt5QWindowIcon', None)
# hwndex1 = win32gui.FindWindowEx(hwndex, None, 'canvasWin', None)

# def keyHwnd(hwndEx, char):
#     """
#     向指定控件输入值
#     :param hwndEx: 控件句柄
#     :param char: 字符串
#     :return: True or Flase
#     """
#     try:
#         for _ in char:
#             print('key:%s    ascii:%d' % (_, ord(_)))
#             win32api.PostMessage(hwndEx, win32con.WM_CHAR, ord(_), 0)
#             time.sleep(random.uniform(0, 0.2))
#     except Exception as e:
#         print(e)
#         return False
#
#     return True
