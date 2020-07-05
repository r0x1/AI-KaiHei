from brawl_stars.device_control.device import DeviceProcess

if __name__ == "__main__":

    # 主程序持续运行标识
    main_active_flag = True

    # 流程控制进程，负责调用所有的进程，进行工作。负责开始游戏，结束游戏等菜单操作。

    # 设备控制进程，负责针对设备的输入和输出，比如：从屏幕输入游戏图像，向键盘输出虚拟键盘按键 等。
    device_process = DeviceProcess()

    # 视觉识别进程，负责检测每一 张/帧 图片的物体位置和类别。

    # 英雄 思考进程，根据视觉识别进程检测到的物体位置和类别，做出相应判断。

    # 英雄 移动进程，根据相应判断，向 [设备进程] 发送键盘 w、a、s、d 消息，再通过模拟器自动转化为游戏中的虚拟键盘，进行 寻路、避障、风筝、贴脸 等位移操作。

    # 英雄 攻击进程，根据相应判断，向 [设备进程] 发送鼠标 按下、拖动、抬起、点击 等消息，进行 对指定角度、指定位置进行攻击，以及施放大招 等攻击操作。

    while main_active_flag is True:

        print('[1+回车] 启动')
        print('[2+回车] 暂停')
        print('[x+回车] 退出')

        key = input()
        if key is 'x':
            # 退出程序
            # 释放资源
            device_process.stop_process()
            main_active_flag = False
            break
        elif key is '2':
            device_process.stop_process()
        elif key is '1':
            device_process.start_process()

        pass
    pass

    # 结束所有进程
    device_process.stop_process()
