import win32api, win32gui, win32con
from time import sleep


def press_key(h_wnd, key_code, sleep_sec=0.2):
    """
    模拟按键
    :param h_wnd: 窗体句柄
    :param key_code: 按键码，在win32con下，比如win32con.VK_F1
    :return:
    """
    win32gui.PostMessage(h_wnd, win32con.WM_KEYDOWN, key_code, 0)
    sleep(sleep_sec)
    win32gui.PostMessage(h_wnd, win32con.WM_KEYUP, key_code, 0)
    sleep(sleep_sec)
