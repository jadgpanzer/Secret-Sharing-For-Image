import numpy as np


def share(threshold: int, secret_shares: int, image: np.ndarray):
    """
    将输入的图片拆分为多个秘密份额
    :param threshold: 门限值
    :param secret_shares: 秘密分额数
    :param image: 要拆分的图片
    :return: secret_shares个秘密份额
    """
    height, width = image.shape
    max_index = height * width - 1
    secret_images = np.zeros(shape=(secret_shares,) + image.shape, dtype=np.int64)
    print("height = " + height.__str__() + " width = " + width.__str__())
    print("原始的秘密图片：")
    print(image)
    for i in range(height):
        for j in range(width):
            index = i * width + j
            numbers = np.zeros(threshold, dtype=int)

            for l in range(threshold):
                present_index = index + l
                present_row = present_index // width
                present_column = present_index % width

                if present_index > max_index:
                    numbers[l] = 0
                else:
                    numbers[l] = image[present_row][present_column]

            for x in range(secret_shares):
                secret_value = 0
                for k in range(threshold):
                    secret_value += numbers[k] * pow(x + 1, k, 256)
                secret_images[x][i][j] = secret_value % 256
    for i in range(secret_shares):
        print("秘密份额：" + i.__str__())
        print(secret_images[i])
    return secret_images


def secret_recovery(threshold: int, index: int, secret_images: np.ndarray):
    """
    将传入的多个秘密份额进行恢复
    :param threshold: 门限值
    :param index: 份额的编号（从0开始）
    :param secret_images: 多个秘密份额
    :return: 原图像
    """
    height, width = secret_images[0].shape
    image = np.zeros(shape=(height, width), dtype=np.int64)

    for i in range(height):
        for j in range(width):
            numbers = np.zeros(threshold, dtype=np.int64)

            for k in range(threshold):
                numbers[k] = secret_images[k][i][j]

            # 利用拉格朗日插值法恢复原图像
            interpolated_pixel = 0.0

            for idx in range(threshold):
                numerator = 1
                denominator = 1
                for l in range(threshold):
                    if index[l] != index[idx]:
                        numerator *= 0 - index[l] - 1
                        denominator *= index[l] - index[idx]
                interpolated_pixel += ((numerator / denominator) * numbers[idx])

            image[i][j] = int(interpolated_pixel) % 256
    print("恢复的秘密图片：")
    print(image)
    return image
