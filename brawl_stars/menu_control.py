import random
from time import sleep

import win32con
import win32gui

# 继续、退出、对战，这3个按钮的中心点一致，可以只设置一个 数字1 的虚拟按钮，都可以点击到
# '1':0x31, '2':0x32, '3':0x33

def click_fight_button(h_wnd):
    randow_sleep = random.uniform(0.509, 0.905)
    win32gui.PostMessage(h_wnd, win32con.WM_KEYDOWN, 0x31, 0)
    sleep(randow_sleep)
    win32gui.PostMessage(h_wnd, win32con.WM_KEYUP, 0x31, 0)
    sleep(randow_sleep)

def click_continue_button(h_wnd):
    randow_sleep = random.uniform(0.509, 0.905)
    win32gui.PostMessage(h_wnd, win32con.WM_KEYDOWN, 0x31, 0)
    sleep(randow_sleep)
    win32gui.PostMessage(h_wnd, win32con.WM_KEYUP, 0x31, 0)
    sleep(randow_sleep)

def click_exit_button(h_wnd):
    randow_sleep = random.uniform(0.509, 0.905)
    win32gui.PostMessage(h_wnd, win32con.WM_KEYDOWN, 0x31, 0)
    sleep(randow_sleep)
    win32gui.PostMessage(h_wnd, win32con.WM_KEYUP, 0x31, 0)
    sleep(randow_sleep)
