import glob
import GraphiteCharacterization
import cv2
import numpy as np
import math
import ctypes
import json

class ProcessImage:
    def __init__(self) -> None:
        self.gcp = GraphiteCharacterization.mainGraphiteCharacterization()
        self.firstLoop = True
        # self.scaleUnitFactorProperty = 0 
        self.text = ''
        pass

    def switch(self,case):
        if case == 'mm':
            return 1000
        elif case == 'um':
            return 10
        elif case == 'nm':
            return 10e-3
        elif case == 'A':
            return 10e-4

    def scaleUnitFactor(self,case):
        if case == 'mm':
            return 1e-3
        elif case == 'um':
            return 1e-6
        elif case == 'nm':
            return 1e-9
        elif case == 'A':
            return 1e-10
    
    def correction2mm(self,case):
        if case == 'um':
            return 1e-3
        elif case == 'nm':
            return 1e-6
        elif case == 'A':
            return 1e-7

    def is_contour_on_border(self, contour, width, height, dist_min):
        # verifica se o contorno está na borda da imagem
        is_on_border = False
        for point in contour:
            # verifica se o ponto está na borda da imagem
            x, y = point[0]
            if x <= dist_min +2 or x >= width - dist_min - 4  or y <= dist_min + 2 or y >= height - dist_min - 2:
                is_on_border = True
                break
        return is_on_border

    def is_contour_on_border_2(self,contour,width,height,dist_min):
        moments = cv2.moments(contour)
        if moments['m00'] == 0:
            # Skip contours with zero area
            return True
        # Calculate center of mass
        cx = int(moments['m10'] / moments['m00'])
        cy = int(moments['m01'] / moments['m00'])
        # Calculate radius of object
        area = moments['m00']
        radius = np.sqrt(area / np.pi)
        # Check if center of mass is within a certain percentage of the radius of the object from the image border
        border_distance = 0.95 * radius
        if cx <= border_distance or cx >= width - border_distance or cy <= border_distance or cy >= height - border_distance:
            # Skip contours that are within the specified percentage of the radius of the object from the image border
            return True
        return False

    def feret_diameter(self,contour):
        max_dist = 0
        min_dist = []
        # Percorre todos os pontos do contorno
        for i in range(len(contour)):
            for j in range(i+1, len(contour)):
                # Calcula a distância euclidiana entre os pontos i e j
                dist = np.linalg.norm(contour[i][0] - contour[j][0])
                min_dist.append(dist)
                if dist > max_dist:
                    max_dist = dist

        return max_dist

    def InputImg(self,img, ppi, flagScaleBarDetection ,minThresholdMask = '',maxThresholdMask = '',minThrOtsu = '', maxThrOtsu = ''):
        self.sumAreaFeret = 0
        MinimumSizeAchieve = 0
        self.ShapeFactorAchieve = 0
        self.sumAreaGraphitesAboveAcceptanceCriteria = 0
        self.sumAreaGraphiteAboveMinimumSize = 0
        self.conversion = None
        contorAboveMinimumSize = []
        size_ranges = {
            '<_20': 0,
            '20_<40': 0,
            '40_<80': 0,
            '80_<160': 0,
            '160_<320': 0,
            '320_<640': 0,
            '640_<1280': 0,
            '>_1280': 0
        }
        # img8bit = cv2.imread(img,0)
        img8bit = img
        # if(self.firstLoop):
        # caso checkbox de detecção de escala esteja true
        if flagScaleBarDetection:
            #  primeiramente redimensiono a imagem caso ela seja muito grande, assim reduzimos tempo de inferencia do scalebardetection
            if img8bit.shape[0]>=980 or img8bit.shape[1]>980:
                widthImage= 720
                ratioScale = widthImage/img8bit.shape[1]
                heightScale = int(img8bit.shape[0]*ratioScale)
                img8bit = cv2.resize(img8bit,(widthImage,heightScale) , interpolation = cv2.INTER_AREA)
            self.conversion, self.text, units, scaleContour = self.gcp.ScaleBarDetection(img8bit)
            if self.conversion == None:
                img8bit = img
                self.conversion, self.text, units, scaleContour = self.gcp.ScaleBarDetection(img)
                if self.conversion == None:
                    return img8bit, "0", "0", "0", "0", "None scalebar detected", ""
            
                    # self.conversion = self.conversion * ratioScale
            self.conversion = 1 / self.conversion
            self.minimumSize = self.switch(units)
            self.scaleUnitFactorProperty = self.scaleUnitFactor(units)
            # um/px
            self.correctionConversion = self.conversion  * self.scaleUnitFactorProperty   
            # self.correctionConversion = (self.conversion)  / self.scaleUnitFactorProperty 
            # px
            minimunsizePx = self.minimumSize * self.correctionConversion
            ratioPxUm = round(self.correctionConversion,3)
        else:
            # supomos q é 210mm de papel, como na norma a superfície captada tem em torno de 0,89mm de largura,multiplicamos pelo fator de 1,28
            widthImage= int(210* 1.28 *ppi/(25.4 * 3))
            ratioScale = widthImage/img8bit.shape[1]
            heightScale = int(img8bit.shape[0]*ratioScale)
            img8bit = cv2.resize(img8bit,(widthImage,heightScale) , interpolation = cv2.INTER_AREA)
            img_zeros = np.zeros(shape=img8bit.shape,dtype=int)
            units = 'um'
            self.minimumSize = self.switch(units)
            # px/um
            ratioPxUm = round(img8bit.shape[1]/894,3)
            minimunsizePx = ratioPxUm * self.minimumSize
            self.text = "Image without scale"
        mask = self.gcp.MakeMask(img8bit,minThresholdMask,maxThresholdMask)
        thr = self.gcp.TreatmentImageOtsu(mask,minThrOtsu,maxThrOtsu)
        listContours = []
        contours1, hierarchy = cv2.findContours(
            thr, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        NewImage = cv2.drawContours(thr, contours1, -1, 255, -1)
        # contours2, hierarchy = cv2.findContours(NewImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours2, hierarchy = cv2.findContours(NewImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # if(self.conversion!=None):
        #     # um/px
        #     # self.correctionConversion =   1 / self.conversion 
        #     self.correctionConversion = 1 / (self.conversion * 1e6)
        #     # px
        #     minimunsizePx = self.minimumSize * self.correctionConversion
        #     # minimunsizePx = self.minimumSize 
        # else:
        #     # px/um
        #     ratioPxUm = img8bit.shape[1]/894
        #     minimunsizePx = ratioPxUm * self.minimumSize
        finalImg = np.ones((NewImage.shape[0],NewImage.shape[1],3), dtype=np.uint8)*255
        for i in range(len(contours2)):
            if self.is_contour_on_border(contours2[i],img8bit.shape[1],img8bit.shape[0],int(img8bit.shape[1]*0.005)): continue
            # if self.is_contour_on_border_2(contours2[i],img8bit.shape[1],img8bit.shape[0],int(img8bit.shape[1]*0.005)): continue
            # AreaFeret, FeretDiameter = gcp.AreaFeret(contours1[i])
            (x, y), FeretRadius = cv2.minEnclosingCircle(contours2[i])

            # if(len(contours2[i]) == 0): continue
            # FeretRadius = self.feret_diameter(contours2[i])
            # FeretRadius  = FeretRadius / 2

            # Criar máscara para eliminar a intersecção com a borda
            # mask = np.zeros_like(NewImage)
            # mask = cv2.circle(mask, (int(x), int(y)), int(FeretRadius), 255, border_size)
            # mask = cv2.bitwise_not(mask)
            # # Aplicar máscara ao círculo mínimo
            # circ = np.zeros_like(NewImage)
            # circ = cv2.circle(circ, (int(x), int(y)), int(FeretRadius), 255, -1)
            # circ = cv2.bitwise_and(circ, mask)
            # Calcular área do círculo mínimo sem a intersecção com a borda
            # AreaFeret = round(cv2.countNonZero(circ) / 255 * math.pi * FeretRadius ** 2, 2)
            #  Resolvi deixar o seguinte método como conta da área do corpo
            moments = cv2.moments(contours2[i])
            if moments['m00'] == 0:
                # Skip contours with zero area
                continue
            # Calculate center of mass
            cx = int(moments['m10'] / moments['m00'])
            cy = int(moments['m01'] / moments['m00'])
            # Calculate radius of object
            area = moments['m00']
            # radius = np.sqrt(area / np.pi)

            diameter = round(FeretRadius*2,2)

            AreaFeret = round(FeretRadius ** 2 * math.pi, 2)

            # FeretDiameterUnit = scaleUnitFactor * FeretDiameter / conversion
            if (AreaFeret == 0.0 or FeretRadius*2 < minimunsizePx):
            # if (AreaFeret == 0.0 or FeretRadius*2 < minimunsizePx):
                continue
            center = (int(x), int(y))
            radius = int(FeretRadius)
            finalImg = cv2.circle(finalImg, center, radius, (255, 255, 0), 1, lineType=cv2.LINE_AA)
            MinimumSizeAchieve += 1
            contorAboveMinimumSize.append(contours2[i])
            areaPx = cv2.contourArea(contours2[i])
            # ShapeFactor = areaPx / AreaFeret
            # self.sumAreaGraphiteAboveMinimumSize += areaPx
            ShapeFactor = area / AreaFeret
            self.sumAreaGraphiteAboveMinimumSize += area
            if (ShapeFactor > 0.57):
                self.ShapeFactorAchieve += 1
                self.sumAreaGraphitesAboveAcceptanceCriteria += area
                # self.sumAreaGraphitesAboveAcceptanceCriteria += areaPx
                listContours.append(contours2[i])

                if diameter < (20 * ratioPxUm):
                    size_ranges['<_20'] += 1
                elif diameter <( 40  * ratioPxUm):
                    size_ranges['20_<40'] += 1
                elif diameter < (80*ratioPxUm):
                    size_ranges['40_<80'] += 1
                elif diameter < 160 * ratioPxUm:
                    size_ranges['80_<160'] += 1
                elif diameter < 320 * ratioPxUm:
                    size_ranges['160_<320'] += 1
                elif diameter < 640 * ratioPxUm:
                    size_ranges['320_<640'] += 1
                elif diameter < 1280 * ratioPxUm:
                    size_ranges['640_<1280'] += 1
                else:
                    size_ranges['<_1280'] += 1

        finalImg = cv2.drawContours(finalImg,(listContours),-1,0,-1)
        finalImg = cv2.drawContours(finalImg,(contorAboveMinimumSize),-1,0,1)
            # finalImg = cv2.drawContours(finalImg,(contours),-1,(0,255,56),1)
        # finalImg = cv2.drawContours(finalImg,(contours1),-1,(0,255,56),1)
        nodularity = self.sumAreaGraphitesAboveAcceptanceCriteria/self.sumAreaGraphiteAboveMinimumSize
        correction2mm = self.correction2mm(units)
        areaImage = (img8bit.shape[0] - 6) * (img8bit.shape[1] - 6) * (correction2mm**2) / (ratioPxUm ** 2)

        density =  self.ShapeFactorAchieve / areaImage 
        return finalImg,MinimumSizeAchieve, self.ShapeFactorAchieve, round(nodularity,2), round(density,2), self.text, f"{ratioPxUm} px/{units}", size_ranges

# mp = MainProcess()
# img = cv2.imread(r'source\images\thumbnail_nodularity 67%.png',0)
# finalimg = mp.InputImg(img)
# cv2.imshow('final',finalimg)
# cv2.waitKey(0)
