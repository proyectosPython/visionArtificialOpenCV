import cv2
import numpy as np

video = cv2.VideoCapture("video.mp4")
(grabbed, img1) = video.read()

img2 = None
img3 = None

i = 0
while True:
    i = i+1
    #print("i: ",i)
    (grabbed, img) = video.read()
    if not grabbed:
        break

    if i==200:
        img2 = img.copy()
        continue

    if i==300:
        img3 = img.copy()
        continue


#cv2.imshow("img1",img1)
#cv2.imshow("img2",img2)
#cv2.imshow("img3",img3)


#image1 = cv2.imread("img1.png",1)
#image2 = cv2.imread("img2.png",1)

difference = cv2.subtract(img3, img3 )

result = not np.any(difference) #if difference is all zeros it will return False

if result is True:
    print("The images are the same")
else:
    cv2.imshow("result", difference)
    print("the images are different")


cv2.waitKey(0)
cv2.destroyAllWindows()