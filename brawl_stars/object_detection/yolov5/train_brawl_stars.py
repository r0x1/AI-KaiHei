import torch
import yaml

# clear_output()
print('Setup complete. Using torch %s %s' % (
    torch.__version__, torch.cuda.get_device_properties(0) if torch.cuda.is_available() else 'CPU'))
# print(torch.cuda.current_device())

# define number of classes based on YAML
with open("./content/data.yaml", 'r') as stream:
    num_classes = str(yaml.safe_load(stream)['nc'])
    pass
pass

# % cd / content /
# write custom model .yaml
# you can configure this based on other YOLOv5 models in the models directory
with open('./models/air_force_r_yolov5s.yaml', 'w') as f:
    # parameters
    f.write('nc: ' + num_classes + '\n')
    # f.write('nc: ' + str(len(class_labels)) + '\n')
    f.write('depth_multiple: 0.33' + '\n')  # model depth multiple
    f.write('width_multiple: 0.50' + '\n')  # layer channel multiple
    f.write('\n')
    f.write('anchors:' + '\n')
    f.write('  - [10,13, 16,30, 33,23] ' + '\n')
    f.write('  - [30,61, 62,45, 59,119]' + '\n')
    f.write('  - [116,90, 156,198, 373,326] ' + '\n')
    f.write('\n')

    f.write('backbone:' + '\n')
    f.write('  [[-1, 1, Focus, [64, 3]],' + '\n')
    f.write('   [-1, 1, Conv, [128, 3, 2]],' + '\n')
    f.write('   [-1, 3, Bottleneck, [128]],' + '\n')
    f.write('   [-1, 1, Conv, [256, 3, 2]],' + '\n')
    f.write('   [-1, 9, BottleneckCSP, [256]],' + '\n')
    f.write('   [-1, 1, Conv, [512, 3, 2]], ' + '\n')
    f.write('   [-1, 9, BottleneckCSP, [512]],' + '\n')
    f.write('   [-1, 1, Conv, [1024, 3, 2]],' + '\n')
    f.write('   [-1, 1, SPP, [1024, [5, 9, 13]]],' + '\n')
    f.write('   [-1, 6, BottleneckCSP, [1024]],' + '\n')
    f.write('  ]' + '\n')
    f.write('\n')

    f.write('head:' + '\n')
    f.write('  [[-1, 3, BottleneckCSP, [1024, False]],' + '\n')
    f.write('   [-1, 1, nn.Conv2d, [na * (nc + 5), 1, 1, 0]],' + '\n')
    f.write('   [-2, 1, nn.Upsample, [None, 2, "nearest"]],' + '\n')

    f.write('   [[-1, 6], 1, Concat, [1]],' + '\n')
    f.write('   [-1, 1, Conv, [512, 1, 1]],' + '\n')
    f.write('   [-1, 3, BottleneckCSP, [512, False]],' + '\n')
    f.write('   [-1, 1, nn.Conv2d, [na * (nc + 5), 1, 1, 0]],' + '\n')

    f.write('   [-2, 1, nn.Upsample, [None, 2, "nearest"]],' + '\n')
    f.write('   [[-1, 4], 1, Concat, [1]],' + '\n')
    f.write('   [-1, 1, Conv, [256, 1, 1]],' + '\n')
    f.write('   [-1, 3, BottleneckCSP, [256, False]],' + '\n')
    f.write('   [-1, 1, nn.Conv2d, [na * (nc + 5), 1, 1, 0]],' + '\n')
    f.write('\n')
    f.write('   [[], 1, Detect, [nc, anchors]],' + '\n')
    f.write('  ]' + '\n')

print('custom model config written!')

# cd /content/yolov5/
# python train.py --img 416 --batch 16 --epochs 100 --data '../data.yaml' --cfg ./models/brawl_starts.yaml --weights '' --name yolov5s_results --nosave --cache
pass
