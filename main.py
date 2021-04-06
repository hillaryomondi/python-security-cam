import cv2
import winsound
cam = cv2.VideoCapture(0)
while cam.isOpened():
    #capturing 2 instance of the camera and making a compariosn
    ret, frame1 = cam.read()
    ret, frame2 = cam.read()
    diff = cv2.absdiff(frame1, frame2)

    #convert to gray color
    gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)

    #convert gray to a blur image
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)

    #Dilate the image
    dilated = cv2.dilate(thresh, None, iterations=3)

    #Add contours
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #Draw the contours
    #cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)

    #detecting bigger things in motion
    for c in contours:
        if cv2.contourArea(c) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(frame1, (x,y), (x+w, y+h), (0, 255, 0), 2)

        #implement smart alert sound asynchronously
        winsound.PlaySound('alert.wav', winsound.SND_ASYNC)
    if cv2.waitKey(10) == ord('q'):
        break
    cv2.imshow('Hillary cam', frame1)
