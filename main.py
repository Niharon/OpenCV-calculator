import cv2
from cvzone.HandTrackingModule import HandDetector

# class for calculator button
class button:
    def __init__(self, pos, width, height, value):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value
    def draw(self, img):
        cv2.rectangle(img, self.pos, (self.pos[0]+self.width, self.pos[1]+self.height),
                      (225, 225, 225), cv2.FILLED)
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                      (75, 75, 75), 3)
        cv2.putText(img, self.value, (self.pos[0] + 40, self.pos[1] + 60),
                    cv2.FONT_HERSHEY_PLAIN, 2, (75, 75, 75), 3)
    def cheakClick(self, x, y):
        if self.pos[0] < x < self.pos[0] + self.width and \
           self.pos[1] < y < self.pos[1] + self.height:
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                          (255, 255, 255), cv2.FILLED)
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                          (75, 75, 75), 3)
            cv2.putText(img, self.value, (self.pos[0] + 25, self.pos[1] + 80),
                        cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 0), 5)
            return True
        else:
            return False


# webcam
cam = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.85, maxHands=1)
cam.set(3, 1240) # width....3 for width
cam.set(4, 720) # height....4 for height

# creating buttons
buttonListValues = [['7', '8', '9', '*'],
                    ['4', '5', '6', '-'],
                    ['1', '2', '3', '+'],
                    ['0', '/', '.', '=']]

buttonList = []
for x in range(4):
    for y in range(4):
        xpos = x * 100 + 800
        ypos = y * 100 + 150
        buttonList.append(button((xpos,ypos), 100, 100, buttonListValues[y][x]))

# variables
myEquation = ''
delayCounter = 0

# loop
while True:
    # get image from webcam
    success, img = cam.read()
    img = cv2.flip(img, 1)

    # detection of hand
    hands, img = detector.findHands(img, flipType=False)

    # draw all buttons
    cv2.rectangle(img, (800,50), (800 + 400, 100 + 50),
                  (225, 225, 225), cv2.FILLED)
    cv2.rectangle(img, (800,50), (800 + 400, 100 + 50),
                  (75, 75, 75), 3)
    for button in buttonList:
        button.draw(img)

    # check for hands
    if hands:
        lmList = hands[0]['lmList']
        length, _, img = detector.findDistance(lmList[4], lmList[8], img)
        # print(length)
        x, y = lmList[4]
        if length < 45:
            for i, button in enumerate(buttonList):
                if button.cheakClick(x, y) and delayCounter == 0:
                    myVal = buttonListValues[int(i % 4)][int(i / 4)]
                    if myVal == '=':
                        myEquation = str(eval(myEquation))
                    else:
                        myEquation += myVal
                    delayCounter = 1

    # avoid duplicate
    if delayCounter != 0:
        delayCounter += 1
        if delayCounter > 10:
            delayCounter = 0

    # display equation/result
    cv2.putText(img, myEquation, (810, 120),
                cv2.FONT_HERSHEY_PLAIN, 3, (75, 75, 75), 3)

    # show image
    cv2.imshow("image", img)
    key = cv2.waitKey(1)
    if key == ord('c'):
        myEquation = ''