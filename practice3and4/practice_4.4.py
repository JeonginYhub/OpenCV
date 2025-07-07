import cv2 as cv 

img=cv.imread("D:/practice_image/apples.jpg")
gray=cv.cvtColor(img,cv.COLOR_BGR2GRAY)

apples=cv.HoughCircles(gray,cv.HOUGH_GRADIENT,1,200,param1=150,param2=20,minRadius=50,maxRadius=120)
#HoughCircles함수: 명암 영상에서 원을 검출해 중심과 반지름을 저장한 리스트 반환, cv.HOUGH_GRADIENT: 에지 방향 정보 활용, 1: 누적 배열 크기(1로 설정하면 입력 영상과 같은 크기), 200: 원 사이 최소 거리(작을수록 많은 원 검출)
#param1: Canny 엣지 검출의 상한 임계값(Thigh), param2: 원비최대 억제를 적용할때 쓰는 임계값, minRadius: 최소 반지름, maxRadius: 최대 반지름

for i in apples[0]: 
    cv.circle(img,(int(i[0]),int(i[1])),int(i[2]),(255,0,0),2)

cv.imshow('Apple detection',img)  

cv.waitKey()
cv.destroyAllWindows()