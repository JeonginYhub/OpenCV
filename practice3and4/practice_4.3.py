import cv2 as cv
import numpy as np

img=cv.imread("D:/practice_image/soccer.jpg")	 # 영상 읽기
gray=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
canny=cv.Canny(gray,100,200) 

contour,hierarchy=cv.findContours(canny,cv.RETR_LIST,cv.CHAIN_APPROX_NONE) #canny = 경계선을 찾을 에지 영상, cv.RETR_LIST = 바깥쪽 경계선만 찾음, cv.CHAIN_APPROX_NONE = 모든 경계선 점을 저장 (_SIMPLE : 직선의 양 끝점만 기록)

lcontour=[]   
for i in range(len(contour)):
    if contour[i].shape[0]>100:	# 실제로는 길이가 50 이상인 경계선만 남음 (시작-끝-시작 추적)
        lcontour.append(contour[i])
    
cv.drawContours(img,lcontour,-1,(0,255,0),3) #img = 영상, lcontour = 그릴 경계선, -1(음수) = 모든 경계선 그리기 cf.양수: 해당 번호에 해당하는 경계선 하나만 출력, (0,255,0) = 초록색, 3 = 선 두께
             
cv.imshow('Original with contours',img)    
cv.imshow('Canny',canny)    

cv.waitKey()
cv.destroyAllWindows()