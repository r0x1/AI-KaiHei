import numpy as np
from enum import Enum

from brawl_stars import config
from brawl_stars.astar import resize, Astar


# 方向，参照数字九宫键盘
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


# 平A/大招/道具
class AttackType(Enum):
    # 普通攻击
    normal_attack = 51
    # 技能攻击
    skills_attack = 52
    # 道具攻击
    items_attack = 53


class BattleThinking:

    def __init__(self):
        # 自身信息
        # self._info_hero_self = ()
        self._hero_center_x = None
        self._hero_center_y = None

        # 敌人们信息列表
        self._list_enemy = []
        # 队友们信息列表
        self._list_teammate = []
        # 补给箱信息列表
        self._list_supply_box = []
        # 绿色升级装备信息列表
        self._list_green_gift = []
        # # 砖块信息列表
        # self._list_brick = []
        # # 墓碑信息列表
        # self._list_tombstone = []
        # # 树桩信息列表
        # self._list_stump = []
        # # 河水信息列表
        # self._list_water = []
        # 毒雾信息列表
        self._list_toxic_fog = []
        # 地图边界信息列表
        self._list_map_boundary = []
        # 障碍物
        self._list_obstacle = []

        pass

    # 计算2点之间的欧氏距离
    def __distance(self, x1, y1, x2, y2):
        return np.sqrt(np.square(x2 - x1) + np.square(y2 - y1))

    # 获取矩形的中心点
    def __center(self, x1, y1, x2, y2):
        return (x2 - x1) / 2 + x1, (y2 - y1) / 2 + y1

    # 以x1, y1为原点，返回x2 ,y2的方向
    def __direction(self, x1=0, y1=0, x2=0, y2=0):
        """
        以x1, y1为原点，计算x2 ,y2的方向
        :param x1: 原点x
        :param y1: 原点y
        :param x2: 目标点x
        :param y2: 目标点y
        :return: Direction 枚举方向
        """
        result_direction = None
        """
        以x1, y1为原点，返回x2 ,y2的方向
        :param x1:
        :param y1:
        :param x2:
        :param y2:
        :return: Direction(Enum)
        """
        if x2 == x1:
            if y2 == y1:
                result_direction = Direction.center
            elif y2 > y1:
                result_direction = Direction.south
            elif y2 < y1:
                result_direction = Direction.north
            pass
        elif x2 > x1:
            if y2 == y1:
                result_direction = Direction.east
            elif y2 > y1:
                result_direction = Direction.south_east
            elif y2 < y1:
                result_direction = Direction.north_east
            pass
        elif x2 < x1:
            if y2 == y1:
                result_direction = Direction.west
            elif y2 > y1:
                result_direction = Direction.south_west
            elif y2 < y1:
                result_direction = Direction.north_west
            pass
        return result_direction

    def __hero_path_finding(self, target_x, target_y):
        """
        英雄寻路
        :param target_x: 目的地 x
        :param target_y: 目的地 y
        :return: list[x, y] 移动方向坐标 x,y 列表
        """
        array_map = np.zeros([config.screen_heigh, config.screen_width], dtype=np.int)

        # list_obstacle = []
        # list_obstacle += self._list_brick
        # list_obstacle += self._list_tombstone
        # list_obstacle += self._list_stump
        # list_obstacle += self._list_water

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
        for (_, _, x1, y1, x2, y2) in self._list_obstacle:
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

    # 处理 地图边界，如果视野中没有可攻击目标，则向地图边界反方向移动
    def __process_map_boundary(self):
        """
        处理 地图边界，如果视野中没有可攻击目标，则向地图边界反方向移动
        :return: 移动方向, 移动距离
        """
        move_to_north = True
        move_to_south = True
        move_to_west = True
        move_to_east = True

        # 移动方向
        result_move_direction = None

        # 移动距离
        result_move_distance = 2

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
            result_move_direction = Direction.west
            pass
        elif move_to_south:
            # 如果能往下走
            result_move_direction = Direction.south
            pass
        elif move_to_east:
            # 如果能往右走
            result_move_direction = Direction.east
            pass
        elif move_to_north:
            # 如果能往北走
            result_move_direction = Direction.north
            pass
        else:
            # 如果都不能走，往 west 走
            result_move_direction = Direction.west
            pass
        pass

        return result_move_direction, result_move_distance

    # 处理 敌人
    def __process_enemy(self):
        """
        处理 敌人
        :return: 移动方向, 移动距离, 攻击方向, 攻击类型
        """
        # 返回结果，移动方向
        result_move_direction = None
        # 返回结果，移动距离，身位
        result_move_distance = None
        # 返回结果，攻击方式，平A/大招/道具
        result_attack_type = None
        # 返回结果，攻击方向
        result_attack_direction = None

        # 目标类别
        target_type = None
        # 目标距离
        target_distance = None
        # 目标位置
        target_x = None
        target_y = None

        # 如果 视野中 包含 enemy，则开始放风筝
        # 计算欧氏距离
        for (cls_name_enemy, _, x1_enemy, y1_enemy, x2_enemy, y2_enemy) in self._list_green_gift:
            enemy_center_x, enemy_center_y = self.__center(x1_enemy, y1_enemy, x2_enemy, y2_enemy)
            distance_enemy = self.__distance(self._hero_center_x, self._hero_center_x,
                                             enemy_center_x, enemy_center_y)
            # 如果距离近，则替换移动目标的位置
            if target_distance is None or distance_enemy < target_distance:
                target_type = cls_name_enemy
                target_distance = distance_enemy
                target_x = enemy_center_x
                target_y = enemy_center_y
            pass
        pass

        # 判断是否进入射程
        if target_distance <= config.hero_maximum_effective_range:
            # 判断攻击角度，攻击
            result_attack_direction = self.__direction(self._hero_center_x, self._hero_center_y,
                                                       target_x, target_y)
            # 攻击类型，优先技能攻击，如果技能cd中，则自动普通攻击
            result_attack_type = AttackType.skills_attack
        pass

        # a star 寻路，找到将要移动到的 x, y 位置
        (x, y) = self.__hero_path_finding(target_x=target_x, target_y=target_y)[0]
        # 移动方向
        # move_direction_temp = Direction.center
        move_direction_temp = self.__direction(self._hero_center_x, self._hero_center_y, x, y)

        # 判断距离，如果小于安全距离，则向反方向移动
        if target_distance < config.hero_safe_distance:
            # 获取反方向
            result_move_direction = 10 - Direction[move_direction_temp.name].value
            # 撤退，跑快点儿
            result_move_distance = 2
        else:
            # 如果大于安全距离，则向目标移动
            result_move_direction = move_direction_temp
            # 进攻，跑慢点儿
            result_move_distance = 1

        return result_move_direction, result_move_distance, result_attack_direction, result_attack_type

    # 处理 补给箱子 和 绿色装备
    def __process_supply_box_and_green_gift(self):
        """
        处理 补给箱子 和 绿色装备
        :return: 移动方向, 移动距离, 攻击方向, 攻击类型
        """
        # 返回结果，移动方向
        result_move_direction = None
        # 返回结果，移动距离，身位
        result_move_distance = None

        # 返回结果，攻击方式，平A/大招/道具
        result_attack_type = None

        # 返回结果，攻击方向
        result_attack_direction = None

        # 如果 视野中 没有 enemy，但是有 green_gift、supply_box
        # 判断哪个最近
        # 如果 green_gift 的距离 <= supply_box 的距离，则优先移动到 green_gift 的位置，加装备

        # 目标类别
        target_type = None
        # 目标距离
        target_distance = None
        # 目标位置
        target_x = None
        target_y = None

        # 计算欧氏距离
        for (cls_name_gg, _, x1_gg, y1_gg, x2_gg, y2_gg) in self._list_green_gift:
            gg_center_x, gg_center_y = self.__center(x1_gg, y1_gg, x2_gg, y2_gg)
            distance_gg = self.__distance(self._hero_center_x, self._hero_center_x, gg_center_x, gg_center_y)
            # 如果距离近，则替换移动目标的位置
            if target_distance is None or distance_gg < target_distance:
                target_type = cls_name_gg
                target_distance = distance_gg
                target_x = gg_center_x
                target_y = gg_center_y
            pass
        pass

        for (cls_name_sb, _, x1_sb, y1_sb, x2_sb, y2_sb) in self._list_supply_box:
            sb_center_x, sb_center_y = self.__center(x1_sb, y1_sb, x2_sb, y2_sb)
            distance_sb = self.__distance(self._hero_center_x, self._hero_center_x, sb_center_x, sb_center_y)
            # 如果距离近，则替换移动目标的位置
            if target_distance is None or distance_sb < target_distance:
                target_type = cls_name_sb
                target_distance = distance_sb
                target_x = sb_center_x
                target_y = sb_center_y
            pass
        pass

        # 如果目标是绿色装备，不需要攻击
        if target_type == ObjectType.green_gift:
            # a star 寻路，找到将要移动到的 x, y 位置
            (x, y) = self.__hero_path_finding(target_x=target_x, target_y=target_y)[0]
            # 移动方向
            result_move_direction = self.__direction(self._hero_center_x, self._hero_center_y, x, y)
            # 移动距离
            result_move_distance = 2
            pass
        elif target_type == ObjectType.supply_box:
            # 如果目标是补给箱，需要攻击
            # 判断距离
            if target_distance < 20:
                # 如果距离小于20像素，则不动
                result_move_direction = Direction.center
                result_move_distance = 0
            else:
                # 如果距离大于等于20像素，则向目标移动
                # a star 寻路，找到将要移动到的 x, y 位置
                (x, y) = self.__hero_path_finding(target_x=target_x, target_y=target_y)[0]
                # 移动方向
                result_move_direction = self.__direction(self._hero_center_x, self._hero_center_y, x, y)
                # 移动距离
                result_move_distance = 2
            pass

            # 判断是否进入射程
            if target_distance <= config.hero_maximum_effective_range:
                # 判断攻击角度，攻击
                result_attack_direction = self.__direction(self._hero_center_x, self._hero_center_y,
                                                           target_x, target_y)
                # 攻击类型，普通攻击
                result_attack_type = AttackType.normal_attack
            pass
        pass

        return result_move_direction, result_move_distance, result_attack_direction, result_attack_type

    # 清理数据
    def clear_data(self):
        """
        清理数据
        :return:
        """
        # 自身信息
        # self._info_hero_self = ()
        self._hero_center_x = None
        self._hero_center_y = None

        # 障碍物
        self._list_obstacle.clear()
        # 敌人们信息列表
        self._list_enemy.clear()
        # 队友们信息列表
        self._list_teammate.clear()
        # 补给箱信息列表
        self._list_supply_box.clear()
        # 绿色升级装备信息列表
        self._list_green_gift.clear()
        # # 砖块信息列表
        # self._list_brick.clear()
        # # 墓碑信息列表
        # self._list_tombstone.clear()
        # # 树桩信息列表
        # self._list_stump.clear()
        # # 河水信息列表
        # self._list_water.clear()
        # 毒雾信息列表
        self._list_toxic_fog.clear()
        # 地图边界信息列表
        self._list_map_boundary.clear()

    # 对物体列表进行分析，返回思考结果
    def process_all(self, objects_list):
        """
        对物体列表进行分析，返回思考结果
        :return: 移动方向, 移动距离, 攻击方向, 攻击类型
        """
        # 返回结果，移动方向
        result_move_direction = None
        # 返回结果，移动距离，身位
        result_move_distance = None

        # 返回结果，攻击方式，平A/大招/道具
        result_attack_type = None

        # 返回结果，攻击方向
        result_attack_direction = None

        # # 由battle_observation 传递来的检测到到物体的 list
        # objects_list = []
        # # 模拟数据
        # cls_name_1 = 'enemy'
        # conf_1 = 0.7008
        # x1_1 = 1
        # y1_1 = 2
        # x2_1 = 3
        # y2_1 = 4
        # objects_list.append((cls_name_1, conf_1, x1_1, y1_1, x2_1, y2_1))

        # 获取所有物体的信息
        for object_one_item in objects_list:
            # 根据类别存入独立的列表，便于分析
            (cls_name, conf, x1, y1, x2, y2) = object_one_item

            if cls_name == ObjectType.hero_self.name:
                # self._info_hero_self = object_one_item
                # 英雄位置中心点
                self._hero_center_x = int((x2 - x1) * 0.5 + x1)
                self._hero_center_y = int((y2 - y1) * 0.75 + y1)
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
            # 将4种障碍物合并到一起
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

        # 如果英雄坐标不为None时，开始移动和攻击
        if self._hero_center_x is not None and self._hero_center_y is not None:
            count_enemy = len(self._list_enemy)
            count_supply_box = len(self._list_supply_box)
            count_green_gift = len(self._list_green_gift)

            # 如果 视野中 有 enemy，则优先处理 enemy
            if count_enemy > 0:
                (result_move_direction, result_move_distance, result_attack_direction, result_attack_type) = \
                    self.__process_enemy()
                pass
            elif count_green_gift > 0 or count_supply_box > 0:
                # 在视野中没有 enemy 时，如果有 green_gift 或 supply_box
                (result_move_direction, result_move_distance, result_attack_direction, result_attack_type) = \
                    self.__process_supply_box_and_green_gift()
                pass
            else:
                # 视野中没有 enemy、green_gift、supply_box，则 向 地图边界 反方向移动，或者随机移动
                result_move_direction, result_move_distance = self.__process_map_boundary()
            pass
        pass

        return result_move_direction, result_move_distance, result_attack_direction, result_attack_type
    pass
