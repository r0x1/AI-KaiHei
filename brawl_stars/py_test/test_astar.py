import numpy as np

from brawl_stars.astar import Astar

if __name__ == "__main__":
    list_obstacle = []

    cls_name_1 = 'enemy'
    conf_1 = 0.7008
    x1_1 = 1
    y1_1 = 2
    x2_1 = 3
    y2_1 = 4
    list_obstacle.append((cls_name_1, conf_1, x1_1, y1_1, x2_1, y2_1))

    array_map = np.zeros([1080, 1920], dtype=np.int)

    for (_, _, x1, y1, x2, y2) in list_obstacle:
        # 根据list中的信息，填充障碍物到 array_map
        array_map[y1:y2, x1:x2, ...] = 5
        pass

    mat = array_map.tolist()

    # mat = [
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    # ]

    astar = Astar(mat)
    result = astar.run([0, 0], [10, 9])
    print(result)
