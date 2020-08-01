import numpy as np
from enum import Enum


# 方向，参照数字九宫键盘
from brawl_stars import config
from brawl_stars.astar import resize, Astar


class Direction(Enum):
    # 中心
    center = 5
    # 北
    north = 8
    # 南
    south = 2
    # 西
    west = 4
    # 东
    east = 6
    # 西北
    north_west = 7
    # 西南
    south_west = 1
    # 东北
    north_east = 9
    # 东南
    south_east = 3


# 检测到的物体类别
class ObjectType(Enum):
    # 自身
    hero_self = 11
    # 敌人
    enemy = 12
    # 队友
    teammate = 13
    # 补给箱
    supply_box = 14
    # 绿色升级装备
    green_gift = 15
    # 砖块
    brick = 16
    # 墓碑
    tombstone = 17
    # 树桩
    stump = 18
    # 河水
    water = 19
    # 毒雾
    toxic_fog = 20
    # 地图边界
    map_boundary = 21


class BattleThinking:

    def __init__(self):
        # 自身信息
        self._info_hero_self = ()
        self._hero_center_x = 0
        self._hero_center_y = 0

        # 敌人们信息列表
        self._list_enemy = []
        # 队友们信息列表
        self._list_teammate = []
        # 补给箱信息列表
        self._list_supply_box = []
        # 绿色升级装备信息列表
        self._list_green_gift = []
        # 砖块信息列表
        self._list_brick = []
        # 墓碑信息列表
        self._list_tombstone = []
        # 树桩信息列表
        self._list_stump = []
        # 河水信息列表
        self._list_water = []
        # 毒雾信息列表
        self._list_toxic_fog = []
        # 地图边界信息列表
        self._list_map_boundary = []
        # 障碍物
        self._list_obstacle = []

        pass

    def _hero_path_finding(self, target_x, target_y):
        """
        英雄寻路
        :param target_x: 目的地 x
        :param target_y: 目的地 y
        :return: 下一步移动的方向 Direction
        """
        array_map = np.zeros([config.screen_heigh, config.screen_width], dtype=np.int)

        list_obstacle = []
        list_obstacle += self._list_brick
        list_obstacle += self._list_tombstone
        list_obstacle += self._list_stump
        list_obstacle += self._list_water

        # # 假设 砖块
        # cls_name_1 = 'brick'
        # conf_1 = 0.7008
        # x1_1 = 100
        # y1_1 = 200
        # x2_1 = 400
        # y2_1 = 700
        # list_obstacle.append((cls_name_1, conf_1, x1_1, y1_1, x2_1, y2_1))
        #
        # # 假设 水
        # cls_name_2 = 'water'
        # conf_2 = 0.7008
        # x1_2 = 700
        # y1_2 = 500
        # x2_2 = 900
        # y2_2 = 1080
        # list_obstacle.append((cls_name_2, conf_2, x1_2, y1_2, x2_2, y2_2))

        # 根据list中的信息，填充障碍物到 array_map
        for (_, _, x1, y1, x2, y2) in list_obstacle:
            array_map[y1:y2, x1:x2, ...] = 99
            pass

        resized_cells_array = resize(array_map, [config.screen_row_count, config.screen_column_count])

        list_cells = resized_cells_array.tolist()

        astar = Astar(list_cells)

        steps_list = astar.run([self._hero_center_x, self._hero_center_y], [target_x, target_y])

        # 绘制，显示
        # for (x, y) in result:
        #     # print(x)
        #     # print(y)
        #     resized_cells_array[y, x] = 1
        #     pass
        # print(resized_cells_array)

        return steps_list

    # 对物体列表进行分析，返回思考结果
    def process_all(self):

        # 返回结果，移动方向
        result_move_direction = None
        # 返回结果，移动距离，身位
        result_move_distance = None

        # 返回结果，攻击方式，平A/大招/道具
        result_attack_type = None

        # 返回结果，攻击方向
        result_attack_direction = None

        # 由battle_observation 传递来的检测到到物体的 list
        objects_list = []
        # 模拟数据
        cls_name_1 = 'enemy'
        conf_1 = 0.7008
        x1_1 = 1
        y1_1 = 2
        x2_1 = 3
        y2_1 = 4
        objects_list.append((cls_name_1, conf_1, x1_1, y1_1, x2_1, y2_1))

        # 获取所有物体的信息
        for object_one_item in objects_list:
            # 根据类别存入独立的列表，便于分析
            (cls_name, conf, x1, y1, x2, y2) = object_one_item

            if cls_name == ObjectType.hero_self.name:
                self._info_hero_self = object_one_item
                # 英雄位置中心点
                self._hero_center_x = (x2 - x1) * 0.5 + x1
                self._hero_center_y = (y2 - y1) * 0.75 + y1
                pass
            elif cls_name == ObjectType.enemy.name:
                self._list_enemy.append(object_one_item)
                pass
            elif cls_name == ObjectType.teammate.name:
                self._list_teammate.append(object_one_item)
                pass
            elif cls_name == ObjectType.supply_box.name:
                self._list_supply_box.append(object_one_item)
                pass
            elif cls_name == ObjectType.green_gift.name:
                self._list_green_gift.append(object_one_item)
                pass
            # 将4种障碍物合并到一起
            # elif cls_name == ObjectType.brick.name:
            #     self._list_brick.append(object_one_item)
            #     pass
            # elif cls_name == ObjectType.tombstone.name:
            #     self._list_tombstone.append(object_one_item)
            #     pass
            # elif cls_name == ObjectType.stump.name:
            #     self._list_stump.append(object_one_item)
            #     pass
            # elif cls_name == ObjectType.water.name:
            #     self._list_water.append(object_one_item)
            #     pass
            elif cls_name == ObjectType.water.name or \
                    cls_name == ObjectType.brick.name or \
                    cls_name == ObjectType.tombstone.name or \
                    cls_name == ObjectType.stump.name:
                self._list_obstacle.append((cls_name, conf, x1, y1, x2, y2))
                pass
            elif cls_name == ObjectType.toxic_fog.name:
                self._list_toxic_fog.append(object_one_item)
                pass
            elif cls_name == ObjectType.map_boundary.name:
                self._list_map_boundary.append(object_one_item)
                pass
            pass

        count_enemy = len(self._list_enemy)
        count_supply_box = len(self._list_supply_box)
        count_green_gift = len(self._list_green_gift)

        # 如果 视野中 有 enemy、green_gift、supply_box
        if count_enemy > 0:
            # 如果 视野中 包含 enemy，则开始放风筝
            # 保持攻击距离

            # 攻击
            pass
        elif count_green_gift > 0 or count_supply_box > 0:
            # 如果 视野中 没有 enemy，但是有 green_gift、supply_box
            # 判断哪个最近
            # 如果 green_gift 的距离 <= supply_box 的距离，则优先移动到 green_gift 的位置，加装备

            # 获取下一个移动 点
            # _hero_path_finding()

            # 如果 视野中 有箱子 或者 绿色升级装备，则找到最近的，与 其 位置重叠，攻击箱子

            pass
        else:
            # 视野中没有 enemy、green_gift、supply_box，则 向 地图边界 反方向移动，或者随机移动
            # 2、识别墙，记录 地图边界 的大概位置，上下左右。例如：地图 边界 在 右侧。
            # 找到 没有墙 的 方向，向此 方向 移动。
            # 3、识别自身位置。记录、更新自身位置。英雄靠近墙壁的时候，自身位置不是居中的。
            # 4、控制英雄 向 地图边界的 相反方向 移动。本例中，向左移动。向游戏窗口，用windows api输入按键 A。
            result_move_direction = self._process_map_boundary()
            # 返回移动的方向和移动的距离（身位）
            result_move_distance = 2
            pass

        # 返回分析结果

        # ------------------------------------------------------------------------------------

        # 返回分析结果

        # 假设英雄的[最大攻击距离]为450～600个像素点。（用于放风筝）
        #
        # 假设距离敌人的[安全距离]为600个像素点。（用于改变自身英雄行为）

        # 5、多进程控制。一边向左移动（避障），一边识别屏幕中的物体，一边攻击敌人或箱子（如果进入攻击范围）。
        #
        # 6、主要识别11类，例如：自身、(队友)、敌人、箱子、绿色装备、石块、墓碑、树桩、河水、毒雾、地图边界。
        #

        # 8、攻击角度计算 和 攻击范围判定 的 实现方法。
        #
        # （1）以英雄自身坐标原点，向四周扩大范围，形成[120,120,1]矩形的矩阵，以九宫格的形式，分为9块，每1块尺寸[40,40,1]，填充
        # z=1、z=2、z=3 ... 至 z=9的值，得到9个z=1至9的[40,40,1]矩阵。
        #
        # （2）箱子设置为值z=10，箱子矩阵 与 英雄矩阵 叠加，如果矩阵最大值大于10，则表示敌人进入攻击范围。判断1-9块，哪块大于10，哪个方向即为攻击方向。
        #
        # 9、攻击操作
        #
        # （1）如果目标是箱子。计算攻击方向，用windows api向游戏窗口连续输出按键 空格（普攻）。
        #
        # （2）如果目标是敌人。计算攻击方向，用windows api向游戏窗口连续输出按键 R（大招）。
        #
        # 10、箱子打爆之后，掉落绿色装备，向绿色装备移动，得到装备。移动方法同上面的 第7点 寻路方法。
        #
        # 11、[荒野决斗]模式的攻击优先级。
        #
        # （1）战斗时识别：自身、队友、敌人、箱子、绿色装备、石块、墓碑、树桩、河水、毒雾、地图边界。
        #
        # （2）其中，将 石块、墓碑、树桩、河水、毒雾、地图边界，这6种，设为障碍物，在寻路的过程中需要躲避。
        #
        # （3）自身、敌人、箱子、绿色装备，这4种，是战斗行为的主要判断依据。
        #
        # （4）因为是单人模式，队友 保留 暂不使用。
        #
        # （5）当 [敌人距离] > [安全距离]，我方不主动攻击敌人。业务处理优先级：获得绿色装备 > 攻击箱子 > [放风筝]（接近敌人，始终尝试和敌人保持最大攻击距离，并持续攻击敌人）。
        #
        # （6）当 [安全距离] > [敌人距离] > [最大攻击距离]，业务处理优先级：[放风筝] > 获得绿色装备 > 攻击箱子。
        #
        # （7）当 [敌人距离] < [最大攻击距离]，业务处理优先级：[贴身追打]（直到敌人消失、隐藏进草丛、技能飞走、敌人死亡，或者自己战败）
        #
        # （8）当 视野中没有 敌人、箱子、绿色装备，开始[主动寻敌]，由边界向中心，顺时针或逆时针，螺旋形移动寻敌。

        return result_move_direction, result_move_distance, result_attack_direction, result_attack_type

    # 处理 地图边界，如果视野中没有可攻击目标，则向地图边界反方向移动
    def _process_map_boundary(self):
        move_to_north = True
        move_to_south = True
        move_to_west = True
        move_to_east = True

        # 结果
        # flag_direction = None

        for (cls_name, conf, x1, y1, x2, y2) in self._list_map_boundary:

            # 判断 左、右，是否有边界
            if self._hero_center_x > x1:
                # 边界在左侧
                move_to_west = False
                pass
            else:
                # 边界在右侧
                move_to_east = False
                pass

            # 判断 上、下，是否有边界
            if self._hero_center_y > y1:
                # 边界在上方
                move_to_north = False
                pass
            else:
                # 边界在下方
                move_to_south = False
                pass
        pass

        # 只需要有一个方向可通行即可
        if move_to_west:
            # 如果能往左走
            flag_direction = Direction.west
            pass
        elif move_to_south:
            # 如果能往下走
            flag_direction = Direction.south
            pass
        elif move_to_east:
            # 如果能往右走
            flag_direction = Direction.east
            pass
        elif move_to_north:
            # 如果能往北走
            flag_direction = Direction.north
            pass
        else:
            # 如果都不能走，往 west 走
            flag_direction = Direction.west
            pass
        pass

        # 控制英雄
        # hero_movement.move_toward(flag_direction)
        return flag_direction

    # 处理 补给箱子
    def _process_supply_box(self):

        pass
    #
    # # 处理 敌人
    # def _process_enemy(self):
    #     pass
