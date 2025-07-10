# LeNet-5로 MNIST 인식하기

import numpy as np
import tensorflow as tf
import tensorflow.keras.datasets as ds

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam

(x_train, y_train), (x_test, y_test) = ds.mnist.load_data() #손글씨 숫자 이미지(MNIST) 데이터셋을 불러오기
x_train = x_train.reshape(60000, 28, 28, 1) #이미지에 채널 차원(흑백: 1)을 추가
x_test = x_test.reshape(10000, 28, 28, 1)
x_train = x_train.astype('float32') / 255.0 #이미지 픽셀 값을 0~1 사이 값으로 바꾸기
x_test = x_test.astype('float32') / 255.0
y_train = tf.keras.utils.to_categorical(y_train, 10) #One-hot 인코딩
y_test = tf.keras.utils.to_categorical(y_test, 10)

cnn = Sequential()
cnn.add(Conv2D(6,(5,5), padding='same', activation='relu', input_shape=(28,28,1))) #첫 번째 합성곱층(Conv2D), 필터 6개, 크기 5x5, 입력 모양: (28, 28, 1), padding='same' → 이미지 크기 유지, relu: 음수는 0, 양수는 그대로 (활성화 함수)
cnn.add(MaxPooling2D(pool_size=(2,2), strides=2)) #정보 압축
cnn.add(Conv2D(16,(5,5),padding='valid', activation='relu')) #필터 16개
cnn.add(MaxPooling2D(pool_size=(2,2), strides=2))
cnn.add(Conv2D(120,(5,5),padding='valid', activation='relu')) #필터 120개
cnn.add(Flatten()) #이미지를 일렬로 펼치기
cnn.add(Dense(units=84, activation='relu')) #완전 연결층 (뉴런 84개)
cnn.add(Dense(units=10, activation='softmax')) #최종 출력층, 0~9까지 10개 숫자 중 하나를 확률로 예측

cnn.compile(loss='categorical_crossentropy', optimizer = Adam(learning_rate=0.001), metrics=['accuracy']) #손실 함수: 다중 분류 → categorical_crossentropy, 최적화 알고리즘: Adam, 평가 지표: 정확도
cnn.fit(x_train, y_train, batch_size=128, epochs=30, validation_data=(x_test,y_test), verbose=2) #128개씩 묶어서 학습 (batch), 총 30번 반복 (epochs)

res=cnn.evaluate(x_test, y_test, verbose=0)
print('정확률=', res[1]*100)