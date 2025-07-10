import tensorflow.keras.datasets as ds
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt

(x_train, y_train), (x_test, y_test) = ds.cifar10.load_data()  # CIFAR-10 데이터셋 불러오기
x_train = x_train.astype('float32'); x_train/=255  # 픽셀 값을 0~1 사이로 정규화
x_train = x_train[0:15,]; y_train=y_train[0:15,]  # 앞 15개에 대해서만 증대 적용 - 증강 결과 간단히 시각화
class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'flog', 'horse', 'ship', 'truck']

plt.figure(figsize=(20,2))
plt.suptitle('First 15 images in the train set')
for i in range(15):
    plt.subplot(1,15,i+1) #1행 15열로 이미지 시각화
    plt.imshow(x_train[i])
    plt.xticks([]); plt.yticks([])
    plt.title(class_names[int(y_train[i])]) #이미지 위에 클래스 이름 표시
plt.show()

batch_siz = 4
#회전: 최대 ±20도까지 랜덤 회전, 가로/세로 이동: 전체 너비/높이의 최대 20%까지 이동, 좌우 반전: 랜덤하게 수행
generator = ImageDataGenerator(rotation_range=20.0, width_shift_range=0.2, height_shift_range=0.2, horizontal_flip=True)
gen=generator.flow(x_train, y_train, batch_size=batch_siz) #flow()는 x/y 데이터를 받아서 증강 이미지를 배치(batch) 단위로 무한히 생성해주는 객체

for a in range(3):
    img, label= next(gen) #next(gen)로 증강된 이미지 4개씩 받아옴, 이를 가로로 나열해서 시각화, 총 3번 반복해서 총 12개 증강 결과를 확인함
    plt.figure(figsize=(8,2.4))
    plt.suptitle("Generatior trial "+str(a+1))
    for i in range(batch_siz):
        plt.subplot(1, batch_siz, i+1)
        plt.imshow(img[i])
        plt.xticks([]); plt.yticks([])
        plt.title(class_names[int(label[i])])
    plt.show()