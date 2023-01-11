import cv2
import time
from emailing import send_email

video = cv2.VideoCapture(0)
time.sleep(3)

frist_frame = None
cont_fact = 0
status_list = [0, 0]

while True:
    status = 0
    check, frame = video.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)
    
    if frist_frame is None and cont_fact < 10:
        cont_fact += 1
        continue
    elif frist_frame is None and cont_fact >= 10:
        frist_frame = gray_frame_gau
        
    delta_frame = cv2.absdiff(frist_frame, gray_frame_gau)
    
    
    thresh_frame = cv2.threshold(delta_frame, 48, 255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)
    
    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) < 11000:
            status_flag = False
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0))
        if rectangle.any() and  not status_flag:
            status = 1
            
        
           
    status_list.append(status)
    status_list = status_list[-2:]
    
    if status_list[0] == 0 and status_list[1] == 1:
        send_email()
        
    status_list.append(status)
    
    cv2.imshow("Video", frame)
            
    key = cv2.waitKey(1)
    if key == ord("q"):
        break


video.release()

