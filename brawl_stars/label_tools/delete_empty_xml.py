import os
import subprocess

# 输入的图片文件目录
origin_image_folder = 'C:\\workspace\\test_video\\images\\'

# 遍历视频文件的目录
files = os.listdir(origin_image_folder)

for xml_file_name in files:

    # 将与xml文件同名的图片文件，连同xml文件，一起拷贝到新目录
    if xml_file_name.endswith('.xml'):

        xml_file_content = ''

        # 读取xml文件内容
        with open(origin_image_folder + xml_file_name) as file_obj:
            xml_file_content = file_obj.read()
        pass

        # 判断里面是否 <object> 文本
        if xml_file_content.find('<object>') > 0:
            pass
        else:
            # 如果没有 <object> 文本，则删除xml文件
            str_cmd = 'del ' + origin_image_folder + xml_file_name
            subp = subprocess.Popen(str_cmd, shell=True)
            subp.wait()
            subp.terminate()

            # 删除图片文件
            # image_file_name = xml_file_name[0:xml_file_name.index('.xml')] + '.png'
            # str_cmd = 'del ' + origin_image_folder + image_file_name
            # subp = subprocess.Popen(str_cmd, shell=True)
            # subp.wait()
            # subp.terminate()
        pass

    pass
