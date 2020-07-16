
import os
import subprocess

# 遍历文件夹，获取所有xml文件
# 输入的视频文件目录
origin_image_folder = 'C:\\workspace\\test_video\\images_20200716\\'
# 输出的图片文件目录
new_image_folder = 'C:\\workspace\\test_video\\image_output_20200716\\'

# 遍历视频文件的目录
files = os.listdir(origin_image_folder)

for video_file_name in files:

    # 将与xml文件同名的图片文件，连同xml文件，一起拷贝到新目录
    if video_file_name.endswith('.xml'):
        xml_file_name = video_file_name[0:video_file_name.index('.xml')] + '.png'

        str_cmd = 'copy ' + origin_image_folder + video_file_name + ' ' + new_image_folder + video_file_name
        subp = subprocess.Popen(str_cmd, shell=True)
        subp.wait()
        subp.terminate()

        str_cmd = 'copy ' + origin_image_folder + xml_file_name + ' ' + new_image_folder + xml_file_name
        subp = subprocess.Popen(str_cmd, shell=True)
        subp.wait()
        subp.terminate()

        pass

    pass

print('done!')
