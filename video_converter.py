import moviepy.editor as mp
import cv2
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.io.VideoFileClip import VideoFileClip

## 모듈 로딩 후 오디오 추출 ##
clip = mp.VideoFileClip("C:/Users/forea/test/조로.mp4")
clip.audio.write_audiofile("audio.mp3")

audio = AudioFileClip("C:/Users/forea/PycharmProjects/untitled1/audio.mp3")


## 동영상을 사진으로 저장 ##
vidcap =cv2.VideoCapture("C:/Users/forea/test/조로.mp4")
cnt =0 # 사진 Number
while vidcap.isOpened():
    ret, image = vidcap.read()
    if ret==False:
        break
    cv2.imwrite("C:/Users/forea/test/" + str(cnt) +".png", image)
    print("save frame" + str(cnt))
    cnt+=1
vidcap.release()

## 새로만들 동영상의 정보 ##
pathOut = "C:/Users/forea/PycharmProjects/untitled1/test.mp4" # output 경로
fps = 30 # 프레임
lent = cnt # 사진의 수
frame_array = [] #사진 정보가 담길 리스트

## 사진 정보를 읽어와 frame_append에 저장 ##
for idx in range(0, lent):
    img = cv2.imread("C:/Users/forea/test/" + str(idx) + ".png")
    height, width, layers = img.shape # img를 읽어서 H,W,L을 가져오는데 사실 채널은 쓸모가 없다..
    size = (width,height) # 사이즈
    frame_array.append(img)
out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'DIVX'), fps, size) # out은 결과물 VideoWriter("경로", 확장자, 프레임, 크기)

## 사진 -> 동영상 ##
for i in range(len(frame_array)): # out에 사진들을 쓰는 반복문
    # writing to a image array
    out.write(frame_array[i])
    print(str(i) + "번째 사진을 쓰는 중")
out.release()

## 위에서 만든 동영상 + 소리 ###
videoclip = VideoFileClip("C:/Users/forea/PycharmProjects/untitled1/test.mp4") # 위에서 새로 만든 Video
audioclip = AudioFileClip("C:/Users/forea/PycharmProjects/untitled1/audio.mp3") # 맨 처음에 추출한 소리

videoclip.audio = audioclip # 소리를 새로 만든 Video에 합성
videoclip.write_videofile("new video.mp4") # Output
