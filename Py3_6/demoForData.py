# coding: utf-8

# # Mask R-CNN Demo
# 
# A quick intro to using the pre-trained model to detect and segment objects.

# In[1]:


import os
import sys
import random
import math
import numpy as np
import skimage.io
import matplotlib
import matplotlib.pyplot as plt

# Root directory of the project
from IPython.core.display import JSON

ROOT_DIR = os.path.abspath("./")

# Import Mask RCNN
sys.path.append(ROOT_DIR)  # To find local version of the library
from mrcnn import utils
import mrcnn.model as modellib
from mrcnn import visualize
# Import COCO config
# sys.path.append(os.path.join(ROOT_DIR, "./coco/"))  # To find local version
import coco

# get_ipython().run_line_magic('matplotlib', 'inline')

# Directory to save logs and trained model
MODEL_DIR = os.path.join(ROOT_DIR, "logs")

# Local path to trained weights file
COCO_MODEL_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")
# Download COCO trained weights from Releases if needed
if not os.path.exists(COCO_MODEL_PATH):
    utils.download_trained_weights(COCO_MODEL_PATH)


# ## Configurations
# 
# We'll be using a model trained on the MS-COCO dataset. The configurations of this model are in the ```CocoConfig``` class in ```coco.py```.
# 
# For inferencing, modify the configurations a bit to fit the task. To do so, sub-class the ```CocoConfig``` class and override the attributes you need to change.

# In[2]:


class InferenceConfig(coco.CocoConfig):
    # Set batch size to 1 since we'll be running inference on
    # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1


config = InferenceConfig()
config.display()

# ## Create Model and Load Trained Weights

# In[3]:


# Create model object in inference mode.
model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)

# Load weights trained on MS-COCO
model.load_weights(COCO_MODEL_PATH, by_name=True)

# ## Class Names
# 
# The model classifies objects and returns class IDs, which are integer value that identify each class. Some datasets assign integer values to their classes and some don't. For example, in the MS-COCO dataset, the 'person' class is 1 and 'teddy bear' is 88. The IDs are often sequential, but not always. The COCO dataset, for example, has classes associated with class IDs 70 and 72, but not 71.
# 
# To improve consistency, and to support training on data from multiple sources at the same time, our ```Dataset``` class assigns it's own sequential integer IDs to each class. For example, if you load the COCO dataset using our ```Dataset``` class, the 'person' class would get class ID = 1 (just like COCO) and the 'teddy bear' class is 78 (different from COCO). Keep that in mind when mapping class IDs to class names.
# 
# To get the list of class names, you'd load the dataset and then use the ```class_names``` property like this.
# ```
# # Load COCO dataset
# dataset = coco.CocoDataset()
# dataset.load_coco(COCO_DIR, "train")
# dataset.prepare()
# 
# # Print class names
# print(dataset.class_names)
# ```
# 
# We don't want to require you to download the COCO dataset just to run this demo, so we're including the list of class names below. The index of the class name in the list represent its ID (first class is 0, second is 1, third is 2, ...etc.)

# In[4]:


# COCO Class names
# Index of the class in the list is its ID. For example, to get ID of
# the teddy bear class, use: class_names.index('teddy bear')
class_names = ['BG', 'person', 'bicycle', 'car', 'motorcycle', 'airplane',
               'bus', 'train', 'truck', 'boat', 'traffic light',
               'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird',
               'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear',
               'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie',
               'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
               'kite', 'baseball bat', 'baseball glove', 'skateboard',
               'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
               'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
               'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
               'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed',
               'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote',
               'keyboard', 'cell phone', 'microwave', 'oven', 'toaster',
               'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors',
               'teddy bear', 'hair drier', 'toothbrush']

import time
from skimage.measure import find_contours


# ## Run Object Detection

# In[5]:


def handleImageByFileName(file_names):
    handleImage(skimage.io.imread(file_names))


def handleImage(image):
    # Load a random image from the images folder
    # file_names = "./image/test1.jpeg"

    # 把数据存入data中。最后转成json
    data = {}
    # 存储图像的大小，在安卓设备绘制遮罩的时候需要根据这个大小进行缩放
    data["shape"] = [image.shape[0], image.shape[1]]
    # 一张图可能有多个人物，一个人物会有多个轮廓，用数组存
    data['contours'] = []
    # Run detection
    results = model.detect([image], verbose=1)

    # Visualize results
    r = results[0]

    # 以下代码修改自visualize.display_instances方法
    # 获取id
    class_ids = r['class_ids']
    masks = r['masks']
    boxes = r['rois']
    # Number of instances
    N = boxes.shape[0]
    ax = None

    # Generate random colors

    # Show area outside image boundaries.
    height, width = image.shape[:2]

    masked_image = image.astype(np.uint32).copy()

    # 转换轮廓数据为坐标数据
    def getContourData(contour):
        contourData = []
        for point in contour:
            contourData.append([point[0], point[1]])
        return contourData

    for i in range(N):
        class_id = class_ids[i]
        label = class_names[class_id]
        # 如果不是人，跳过
        if (label != 'person'):
            continue
        # Bounding box
        if not np.any(boxes[i]):
            # Skip this instance. Has no bbox. Likely lost in image cropping.
            continue
        y1, x1, y2, x2 = boxes[i]

        # Mask
        mask = masks[:, :, i]

        # Mask Polygon
        # Pad to ensure proper polygons for masks that touch image edges.
        padded_mask = np.zeros(
            (mask.shape[0] + 2, mask.shape[1] + 2), dtype=np.uint8)
        padded_mask[1:-1, 1:-1] = mask
        contours = find_contours(padded_mask, 0.5)
        # for verts in contours:
        # 遍历轮廓
        for contour in contours:
            # Subtract the padding and flip (y, x) to (x, y)
            contour = np.fliplr(contour) - 1
            # 轮廓数据构添加到集合中。
            contourData = getContourData(contour)
            data['contours'].append(contourData)
            # printImg(contour, contour)

    return data
    # print(data)
    # visualize.display_instances(image, r['rois'], r['masks'], r['class_ids'],
    #                             class_names, r['scores'], show_bbox=False, show_mask=False)


