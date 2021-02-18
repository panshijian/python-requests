import os
import random
class UplaodData:
    def uploadimage(self):

        local_path = "D:\\MicoApi\\data\\image"
            # 打開對應的文件夾
        filelist = os.listdir(local_path)
            # 得到文件中圖片個數
        total_num = len(filelist)
        img_paths= []

        for i in range(total_num):
            # 拼接圖片讀取地址
            filename = "%s.jpg" % (i + 1,)
            image_path = os.path.join(local_path, filename)
            img_paths.append(image_path)

        random.shuffle(img_paths)
        return img_paths





