import argparse
import random
import shutil
import os

import cv2 as cv


def divide_train_test(path_videos, path_images):
    if os.path.exists(path_images):
        if os.path.exists('{}/train2022'.format(path_images)):
            shutil.rmtree('{}/train2022'.format(path_images))
        if os.path.exists('{}/test2022'.format(path_images)):
            shutil.rmtree('{}/test2022'.format(path_images))
        print('previous dir has been deleted')
    else:
        os.mkdir(path_images)
    os.mkdir('{}/train2022'.format(path_images))
    os.mkdir('{}/test2022'.format(path_images))
    print('new empty dir has been created')

    video_names = os.listdir(path_videos)
    for video_name in video_names:
        file_name = video_name.split('.')[0]
        video_name = os.path.join(path_videos, video_name)
        # 进入第一个视频
        cap = cv.VideoCapture(video_name)
        number_frames = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
        sample_number_frames = int(number_frames / 25)
        print('{} sample frames number: {}'.format(video_name, sample_number_frames))
        number_frames_test = int(0.2 * sample_number_frames)
        test_array = random.sample(range(0 + 1, sample_number_frames + 1), number_frames_test)

        count = 1
        count_loop = 1
        while cap.isOpened():
            flag, frame = cap.read()
            if not flag:
                break
            if count_loop % 25 == 0:
                # 判断是测试集还是训练集
                if count in test_array:
                    cv.imwrite('{}/test2022/test_{}_{:0>4d}.jpg'.format(path_images, file_name, count), frame)
                else:
                    cv.imwrite('{}/train2022/train_{}_{:0>4d}.jpg'.format(path_images, file_name, count), frame)
                count += 1
            count_loop += 1

        print('{} has been finished'.format(file_name))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='divide a video into train and test.')
    parser.add_argument('--videos', default='../data/videos')
    parser.add_argument('--images', default='../data/images')
    args = parser.parse_args()
    path_videos = args.videos
    path_images = args.images
    divide_train_test(path_videos, path_images)
