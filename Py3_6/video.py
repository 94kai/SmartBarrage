# -*- coding: utf-8 -*-

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



import cv2
import time
import demoForData

import numpy as np

######################     视频载入       #############################
cap = cv2.VideoCapture("../app/src/main/res/raw/video.mp4")
fourcc = cv2.VideoWriter_fourcc(*'XVID')
# out = cv2.VideoWriter('E:\\Data_Set\\AODnet\\测试视频\\生成视频\\output11.avi', fourcc, 20, (1920, 1080))

#####################       模型载入      #############################

#####################      视频处理       #############################
num = 0
currentTime = time.time()
# 总共215帧
file = open("video.txt", "a+",encoding="utf-8")

currentFrame = 0
while cap.isOpened():
    preFrameTime = time.time()
    currentFrame += 1
    # get a frame
    # 小于几就是从几开始
    if currentFrame<1:
        continue
    rval, frame = cap.read()
    # save a frame
    if rval == True:
        # print(type(rval))
        # print(type(frame))
        # 获取到当前帧的数据
        try:
            print("====开始处理第" + str(currentFrame) + "帧")
            try:
                frameData = demoForData.handleImage(frame)
                print("====处理完毕第" + str(currentFrame) + "帧" + str(time.time() - preFrameTime))
                file.write("\n"+str(currentFrame)+str(frameData))
            except:
                file.write("\nerror")

                print("====识别错误第" + str(currentFrame) + "帧" + str(time.time() - preFrameTime))

        except Exception as e:
            print("====错误处理第" + str(currentFrame) + "帧")
            print(e)

        print("====用时" + str(time.time() - currentTime) + ",总共215帧，当前处理了" + str(currentFrame) + "帧")
        print("===============================================")

    else:
        print("====error处理第" + str(currentFrame) + "帧")
        break
print("====close")

file.close()
