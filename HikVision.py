import numpy as np
import cv2

cap = cv2.VideoCapture()
cap.open("rtsp://admin:Nashua123@192.168.68.132:554/Streaming/Channels/1502/")

while(True):
     # Capture frame-by-frame
    ret, frame = cap.read()
    #cv2.imwrite("holo.jpg", frame)
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()