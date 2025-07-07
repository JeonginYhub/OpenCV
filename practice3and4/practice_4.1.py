import cv2 as cv

img = cv.imread("D:/practice_image/soccer.jpg")
gray=cv.cvtColor(img, cv.COLOR_BGR2GRAY)

grad_x = cv.Sobel(gray, cv.CV_32F, 1, 0, ksize=3) #x방향 미분 (32F = 32비트 float 맵, ksize=3 = 3x3 커널 사용)
grad_y = cv.Sobel(gray, cv.CV_32F, 0, 1, ksize=3) #y방향 미분

sobel_x = cv.convertScaleAbs(grad_x) #x방향 미분 결과를 절대값으로 변환
sobel_y = cv.convertScaleAbs(grad_y) #y방향 미분 결과를 절대값으로 변환

edge_strength = cv.addWeighted(sobel_x, 0.5, sobel_y, 0.5, 0) #x,y방향 미분 결과를 합쳐서 엣지 강도 계산

cv.imshow('Original', gray)
cv.imshow('Sobel X', sobel_x)
cv.imshow('Sobel Y', sobel_y)
cv.imshow('Edge Strength', edge_strength)

cv.waitKey()
cv.destroyAllWindows()