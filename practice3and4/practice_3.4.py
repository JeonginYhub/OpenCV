import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

img=cv.imread("D:/practice_image/JohnHancocksSignature.png", cv.IMREAD_UNCHANGED) #모든 인수를 읽어오게 설정

t,bin_img = cv.threshold(img[:,:,3],0,255,cv.THRESH_BINARY+cv.THRESH_OTSU) #이미지의 3번 채널에 오츄 이진화를 적용한 결과를 bin_img에 저장
plt.imshow(bin_img, cmap='gray'), plt.xticks([]), plt.yticks([]) #cmap='gray' > 명암 영상 출력
plt.show()

b=bin_img[bin_img.shape[0]//2:bin_img.shape[0],0:bin_img.shape[0]//2+1]
plt.imshow(b,cmap='gray'), plt.xticks([]), plt.yticks([])
plt.show()

se=np.uint8([[0,0,1,0,0],
             [0,1,1,1,0],
             [1,1,1,1,1],
             [0,1,1,1,0],
             [0,0,1,0,0]])

b_dilation = cv.dilate(b,se,iterations=1) #팽창 연산, iterations: 적용 회수를 나타내는 매개변수
plt.imshow(b_dilation,cmap='gray'), plt.xticks([]), plt.yticks([])
plt.show()

b_erosion = cv.erode(b,se,iterations=1) #침식 연산
plt.imshow(b_erosion,cmap='gray'), plt.xticks([]), plt.yticks([])
plt.show()

b_closing = cv.erode(cv.dilate(b,se,iterations=1), se, iterations = 1) #팽창 연산 후 침식 연산
plt.imshow(b_closing,cmap='gray'), plt.xticks([]), plt.yticks([])
plt.show()