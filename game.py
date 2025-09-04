import cv2
import mediapipe as mp 
import view
player= view.visual()
cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX
while True:
    ret, frame = cap.read()
    frame= cv2.flip(frame , 1 )
    if not ret:
        break
    #this module work on rgb frames
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = player.hands.process(rgb_frame) #use methode to bring back points of each hand
    frame , position=player.check_for_detector(results , frame) 
    cv2.putText(frame,text=' hand :',org=(10,50), fontFace=font,fontScale= 1,color=(255,255,255),thickness=2,lineType=cv2.LINE_AA)
    if position:
        player.checker_for_opening(frame)
    else :
        cv2.putText(frame,text='no hand detected',org=(150,50), fontFace=font,fontScale= 1,color=(0,0,255),thickness=2,lineType=cv2.LINE_AA)
    cv2.imshow('MediaPipe Hands', frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break
cap.release()
cv2.destroyAllWindows()
