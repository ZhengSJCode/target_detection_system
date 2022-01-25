import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import numpy as np
from PIL import Image, ImageTk


class Button:
    def __init__(self, pos, box_size, value):
        self.pos = pos
        self.size = box_size
        self.value = value

    def draw(self, img, side="center", inside_color=(225, 225, 225), edge_color=(50, 50, 50), font=(4, 2)):
        cv2.rectangle(img, self.pos, (self.pos[0] + self.size[0], self.pos[1] + self.size[1]), inside_color,
                      cv2.FILLED)
        cv2.rectangle(img, self.pos, (self.pos[0] + self.size[0], self.pos[1] + self.size[1]), edge_color, 3)
        if side == "left":
            size = (self.pos[0] + 10, self.pos[1] + int(self.size[1] * 0.8))
        else:
            size = (self.pos[0] + int(0.2 * self.size[0]), self.pos[1] + int(self.size[1] * 0.8))
        cv2.putText(img, self.value, size,
                    cv2.FONT_HERSHEY_PLAIN, font[0], (50, 50, 50), font[1])

    def check_button(self, img, x, y, x1, y1) -> (str):
        if self.pos[0] < x < self.pos[0] + self.size[0] and self.pos[1] < y < self.pos[1] + self.size[1]:
            if self.pos[0] < x1 < self.pos[0] + self.size[0] and self.pos[1] < y1 < self.pos[1] + self.size[1]:
                self.draw(img, inside_color=(220, 87, 18), edge_color=(200, 200, 200), font=(6, 5))
                return self.value
        return 0


# ButtonList_value = [["7", "8", "9", "*"],
#                     ["4", "5", "6", "-"],
#                     ["1", "2", "3", "+"],
#                     ["0", "/", "C", "="]]
ButtonList_value = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
                    ["A", "S", "D", "F", "G", "H", "J", "K", "L", "del"],
                    ["Z", "X", "C", "V", "B", "N", "M", "!", " ", "clr"]]
ButtonList_value = np.transpose(ButtonList_value)
ButtonList = []
start_Position = (50, 0)
size = (100, 100)
for x, line_value in enumerate(ButtonList_value):
    for y, _ in enumerate(line_value):
        xPos = start_Position[0] + size[0] * x
        yPos = start_Position[1] + size[1] * y
        ButtonList.append(Button((xPos, yPos), size, ButtonList_value[x][y]))

# 输出面板
eqution = ''
space = Button((50, 350), (800, 100), eqution)


def main(master=None, Video_Size=(1280, 720), i=1):
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)
    detector = HandDetector(detectionCon=0.5)
    delay = 0
    while True:
        ret, img = cap.read()
        img = cv2.flip(img, 1)
        if ret:

            # 检查手
            hands, img = detector.findHands(img)

            # draw all button
            for btn in ButtonList:
                btn.draw(img)
            # 显示结果
            space.draw(img, side="left", font=(3, 2))

            if hands:
                lmList = hands[0]['lmList']
                length, _, img = detector.findDistance(lmList[8], lmList[12], img)
                print(length)

                x8, y8 = lmList[8]
                x12, y12 = lmList[12]
                if -100 < lmList[0][1] - lmList[16][1] < 100 and delay == 0:
                    delay = 1
                    space.value = space.value[:-1]
                for btn in ButtonList:
                    key = btn.check_button(img, x8, y8, x12, y12)
                    if key and delay == 0:
                        if key == 'clr':
                            space.value = ''
                        elif key == 'del':
                            space.value = space.value[:-1]
                        else:
                            space.value += key
                        delay = 1

            if delay != 0:
                delay += 1
                if delay > 10:
                    delay = 0
            if i:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                newImage = Image.fromarray(img).resize(Video_Size, Image.ANTIALIAS)
                newCover = ImageTk.PhotoImage(image=newImage)

                # 在指定的位置显示视频帧
                master.configure(image=newCover)
                master.image = newCover
                master.update()
            else:
                cv2.imshow("img", img)

if __name__ == '__main__':
    main()
