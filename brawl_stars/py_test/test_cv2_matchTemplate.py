import cv2
import numpy as np


# 在图片中找到按钮，并返回按钮的位置
def _get_button_position(img_gray, template, value_in):
    """
    在图片中找到按钮，并返回按钮的位置
    :param img_gray: 大图
    :param template: 小图
    :param value_in: 阈值
    :return: x,y,w,h
    """
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)

    w, h = template.shape[::-1]
    loc = np.where(res >= value_in)

    for pt in zip(*loc[::-1]):
        # 返回 x,y,w,h
        return pt[0], pt[1], w, h
    return None


def mathc_img(image_in, target_in, value_in):
    img_rgb = cv2.imread(image_in)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(target_in, 0)

    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)

    loc = np.where(res >= value_in)

    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (7, 249, 151), 2)

    img_rgb = cv2.resize(img_rgb, (960, 540))
    cv2.imshow('Detected', img_rgb)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# 图片image_rgb中，是否包含图片template
def is_contained(image_rgb, template, value_in):
    """
    图片image_rgb中，是否包含图片template
    :param image_rgb: 大图
    :param template: 小图
    :param value_in: 阈值
    :return: True / False
    """
    img_gray = cv2.cvtColor(image_rgb, cv2.COLOR_BGR2GRAY)
    res = np.array(cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED))
    if (res >= value_in).max():
        return True
    else:
        return False


if __name__ == "__main__":
    image_path = r"D:\workspace\test_video\game_control\origin\RPReplay_Final1592827562_Moment-3.jpg"
    # image_path = r"D:\workspace\test_video\game_control\origin\RPReplay_Final1592827562_Moment-4.jpg"
    # image_path = r"D:\workspace\test_video\game_control\origin\RPReplay_Final1592827562_Moment-8.jpg"

    # templat_path = r"D:\workspace\AI-KaiHei\brawl_stars\images\continue.jpg"
    # templat_path = r"D:\workspace\AI-KaiHei\brawl_stars\images\exit.jpg"
    templat_path = r"D:\workspace\AI-KaiHei\brawl_stars\images\fight.jpg"

    # 阈值
    value = 0.7

    # 要检测的大图
    image_obj = cv2.imread(image_path)
    img_gray = cv2.cvtColor(image_obj, cv2.COLOR_BGR2GRAY)

    # 要匹配的小图
    # 参数flags=0 : 8位深度，1通道
    template_obj = cv2.imread(templat_path, flags=0)

    print('is contain? ', _get_button_position(img_gray, template_obj, value))

    pass
