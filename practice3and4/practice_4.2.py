import cv2 as cv

img=cv.imread("D:/practice_image/soccer.jpg")

gray=cv.cvtColor(img, cv.COLOR_BGR2GRAY)

canny1 = cv.Canny(gray, 50, 150) #첫 번째 Canny 엣지 검출 (Tlow=50, Thigh=150)
canny2 = cv.Canny(gray, 100, 200) #두 번째 Canny 엣지 검출 (Tlow=100, Thigh=200)

cv.imshow('Original', gray)
cv.imshow('Canny 1', canny1)
cv.imshow('Canny 2', canny2)

cv.waitKey()
cv.destroyAllWindows()

#임계값이 높을수록 에지 강도가 큰 화소만 추적 > 더 적은 에지 발생(등번호 3 일부 손실)
#임계값이 낮은 경우 등번호 3이 온전히 검출, 잔디밭에서 잡음 에지 다수 발생