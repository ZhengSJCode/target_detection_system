from tkinter import *
import cv2
from tkinter import filedialog
from PIL import Image, ImageTk
import mediapipe as mp



def playVideo(master=None, Video_Size=(1060, 600)):
    # 用于播放视频
    moviePath = filedialog.askopenfilename()  # 选择视频路径
    print(moviePath)
    movie = cv2.VideoCapture(moviePath)

    waitTime = int( 1000 / movie.get(5) ) # movie.get(5) 为视频的帧数. 1000/帧数为每帧的等待时间
    movieTime = (movie.get(7) / movie.get(5)) / 60  # movie.get(7)为视频的总帧数
    while movie.isOpened():
        ret, readyFrame = movie.read()
        if ret:
            movieFrame = cv2.cvtColor(readyFrame, cv2.COLOR_BGR2RGB)
            # print(Video_Size)
            # newImage=Image.fromarray(movieFrame).resize(Video_Size)
            newImage = Image.fromarray(movieFrame).resize(Video_Size, Image.ANTIALIAS)
            newCover = ImageTk.PhotoImage(image=newImage)
            master.configure(image=newCover)
            master.image = newCover
            master.update()
            cv2.waitKey(waitTime)
        else:
            break


def figure(master=None, Video_Size=(1060, 600)):
    cap = cv2.VideoCapture(0)
    waitTime = int(1000 / cap.get(5))

    mpHands = mp.solutions.hands
    hands = mpHands.Hands()

    # 显示捕捉点位
    mpDraw = mp.solutions.drawing_utils
    # 显示线段
    handLmsStyle = mpDraw.DrawingSpec(color=(0, 0, 255), thickness=5)
    handConStyle = mpDraw.DrawingSpec(color=(0, 255, 255), thickness=5)

    while True:
        ret, img = cap.read()
        if ret:

            # BRG转RGB
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            result = hands.process(imgRGB)

            imgHeight = img.shape[0]
            imgWidth = img.shape[1]
            if result.multi_hand_landmarks:
                # 把侦测到的手都画出来
                for handlms in result.multi_hand_landmarks:
                    mpDraw.draw_landmarks(imgRGB, handlms, mpHands.HAND_CONNECTIONS, handLmsStyle, handConStyle)
                    for i, lm in enumerate(handlms.landmark):  # lm is landmark
                        xPos = int(lm.x * imgHeight)
                        yPos = int(lm.y * imgWidth)
                        cv2.putText(imgRGB, str(i), (xPos - 10, yPos + 5), cv2.FONT_ITALIC, 0.4, (0, 2, 111), 2)

                        if i == 4:
                            cv2.circle(imgRGB, (xPos, yPos), 10, (0, 0, 56), cv2.FILLED)

                        print(i, xPos, yPos)
            # cv2.imshow('img', img)

            newImage = Image.fromarray(imgRGB).resize(Video_Size, Image.ANTIALIAS)
            newCover = ImageTk.PhotoImage(image=newImage)
            master.configure(image=newCover)
            master.image = newCover
            master.update()


        cv2.waitKey(waitTime)

        if cv2.waitKey(1) == ord('q'):
            break