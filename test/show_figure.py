import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()

# 显示捕捉点位
mpDraw = mp.solutions.drawing_utils
# 显示线段
handLmsStyle = mpDraw.DrawingSpec(color=(0, 0, 255), thickness=5)
handConStyle = mpDraw.DrawingSpec(color=(0, 255, 255), thickness=5)

pTime = 0
cTime = 0
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
                mpDraw.draw_landmarks(img, handlms, mpHands.HAND_CONNECTIONS, handLmsStyle, handConStyle)
                for i, lm in enumerate(handlms.landmark):  # lm is landmark
                    xPos = int(lm.x * imgHeight)
                    yPos = int(lm.y * imgWidth)
                    cv2.putText(img, str(i), (xPos - 10, yPos + 5), cv2.FONT_ITALIC, 0.4, (0, 2, 111), 2)

                    if i == 4:
                        cv2.circle(img, (xPos, yPos), 10, (0, 0, 56), cv2.FILLED)

                    print(i, xPos, yPos)

        cTime = time.time()
        fps_show = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, "FPS:" + str(int(fps_show)), (10, 20), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 1)

        cv2.imshow('img', img)

    cv2.waitKey(1)

    if cv2.waitKey(1) == ord('q'):
        break
