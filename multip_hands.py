#!/usr/bin/env python
# coding: utf-8

# In[2]:


class handsTracking:
    def __init__(self,mode = False,maxHands = 2,detectionCon=0.5,trackCon=.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.maxHands,self.detectionCon,self.trackCon)
        self.myDraw = mp.solutions.drawing_utils
    def findHands(self,img,draw = True):
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for hand in self.results.multi_hand_landmarks:
                if draw:
                    self.myDraw.draw_landmarks(img,hand,self.mpHands.HAND_CONNECTIONS)
        return img
    def getPosition(self,img,draw = True):
        ls = []
        if self.results.multi_hand_landmarks:
            for hand in self.results.multi_hand_landmarks:
                for id,land in enumerate(hand.landmark):
                    h,w,c = img.shape
                    cx,cy = int(land.x * w) , int(land.y * h)
                    ls.append([id,cx,cy])
                    if draw:
                        cv2.circle(img,(cx,cy),8,(200,99,111),cv2.FILLED)
        return ls
def main():
    cap = cv2.VideoCapture(0)
    cTime = 0
    pTime = 0
    detect = handsTracking()
    while True:
        ref,img = cap.read()
        img = detect.findHands(img)
        lst = detect.getPosition(img)
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img,str(int(fps)),(10,50),cv2.FONT_HERSHEY_PLAIN,3,(250,127,120),2,cv2.LINE_AA)
        cv2.imshow("Video",img)
        if cv2.waitKey(1) & 0xFF == ord("q"):
                break
main()
cv2.destroyAllWindows()


# In[ ]:




