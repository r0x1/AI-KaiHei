# AI-KaiHei
和AI队友开黑，打游戏！

## 简介

项目中文名称：AI开黑

项目英文名称：AI Kai Hei

项目方向：人工智能 游戏队友

短期目标：用 人工智能 玩荒野乱斗 [双人荒野决斗] 模式 和 自己开黑

## 工作目录

> 在 brawl_stars 目录中


## 运行环境

- windows10，网易MuMu模拟器

- 下载安装 python 3.7.7：```https://www.python.org/ftp/python/3.7.7/python-3.7.7-amd64.exe```

- 终端安装 pip 20.1.1：```$ python -m pip install --upgrade pip```

- 下载安装 cuda 10.1：```https://developer.nvidia.com/compute/cuda/10.1/Prod/local_installers/cuda_10.1.105_418.96_win10.exe```

- 终端安装 pytorch 1.5.1：```$ pip install torch==1.5.1+cu101 torchvision==0.6.1+cu101 -f https://download.pytorch.org/whl/torch_stable.html```

- 终端安装 依赖软件包：```$ pip install -r requirements.txt```

- 运行程序：```$ python ./brawl_stars/main.py```


## 功能模块

- [game_control]：游戏控制，负责调用所有的进程，负责游戏菜单操作，开始战斗，结束战斗等。

- [battle_observation]：战斗观察，负责从屏幕"截取图片"、调用[object_detection]、[battle_thinking]、[hero_movement]、[hero_attack]。

- [object_detection]：物体检测，负责调用yolo5检测图片中的物体。

- [battle_thinking]：战斗思考，负责分析物体信息，调用[hero_movement]、[hero_attack]

- [hero_movement]：英雄移动，控制英雄持续性的走位，即使没有任何指令，也要一直移动，保持apm节奏。

- [hero_attack]：英雄攻击，控制英雄持续性的攻击，即使没有任何指令，也要一直调整攻击方向，保持apm节奏。

- [device_control]：设备控制，负责向模拟器发送消息，用于模拟键盘输入、模拟鼠标输入。


## 整体流程

- 启动[game_control]进程：负责调用所有的进程，进行工作。负责开始游戏，结束游戏等菜单操作。

- 由[game_control]进程，启动[battle_observation]进程，

- [battle_observation]进程，循环读取游戏图片，

- [battle_observation]进程，调用[物体检测]功能，对图片进行检测，返回物体信息list，

- [battle_observation]进程，调用[战斗思考]功能，对物体信息list进行分析，

- [battle_observation]进程，启动[hero_movement]进程，由[hero_movement]进程，调用[device_control]功能，实现移动功能。

- [battle_observation]进程，启动[hero_attack]进程，由[hero_attack]进程，调用[device_control]功能，实现攻击功能。


## 移动和攻击举例 

- 荒野乱斗 - [单人荒野决斗] 模式的移动、攻击的流程及实现方式

- 本例中，使用英雄 雪莉。
- 攻击模式比较简单，只有弹道方向，没有子弹落点。
- 假设英雄的[最大攻击距离]为450～600个像素点。（用于放风筝）
- 假设距离敌人的[安全距离]为600个像素点。（用于改变自身英雄行为）

- [ ] 1、开局前不能动，开局后能看到墙。确定已经开局后，才开始视觉识别。
- [ ] 2、识别墙，记录 地图边界 的大概位置，上下左右。例如：地图 边界 在 右侧。
- [ ] 3、识别自身位置。记录、更新自身位置。英雄靠近墙壁的时候，自身位置不是居中的。
- [ ] 4、控制英雄 向 地图边界的 相反方向 移动。本例中，向左移动。向游戏窗口，用windows api输入按键 W。
- [ ] 5、多进程控制。一边向左移动（避障），一边识别屏幕中的物体，一边攻击敌人或箱子（如果进入攻击范围）。
- [ ] 6、主要识别11类，例如：自身、(队友)、敌人、箱子、绿色装备、石块、墓碑、树桩、河水、毒雾、地图边界。

- [ ] 7、向攻击目标移动的寻路。
- [ ] （1）屏幕图片为[x,y,z]，[1080,1920,1]，本例中，矩阵计算，英雄自身设置为值z=20，箱子设置为值z=30，障碍物设置为z=0，其余区域（地面、草地）设置为z=1，不看z=0的部分，得到矩阵中只有 z=1、z=20、z=30。 凡是z>=1 的区域，都是可以通行的路径，从这个区域，由 z=20的 区域 逐步到达 z=30 的区域。 
- [ ] （2）以数字小键盘为例，计算方位。假设 箱子 在方位1，即 左下角，则优先根据z=1和z=20矩阵，向左下角移动，如遇障碍，优先向左下移动，直至到达z=30。
- [ ] （3）本例中，为了向方位1移动，英雄移动方向的优先级为：1>2>4>3>7>8>6>9。

