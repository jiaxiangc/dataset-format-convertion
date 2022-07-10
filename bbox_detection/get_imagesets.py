import os


if __name__ == '__main__':
    path_images = r'D:\Users\ChengJiaxiang\Adobe\An\gaud-map\image\test2022'
    path_save_imagesets = r'D:\Users\ChengJiaxiang\Tool\dataset-format-convertion\gaud_map\bbox_detection\data_dataset_voc\ImageSets\Main'
    mode = 'test'


    names_list = os.listdir(path_images)
    image_sets_list = []
    for name in names_list:
        if name.endswith('jpg'):
            name = name.split('.')[0]
            image_sets_list.append(name + '\n')

    if not os.path.exists(path_save_imagesets):
        os.makedirs(path_save_imagesets)

    with open('{}/{}.txt'.format(path_save_imagesets, mode), 'w') as f:
        f.writelines(image_sets_list)
    print('done')
