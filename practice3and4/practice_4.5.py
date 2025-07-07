import skimage
import numpy as np
import cv2 as cv

img=skimage.data.coffee()
cv.imshow('Coffee image', cv.cvtColor(img, cv.COLOR_RGB2BGR))

slic1 = skimage.segmentation.slic(img, n_segments=600, compactness=20) #slic 함수 > 슈퍼화소분할, slic1 객체에 저장 / compactness: 슈퍼화소 모양 조절 - 값이 클수록 네모에 가까워짐 / n_segments: 슈퍼화소 개수
sp_img1 = skimage.segmentation.mark_boundaries(img, slic1)
sp_img1 = np.uint8(sp_img1 * 255.0) #0~1 사이의 실수의 sp_img1을 0~255 사이의 unit8로 변환

slic2 = skimage.segmentation.slic(img, n_segments=600, compactness=40)
sp_img2 = skimage.segmentation.mark_boundaries(img, slic2)
sp_img2 = np.uint8(sp_img2 * 255.0)

cv.imshow('Super pixels (compact 20)', cv.cvtColor(sp_img1, cv.COLOR_RGB2BGR))
cv.imshow('Super pixels (compact 40)', cv.cvtColor(sp_img2, cv.COLOR_RGB2BGR))

cv.waitKey()
cv.destroyAllWindows()

