from image_tools import *
from secret_sharing import *

start = time.time()
red, green, blue = split_channels("Origin.png")
result_r = share(threshold=3, secret_shares=4, image=red)
result_g = share(threshold=3, secret_shares=4, image=green)
result_b = share(threshold=3, secret_shares=4, image=blue)
secret_images = []
for i in range(4):
    secret_images.append(merge_channels(result_r[i], result_g[i], result_b[i]))
    secret_images[i].save(i.__str__() + ".png")

index = [1, 2, 3]
_red = []
_green = []
_blue = []
j = 0
for i in index:
    r , g ,b = split_channels(i.__str__() + ".png")
    _red.append(r), _green.append(g), _blue.append(b)
    j += 1
recovery_red = secret_recovery(threshold=3, secret_images=_red ,index=index)
recovery_green = secret_recovery(threshold=3, secret_images=_green,index=index)
recovery_blue = secret_recovery(threshold=3, secret_images=_blue,index=index)
recovery = merge_channels(recovery_red, recovery_green, recovery_blue)
recovery.save("recovery_rgb.png")
end = time.time()
run_time = end - start
print("程序运行了" + run_time.__str__() + " s")