- [ ] 8、攻击角度计算 和 攻击范围判定 的 实现方法。
- [ ] （1）以英雄自身坐标原点，向四周扩大范围，形成[120,120,1]矩形的矩阵，以九宫格的形式，分为9块，每1块尺寸[40,40,1]，填充 z=1、z=2、z=3 ... 至 z=9的值，得到9个z=1至9的[40,40,1]矩阵。
- [ ] （2）箱子设置为值z=10，箱子矩阵 与 英雄矩阵 叠加，如果矩阵最大值大于10，则表示敌人进入攻击范围。判断1-9块，哪块大于10，哪个方向即为攻击方向。

- [ ] 9、攻击操作
- [ ] （1）如果目标是箱子。计算攻击方向，用windows api向游戏窗口连续输出按键 空格（普攻）。
- [ ] （2）如果目标是敌人。计算攻击方向，用windows api向游戏窗口连续输出按键 R（大招）。

- [ ] 10、箱子打爆之后，掉落绿色装备，向绿色装备移动，得到装备。移动方法同上面的 第7点 寻路方法。

- [ ] 11、[荒野决斗]模式的攻击优先级。
- [ ] （1）战斗时识别：自身、队友、敌人、箱子、绿色装备、石块、墓碑、树桩、河水、毒雾、地图边界。
- [ ] （2）其中，将 石块、墓碑、树桩、河水、毒雾、地图边界，这6种，设为障碍物，在寻路的过程中需要躲避。
- [ ] （3）自身、敌人、箱子、绿色装备，这4种，是战斗行为的主要判断依据。
- [ ] （4）因为是单人模式，队友 保留 暂不使用。
- [ ] （5）当 [敌人距离] > [安全距离]，我方不主动攻击敌人。业务处理优先级：获得绿色装备 > 攻击箱子 > [放风筝]（接近敌人，始终尝试和敌人保持最大攻击距离，并持续攻击敌人）。
- [ ] （6）当 [安全距离] > [敌人距离] > [最大攻击距离]，业务处理优先级：[放风筝] > 获得绿色装备 > 攻击箱子。
- [ ] （7）当 [敌人距离] < [最大攻击距离]，业务处理优先级：[贴身追打]（直到敌人消失、隐藏进草丛、技能飞走、敌人死亡，或者自己战败）
- [ ] （8）当 视野中没有 敌人、箱子、绿色装备，开始[主动寻敌]，由边界向中心，顺时针或逆时针，螺旋形移动寻敌。

## 战斗中 实时目标检测 数据集采集和样本标注

- [ ] 1、荒野乱斗游戏 确定有哪些检测的物体类别。例如 对手、队友、自己、墙壁、草地、栅栏、墓碑、箱子 等

- [ ] 2、荒野乱斗游戏 定义有效样本。例如 如何让 卷机神经网络 采集到 对手的某个特征，标注的时候应该标注哪些区域，不应标注哪些区域

- [ ] 3、荒野乱斗游戏 样本采集。例如 玩游戏，录视频，转图片，挑取包含有效样本的图片，待用。

- [ ] 4、荒野乱斗游戏 样本标注，形成训练数据集。

举例

- [ ] （1）用 labelImg 手工标注图片。

- [ ] （2）上传至 roboflow.ai导出yolo v5的数据集。

- [ ] （3）配合 训练卷积神经网络 对 样本标注 进行返工，手工标注图片。

- [ ] （4）日后，如果训练成功，用 卷积神经网络 识别出的图片，再生成更多的数据集。

## 战斗中 实时目标检测 训练卷积神经网络

- [ ] 选择 一种或多种 适合的 卷积神经网络。例如 yolo v5，试验yolo v5自带各种网络的差异性。

- [ ] 循环截取 android 模拟器的图像，传递给 yolo v5 供图像检测使用。

- [ ] 使用 google colab 对标注完的样本 进行训练。试验 定义的样本是否有效（能否检测得到）

- [ ] 如果 训练失败，找出原因，配合 数据集采集和样本标注 对 样本标注 进行返工。

- [ ] 如果 训练成功，继续训练下一个目标检测。

## 未来

- [ ] 2个AI队友开黑，共享视野，玩荒野乱斗游戏。
