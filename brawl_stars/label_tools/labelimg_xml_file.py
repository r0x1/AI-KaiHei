# 将检测结果，x1,y1,x2,y2 写入 labelImg格式的xml文件
# xml格式如下：

# <annotation>
# 	<folder>images</folder>
# 	<filename>RPReplay_Final1594286214_102.png</filename>
# 	<path>C:\workspace\test_video\images\RPReplay_Final1594286214_102.png</path>
# 	<source>
# 		<database>Unknown</database>
# 	</source>
# 	<size>
# 		<width>1920</width>
# 		<height>1080</height>
# 		<depth>3</depth>
# 	</size>
# 	<segmented>0</segmented>
# 	<object>
# 		<name>enemy</name>
# 		<pose>Unspecified</pose>
# 		<truncated>0</truncated>
# 		<difficult>0</difficult>
# 		<bndbox>
# 			<xmin>1192</xmin>
# 			<ymin>205</ymin>
# 			<xmax>1319</xmax>
# 			<ymax>369</ymax>
# 		</bndbox>
# 	</object>
# 	<object>
# 		<name>enemy</name>
# 		<pose>Unspecified</pose>
# 		<truncated>0</truncated>
# 		<difficult>0</difficult>
# 		<bndbox>
# 			<xmin>927</xmin>
# 			<ymin>230</ymin>
# 			<xmax>1054</xmax>
# 			<ymax>391</ymax>
# 		</bndbox>
# 	</object>
# </annotation>


# 获取labelImg的xml格式字符串
def get_labelimg_xml_string(
        folder='images',
        filename='RPReplay_Final1594286214_20.png',
        path='C:\\images\\RPReplay_Final1594286214_20.png',
        database='Unknown',
        width='1920',
        height='1080',
        depth='3',
        segmented='0',
        object_list=None):
    """
    获取labelImg的xml格式字符串
    :param folder: <folder>images</folder>
    :param filename: <filename>RPReplay_Final1594286214_102.png</filename>
    :param path: <path>C:\\workspace\\test_video\\images\\RPReplay_Final1594286214_102.png</path>
    :param database: <database>Unknown</database>
    :param width: <width>1920</width>
    :param height: <height>1080</height>
    :param depth: <depth>3</depth>
    :param segmented: <segmented>0</segmented>
    :param object_list:list[
    dict(
    name='enemy', pose='Unspecified', truncated='0', difficult='0', xmin='1192', ymin='205', xmax='1319', ymax='369'),
    dict(
    name='enemy', pose='Unspecified', truncated='0', difficult='0', xmin='927', ymin='230', xmax='1054', ymax='391')]
    :return: labelImg格式的xml字符串
    """

    str_header = '<annotation>' + '\n'
    str_header += '	<folder>' + folder + '</folder>' + '\n'
    str_header += '	<filename>' + filename + '</filename>' + '\n'
    str_header += '	<path>' + path + '</path>' + '\n'
    str_header += '	<source>' + '\n'
    str_header += '		<database>' + database + '</database>' + '\n'
    str_header += '	</source>' + '\n'
    str_header += '	<size>' + '\n'
    str_header += '		<width>' + width + '</width>' + '\n'
    str_header += '		<height>' + height + '</height>' + '\n'
    str_header += '		<depth>' + depth + '</depth>' + '\n'
    str_header += '	</size>' + '\n'
    str_header += '	<segmented>' + segmented + '</segmented>' + '\n'

    # 检测到的物体
    str_objects = ''
    for object_dict in object_list:
        str_objects += '	<object>' + '\n'
        str_objects += '		<name>' + object_dict['name'] + '</name>' + '\n'
        str_objects += '		<pose>Unspecified</pose>' + '\n'
        str_objects += '		<truncated>0</truncated>' + '\n'
        str_objects += '		<difficult>0</difficult>' + '\n'
        str_objects += '		<bndbox>' + '\n'
        str_objects += '			<xmin>' + object_dict['xmin'] + '</xmin>' + '\n'
        str_objects += '			<ymin>' + object_dict['ymin'] + '</ymin>' + '\n'
        str_objects += '			<xmax>' + object_dict['xmax'] + '</xmax>' + '\n'
        str_objects += '			<ymax>' + object_dict['ymax'] + '</ymax>' + '\n'
        str_objects += '		</bndbox>' + '\n'
        str_objects += '	</object>' + '\n'
        pass

    str_footer = '</annotation>'
    str_result = str_header + str_objects + str_footer

    return str_result


if __name__ == "__main__":
    # 测试 get_labelimg_xml_string

    # 检测到的物体列表
    list_objects = []
    # 检测到的第一个物体
    # name='enemy', xmin='1192', ymin='205', xmax='1319', ymax='369'),
    dict1 = {'name': 'enemy', 'xmin': '1192', 'ymin': '205', 'xmax': '1319', 'ymax': '369'}
    # 添加到list中
    list_objects.append(dict1)

    # 检测到的第二个物体
    # name='teammate', xmin='927', ymin='230', xmax='1054', ymax='391')]
    dict2 = {'name': 'enemy', 'xmin': '927', 'ymin': '230', 'xmax': '1054', 'ymax': '391'}
    # 添加到list中
    list_objects.append(dict2)

    str_folder = 'images'
    str_filename = 'RPReplay_Final1594286214_102.png'
    str_path = 'C:\\workspace\\test_video\\temp_img\\RPReplay_Final1594286214_102.png'

    # str_width = '1920'
    # str_height = '1080'

    str_xml_file = get_labelimg_xml_string(folder=str_folder, filename=str_filename, path=str_path,
                                           object_list=list_objects)

    str_xml_path = 'C:\\workspace\\test_video\\temp_img\\RPReplay_Final1594286214_102.xml'
    # 写入文件
    with open(str_xml_path, 'w') as f:
        f.write(str_xml_file)
    pass

    # print(str_xml_file)
    print('done!')
    pass
