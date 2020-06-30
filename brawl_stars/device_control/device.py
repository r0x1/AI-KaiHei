# 对后台窗口截图
import win32gui, win32ui, win32con
from ctypes import windll
from PIL import Image
import cv2
import numpy


def run():
    # 获取后台窗口的句柄，注意后台窗口不能最小化
    hWnd = win32gui.FindWindow("Qt5QWindowIcon", "荒野乱斗 - MuMu模拟器")  # 窗口的类名可以用Visual Studio的SPY++工具获取
    # 获取句柄窗口的大小信息
    left, top, right, bot = win32gui.GetWindowRect(hWnd)
    width = right - left
    height = bot - top
    # 返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
    hWndDC = win32gui.GetWindowDC(hWnd)
    # 创建设备描述表
    mfcDC = win32ui.CreateDCFromHandle(hWndDC)
    # 创建内存设备描述表
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建位图对象准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 为bitmap开辟存储空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)

    # 循环截图
    loop(saveDC, saveBitMap, width, height, mfcDC)

    pass


def loop(saveDC, saveBitMap, width, height, mfcDC):
    while True:
        # 将截图保存到saveBitMap中
        saveDC.SelectObject(saveBitMap)
        # 保存bitmap到内存设备描述表
        saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)

        signedIntsArray = saveBitMap.GetBitmapBits(True)
        img = numpy.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (height, width, 4)

        # 显示
        cv2.imshow('image', img)  # 第一个参数是窗口名称，是字符串。第二个参数是我们的图片
        cv2.waitKey(1)  # 0 表示程序会无限制的等待用户的按键事件

    pass


def capture_window_image2():
    # 获取后台窗口的句柄，注意后台窗口不能最小化
    hWnd = win32gui.FindWindow("Qt5QWindowIcon", "荒野乱斗 - MuMu模拟器")  # 窗口的类名可以用Visual Studio的SPY++工具获取
    # 获取句柄窗口的大小信息
    left, top, right, bot = win32gui.GetWindowRect(hWnd)
    width = right - left
    height = bot - top
    # 返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
    hWndDC = win32gui.GetWindowDC(hWnd)
    # 创建设备描述表
    mfcDC = win32ui.CreateDCFromHandle(hWndDC)
    # 创建内存设备描述表
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建位图对象准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 为bitmap开辟存储空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
    # 将截图保存到saveBitMap中
    saveDC.SelectObject(saveBitMap)
    # 保存bitmap到内存设备描述表
    saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)

    signedIntsArray = saveBitMap.GetBitmapBits(True)
    img = numpy.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (height, width, 4)

    # 显示
    cv2.imshow('image', img)  # 第一个参数是窗口名称，是字符串。第二个参数是我们的图片
    cv2.waitKey(1)  # 表示程序会无限制的等待用户的按键事件
    # cv2.destroyAllWindows()

    mfcDC.DeleteDC()
    saveDC.DeleteDC()
    win32gui.ReleaseDC(hWnd, hWndDC)
    win32gui.DeleteObject(saveBitMap.GetHandle())

    # 如果要截图到打印设备：
    # 最后一个int参数：0-保存整个窗口，1-只保存客户区。如果PrintWindow成功函数返回值为1
    # result = windll.user32.PrintWindow(hWnd, saveDC.GetSafeHdc(), 0)
    # print(result)  # PrintWindow成功则输出1

    # 保存图像
    # 方法一：windows api保存
    # 保存bitmap到文件
    # saveBitMap.SaveBitmapFile(saveDC, ".\\img_Winapi.bmp")


def save_window_image1():
    # 获取后台窗口的句柄，注意后台窗口不能最小化
    hWnd = win32gui.FindWindow("Qt5QWindowIcon", "荒野乱斗 - MuMu模拟器")  # 窗口的类名可以用Visual Studio的SPY++工具获取
    # 获取句柄窗口的大小信息
    left, top, right, bot = win32gui.GetWindowRect(hWnd)
    width = right - left
    height = bot - top
    # 返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
    hWndDC = win32gui.GetWindowDC(hWnd)
    # 创建设备描述表
    mfcDC = win32ui.CreateDCFromHandle(hWndDC)
    # 创建内存设备描述表
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建位图对象准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 为bitmap开辟存储空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
    # 将截图保存到saveBitMap中
    saveDC.SelectObject(saveBitMap)
    # 保存bitmap到内存设备描述表
    saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)

    # 如果要截图到打印设备：
    # 最后一个int参数：0-保存整个窗口，1-只保存客户区。如果PrintWindow成功函数返回值为1
    result = windll.user32.PrintWindow(hWnd, saveDC.GetSafeHdc(), 0)
    print(result)  # PrintWindow成功则输出1

    # 保存图像
    # 方法一：windows api保存
    # 保存bitmap到文件
    saveBitMap.SaveBitmapFile(saveDC, ".\\img_Winapi.bmp")


def loop_hwnd():
    hwnd_title = dict()

    def get_all_hwnd(hwnd, mouse):
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
            hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})

    win32gui.EnumWindows(get_all_hwnd, 0)

    for h, t in hwnd_title.items():
        if t is not "":
            print(h, t)
    pass
