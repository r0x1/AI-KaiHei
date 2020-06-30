import multiprocessing

from brawl_stars.device_control import device

if __name__ == "__main__":

    active_flag = True

    # 设备控制进程
    # device_process = multiprocessing.Process(target=device.run, args=(0, 1))
    device_process = multiprocessing.Process(target=device.run)
    device_process.daemon = True
    device_process.start()

    # 物体检测进程

    # 流程控制进程

    # 英雄移动进程

    # 英雄攻击进程

    while active_flag is True:

        print('[1+回车] 启动')
        print('[2*回车] 暂停')
        print('[x+回车] 退出')

        key = input()
        if key is 'x':
            active_flag = False
        else:
            pass
        pass
    pass
