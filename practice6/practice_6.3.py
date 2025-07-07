import cv2 as cv
import numpy as np
import sys
from PyQt5.QtWidgets import *

class Orim(QMainWindow): #PyQt5의 QMainWindow 상속 → 기본 윈도우 창 생성
    def __init__(self):
        super().__init__()
        self.setWindowTitle('오림') #창 제목
        self.setGeometry(200,200,700,200) #창 위치 및 크기
        
        fileButton = QPushButton('파일', self) #버튼 생성
        paintButton = QPushButton('페인팅', self)
        cutButton = QPushButton('오림', self)
        incButton = QPushButton('+', self)
        decButton = QPushButton('-', self)
        saveButton = QPushButton('저장', self)
        quitButton = QPushButton('나가기', self)
        
        fileButton.setGeometry(10,10,100,30) #버튼 위치 조정
        paintButton.setGeometry(110,10,100,30)
        cutButton.setGeometry(210,10,100,30)
        incButton.setGeometry(310,10,50,30)
        decButton.setGeometry(360,10,50,30)
        saveButton.setGeometry(410,10,100,30)
        quitButton.setGeometry(510,10,100,30)
        
        fileButton.clicked.connect(self.fileOpenFunction) #버튼 기능 연결
        paintButton.clicked.connect(self.paintFunction)
        cutButton.clicked.connect(self.cutFunction)
        incButton.clicked.connect(self.incFunction)
        decButton.clicked.connect(self.decFunction)
        saveButton.clicked.connect(self.saveFunction)
        quitButton.clicked.connect(self.quitFunction)
        
        self.BrushSiz = 5 #페인팅 붓 크기
        self.Lcolor, self.Rcolor = (255,0,0), (0,0,255) #파란색 물체, 빨간색 배경
        
    def fileOpenFunction(self):
        fname = QFileDialog.getOpenFileName(self,'Open file','./') #파일 선택 창
        self.img = cv.imread(fname[0]) #이미지 읽기
        if self.img is None: sys.exit('파일을 찾을 수 없습니다.') #오류 시 종료
        
        self.img_show = np.copy(self.img) #표시용 영상
        cv.imshow('Painting', self.img_show)
        
        self.mask=np.zeros((self.img.shape[0], self.img.shape[1]),np.uint8)
        self.mask[:,:]=cv.GC_PR_BGD # 모든 화소를 배겨일 것 같음으로 초기화
        
    def paintFunction(self):
        cv.setMouseCallback('Painting', self.painting) #마우스 이벤트 연결
        
    # self.img_show: 사용자 보이는 화면에 색 표시
    # self.mask: GrabCut용 마스크에 전경(1), 배경(0) 표시    
    def painting(self, event, x, y, flags, param):
        if event == cv.EVENT_LBUTTONDOWN:
            cv.circle(self.img_show, (x,y), self.BrushSiz, self.Lcolor, -1) #왼쪽 버튼 - 파란색
        elif event==cv.EVENT_RBUTTONDOWN:
            cv.circle(self.img_show, (x,y), self.BrushSiz,self.Rcolor,-1) #오른쪽 버튼 - 빨간색
            cv.circle(self.mask,(x,y),self.BrushSiz, cv.GC_BGD, -1)
        elif event == cv.EVENT_MOUSEMOVE and flags==cv.EVENT_FLAG_LBUTTON:
            cv.circle(self.img_show,(x,y),self.BrushSiz,self.Lcolor,-1) # 왼쪽 버튼 클릭하고 이동 - 파란색
            cv.circle(self.mask,(x,y),self.BrushSiz,cv.GC_FGD,-1)
        elif event == cv.EVENT_MOUSEMOVE and flags==cv.EVENT_FLAG_RBUTTON:
            cv.circle(self.img_show,(x,y),self.BrushSiz,self.Rcolor,-1) # 오른쪽 버튼 클릭하고 이동 - 빨간색
            cv.circle(self.mask,(x,y),self.BrushSiz,cv.GC_BGD,-1)
            
        cv.imshow('Painting', self.img_show)
        
    def cutFunction(self):
        background=np.zeros((1,65),np.float64)
        foreground=np.zeros((1,65),np.float64)
        cv.grabCut(self.img, self.mask, None, background, foreground, 5, cv.GC_INIT_WITH_MASK)
        #self.img: 원본 이미지, self.mask: 사용자 전경/배경 표시 반영, cv.GC_INIT_WITH_MASK: 마스크 기반 GrabCut 실행
        mask2 = np.where((self.mask == cv.GC_FGD) | (self.mask == cv.GC_PR_FGD), 1, 0).astype('uint8')
        self.grabImg = self.img*mask2[:,:,np.newaxis]
        cv.imshow('Scissoring', self.grabImg)
        
    def incFunction(self):
        self.BrushSiz=min(20, self.BrushSiz+1) #최대 20
        
    def decFunction(self):
        self.BrushSiz = max(1,self.BrushSiz-1) #최소 1
        
    def saveFunction(self):
        fname=QFileDialog.getSaveFileName(self,'파일 저장','./')
        cv.imwrite(fname[0],self.grabImg)
        
    def quitFunction(self):
        cv.destroyAllWindows()
        self.close()
        
app = QApplication(sys.argv)
win=Orim()
win.show()
app.exec_()