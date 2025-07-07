from PyQt5.QtWidgets import *
import cv2 as cv
import numpy as np
import winsound
import sys
   
class Panorama(QMainWindow) : #PyQt5의 QMainWindow 상속 → 기본 윈도우 창 생성
    def __init__(self) :
        super().__init__()
        self.setWindowTitle('파노라마 영상') #창 제목
        self.setGeometry(200,200,700,200) #창 위치 및 크기
        
        collectButton=QPushButton('영상 수집',self) # 버튼 생성
        self.showButton=QPushButton('영상 보기',self) 
        self.stitchButton=QPushButton('봉합',self) 
        self.saveButton=QPushButton('저장',self)
        quitButton=QPushButton('나가기',self)
        self.label=QLabel('환영합니다!',self)
        
        collectButton.setGeometry(10,25,100,30) #버튼 위치 조정
        self.showButton.setGeometry(110,25,100,30) 
        self.stitchButton.setGeometry(210,25,100,30) 
        self.saveButton.setGeometry(310,25,100,30)
        quitButton.setGeometry(450,25,100,30) 
        self.label.setGeometry(10,70,600,170)

        self.showButton.setEnabled(False) #비활성 설정(클릭불가하게 설정) - 영상 수집이 끝나야 수행할 수 있는 단계
        self.stitchButton.setEnabled(False) 
        self.saveButton.setEnabled(False)
        
        collectButton.clicked.connect(self.collectFunction) #버튼 기능 연결
        self.showButton.clicked.connect(self.showFunction)       
        self.stitchButton.clicked.connect(self.stitchFunction) 
        self.saveButton.clicked.connect(self.saveFunction)   
        quitButton.clicked.connect(self.quitFunction)        

    def collectFunction(self):
        self.showButton.setEnabled(False) 
        self.stitchButton.setEnabled(False) 
        self.saveButton.setEnabled(False)
        self.label.setText('c를 여러 번 눌러 수집하고 끝나면 q를 눌러 비디오를 끕니다.')
        
        self.cap=cv.VideoCapture(0,cv.CAP_DSHOW) #웹캠 연결 (0 기본 카메라), 연결 실패 시 종료
        if not self.cap.isOpened(): sys.exit('카메라 연결 실패')
        
        self.imgs=[]   
        while True: #프레임 읽기, 실패 시 종료
            ret,frame=self.cap.read()  
            if not ret: break
            
            cv.imshow('video display', frame)
            
            key=cv.waitKey(1) 
            if key==ord('c'):            
                self.imgs.append(frame)	# 영상 저장
            elif key==ord('q'):
                self.cap.release() 
                cv.destroyWindow('video display')                
                break  #영상 종료
        
        if len(self.imgs)>=2:		# 수집한 영상이 2장 이상이면 버튼 활성화
            self.showButton.setEnabled(True) 
            self.stitchButton.setEnabled(True) 
            self.saveButton.setEnabled(True)        
                    
    def showFunction(self):
        self.label.setText('수집된 영상은 '+str(len(self.imgs))+'장 입니다.') #수집 이미지 개수 표시
        stack=cv.resize(self.imgs[0],dsize=(0,0),fx=0.25,fy=0.25) #이미지 25%로 축소, 가로로 이어붙이기
        for i in range(1,len(self.imgs)):
            stack=np.hstack((stack,cv.resize(self.imgs[i],dsize=(0,0),fx=0.25,fy=0.25))) 
        cv.imshow('Image collection',stack)      #결과 창에 표시  
        
    def stitchFunction(self): #OpenCV의 파노라마 생성 객체 생성, 이미지 리스트로 파노라마 합성 시도
        stitcher=cv.Stitcher_create()
        status,self.img_stitched=stitcher.stitch(self.imgs)
        if status==cv.STITCHER_OK:
            cv.imshow('Image stitched panorama',self.img_stitched)     #합성 성공 시 결과 창 표시
        else:
            winsound.Beep(3000,500)            
            self.label.setText('파노라마 제작에 실패했습니다. 다시 시도하세요.')    #실패 시 경고음 & 안내 문구 표시
            
    def saveFunction(self):
        fname=QFileDialog.getSaveFileName(self,'파일 저장','./')
        cv.imwrite(fname[0],self.img_stitched)
        
    def quitFunction(self): 
        self.cap.release() 
        cv.destroyAllWindows()  
        self.close()

app=QApplication(sys.argv) 
win=Panorama() 
win.show()
app.exec_()