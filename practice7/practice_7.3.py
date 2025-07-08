import numpy as np
import tensorflow as tf
import tensorflow.keras.datasets as ds

from tensorflow.keras.models import Sequential #계산이 한쪽으로 흐르는 경우 Sequential 모델 사용 (이외: functinal API)
from tensorflow.keras.layers import Dense #다층 퍼셉트론을 구성하는 완전연결층 - Dense
from tensorflow.keras.optimizers import Adam #Adam 옵티마이저

(x_train, y_train), (x_test, y_test) = ds.mnist.load_data() #MNIST 손글씨 데이터셋을 train/test 나눠서 로드

#28x28 → 784 픽셀로 1차원 벡터로 평탄화
x_train = x_train.reshape(60000, 784)
x_test = x_test.reshape(10000, 784)

#픽셀 값 범위를 0~1로 정규화
x_train = x_train.astype(np.float32) / 255.0
x_test = x_test.astype(np.float32) / 255.0

# 정수형 라벨을 원-핫 인코딩
y_train = tf.keras.utils.to_categorical(y_train, 10)
y_test = tf.keras.utils.to_categorical(y_test, 10)

mlp = Sequential()
mlp.add(Dense(units=512, activation='tanh', input_shape=(784,))) #첫 번째 은닉층 (입력 784차원 → 출력 512 노드), 비선형 활성화 함수 하이퍼볼릭 탄젠트
mlp.add(Dense(units=10, activation='softmax')) #출력층 (클래스 10개 → 10 노드), softmax: 다중 클래스 확률 출력

mlp.compile(loss='MSE', optimizer=Adam(learning_rate=0.001), metrics=['accuracy']) #손실 함수: MSE, 옵티마이저: Adam(학습률 0.001), 평가 지표: 정확률 (accuracy)
mlp.fit(x_train,y_train,batch_size=128,epochs=50,validation_data=(x_test, y_test), verbose=2) #학습 데이터로 50 에폭 학습, 배치 크기: 128, 매 에폭마다 검증 데이터로 평가, verbose=2: 간결하게 학습 로그 출력

res=mlp.evaluate(x_test,y_test,verbose=0)
print('정확률=', res[1]*100) #res[1]: metrics=['accuracy']에 해당하는 결과값 > 정확률(%)로 변환해 출력