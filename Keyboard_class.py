import video_class
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import numpy as np


def drawAll(img,KeyboardList):
    for key in KeyboardList:
        x, y = key.pos
        w, h = key.size
        cvzone.cornerRect(img, (key.pos[0], key.pos[1], key.size[0], key.size[1]),
                          10, rt=0)


        cv2.rectangle(img, key.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, key.text, (x + 10, y + 30),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
    return img

def drawAll_alpha(img,KeyboardList,alpha = 0.1):
    imgNew = np.zeros_like(img, np.uint8)
    for key in KeyboardList:
        x, y = key.pos
        cvzone.cornerRect(imgNew, (key.pos[0], key.pos[1], key.size[0], key.size[1]),
                          20, rt=0)
        cv2.rectangle(imgNew, key.pos, (x + key.size[0], y + key.size[1]),
                      (255, 0, 255), cv2.FILLED)
        cv2.putText(imgNew, key.text, (x + 10, y + 30),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
    out = img.copy()

    mask = imgNew.astype(bool)
    print(mask.shape)
    out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]
    return out


class Keyboard:
    def __init__(self, pos, text, size=[50, 50]):
        self.pos = pos
        self.text = text
        self.size = size


class Virtual_Keyboard(video_class.video):

    keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
            ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]
    KeyboardList = []
    for i, x in enumerate(keys):
        for j, key in enumerate(x):
            KeyboardList.append(Keyboard([60 * j + 20, 60 * i + 50], key))

    def __init__(self,master=None, video_Path=0, Video_Size=(1280, 720)):
        super().__init__(master, video_Path, Video_Size)
        self.detector = HandDetector(detectionCon=0.5)


    def func(self,img):
        hands = self.detector.findHands(img, draw=False)
        lmList, bboxInfo = self.detector.findHands(img)
        img = drawAll_alpha(img,self.KeyboardList)
        return img

    # def drawAll(self, img):
    #     for key in self.KeyboardList:
    #         x, y = key.pos
    #         w, h = key.size
    #         cvzone.cornerRect(img, (key.pos[0], key.pos[1], key.size[0], key.size[1]),
    #                           10, rt=0)
    #
    #
    #         cv2.rectangle(img, key.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
    #         cv2.putText(img, key.text, (x + 10, y + 30),
    #                     cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
    #     return img
    #
    # def drawAll_alpha(self,img,alpha = 0.1):
    #     imgNew = np.zeros_like(img, np.uint8)
    #     for key in self.KeyboardList:
    #         x, y = key.pos
    #         cvzone.cornerRect(imgNew, (key.pos[0], key.pos[1], key.size[0], key.size[1]),
    #                           20, rt=0)
    #         cv2.rectangle(imgNew, key.pos, (x + key.size[0], y + key.size[1]),
    #                       (255, 0, 255), cv2.FILLED)
    #         cv2.putText(imgNew, key.text, (x + 10, y + 30),
    #                     cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
    #     out = img.copy()
    #
    #     mask = imgNew.astype(bool)
    #     print(mask.shape)
    #     out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]
    #     return out
