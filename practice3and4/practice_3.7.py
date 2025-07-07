import cv2 as cv
import numpy as np

img=cv.imread("D:\practice_image\soccer.jpg")
img=cv.resize(img, dsize=(0,0), fx=0.4, fy=0.4)
gray=cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.putText(gray, 'soccer', (10,20),cv.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),2) #스무딩 효과를 보기 위해 글씨 삽입
cv.imshow('Original', gray)

smooth = np.hstack((cv.GaussianBlur(gray,(5,5),0.0),cv.GaussianBlur(gray,(9,9),0.0),cv.GaussianBlur(gray,(15,15),0.0))) #hstack으로 영상 3개 이어붙임
#gray = 스무딩을 적용할 영상, (x,x) = 필터 크기 > 필터 크기가 작으면 약한 흐림, 크면 강한 흐림
cv.imshow('Smooth', smooth)

femboss=np.array([[-1.0,0.0,0.0],
                  [0.0,0.0,0.0],
                  [0.0,0.0,1.0]])

#cv.filter2D는 결과를 원래 이미지와 같은 uint8로 변환하기 때문에 값 손실 방지를 위해 128을 더해 중간 밝기로 기준 잡음
gray16 = np.int16(gray) #음수를 표현하가 위해 np.int16함수를 적용해 부호가 있는 16비트형으로 변환
emboss=np.uint8(np.clip(cv.filter2D(gray16, -1, femboss) + 128, 0, 255)) #결과 영상 uint8로 변환
emboss_bad = np.uint8(cv.filter2D(gray16, -1, femboss) + 128) #nplclip을 생략했는데 적용하지 않았을 때 부작용
emboss_worse = cv.filter2D(gray, -1, femboss) #np.int16형으로 변환하지 않았을 때 부작용

cv.imshow('Emboss', emboss)
cv.imshow('Emboss_bad', emboss_bad)
cv.imshow('Emboss_worse', emboss_worse)

cv.waitKey()
cv.destroyAllWindows()