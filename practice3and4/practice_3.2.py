import cv2 as cv
import matplotlib.pyplot as plt

img=cv.imread("D:/practice_image/soccer.jpg")

if img is None:
    print("이미지를 불러올 수 없습니다. 경로를 확인하세요.")
    exit()

h=cv.calcHist([img],[2],None,[256],[0,256])
plt.plot(h, color='r',linewidth=1)