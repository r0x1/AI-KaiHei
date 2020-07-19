import torch.backends.cudnn as cudnn

from models.experimental import *
from utils.datasets import *
from utils.utils import *


class ObjectDetection:

    def __init__(self, weights='..\\..\\weights\\brawl_stars_enemy_and_teammate.pt', imgsz=1920, confidence=0.4):
        self.weights = weights
        self.imgsz = imgsz
        self.device_name = ''
        self.confidence = confidence

        # Initialize
        self.device = torch_utils.select_device(self.device_name)
        self.half = self.device.type != 'cpu'  # half precision only supported on CUDA

        # Load model
        self.model = attempt_load(self.weights, map_location=self.device)  # load FP32 model
        self.imgsz = check_img_size(self.imgsz, s=self.model.stride.max())  # check img_size
        if self.half:
            self.model.half()  # to FP16
        pass

        # Get names and colors
        self.names = self.model.module.names if hasattr(self.model, 'module') else self.model.names
        self.colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(self.names))]

        # Run inference
        img = torch.zeros((1, 3, self.imgsz, self.imgsz), device=self.device)  # init img
        _ = self.model(img.half() if self.half else img) if self.device.type != 'cpu' else None  # run once

        pass

    pass

    def detect(self, image_input, draw_box=False):

        # 检测结果列表
        result_list = []

        t0 = time.time()

        # ---------------------开始识别---------------------
        # img0 = cv2.imread('')  # BGR
        # image_input = image_input

        # Padded resize
        img = letterbox(image_input, new_shape=self.imgsz)[0]

        # Convert
        img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
        img = np.ascontiguousarray(img)

        # for path, img, im0s, vid_cap in dataset:

        img = torch.from_numpy(img).to(self.device)
        img = img.half() if self.half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # Inference
        t1 = torch_utils.time_synchronized()
        pred = self.model(img, False)[0]

        # Apply NMS
        pred = non_max_suppression(prediction=pred, conf_thres=self.confidence, iou_thres=0.5,
                                   classes=None, agnostic=False)
        t2 = torch_utils.time_synchronized()

        # Apply Classifier
        # if classify:
        #     pred = apply_classifier(pred, self.modelc, img, im0s)

        # Process detections
        for i, det in enumerate(pred):  # detections per image
            s = ''

            # gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
            if det is not None and len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], image_input.shape).round()

                # Print results
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections per class
                    s += '%g %ss, ' % (n, self.names[int(c)])  # add to string

                # Write results
                for *xyxy, conf, cls in det:
                    # 坐标
                    x1 = int(xyxy[0])
                    y1 = int(xyxy[1])
                    x2 = int(xyxy[2])
                    y2 = int(xyxy[3])
                    # 类别
                    cls_name = self.names[int(cls)]
                    # 置信度
                    conf = round(float(conf), 4)
                    # 保存到list
                    result_list.append((cls_name, conf, x1, y1, x2, y2))

                    # if save_txt:  # Write to file
                    #     xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                    #     with open(txt_path + '.txt', 'a') as f:
                    #         f.write(('%g ' * 5 + '\n') % (cls, *xywh))  # label format

                    # 画框
                    if draw_box:
                        # if save_img or view_img:  # Add bbox to image
                        label = '%s %s' % (cls_name, conf)
                        plot_one_box(xyxy, image_input, label=label, color=self.colors[int(cls)],
                                     line_thickness=3)
                    pass
                pass

            # Print time (inference + NMS)
            # print('%sDone. (%.3fs)' % (s, t2 - t1))
            pass

        # print('Done. (%.3fs)' % (time.time() - t0))
        return result_list, image_input

#
# def draw_one_box(x, img, color=None, label=None, line_thickness=None):
#     # Plots one bounding box on image img
#     tl = line_thickness or round(0.002 * (img.shape[0] + img.shape[1]) / 2) + 1  # line/font thickness
#     color = color or [random.randint(0, 255) for _ in range(3)]
#     c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
#     img = cv2.rectangle(img, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
#     if label:
#         tf = max(tl - 1, 1)  # font thickness
#         t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
#         c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
#         img = cv2.rectangle(img, c1, c2, color, -1, cv2.LINE_AA)  # filled
#         img = cv2.putText(img, label, (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf,
#                           lineType=cv2.LINE_AA)
#     pass
