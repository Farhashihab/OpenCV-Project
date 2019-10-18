import cv2
import numpy as np

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(grey,threshold1=50,threshold2=250,apertureSize=5,L2gradient=True)

    lines = cv2.HoughLines(edges, 1,np.pi/180,250) #lines in the polar cordinate

    if lines is not None:
        for rho,theta in lines[0]:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            pts1 =(int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
            pst2 =(int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
            cv2.line(frame,pts1 ,pst2,(0,255,0),3)

    print(lines)

    cv2.imshow('Gray', frame)
    # cv2.imshow('LInes',lines)
    # cv2.imshow('frame2', output)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
