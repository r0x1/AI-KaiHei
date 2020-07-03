from brawl_stars.device_control.device import DeviceProcess

if __name__ == "__main__":

    # 主程序持续运行标识
    main_active_flag = True

    # 设备控制进程
    device_process = DeviceProcess()

    # 物体检测进程

    # 流程控制进程

    # 英雄移动进程

    # 英雄攻击进程

    while main_active_flag is True:

        print('[1+回车] 启动')
        print('[2*回车] 暂停')
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
