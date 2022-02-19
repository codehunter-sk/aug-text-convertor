# importing the modules
import cv2
import numpy as np
import time
from tkinter import *
from tkinter import messagebox as msgbox
from datetime import datetime


def startcap():
    global cap, myColors, myColorValues, myColorValues2, myPoints, thetemp
    # set Width and Height of output Screen
    frameWidth = 850
    frameHeight = 500

    # capturing Video from Webcam
    cap = cv2.VideoCapture(0)
    cap.set(3, frameWidth)
    cap.set(4, frameHeight)

    # set brightness, id is 10 and
    # value can be changed accordingly
    # cap.set(10,150)
    # cap.set(10,85)

        
    # object color values
    # myColors = [[5, 107, 0, 19, 255, 255],
    #             [133, 56, 0, 159, 156, 255],
    #             [57, 76, 0, 100, 255, 255],
    #             [90, 48, 0, 118, 255, 255]]

    # myColors = [60, 65, 120, 180, 200, 240]
    # myColors = [5, 107, 0, 190, 255, 255]
    # myColors = [45 ,180 ,20 ,67 ,240 ,250]
    myColors = [36 ,50 ,20 ,76 ,255 ,250]


    # color values which will be used to paint
    # values needs to be in BGR
    # myColorValues = [[51, 153, 255],        
    #                 [255, 0, 255],
    #                 [0, 255, 0],        
    #                 [255, 0, 0]]

    myColorValues = [41, 255, 70]
    myColorValues2 = [0, 0, 0]

    # [x , y ]
    myPoints = [[]]
    thetemp=1
        
# function to pick color of object
def findColor(img, myColors, myColorValues):

    # converting the image to HSV format
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newPoints = []
    
    
    lower = np.array(myColors[0:3])
    upper = np.array(myColors[3:6])
    mask = cv2.inRange(imgHSV,lower,upper)
    x, y = getContours(mask)

    # making the circles
    cv2.circle(imgResult, (x,y), 15,
        myColorValues, cv2.FILLED)
    if x != 0 and y != 0:
        newPoints.append([x,y])
    
    return newPoints, mask
    

# contouyrs function used to improve accuracy of paint
def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL,
                                            cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    
    # working with contours
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 450:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
    return x + w // 2, y
    

# draws your action on virtual canvas
def drawOnCanvas(myPoints, myColorValues):
    for myPoint in myPoints:

        # for point in myPoint:
        #     cv2.circle(imgResult, (point[0], point[1]),
        #             4, myColorValues, cv2.FILLED)
        #     cv2.circle(imgPlain, (point[0], point[1]),
        #             4, myColorValues2, cv2.FILLED)

        # # simple pointer
        # cv2.circle(imgResult, myPoint[-1],
        #             7, myColorValues, cv2.FILLED)
        # cv2.circle(imgPlain, myPoint[-1],
        #             7, myColorValues2, cv2.FILLED)
        
        # # simple pointer with tail
        # cv2.line(imgResult, myPoint[-2], myPoint[-1],
        #              myColorValues, 7)
        # cv2.line(imgPlain, myPoint[-2], myPoint[-1],
        #              myColorValues2, 7)

        for point in range(len(myPoint)-1):
            cv2.line(imgResult, myPoint[point], myPoint[point+1],
                     myColorValues, 4)
            cv2.line(imgPlain, myPoint[point], myPoint[point+1],
                     myColorValues2, 4)

def saveit():
    now = datetime.now() 
    # %H:%M:%S can not be used as ":" can not be in file name
    current_time = now.strftime('_%d-%m-%Y_%H-%M-%S')
    print('ct',current_time)
    # print(now.strftime('%S'))
    # loc='C:\\Pytemp1\\Myvenv1\\mini-project-1\\'
    loc=''
    c='picsave'+current_time+'.jpg'
    b=cv2.imwrite(loc+c,imgPlain)
    print('b',b)
    
# running infinite while loop so that
# program keep running untill we close it
def main():
    global imgResult, imgPlain, thetemp, myPoints

    storedict={}
    storevar=1

    startcap()

    minandsec1 = list(map(int,datetime.now().strftime('%M-%S').split('-')))

    while True:
        start=time.time()
        success, img = cap.read()
        imgResult = img.copy()

        imgPlain = cv2.imread('plainwhite.jpg')

        # finding the colors for the points
        newPoints,mask1 = findColor(img, myColors, myColorValues)
        if len(newPoints)!= 0:
            minandsec2 = list(map(int,datetime.now().strftime('%M-%S').split('-')))
            thetemp2=0
            if minandsec2[0]==minandsec1[0]:
                if minandsec2[1]-minandsec1[1]>1:
                    thetemp2=1
            elif minandsec2[1]+60-minandsec1[1]>1:
                thetemp2=1
            if thetemp2:
                if thetemp:
                    myPoints[0].extend(newPoints)
                else:
                    myPoints.append(newPoints)
            else:
                myPoints[-1].extend(newPoints)
            if thetemp:
                # print(myPoints)
                myPoints[0].append(myPoints[0][0])
                thetemp=0
            minandsec1=minandsec2[:]
        if len(myPoints[-1])!= 0:

            # drawing the points
            drawOnCanvas(myPoints, myColorValues)
        
        # displaying output on Screen
        for _it in range(480):
            imgResult[_it]=imgResult[_it][::-1]
            imgPlain[_it]=imgPlain[_it][::-1]
            mask1[_it]=mask1[_it][::-1]

        cv2.imshow("Result_imgResult", imgResult)
        cv2.imshow("Result_imgPlain", imgPlain)
        cv2.imshow("Result_mask1", mask1)

        
        end=time.time()
        fps=1/(end - start)
        wait_t=max(1,int(fps/4))
        # print(wait_t,ord('q'),0xFF)

        # condition to break programs execution
        # press q to stop the execution of program
        keyp = cv2.waitKey(wait_t) & 0xFF
        if keyp == ord('s'):
            saveit()
        elif keyp == ord('c'):
            storedict[storevar]=myPoints
            myPoints=[[]]
            thetemp=1
            storevar+=1
            # close='c'
            # break
        elif keyp == ord('q'):
            close='q'
            break



    cap.release()

    cv2.destroyAllWindows()

    return close

if __name__ == '__main__':
    while True:
        a=main()
        if a=='q':
            break
        # elif a=='c':
        #     print('Please wait reloading...')
        #     root=Tk()
        #     msgbox.showinfo(title = 'Alert!' , message = 'Please wait clearing...')
        #     root.destroy()
        #     continue

'''
https://stackoverflow.com/questions/10948589/choosing-the-correct-upper-and-lower-hsv-boundaries-for-color-detection-withcv/48367205#48367205
'''