# ======================

# import cv2
# import time
# import demoForData
# from PIL import Image
#
# cap = cv2.VideoCapture("../app/src/main/res/raw/video.mp4")
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# num = 0
# currentTime = time.time()
# # 获取总的帧数
# frames_num = cap.get(7)
#
# print(frames_num)
# currentFrame = 0
# lastFrame = ""
# while cap.isOpened():
#     currentFrame += 1
#     # get a frame
#     rval, frame = cap.read()
#     # save a frame
#     if currentFrame == 3:
#         rval = False
#     if rval == True:
#         lastFrame = frame
#         # print(type(rval))
#         # print(type(frame))
#         # 获取到当前帧的数据
#         try:
#             print("成功处理第" + str(currentFrame) + "帧")
#             # frameData = demoForData.handleImage(frame)
#         except:
#             print("错误处理第" + str(currentFrame) + "帧")
#         #  frame = cv2.flip(frame,0)
#         # Start time
#         # start = time.time()
#         # #        rclasses, rscores, rbboxes=process_image(frame) #换成自己调用的函数
#         #
#         # clean_image_tensor = process_image(data_hazy)  # 换成自己调用的函数
#         # # End time
#         #
#         # end = time.time()
#         # # Time elapsed
#         # seconds = end - start + 0.0001
#         # print("Time taken : {0} seconds".format(seconds))
#         # # Calculate frames per second
#         # fps = 1 / seconds;
#         # print("Estimated frames per second : {0}".format(fps));
#         # # bboxes_draw_on_img(frame,rclasses,rscores,rbboxes)
#         # # print(rclasses)
#         # out.write(clean_image)
#         # num = num + 1
#         # print(num)
#         # fps = cap.get(cv2.CAP_PROP_FPS)
#         # print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))
#         print("用时" + str(time.time() - currentTime) + ",总共" + str(frames_num) + "帧，当前处理了" + str(currentFrame) + "帧")
#     else:
#         # plt.imshow(lastFrame)
#         # plt.show()
#         print("error处理第" + str(currentFrame) + "帧")
#         break


# # 以下为图片转换
# # image = skimage.io.imread("./image/paonan.jpg")
# image = lastFrame
# # Load a random image from the images folder
# # file_names = "./image/test1.jpeg"
#
# # 把数据存入data中。最后转成json
# data = {}
# # 存储图像的大小，在安卓设备绘制遮罩的时候需要根据这个大小进行缩放
# data["shape"] = [image.shape[0], image.shape[1]]
# # 一张图可能有多个人物，一个人物会有多个轮廓，用数组存
# data['contours'] = []
# # Run detection
# results = model.detect([image], verbose=1)
#
# # Visualize results
# r = results[0]
#
# # 以下代码修改自visualize.display_instances方法
# # 获取id
# class_ids = r['class_ids']
# masks = r['masks']
# boxes = r['rois']
# # Number of instances
# N = boxes.shape[0]
# ax = None
#
# # Generate random colors
#
# # Show area outside image boundaries.
# height, width = image.shape[:2]
#
# masked_image = image.astype(np.uint32).copy()
#
# # 转换轮廓数据为坐标数据
# def getContourData(contour):
#     contourData = []
#     for point in contour:
#         contourData.append([point[0], point[1]])
#     return contourData
#
# for i in range(N):
#     class_id = class_ids[i]
#     label = class_names[class_id]
#     # 如果不是人，跳过
#     if (label != 'person'):
#         continue
#     # Bounding box
#     if not np.any(boxes[i]):
#         # Skip this instance. Has no bbox. Likely lost in image cropping.
#         continue
#     y1, x1, y2, x2 = boxes[i]
#
#     # Mask
#     mask = masks[:, :, i]
#
#     # Mask Polygon
#     # Pad to ensure proper polygons for masks that touch image edges.
#     padded_mask = np.zeros(
#         (mask.shape[0] + 2, mask.shape[1] + 2), dtype=np.uint8)
#     padded_mask[1:-1, 1:-1] = mask
#     contours = find_contours(padded_mask, 0.5)
#     # for verts in contours:
#     # 遍历轮廓
#     for contour in contours:
#         # Subtract the padding and flip (y, x) to (x, y)
#         contour = np.fliplr(contour) - 1
#         # 轮廓数据构添加到集合中。
#         contourData = getContourData(contour)
#         data['contours'].append(contourData)
#         # printImg(contour, contour)
#
# print(data)
# visualize.display_instances(image, r['rois'], r['masks'], r['class_ids'],
#                             class_names, r['scores'], show_bbox=False, show_mask=False)
