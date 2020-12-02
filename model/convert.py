#!/usr/bin/env python
# coding: utf-8

# In[12]:


import moviepy.editor as mp
import cv2
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.io.VideoFileClip import VideoFileClip
import numpy as np

from data import create_dataset
from models import create_model
import os
import shutil
import argparse

# parser = argparse.ArgumentParser(description='input mp4 & output dir')
# parser.add_argument('--input', dest='input', metavar='i', type=str,
#                     help='input video')
# parser.add_argument('--output', dest='output', metavar='o', type=str, default = './out',
#                     help='output path')
os.mkdir('./tmp')
os.mkdir('./out')

# In[2]:
try:
    clip = mp.VideoFileClip("./input.mp4")
    clip.audio.write_audiofile("./out/audio.mp3")
except:
    print('')

vidcap = cv2.VideoCapture('./input.mp4')

length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = vidcap.get(cv2.CAP_PROP_FPS)


# In[3]:


print('len: ',length, 'fps: ', fps)


# In[4]:


length


# In[5]:





# In[6]:


cnt =0 # 사진 Number
images = []
while vidcap.isOpened():
    ret, image = vidcap.read()
    if ret==False:
        break
    images.append(image)
    cv2.imwrite("./tmp/" + str(cnt) +".png", image)
    print("save frame" + str(cnt))
    cnt+=1


# In[7]:


len(images)


# In[ ]:





# In[8]:


get_ipython().system('python test.py --dataroot ./tmp/ --name Unet_n_layer --netG unet_256 --model test --results_dir ./out --no_dropout --num_test %s' %(length))


# In[ ]:





# In[9]:


## 새로만들 동영상의 정보 ##
pathOut = "./out/result.mp4" # output 경로
frame_array = [] #사진 정보가 담길 리스트
size = (256,256) # 사이즈


# In[10]:


## 사진 정보를 읽어와 frame_append에 저장 ##
for idx in range(0, length):
    img = cv2.imread("./out/Unet_n_layer/test_latest/images/" + str(idx) + "_fake.png")
    frame_array.append(img)
out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'DIVX'), fps, size) # out은 결과물 VideoWriter("경로", 확장자, 프레임, 크기)

## 사진 -> 동영상 ##
for i in range(length): # out에 사진들을 쓰는 반복문
    # writing to a image array
    out.write(frame_array[i])
out.release()


# In[13]:
try:
    videoclip = VideoFileClip("./out/result.mp4") # 위에서 새로 만든 Video
    audioclip = AudioFileClip("./out/audio.mp3") # 맨 처음에 추출한 소리

    videoclip.audio = audioclip # 소리를 새로 만든 Video에 합성
    videoclip.write_videofile("result.mp4") # Output
except:
    shutil.copy2('./out/result.mp4','./result.mp4')
shutil.rmtree('./tmp', ignore_errors=True)
shutil.rmtree('./out/', ignore_errors=True)

# In[ ]:




