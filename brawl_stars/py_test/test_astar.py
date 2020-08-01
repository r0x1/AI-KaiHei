import numpy as np

from brawl_stars import config
from brawl_stars.astar import Astar, resize

if __name__ == "__main__":
    list_obstacle = []

    # 假设 砖块
    cls_name_1 = 'brick'
    conf_1 = 0.7008
    x1_1 = 100
    y1_1 = 200
    x2_1 = 400
    y2_1 = 700
    list_obstacle.append((cls_name_1, conf_1, x1_1, y1_1, x2_1, y2_1))

    # 假设 水
    cls_name_2 = 'water'
    conf_2 = 0.7008
    x1_2 = 700
    y1_2 = 500
    x2_2 = 900
    y2_2 = 1080
    list_obstacle.append((cls_name_2, conf_2, x1_2, y1_2, x2_2, y2_2))

    array_map = np.zeros([1080, 1920], dtype=np.int)

    for (_, _, x1, y1, x2, y2) in list_obstacle:
        # 根据list中的信息，填充障碍物到 array_map
        array_map[y1:y2, x1:x2, ...] = 99
        pass

    resized_cells_array = resize(array_map, [config.screen_row_count, config.screen_column_count])

    list_cells = resized_cells_array.tolist()

    astar = Astar(list_cells)
    result = astar.run([1, 1], [29, 14])

    for (x, y) in result:
        # print(x)
        # print(y)

        resized_cells_array[y, x] = 1

        pass

    print(resized_cells_array)

