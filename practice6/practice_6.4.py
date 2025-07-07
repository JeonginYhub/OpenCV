import cv2 as cv
import numpy as np
from PyQt5.QtWidgets import *
import sys
import winsound

class TrafficWeak(QMainWindow): #PyQt5의 QMainWindow 상속 → 기본 윈도우 창 생성
    def __init__(self):
        super().__init__()
        self.setWindowTitle('교통약자 보호') #창 제목
        self.setGeometry(200,200,700,200) #창 위치 및 크기
       
        signButton=QPushButton('표지판 등록',self) #버튼 생성
        roadButton=QPushButton('도로 영상 불러옴',self)
        recognitionButton=QPushButton('인식',self)
        quitButton=QPushButton('나가기',self)
        self.label=QLabel('환영합니다!',self)
        
        signButton.setGeometry(10,10,100,30) #버튼 위치 조정
        roadButton.setGeometry(110,10,100,30)
        recognitionButton.setGeometry(210,10,100,30)
        quitButton.setGeometry(510,10,100,30)
        self.label.setGeometry(10,40,600,170)
        
        signButton.clicked.connect(self.signFunction) #버튼 기능 연결
        roadButton.clicked.connect(self.roadFunction) 
        recognitionButton.clicked.connect(self.recognitionFunction)        
        quitButton.clicked.connect(self.quitFunction)

        self.signFiles=[["D:\practice_image\child.png",'어린이'],["D:\practice_image\elder.png",'노인'],["D:\practice_image\disabled.png",'장애인']]	# 표지판 모델 영상
        self.signImgs=[]				# 표지판 모델 영상 저장
        
    def signFunction(self):
        self.label.clear()
        self.label.setText('교통약자 번호판을 등록합니다.')
        
        #self.signFiles: (파일경로, 이름) 형태 목록, 이미지 읽어와 self.signImgs에 저장하고 이미지 창에 각각 표시
        for fname,_ in self.signFiles:
            self.signImgs.append(cv.imread(fname))
            cv.imshow(fname,self.signImgs[-1])        

    def roadFunction(self):
        if self.signImgs==[]: 
            self.label.setText('먼저 번호판을 등록하세요.')
        else:
            fname=QFileDialog.getOpenFileName(self,'파일 읽기','./') #도로 이미지 선택 및 읽기
            self.roadImg=cv.imread(fname[0])
            if self.roadImg is None: sys.exit('파일을 찾을 수 없습니다.')  #실패시 종료
    
            cv.imshow('Road scene',self.roadImg)  #정상 로딩시 화면에 표시
        
    def recognitionFunction(self):
        if self.roadImg is None: 
            self.label.setText('먼저 도로 영상을 입력하세요.')
        else:
            sift=cv.SIFT_create() #SIFT 알고리즘 객체 생성
        
            KD=[] # 여러 표지판 영상의 키포인트와 기술자 저장
            for img in self.signImgs: 
                gray=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
                KD.append(sift.detectAndCompute(gray,None)) #키포인트 & 디스크립터 추출
                
            grayRoad=cv.cvtColor(self.roadImg,cv.COLOR_BGR2GRAY) # 도로영상 > 그레이 스케일로 변환
            road_kp,road_des=sift.detectAndCompute(grayRoad,None) # 키포인트 추출
                
            matcher=cv.DescriptorMatcher_create(cv.DescriptorMatcher_FLANNBASED) #FLANN 기반 매칭기 생성
            GM=[]			# 여러 표지판 영상의 good match를 저장
            for sign_kp,sign_des in KD: #각 표지판과 도로 영상 간 KNN 매칭
                knn_match=matcher.knnMatch(sign_des,road_des,2)
                T=0.7
                good_match=[] #거리 비율 기준으로 good match 선별
                for nearest1,nearest2 in knn_match:
                    if (nearest1.distance/nearest2.distance)<T:
                        good_match.append(nearest1)
                GM.append(good_match)     #Lowe's ratio test로 신뢰성 높은 매칭만 저장
   
            
            best=GM.index(max(GM,key=len)) # 매칭 쌍 개수가 최대인 번호판 찾기
            
            if len(GM[best])<4:	# 최선의 번호판이 매칭 쌍 4개 미만이면 실패
                self.label.setText('표지판이 없습니다.')  
            else:			# 성공(호모그래피 찾아 영상에 표시)
                sign_kp=KD[best][0]
                good_match=GM[best]
            
                points1=np.float32([sign_kp[gm.queryIdx].pt for gm in good_match])
                points2=np.float32([road_kp[gm.trainIdx].pt for gm in good_match])
                
                H,_=cv.findHomography(points1,points2,cv.RANSAC)
                
                h1,w1=self.signImgs[best].shape[0],self.signImgs[best].shape[1] # 번호판 영상의 크기
                h2,w2=self.roadImg.shape[0],self.roadImg.shape[1] # 도로 영상의 크기
                
                box1=np.float32([[0,0],[0,h1-1],[w1-1,h1-1],[w1-1,0]]).reshape(4,1,2) #표지판 영상의 네 꼭짓점을 도로 영상에 투영 변환
                box2=cv.perspectiveTransform(box1,H)
                
                self.roadImg=cv.polylines(self.roadImg,[np.int32(box2)],True,(0,255,0),4) #변환된 네모를 초록색으로 도로 영상에 표시
                
                img_match=np.empty((max(h1,h2),w1+w2,3),dtype=np.uint8) #표지판 이미지와 도로 영상을 가로로 나란히 붙임
                cv.drawMatches(self.signImgs[best],sign_kp,self.roadImg,road_kp,good_match,img_match,flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
                cv.imshow('Matches and Homography',img_match)
                
                self.label.setText(self.signFiles[best][1]+' 보호구역입니다. 30km로 서행하세요.')       #라벨에 해당 표지판 이름 및 경고 문구 표시           
                winsound.Beep(3000,500)    #3000Hz 소리 0.5초 재생
                      
    def quitFunction(self):
        cv.destroyAllWindows()        
        self.close()
                
app=QApplication(sys.argv) 
win=TrafficWeak() 
win.show()
app.exec_()