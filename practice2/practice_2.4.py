import cv2 as cv
import sys

img= cv.imread(cv.samples.findFile("tree.jpg"))

if img is None:
    sys.exit("파일을 찾을 수 없습니다.")
    
cv.imshow("Image Display", img)

cv.waitKey(0)  # Wait for a key press indefinitely
cv.destroyAllWindows()  # Close all OpenCV windows

print(img.shape)

print(img[0,0,0], img[0,0,1], img[0,0,2])  # Print the BGR values of the pixel at (0, 0)