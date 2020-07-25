import numpy as np
from past.builtins import xrange

from brawl_stars import config
from brawl_stars.astar import Astar


def resize(array_in, shape=None):
    if shape is None:
        return array_in
    m, n = shape
    Y = np.zeros((m, n), dtype=type(array_in[0, 0]))
    k = len(array_in)
    p, q = k / m, k / n
    for i in xrange(m):
        Y[i, :] = array_in[np.int_(i * p), np.int_(np.arange(n) * q)]
    return Y


if __name__ == "__main__":
    list_obstacle = []

    # 假设 砖块
    cls_name_1 = 'brick'
    conf_1 = 0.7008
    x1_1 = 100
    y1_1 = 200
    x2_1 = 500
    y2_1 = 700
    list_obstacle.append((cls_name_1, conf_1, x1_1, y1_1, x2_1, y2_1))

    array_map = np.zeros([1080, 1920], dtype=np.int)

    for (_, _, x1, y1, x2, y2) in list_obstacle:
        # 根据list中的信息，填充障碍物到 array_map
        array_map[y1:y2, x1:x2, ...] = 5
        pass

    resized_cells_array = resize(array_map, [config.screen_row_count, config.screen_column_count])

    list_cells = resized_cells_array.tolist()

    astar = Astar(list_cells)
    result = astar.run([1, 1], [29, 15])
    print(result)

