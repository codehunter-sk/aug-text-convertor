import cv2
import time
from datetime import datetime
import os
from tkinter import messagebox as msgbox
import code_vrecog
def startcap():
    global cap, greenrange, greencolour, blackcolour, mainpnts, thetemp
    fWidth = 850
    fHeight = 500
    fbright = 120
    cap = cv2.VideoCapture(0)
    cap.set(3, fWidth)
    cap.set(4, fHeight)
    cap.set(10, fbright)
    greenrange = [36 ,50 ,20 ,76 ,255 ,250]
    greencolour = [41, 255, 70]
    blackcolour = [0, 0, 0]
    mainpnts = [[]]
    thetemp=1
def findgreen(img, greenrange, greencolour,v):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    newpnts = []
    lower = tuple(greenrange[0:3])
    upper = tuple(greenrange[3:6])
    mask = cv2.inRange(imgHSV,lower,upper)
    x, y = getcontours(mask)
    if v in [0,1]:
        cv2.circle(finalimg, (x,y), 15, greencolour, cv2.FILLED)
    if x != 0 and y != 0:
        newpnts.append([x,y])
    return newpnts, mask
def getcontours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 450:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
    return x + w // 2, y
def drawonimage(mainpnts, greencolour):
    for myPoint in mainpnts:
        for point in range(len(myPoint)-1):
            cv2.line(finalimg, myPoint[point], myPoint[point+1], greencolour, 4)
            cv2.line(plainimg, myPoint[point], myPoint[point+1], blackcolour, 4)
def saveit(folder_path,v):
    if v in [0,1]:
        now = datetime.now() 
        current_time = now.strftime('_%d-%m-%Y_%H-%M-%S')
        loc=str(folder_path)+'/'
        c='picsave'+current_time+'.jpg'
        b=cv2.imwrite(loc+c,plainimg)
        text=code_vrecog.recog(loc+c)
        if text:
            with open((loc+c)[:-4]+'_text.txt','w') as f:
                f.write(text)
            msgbox.showinfo(title = 'Alert!' , message = 'Plain text image and text saved in\nspecified folder location!')
        else:
            msgbox.showinfo(title = 'Alert!' , message = 'Text not detected properly, try again\n(Note:Image is saved for reference)')
    else:
        msgbox.showinfo(title = 'Alert!' , message = 'Cannot save in this open mode!')
def main(v=1,folder_path=(os.getcwd())):
    global finalimg, plainimg, thetemp, mainpnts
    storedict={}
    storevar=1
    startcap()
    secandmicsec1 = list(map(int,datetime.now().strftime('%S-%f').split('-')))
    while True:
        start=time.time()
        success, img = cap.read()
        finalimg = img.copy()
        plainimg = cv2.imread('images/plainwhite.jpg')
        newpnts,mask1 = findgreen(img, greenrange, greencolour,v)
        if len(newpnts)!= 0:
            secandmicsec2 = list(map(int,datetime.now().strftime('%S-%f').split('-')))
            thetemp2=0
            if secandmicsec2[0]==secandmicsec1[0]:
                if secandmicsec2[1]-secandmicsec1[1]>370000:
                    thetemp2=1
            elif secandmicsec2[0]-secandmicsec1[0]==1:
                if secandmicsec2[1]+1000000-secandmicsec1[1]>370000:
                    thetemp2=1
            else:
                thetemp2=1
            if thetemp2:
                if thetemp:
                    mainpnts[0].extend(newpnts)
                    thetemp=0
                else:
                    mainpnts.append(newpnts)
            else:
                mainpnts[-1].extend(newpnts)
            secandmicsec1=secandmicsec2[:]
        if len(mainpnts[-1])!= 0:
            drawonimage(mainpnts, greencolour)
        for _it in range(480):
            finalimg[_it]=finalimg[_it][::-1]
            plainimg[_it]=plainimg[_it][::-1]
            mask1[_it]=mask1[_it][::-1]
        if v==1:
            cv2.imshow("Result_video", finalimg)
        elif v==0:
            cv2.imshow("Result_plain", plainimg)
        else:
            cv2.imshow("Result_check", mask1)        
        end=time.time()
        fps=1/(end - start)
        wait_t=max(1,int(fps/4))
        keyp = cv2.waitKey(wait_t) & 0xFF
        if keyp == ord('s'):
            saveit(folder_path,v)
        elif keyp == ord('c'):
            storedict[storevar]=mainpnts
            mainpnts=[[]]
            thetemp=1
            storevar+=1
        elif keyp == ord('q'):
            close='q'
            break
    cap.release()
    cv2.destroyAllWindows()
    return close
if __name__ == '__main__':
    main()