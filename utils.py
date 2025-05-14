import time
import threading
from functools import wraps

import numpy as np
import cv2


def contains_similar_color(image, color, threshold=15):
    diff = image - np.array(color, dtype=np.uint8)
    dist = np.linalg.norm(diff, axis=-1)  # 计算 L2 距离（欧几里得距离）

    return np.any(dist <= threshold)


def show_image(image):
    height, width = image.shape[:2]

    # 网格参数
    grid_rows = 14  # 横向分隔线数量（行数+1）
    grid_cols = 22  # 纵向分隔线数量（列数+1）
    color = (0, 0, 255)  # 网格颜色（BGR格式，绿色）
    thickness = 1  # 线条粗细

    # 计算间隔距离
    horizontal_step = height / grid_rows
    vertical_step = width / grid_cols

    # 绘制横向网格线
    for i in range(1, grid_rows):
        y = int(round(i * horizontal_step))  # 确保坐标为整数
        cv2.line(image, (0, y), (width, y), color, thickness)

    # 绘制纵向网格线
    for i in range(1, grid_cols):
        x = int(round(i * vertical_step))  # 确保坐标为整数
        cv2.line(image, (x, 0), (x, height), color, thickness)

    # 保存结果
    cv2.imwrite('output_with_grid.jpg', image)
    cv2.imshow('Image with Grid', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def add_grid_to_image(img, grid_size_h=75, grid_size_v=75, color=(0, 0, 255), thickness=1):
    # 创建图像副本
    img_with_grid = np.copy(img)

    # 获取图像尺寸
    height, width = img.shape[:2]

    # 绘制水平线
    for y in range(0, height, grid_size_h):
        cv2.line(img_with_grid, (0, y), (width - 1, y), color, thickness)

    # 绘制垂直线
    for x in range(0, width, grid_size_v):
        cv2.line(img_with_grid, (x, 0), (x, height - 1), color, thickness)

    return img_with_grid


def timer(interval=10.0):
    """
    装饰器工厂，返回一个装饰器。
    interval: 报点间隔（秒），默认 10s。
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            t = None  # 将用于保存当前的 Timer 实例

            def report():
                elapsed = time.time() - start_time
                print(f"{func.__name__} 已运行 {elapsed:.2f} 秒…")
                # 打印完再安排下一次
                nonlocal t
                t = threading.Timer(interval, report)
                t.daemon = True
                t.start()

            # 第一次安排在 interval 秒后
            t = threading.Timer(interval, report)
            t.daemon = True
            t.start()

            try:
                return func(*args, **kwargs)
            finally:
                # 函数一返回就取消后续打印
                t.cancel()
                total = time.time() - start_time
                print(f"{func.__name__} 总执行时间：{total:.2f} 秒")

        return wrapper

    return decorator
