from PIL import Image
import numpy as np
from image_tools import *
from secret_sharing import *

start = time.time()
array = image2array("Origin.png",mode="L")
result = share(threshold=3, secret_shares=4, image=array)
# 将产生的多个图片保存下来
array2image(image_array=result[0], save_path="00.png", is_save=True)
array2image(image_array=result[1], save_path="11.png", is_save=True)
array2image(image_array=result[2], save_path="22.png", is_save=True)
array2image(image_array=result[3], save_path="33.png", is_save=True)
# 选择1、2、3号秘密进行恢复
secret_index = (1, 2, 3)
secret_collection = [result[1], result[2], result[3]]
recovery = secret_recovery(threshold=3, index=secret_index, secret_images=secret_collection)
array2image(image_array=recovery, save_path="recovery.png", is_save=True,mode="L")
end = time.time()
run_time = end - start
print("程序运行了" + run_time.__str__() + " s")
