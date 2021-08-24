import cv2
import numpy as np
import mediapipe as mp
import time
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import multip_hands as detects
cap =  cv2.VideoCapture(0)
wCam,hCam = 500,300
cap.set(3,wCam)
cap.set(4,hCam)
pTime = 0
cTime = 0
detect = detects.handsTracking(detectionCon=0.7)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange=volume.GetVolumeRange()
volume.SetMasterVolumeLevel(-5.0, None)
minVol = (volRange[0])
maxVol = volRange[1]
vol = 0
volBar = 400
while True:
    ref,img = cap.read()
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    img = detect.findHands(img)
    lmlist = detect.getPosition(img,draw=False)
    
    #Tính toán Line và vẽ các nốt tại cột mốc 4 và 8
    if len(lmlist) != 0:
        x1,y1 = lmlist[4][1],lmlist[4][2]
        x2,y2 = lmlist[8][1],lmlist[8][2]
        cx,cy = (x1+x2)//2,(y1+y2)//2
        cv2.circle(img,(lmlist[4][1],lmlist[4][2]),10,(255,0,255),cv2.FILLED)
        cv2.circle(img,(lmlist[8][1],lmlist[8][2]),10,(255,0,255),cv2.FILLED)
        cv2.line(img,(lmlist[4][1],lmlist[4][2]),(lmlist[8][1],lmlist[8][2]),(255,0,255),3)
        cv2.circle(img,(cx,cy),10,(255,0,123),cv2.FILLED)
        #Tính chiều dài line
        len_line = math.hypot(x2-x1,y2-y1)
#         print(len_line)
        
        #Range line 50 400
        #Vol -65 - 0
        vol = np.interp(len_line,[50,400],[minVol,maxVol])
        print(vol)
        volBar = np.interp(len_line,[50,400],[400,150])
        volume.SetMasterVolumeLevel(vol, None)
        
        
        if len_line < 50:
            cv2.circle(img,(cx,cy),10,(111,1,10),cv2.FILLED)
    cv2.rectangle(img,(50,150),(85,400),(0,255,0),3)
    cv2.rectangle(img,(50,int(volBar)),(85,400),(0,255,0),cv2.FILLED)
    
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img,"FPS:" +str(int(fps)),(10,50),cv2.FONT_HERSHEY_PLAIN,2,(0,255,5),2,cv2.LINE_AA)
    cv2.imshow("video",img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
            break
cv2.destroyAllWindows()