import moviepy.editor as mp
import cv2
from moviepy.audio.io.AudioFileClip import AudioFileClip

# 모듈 로딩 후 오디오 추출
clip = mp.VideoFileClip("C:/Users/forea/test/아빠만큼 축구 잘할것 같은 유망주 TOP 10.mp4")
clip.audio.write_audiofile("audio.mp3")

audio = AudioFileClip("C:/Users/forea/PycharmProjects/untitled1/audio.mp3")
# 영상의 이미지를 연속적으로 캡쳐
vidcap =cv2.VideoCapture("C:/Users/forea/test/아빠만큼 축구 잘할것 같은 유망주 TOP 10.mp4")

cnt =0
# 프레임별로 짤라서 사진으로 저장
while vidcap.isOpened():
    ret, image = vidcap.read()
    if int(vidcap.get(1))%20 == 0: # Frame
        print("Save frame number:" + str(int(vidcap.get(1))))
        cv2.imwrite("C:/Users/forea/test/" + str(cnt) +".png", image)
        print("save frame" + str(cnt))
        cnt+=1

pathOut = "C:/Users/forea/PycharmProjects/untitled1/test.mp4"
fps = 30
lent = 1160
frame_array = []

# 사진을 동영상으로 합침
for idx in range(0, lent):
    img = cv2.imread("C:/Users/forea/test/" + str(idx) + ".png")
    height, width, layers = img.shape
    size = (width,height)
    frame_array.append(img)
out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'DIVX'), fps, size)

for i in range(len(frame_array)):
    # writing to a image array
    out.write(frame_array[i])
    print(i)
out.release()
