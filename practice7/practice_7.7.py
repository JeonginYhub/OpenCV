import numpy as np
import tensorflow as tf
import cv2 as cv 
import matplotlib.pyplot as plt
import winsound

model=tf.keras.models.load_model('dmlp_trained.h5') #신경망 파일을 읽어 dmlp 객체에 저장

def reset(): #e명령어 수행
    global img #img 전역변수 선언 - 다른 함수와 img 공유
       
    img=np.ones((200,520,3),dtype=np.uint8)*255 #200x520 크기의 흰색 이미지 생성(모든 화소가 255=흰색)
    for i in range(5): #지정된 위치에 5개 빨간색 박스 그리기
        cv.rectangle(img,(10+i*100,50),(10+(i+1)*100,150),(0,0,255))
    cv.putText(img,'e:erase s:show r:recognition q:quit',(10,40),cv.FONT_HERSHEY_SIMPLEX,0.8,(255,0,0),1) #e: 박스 지우기, s: 박스에서 숫자를 떼내 명암 영상 표시, r: 인식, q: 종료

def grab_numerals():
    numerals=[]
    for i in range(5):
        roi=img[51:149,11+i*100:9+(i+1)*100,0]
        roi=255-cv.resize(roi,(28,28),interpolation=cv.INTER_CUBIC)
        numerals.append(roi)  
    numerals=np.array(numerals)
    return numerals

def show(): #s명령어 수행
    numerals=grab_numerals() #함수로 5개 숫자 떼어내기
    plt.figure(figsize=(25,5))
    for i in range(5):
        plt.subplot(1,5,i+1)
        plt.imshow(numerals[i],cmap='gray')
        plt.xticks([]); plt.yticks([])
    plt.show()
    
def recognition(): #r명령어 수행
    numerals=grab_numerals()
    numerals=numerals.reshape(5,784) #reshape 함수로 2차원 구조를 1차원으로 펼치기
    numerals=numerals.astype(np.float32)/255.0 #실수 배열로 바꾸고 255로 나누어 0~1 범위로 정규화
    res=model.predict(numerals) # 신경망 모델로 예측
    class_id=np.argmax(res,axis=1)
    for i in range(5):
        cv.putText(img,str(class_id[i]),(50+i*100,180),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),1)
    winsound.Beep(1000,500)    
        
BrushSiz=4
LColor=(0,0,0)

def writing(event,x,y,flags,param): #마우스 콜백 함수 - 마우스 왼쪽 버튼 클릭 or 누른 채 이동 : BrushSiz 크기의 원을 그려 글씨 쓰기
    if event==cv.EVENT_LBUTTONDOWN:
        cv.circle(img,(x,y),BrushSiz,LColor,-1) 
    elif event==cv.EVENT_MOUSEMOVE and flags==cv.EVENT_FLAG_LBUTTON: 
        cv.circle(img,(x,y),BrushSiz,LColor,-1)

reset() #프로그램 메인
cv.namedWindow('Writing') #윈도우 생성
cv.setMouseCallback('Writing',writing) #윈도우 콜백 함수로 writing 함수 등록

while(True):
    cv.imshow('Writing',img)
    key=cv.waitKey(1)
    if key==ord('e'):
        reset()
    elif key==ord('s'):
        show()        
    elif key==ord('r'):
        recognition()
    elif key==ord('q'):
        break
    
cv.destroyAllWindows()