import skimage
import cv2 as cv
import numpy as np
import time
from skimage import io, color, segmentation, graph


coffee = skimage.data.coffee()

start = time.time()
slic = skimage.segmentation.slic(coffee, n_segments=600, compactness=20, start_label=1)
g = graph.rag_mean_color(coffee, slic, mode='similarity')
ncut = graph.cut_normalized(slic, g) #정규화 절단(slic1과 g 객체 정보 활용), 결과는 ncut 객체에 저장
print(coffee.shape, 'Coffee 영상을 분할하는 데 ', time.time() - start, '초 소요')

marking = skimage.segmentation.mark_boundaries(coffee, ncut)
ncut_coffee = np.uint8(marking * 255.0) #0~1 사이의 실수의 ncut_coffee를 0~255 사이의 uint8로 변환

cv.imshow('Normalized cut', cv.cvtColor(ncut_coffee, cv.COLOR_RGB2BGR))

cv.waitKey()
cv.destroyAllWindows()