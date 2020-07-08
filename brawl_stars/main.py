import sys
import os

if __name__ == "__main__":
    curPath = os.path.abspath(os.path.dirname(__file__))
    rootPath = os.path.split(curPath)[0]
    sys.path.append(rootPath)

    from brawl_stars.game_control import GameControlProcess

    # 主程序持续运行标识
    main_active_flag = True

    game_control_process = GameControlProcess()

    while main_active_flag is True:
        print('[1+回车] 启动')
        print('[2+回车] 暂停')
        print('[x+回车] 退出')

        key = input()
        if key is 'x':
            # 退出程序
            # 释放资源
            game_control_process.stop_process()
            main_active_flag = False
            break
        elif key is '2':
            game_control_process.stop_process()
            pass
        elif key is '1':
            # [game_control]：游戏控制，负责调用所有的进程，负责游戏菜单操作，开始战斗，结束战斗等。
            game_control_process.start_process()

            pass

        pass
    pass

    # 结束所有进程
    game_control_process.stop_process()
