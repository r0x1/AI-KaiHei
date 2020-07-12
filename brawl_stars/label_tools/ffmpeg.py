import os
import subprocess

# ffmpeg的exe文件地址
ffmpeg_exe = 'C:\\Program Files\\ffmpeg-4.3-win64-static\\bin\\ffmpeg.exe'
# 输入的视频文件目录
input_folder = 'C:\\workspace\\test_video\\valid_video\\'
# 输出的图片文件目录
output_folder = 'C:\\workspace\\test_video\\valid\\'

# 遍历视频文件的目录
files = os.listdir(input_folder)

for video_file_name in files:
    # 视频文件路径
    video_file_path = input_folder + video_file_name

    # 图片文件路径
    image_file_path = output_folder + video_file_name[0:video_file_name.index('.')] + '_%d.png'

    # 组合命令行
    str_cmd = '\"' + ffmpeg_exe + '\" -i ' + video_file_path + ' -f image2 -vf fps=5.0 -qscale:v 2 ' +\
              image_file_path

    subp = subprocess.Popen(str_cmd, shell=True)
    subp.wait()
    # print('#pid: ', subp.pid)
    subp.terminate()

    pass
