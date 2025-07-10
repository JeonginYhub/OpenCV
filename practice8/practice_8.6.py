import cv2 as cv 
import numpy as np
#ResNet50: Keras의 ImageNet 사전 학습 모델, preprocess_input: 모델에 맞게 이미지 전처리, decode_predictions: 모델의 예측결과 → 사람이 읽을 수 있게 변환
from tensorflow.keras.applications.resnet50 import ResNet50,preprocess_input,decode_predictions

model=ResNet50(weights='imagenet') #ImageNet으로 학습된 가중치를 읽어오라고 지시

img=cv.imread("D:/practice_image/rabbit.jpg")
x=np.reshape(cv.resize(img,(224,224)),(1,224,224,3)) #ResNet50은 입력 크기 224×224를 요구하므로 이미지 크기 변경, reshape을 통해 배치 차원 추가 → 모델 입력 shape: (1, 224, 224, 3)
x=preprocess_input(x) #ResNet50에 맞게 픽셀값 전처리

preds=model.predict(x) #이미지에 대해 예측 수행
top5=decode_predictions(preds,top=5)[0] #확률이 높은 상위 5개 클래스를 디코딩해서 반환
print('예측 결과:',top5)

for i in range(5):
    cv.putText(img,top5[i][1]+':'+str(top5[i][2]),(10,20+i*20),cv.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),1) #이미지에 Top 5 예측 결과를 위에서부터 아래로 출력


cv.imshow('Recognition result',img)

cv.waitKey()
cv.destroyAllWindows()