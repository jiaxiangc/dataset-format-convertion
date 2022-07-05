import collections
import os
import xml.etree.ElementTree as ET
from PIL import Image


def convert_to_voc_format(annotations_path, image_sets_path, origin_images_path, origin_annotations_path,
                          class_names_path):
    category_id_to_name_dict = category_id_to_name(class_names_path)
    # 获取原始标注路径
    filenames_list = os.listdir(origin_annotations_path)
    image_sets_list = [filename.split('.')[0] + '\n' for filename in filenames_list]
    with open(image_sets_path, 'w') as f:
        f.writelines(image_sets_list)
    filenames_list = [os.path.join(origin_annotations_path, filename) for filename in filenames_list]
    for filename in filenames_list:
        # 获取原始标注信息
        xml_folder = 'name of dataset'
        xml_filename = filename.split(os.sep)[-1].split('.')[0] + '.jpg'
        xml_segmented = '0'
        image_path = os.path.join(origin_images_path, xml_filename)
        image = Image.open(image_path)
        xml_width, xml_height = image.size
        xml_width = str(xml_width)
        xml_height = str(xml_height)
        xml_depth = '3'
        xml_objects = []
        xml_pose = 'Unspecified'
        xml_truncated = '0'
        xml_difficult = '0'
        with open(filename, 'r') as f:
            bboxes_cats = f.readlines()
        for bbox_cat in bboxes_cats:
            # 15 0.980000 0.445266 0.500000 0.399408
            if len(bbox_cat.strip()) > 0:
                xml_objects.append(bbox_cat.strip())
        # 创建voc format xml 文件
        annotation = ET.Element('annotation')
        tree = ET.ElementTree(annotation)
        folder = ET.Element('folder')
        folder.text = xml_folder
        et_filename = ET.Element('filename')
        et_filename.text = xml_filename
        size = ET.Element('size')
        width = ET.Element('width')
        height = ET.Element('height')
        depth = ET.Element('depth')
        width.text = xml_width
        height.text = xml_height
        depth.text = xml_depth
        size.append(width), size.append(height), size.append(depth)
        segmented = ET.Element('segmented')
        segmented.text = xml_segmented
        annotation.append(folder), annotation.append(et_filename)
        annotation.append(size), annotation.append(segmented)
        for xml_object in xml_objects:
            et_object = ET.Element('object')
            name = ET.Element('name')
            name.text = category_id_to_name_dict[xml_object.split(' ')[0]]
            pose = ET.Element('pose')
            pose.text = xml_pose
            truncated = ET.Element('truncated')
            truncated.text = xml_truncated
            difficult = ET.Element('difficult')
            difficult.text = xml_difficult
            bndbox = ET.Element('bndbox')
            xmin = ET.Element('xmin')
            x_center = float(xml_object.split(' ')[1]) * float(xml_width)
            y_center = float(xml_object.split(' ')[2]) * float(xml_height)
            image_width = float(xml_object.split(' ')[3]) * float(xml_width)
            image_height = float(xml_object.split(' ')[4]) * float(xml_height)
            xmin.text = '{:.6f}'.format(x_center - image_width / 2)
            ymin = ET.Element('ymin')
            ymin.text = '{:.6f}'.format(y_center - image_height / 2)
            xmax = ET.Element('xmax')
            xmax.text = '{:.6f}'.format(x_center + image_width / 2)
            ymax = ET.Element('ymax')
            ymax.text = '{:.6f}'.format(y_center + image_height / 2)
            bndbox.append(xmin), bndbox.append(ymin)
            bndbox.append(xmax), bndbox.append(ymax)
            et_object.append(name), et_object.append(pose), et_object.append(truncated)
            et_object.append(difficult), et_object.append(bndbox)
            annotation.append(et_object)
        __indent(annotation)
        xml_path = os.path.join(annotations_path, filename.split(os.sep)[-1].split('.')[0] + '.xml')
        tree.write(xml_path, encoding='utf-8', xml_declaration=True)


# 创建xml缩进
def __indent(elem, level=0):
    """
    Confirm the right format of xml file.
    Args:
        elem: root.
        level: level of current node.

    Returns: right format of xml file.

    """
    i = "\n" + level * "\t"
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "\t"
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            __indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def category_id_to_name(class_names_path):
    with open(class_names_path, 'r') as f:
        classes_names = f.readlines()
    category_id_to_name_dict = collections.OrderedDict()
    for i, class_name in enumerate(classes_names):
        category_id_to_name_dict[str(i)] = class_name.strip()

    return category_id_to_name_dict


if __name__ == '__main__':
    mode = 'train'
    annotations_path = '../bbox_detection/data_dataset_voc/Annotations'
    image_sets_path = f'../bbox_detection/data_dataset_voc/ImageSets/Main/{mode}.txt'
    origin_images_path = f'../bbox_detection/data_dataset_yolo/{mode}'
    origin_annotations_path = f'../bbox_detection/data_dataset_yolo/{mode}_annotations'
    class_name_path = '../bbox_detection/data_dataset_yolo/class_names.txt'
    convert_to_voc_format(annotations_path, image_sets_path, origin_images_path, origin_annotations_path,
                          class_name_path)
