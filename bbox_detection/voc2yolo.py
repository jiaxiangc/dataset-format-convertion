# 一张一张的读取xml文件，从中获取类别，边框坐标，拿出存储到train_annotations，并且复制图像至对应文件下方
import collections
import os
import shutil
import xml.etree.ElementTree as ET


def voc2yolo(path_data, path_save_data, mode='train'):
    # 想办法将voc的格式转至yolo
    # 首先是要知道自己弄的是测试集还是训练集

    if mode == 'train':
        path_image_sets = 'ImageSets/Main/train.txt'
        path_image_sets = os.path.join(path_data, path_image_sets)
    else:
        path_image_sets = 'ImageSets/Main/test.txt'
        path_image_sets = os.path.join(path_data, path_image_sets)

    # 拿到txt文件后，打开，获取图像名称
    with open(path_image_sets, 'r') as f:
        image_names = f.readlines()

    # 获取对应
    path_class_names = '{}/class_names.txt'.format(path_data)
    name_to_category_id_dict = name_to_category_id(path_class_names)
    print(name_to_category_id_dict)

    # 拿到具体的名称，获取xml的名称
    for image_name in image_names:
        # 首先复制文件到目标区域
        src = '{}/JPEGImages/{}.jpg'.format(path_data, image_name.strip())
        if mode == 'train':
            dst = '{}/images/train/{}.jpg'.format(path_save_data, image_name.strip())
            if not os.path.exists('{}/images/train'.format(path_save_data)):
                os.makedirs('{}/images/train'.format(path_save_data))
        else:
            dst = '{}/images/test/{}.jpg'.format(path_save_data, image_name.strip())
            if not os.path.exists('{}/images/test'.format(path_save_data)):
                os.makedirs('{}/images/test'.format(path_save_data))
        shutil.copyfile(src, dst)

        path_xml = 'Annotations/{}.xml'.format(image_name.strip())
        path_xml = os.path.join(path_data, path_xml)
        # 读出xml中的信息，将信息写入yolo格式的annotation中
        tree = ET.ElementTree(file=path_xml)
        # 首先获取宽高
        height = float(tree.find('size/height').text)
        width = float(tree.find('size/width').text)

        yolo_annotations = []
        # 然后循环获取目标
        for object_i in tree.iter('object'):
            name = object_i.find('name').text
            category_id = name_to_category_id_dict[name]
            # 获取四个坐标信息
            xmin = float(object_i.find('bndbox/xmin').text)
            ymin = float(object_i.find('bndbox/ymin').text)
            xmax = float(object_i.find('bndbox/xmax').text)
            ymax = float(object_i.find('bndbox/ymax').text)
            object_width = xmax - xmin
            object_height = ymax - ymin
            x_center = (xmin + object_width / 2) / width
            y_center = (ymin + object_height / 2) / height
            object_width = object_width / width
            object_height = object_height / height
            yolo_annotations.append(
                '{} {:.6f} {:.6f} {:.6f} {:.6f}\n'.format(category_id, x_center, y_center, object_width, object_height))
        # 接下来将这些信息，保存进text
        if mode == 'train':
            path_txt = 'labels/train/{}.txt'.format(image_name.strip())
            path_txt = os.path.join(path_save_data, path_txt)
            if not os.path.exists('{}/labels/train'.format(path_save_data)):
                os.makedirs('{}/labels/train'.format(path_save_data))
        else:
            path_txt = 'labels/test/{}.txt'.format(image_name.strip())
            path_txt = os.path.join(path_save_data, path_txt)
            if not os.path.exists('{}/labels/test'.format(path_save_data)):
                os.makedirs('{}/labels/test'.format(path_save_data))
        with open(path_txt, 'w') as f:
            f.writelines(yolo_annotations)
        # 好，现在我们把验证信息搞完之后，要能够将对应区域的图像移动到
        print('{} done '.format(image_name))


def name_to_category_id(path_class_names):
    # 读取文件
    with open(path_class_names, 'r') as f:
        classes_names = f.readlines()
    names_to_category_id_dict = collections.OrderedDict()
    for i, class_name in enumerate(classes_names, -1):
        # 拿到名称后，形成字典
        names_to_category_id_dict[class_name.strip()] = str(i)
    return names_to_category_id_dict


if __name__ == '__main__':
    # ok 我们现在尝试一下
    path_data = r'D:\Users\ChengJiaxiang\Tool\dataset-format-convertion\bbox_detection\gaud_map_dataset_voc'
    path_save_data = r'D:\Users\ChengJiaxiang\Tool\dataset-format-convertion\bbox_detection\gaud_map_dataset_yolo'
    voc2yolo(path_data, path_save_data, mode='test')
