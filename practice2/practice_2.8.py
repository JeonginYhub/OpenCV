import cv2 as cv
import sys

img=cv.imread('tree.jpg')

if img is None:
    sys.exit("파일을 찾을 수 없습니다.")
    
BrushSize = 5
LColor, RColor = (255,0,0), (0,0,255)

def painting(event, x, y, flags, param):
    
    if event == cv.EVENT_LBUTTONDOWN:  # 마우스 왼쪽 버튼 클릭하면 파랑
        cv.circle(img, (x,y), BrushSize, LColor, -1)
    elif event == cv.EVENT_RBUTTONDOWN:  # 마우스 오른쪽 버튼 클릭하면 빨강
        cv.circle(img, (x,y), BrushSize, RColor, -1)
    elif event == cv.EVENT_MOUSEMOVE and flags == cv.EVENT_FLAG_LBUTTON: # 왼쪽 버튼 클릭하고 이동하면 파랑
        cv.circle(img, (x,y), BrushSize, LColor, -1)
    elif event == cv.EVENT_MOUSEMOVE and flags == cv.EVENT_FLAG_RBUTTON: # 오른쪽 버튼 클릭하고 이동하면 빨강
        cv.circle(img, (x,y), BrushSize, RColor, -1)
        
    cv.imshow('Painting', img) # 수정된 영상을 다시 그림
    
cv.namedWindow('Painting')
cv.imshow('Painting', img)

cv.setMouseCallback('Painting', painting)

while(True):
    if cv.waitKey(1)==ord('q'):
        cv.destroyAllWindows()
        break