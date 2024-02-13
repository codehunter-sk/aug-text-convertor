import cv2
import time
from datetime import datetime
import os
from tkinter import messagebox as msgbox
import code_vrecog
import keras_ocr
import matplotlib.pyplot as plt
import numpy as np

mouse_pressed = False
def mouse_callback(event, x, y, flags, param):
    global mouse_pressed, mainpnts, thetemp, storevar
    if event == cv2.EVENT_LBUTTONDOWN:
        mouse_pressed = True
    elif event == cv2.EVENT_LBUTTONUP:
        mouse_pressed = False
    elif event == cv2.EVENT_RBUTTONDOWN:
        mainpnts=[[]]
        thetemp=1
        storevar+=1

def startcap():
    global cap, greenrange, greencolour, blackcolour, mainpnts, thetemp
    fWidth = 1280
    fHeight = 720
    # fbright = 120
    cap = cv2.VideoCapture(0)
    cap.set(3, fWidth)
    cap.set(4, fHeight)
    # cap.set(10, fbright)
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
    if mouse_pressed and x != 0 and y != 0:
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
def saveit(folder_path,v,detect):
    if v in [0,1]:
        now = datetime.now() 
        current_time = now.strftime('_%d-%m-%Y_%H-%M-%S')
        loc=str(folder_path)+'/'
        c='picsave'+current_time+'.jpg'
        b=cv2.imwrite(loc+c,plainimg)
        msgbox.showinfo(title = 'Alert!' , message = 'Plain text image saved in specified folder location!')
        if detect:
            text=code_vrecog.recog(loc+c)
            if text:
                with open((loc+c)[:-4]+'_text.txt','w') as f:
                    f.write(text)
                msgbox.showinfo(title = 'Alert!' , message = 'Plain text image and text saved in\nspecified folder location!')
            else:
                msgbox.showinfo(title = 'Alert!' , message = 'Text not detected properly, try again\n(Note:Image is saved for reference)')
    else:
        msgbox.showinfo(title = 'Alert!' , message = 'Cannot save in this open mode!')

def adjust_brightness(img):
    # hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # brightness = hsv_image[:,:,2].mean()
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    min_val, max_val, _, _ = cv2.minMaxLoc(gray_img)
    brightness = (max_val + min_val) / 2
    target_brightness = 70 # any preferred value
    brightness_factor = target_brightness / brightness
    adjusted_image = cv2.convertScaleAbs(img, alpha=brightness_factor, beta=0)
    return adjusted_image

def main(v=1,folder_path=(os.getcwd())):
    global finalimg, plainimg, thetemp, mainpnts, storevar

    pipeline = keras_ocr.pipeline.Pipeline()

    storedict={}
    storevar=1
    startcap()

    if v==1:
        cv2.namedWindow("Result_video")
        cv2.setMouseCallback("Result_video", mouse_callback)
    elif v==0:
        cv2.namedWindow("Result_plain")
        cv2.setMouseCallback("Result_plain", mouse_callback)
    else:
        cv2.namedWindow("Result_check")
        cv2.setMouseCallback("Result_check", mouse_callback)
    secandmicsec1 = list(map(int,datetime.now().strftime('%S-%f').split('-')))
    while True:
        start=time.time()
        success, img = cap.read()
        img = adjust_brightness(img)
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
        for _it in range(len(finalimg)):
            finalimg[_it]=finalimg[_it][::-1]
            plainimg[_it]=plainimg[_it][::-1]
            mask1[_it]=mask1[_it][::-1]
        # break
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
        if keyp == ord('d'):
            background_image = np.ones((720,1280,3),dtype=np.uint8)*255
            x_offset = (1280 - 400) // 2
            y_offset = (720 - 225) // 2
            background_image[y_offset:y_offset+225, x_offset:x_offset+400] = cv2.resize(plainimg, (400,225))
            images = [keras_ocr.tools.read(cv2.GaussianBlur(background_image, (5, 5),0))]
            prediction_groups = pipeline.recognize(images)
            fig, ax = plt.subplots(figsize=(10,20))
            keras_ocr.tools.drawAnnotations(image=images[0], predictions=prediction_groups[0], ax=ax)
            plt.show()
            for text, box in prediction_groups[0]:
                print("Text: ",text)
        elif keyp == ord('s'):
            saveit(folder_path,v,False)
        elif keyp == ord('l'):
            saveit(folder_path,v,True)
        elif keyp == ord('c'):
            # storedict[storevar]=mainpnts
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