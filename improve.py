import concurrent.futures
from image_tools import *


def share(threshold: int, secret_shares: int, image: np.ndarray):
    height, width = image.shape
    max_index = height * width - 1
    secret_images = np.zeros(shape=(secret_shares,) + image.shape, dtype=np.int64)
    print("height =", height, "width =", width)
    print("原始的秘密图片：")
    print(image)

    def process_pixel(i, j):
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

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for i in range(height):
            for j in range(width):
                futures.append(executor.submit(process_pixel, i, j))

        for future in concurrent.futures.as_completed(futures):
            pass

    for i in range(secret_shares):
        print("秘密份额：" + i.__str__())
        print(secret_images[i])
    return secret_images


def secret_recovery(threshold: int, index: int, secret_images: np.ndarray):
    height, width = secret_images[0].shape
    image = np.zeros(shape=(height, width), dtype=np.int64)

    def process_pixel(i, j):
        numbers = np.zeros(threshold, dtype=np.int64)

        for k in range(threshold):
            numbers[k] = secret_images[k][i][j]

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

    # 创建一个线程池执行器，用于并发执行像素处理任务
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for i in range(height):
            for j in range(width):
                futures.append(executor.submit(process_pixel, i, j))  # 将像素处理任务添加到 futures 列表中，以便稍后跟踪任务的完成状态
        # 迭代 futures 列表中的完成任务
        for future in concurrent.futures.as_completed(futures):
            pass
    print("恢复的秘密图片：")
    print(image)
    return image


start = time.time()
array = image2array("Origin.png")
result = share(threshold=3, secret_shares=4, image=array)
array2image(image_array=result[0], save_path="00.png", is_save=True)
array2image(image_array=result[1], save_path="11.png", is_save=True)
array2image(image_array=result[2], save_path="22.png", is_save=True)
array2image(image_array=result[3], save_path="33.png", is_save=True)
secret_index = (1, 2, 3)
secret_collection = [result[1], result[2], result[3]]
recovery = secret_recovery(threshold=3, index=secret_index, secret_images=secret_collection)
array2image(image_array=recovery, save_path="recovery.png", is_save=True)
end = time.time()
run_time = end - start
print("并行程序运行了" + run_time.__str__() + " s")
