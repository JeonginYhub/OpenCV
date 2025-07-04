import cv2 as cv
import sys

img=cv.imread('tree.jpg')

if img is None:
    sys.exit("파일을 찾을 수 없습니다.")
    
cv.rectangle(img, (830,30), (1000,200), (0,0,255), 2)
cv.putText(img, "Tree", (830,24), cv.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
cv.imshow('draw', img)

cv.waitKey()
cv.destroyAllWindows()

## -----

import cv2 as cv
import sys

img=cv.imread('tree.jpg')

if img is None:
    sys.exit("파일을 찾을 수 없습니다.")
    
def draw(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN: # 마우스 왼쪽 버튼 클릭
        cv.rectangle(img, (x,y), (x+200, y+200), (0,0,255), 2)
    elif event == cv.EVENT_RBUTTONDOWN: # 마우스 오른쪽 버튼 클릭
        cv.rectangle(img, (x,y), (x+100, y+100), (255,0,0), 2)
        
    cv.imshow('Drawing', img)
    
cv.namedWindow('Drawing')
cv.imshow('Drawing', img)

cv.setMouseCallback('Drawing', draw)

while(True):
    if cv.waitKey(1)==ord('q'):
        cv.destroyAllWindows()
        break

## ---


import cv2 as cv
import sys

img=cv.imread('tree.jpg')

if img is None:
    sys.exit("파일을 찾을 수 없습니다.")
    
def draw(event, x, y, flags, param):
    global ix, iy
    
    if event == cv.EVENT_LBUTTONDOWN:  # 마우스 왼쪽 버튼 클릭했을 때 초기 위치 저장
        ix, iy = x, y
    elif event == cv.EVENT_LBUTTONUP:  # 마우스 왼쪽 버튼 클릭했을 때 직사각형 그리기
        cv.rectangle(img, (ix, iy), (x,y), (0,0,255), 2)
        
    cv.imshow('Drawing', img)
    
cv.namedWindow('Drawing')
cv.imshow('Drawing', img)

cv.setMouseCallback('Drawing', draw)

while(True):
    if cv.waitKey(1)==ord('q'):
        cv.destroyAllWindows()
        break