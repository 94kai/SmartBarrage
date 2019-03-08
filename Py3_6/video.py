# -*- coding: utf-8 -*-

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
# 获取总的帧数
frames_num = cap.get(7)

data = {
    "framesNum": frames_num,
    "framesData": []
}
currentFrame = 0
while cap.isOpened():

    if(currentFrame>frames_num/2):
        break
    currentFrame += 1

    if (currentFrame % 5 != 0):
        continue
    # get a frame
    rval, frame = cap.read()
    # save a frame
    if rval == True:
        print(type(rval))
        print(type(frame))
        # 获取到当前帧的数据
        try:
            print("成功处理第" + str(currentFrame) + "帧")
            frameData = demoForData.handleImage(frame)
            data['framesData'].append(frameData)
        except:
            print("错误处理第" + str(currentFrame) + "帧")
            data['framesData'].append({})
        #  frame = cv2.flip(frame,0)
        # Start time
        # start = time.time()
        # #        rclasses, rscores, rbboxes=process_image(frame) #换成自己调用的函数
        #
        # clean_image_tensor = process_image(data_hazy)  # 换成自己调用的函数
        # # End time
        #
        # end = time.time()
        # # Time elapsed
        # seconds = end - start + 0.0001
        # print("Time taken : {0} seconds".format(seconds))
        # # Calculate frames per second
        # fps = 1 / seconds;
        # print("Estimated frames per second : {0}".format(fps));
        # # bboxes_draw_on_img(frame,rclasses,rscores,rbboxes)
        # # print(rclasses)
        # out.write(clean_image)
        # num = num + 1
        # print(num)
        # fps = cap.get(cv2.CAP_PROP_FPS)
        # print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))
        print("用时" + str(time.time() - currentTime) + ",总共" + str(frames_num) + "帧，当前处理了" + str(currentFrame) + "帧")

    else:
        print("error处理第" + str(currentFrame) + "帧")
        break
    # show a frame
    # cv2.imshow("capture", frame)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

# demoForData.handleImageByFileName("./image/test1.jpeg")
file = open("video.txt", "w")
file.write(str(data))
