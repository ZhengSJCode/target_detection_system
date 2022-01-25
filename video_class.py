from tkinter import *
import cv2
from tkinter import filedialog
from PIL import Image, ImageTk
import mediapipe as mp
import time


class video:

    def __init__(self, master=None, video_Path=0, Video_Size=(1280, 720)):
        cv2.destroyAllWindows()
        # 视频路径默认是0用摄像头打开
        self.master = master
        self.video_Path = video_Path
        self.Video_Size = Video_Size

    def open(self, func=0):
        movie = cv2.VideoCapture(self.video_Path)


        # 获取视频的fps
        fps = movie.get(5)
        waitTime = int(1000 / fps)  # movie.get(5) 为视频的帧数. 1000/帧数为每帧的等待时间
        # movieTime = (movie.get(7) / movie.get(5)) / 60  # movie.get(7)为视频的总帧数

        while movie.isOpened():
            ret, img = movie.read()
            if ret:
                imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                show_imgRGB = self.func(imgRGB)

                # fps
                # cv2.putText(show_imgRGB, "FPS:" + str(int(fps)), (10, 20), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 1)
                # 用PIL打开文件,并变为tk可识别的
                newImage = Image.fromarray(show_imgRGB).resize(self.Video_Size, Image.ANTIALIAS)
                newCover = ImageTk.PhotoImage(image=newImage)

                # 在指定的位置显示视频帧
                self.master.configure(image=newCover)
                self.master.image = newCover
                self.master.update()

                cv2.waitKey(waitTime)
            else:
                break

    def func(self, img):
        # overload func就可以变化图片
        return img


class Mp_figure(video):
    mpHands = mp.solutions.hands
    hands = mpHands.Hands()
    # 显示捕捉点位
    mpDraw = mp.solutions.drawing_utils
    # 显示线段样式
    handLmsStyle = mpDraw.DrawingSpec(color=(0, 0, 255), thickness=5)
    handConStyle = mpDraw.DrawingSpec(color=(0, 255, 255), thickness=5)

    def __init__(self, master=None, video_Path=0, Video_Size=(1920, 1080)):
        super().__init__(master, video_Path, Video_Size)
        # self.movie.set(3, 1920)
        # self.movie.set(2, 1080)


    def func(self, imgRGB):
        result = self.hands.process(imgRGB)

        imgHeight = imgRGB.shape[0]
        imgWidth = imgRGB.shape[1]
        if result.multi_hand_landmarks:
            # 把侦测到的手都画出来
            for handlms in result.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(imgRGB, handlms, self.mpHands.HAND_CONNECTIONS, self.handLmsStyle,
                                           self.handConStyle)

                # i为手指的编号,landmark为手指的坐标(0~1)
                for i, lm in enumerate(handlms.landmark):  # lm is landmark
                    xPos = int(lm.x * imgHeight)
                    yPos = int(lm.y * imgWidth)
                    cv2.putText(imgRGB, str(int(i)), (xPos , yPos), cv2.FONT_HERSHEY_PLAIN,1, (0, 0, 255), 2)

                    # 大拇指为4
                    if i == 4:
                        cv2.circle(imgRGB, (xPos, yPos), 10, (0, 0, 56), cv2.FILLED)
                        self.mpDraw.draw_landmarks(imgRGB, handlms)

                    # 打印手指的坐标
                    print(i, xPos, yPos)
        return imgRGB
