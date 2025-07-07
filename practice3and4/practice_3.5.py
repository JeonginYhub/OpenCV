import cv2 as cv
import numpy as np

img=cv.imread("D:\practice_image\soccer.jpg")
img=cv.resize(img, dsize=(0,0), fx=0.25, fy=0.25) #이미지 크기를 1/4로 축소

def gamma(f, gamma=1.0): #f : 입력 영상, gamma: 감마 값(기본 1로 설정)
    f1=f/255.0 #L=256이라고 가정 > 0~1로 정규화
    return np.uint8(255*(f1**gamma))

gc=np.hstack((gamma(img,0.5), gamma(img,0.75),gamma(img,1.0), gamma(img,2.0), gamma(img,3.0))) 

#gamma=1 > 원래 영상 유지, 1보다 작을 경우 밝아지고 커질 경우 어두워짐
cv.imshow('gamma', gc)

cv.waitKey()
cv.destroyAllWindows()