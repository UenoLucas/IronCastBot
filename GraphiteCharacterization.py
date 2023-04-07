import cv2
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import math
from imagedataextractor.scalebar import ScalebarDetector
from imagedataextractor.data import EMData
class mainGraphiteCharacterization():
    def __init__(self,):
        self.scalebar_detector = ScalebarDetector()
        self.em_data = EMData()
        pass

    def AreaFeret(self, Contour):
        (x,y),FeretRadius = cv2.minEnclosingCircle(Contour)
        AreaFeret = round(FeretRadius **2 * math.pi,2)
        return [AreaFeret, FeretRadius]

    def AreaPixels(self, Contour):
        AreaPixels = cv2.contourArea(Contour)
        AreaPixels = round(AreaPixels,2)
        return AreaPixels
    

    def TreatmentImageOtsu(self, img,min="",max=""):
        if(min!="" and max!=""):
            min = int(min)
            max = int(max)
            if min<0 or min>255: min=0
            if max<0 or max>255: max=255
            ret,thr = cv2.threshold(img, min, max, cv2.THRESH_BINARY_INV)
        else:
            ret,thr = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV +cv2.THRESH_OTSU)
        return thr

    def TreatmentImage(self, img, min = 0, max = 255):
        img_erosion = cv2.erode(img, (5,5), iterations=1)
        blur = cv2.GaussianBlur(img_erosion, (5,5), 0)
        ret,thr = cv2.threshold(img_erosion, min, max, cv2.THRESH_BINARY_INV)
        return thr

    def ScaleBarDetection(self,grayImage):
        imgThr = cv2.cvtColor(grayImage,cv2.COLOR_GRAY2BGR)
        scalebar = self.scalebar_detector.detect(imgThr)
        self.em_data.scalebar = imgThr
        text, units, conversion, scalebar_contour = scalebar.data
        return [conversion, text, units, scalebar_contour]
    
    def MakeMask(self,grayImage,minThresh=45,maxThresh=255):
        # img_zeros1 = np.zeros(shape=grayImage.shape,dtype=int).astype('uint8')
        # ret,thMask = cv2.threshold(grayImage.copy(),50,255,cv2.THRESH_BINARY_INV)
        # contours, _ = cv2.findContours(thMask,cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        # img_zeros1 = cv2.drawContours(img_zeros1, contours, -1, 255, -1)
        # img_zeros1 = cv2.dilate(img_zeros1,(10,10),iterations=1)
        # img_zeros1 = cv2.morphologyEx(img_zeros1, cv2.MORPH_CLOSE, (10,10))
        # opening = cv2.morphologyEx(img_zeros1, cv2.MORPH_OPEN, (10,10), iterations=1)
        # imgReturn = cv2.bitwise_or(grayImage, opening)

        if minThresh=="" or int(minThresh)<0 or int(minThresh)>255: minThresh=45
        if maxThresh=="" or int(maxThresh)<0 or int(maxThresh)>255: maxThresh=255
        ret,thMask = cv2.threshold(grayImage,int(minThresh),int(maxThresh),cv2.THRESH_BINARY)
        img_zeros1 = np.zeros(shape=grayImage.shape,dtype=int).astype('uint8')
        contours, _ = cv2.findContours(thMask,cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        img_zeros1 = cv2.drawContours(img_zeros1, contours, -1, 255, 3)
        img_zeros1 = cv2.dilate(img_zeros1,(15,15),iterations=1)
        img_zeros1 = cv2.morphologyEx(img_zeros1, cv2.MORPH_OPEN, (10,10))
        close = cv2.morphologyEx(img_zeros1, cv2.MORPH_CLOSE, (10,10), iterations=1)
        imgReturn = cv2.bitwise_or(grayImage, close)
        return imgReturn