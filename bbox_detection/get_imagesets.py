import os


def get_image_sets(path_images, path_save_imagesets, mode):
    names_list = os.listdir(path_images)
    image_sets_list = []
    for name in names_list:
        if name.endswith('json'):
            name = name.split('.')[0]
            image_sets_list.append(name + '\n')

    if not os.path.exists(path_save_imagesets):
        os.makedirs(path_save_imagesets)

    with open('{}/{}.txt'.format(path_save_imagesets, mode), 'w') as f:
        f.writelines(image_sets_list)
    print('done')


if __name__ == '__main__':
    train_path_images = r'D:\Users\ChengJiaxiang\Tool\dataset-format-convertion\bbox_detection\atr\atr_dataset_origin'
    test_path_images = r'D:\Users\ChengJiaxiang\Tool\dataset-format-convertion\bbox_detection\gaud_map\gaud_map_dataset02_origin\test2022'
    path_save_imagesets = r'D:\Users\ChengJiaxiang\Tool\dataset-format-convertion\bbox_detection\atr\atr_dataset_voc\ImageSets\Main'
    get_image_sets(train_path_images, path_save_imagesets, mode='train')
    # get_image_sets(test_path_images, path_save_imagesets, mode='test')
