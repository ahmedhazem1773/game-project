import cv2
import mediapipe as mp
def find_bm_tp (x, n) :
    if n==1 :
        for index , lm in enumerate(x.landmark ):
            if index == 9:
                bottom = lm
            if index == 12:
                top = lm
        return top, bottom
    elif n==0:
        for index , lm in enumerate(x.landmark ):
            if index == 9:
                bottom = lm
            if index == 12:
                top = lm
        return top, bottom
mp_hands = mp.solutions.hands #choose hand detector class
hands = mp_hands.Hands() #creat hand detector obj and it has default values  def __init__(self,static_image_mode=False,max_num_hands=2,model_complexity=1,min_detection_confidence=0.5,min_tracking_confidence=0.5)
drawing_mp=mp.solutions.drawing_utils #choose frawing class
cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX
while True:
    ret, frame = cap.read()
    frame= cv2.flip(frame , 1 )
    if not ret:
        break
    #this module work on rgb frames
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame) #use methode to bring back points of each hand
    if results.multi_hand_landmarks: #checks if there hand or not 
        for num_of_hands, hand_landmarks in enumerate(results.multi_hand_landmarks):
            if num_of_hands ==1 :
                hand_two= find_bm_tp(hand_landmarks , num_of_hands)
                # print(hand_one[0].y ,hand_two[0].y )
                print("i work")
            else :
                hand_two=False
            if num_of_hands==0 :
                hand_one= find_bm_tp(hand_landmarks , num_of_hands)
            #draw lines between point in each hand it tkes 
            # frame u will show (bgr) , indevual hand as set of points , method of class hand called hand_connection  
            # if i didn't pass last para it will draw only points without connecting them 
            #we can access each point by call attribute of hand (hand_landmarks.landmark )it will return something like list of coordinates of each point all as a one ele is a list

            # u notice each point its coordinates in decimal because it reperesented in  relative to width and height
            #to access to one coordinate call it as attribute because it don"t has slicing 
            # notice that y represennted as in plt so the highest point is closest to zero
           
            drawing_mp.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    else :
        hand_one=False
        hand_two=False 
    cv2.putText(frame,text='right hand :',org=(10,50), fontFace=font,fontScale= 1,color=(255,255,255),thickness=2,lineType=cv2.LINE_AA)
    cv2.putText(frame,text='left hand :',org=(10,90), fontFace=font,fontScale= 1,color=(255,255,255),thickness=2,lineType=cv2.LINE_AA)
    if hand_one:
        if hand_one[1].y> hand_one[0].y :
            cv2.putText(frame,text='opened',org=(200,50), fontFace=font,fontScale= 1,color=(0,255,0),thickness=2,lineType=cv2.LINE_AA)
        else :
            cv2.putText(frame,text='closed',org=(200,50), fontFace=font,fontScale= 1,color=(0,0,255),thickness=2,lineType=cv2.LINE_AA)
    if hand_two :
        if hand_two[1].y> hand_two[0].y:
            cv2.putText(frame,text='opened',org=(200,90), fontFace=font,fontScale= 1,color=(0,255,0),thickness=2,lineType=cv2.LINE_AA)
        else :
            cv2.putText(frame,text='closed',org=(200,90), fontFace=font,fontScale= 1,color=(0,0,255),thickness=2,lineType=cv2.LINE_AA)
    cv2.imshow('MediaPipe Hands', frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break
cap.release()
cv2.destroyAllWindows()