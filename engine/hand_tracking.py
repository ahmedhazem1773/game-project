import cv2
import mediapipe as mp

def hand_gestures(landmarks,tol=.002): #this class track finger landmarks to detect gestures as commands  
    #add 0.002 tolerance for tracking
    min_y=min(lm.y for lm in landmarks.landmark)
    max_y=max(lm.y for lm in landmarks.landmark)
    min_x=min(lm.x for lm in landmarks.landmark)
    thump_tip = landmarks.landmark[4]
    index_finger_tip = landmarks.landmark[8]

    if abs(thump_tip.y-min_y)<=tol:
        gesture=1
    elif abs(thump_tip.y-max_y)<=tol:   
        gesture=-1
    else :
        gesture=0    
    if index_finger_tip.x-min_x>=tol:
        shooting = True     
    else :
        shooting = False  
    return gesture,shooting     

def checkpause(landmarks,tol=.02): # this class check if hand is open by tracking the middle finger tip
    min_y=min(lm.y for lm in landmarks.landmark)
    return tol>abs(landmarks.landmark[12].y-min_y)

def label_color(label): #this class give different colors for right and left hand 
    if label=='Right': #c_color and l_color is the circle and line colors
        c_color=(0,0,255)
        l_color=(0,0,0)
    else:
        c_color=(255,0,0)
        l_color=(0,0,0)
    return c_color,l_color    

def prepare_tracking():
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False,max_num_hands=2,min_detection_confidence=0.6,min_tracking_confidence=0.6)
    mp_draw=mp.solutions.drawing_utils
    font = cv2.FONT_HERSHEY_SIMPLEX
    cap = cv2.VideoCapture(0)
    return mp_hands,hands,mp_draw,font,cap

def process_frame(mp_hands,hands,mp_draw,font,cap,c_width,c_hight):
    while True:
        #read and flip the frame
        ret,frame = cap.read()
        frame= cv2.flip(frame , 1 )
        if not ret:
            break
        f_hight,f_width,_=frame.shape #frame hight and width
        image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB) 
        results = hands.process(image)
        stop,shoot,gesture=False,False,None
        
        if results.multi_hand_landmarks: #if camera detect a hand >> true
            open_right,open_left=False,False
            for hand_landmarks,handness in zip(results.multi_hand_landmarks,results.multi_handedness):
                label = handness.classification[0].label #classify the hands to left and right
                c_color,l_color = label_color(label)
                draw_circle=mp_draw.DrawingSpec(color=c_color,thickness=2,circle_radius=4)
                draw_line=mp_draw.DrawingSpec(color=l_color,thickness=2)
                mp_draw.draw_landmarks(frame,hand_landmarks,mp_hands.HAND_CONNECTIONS,draw_circle,draw_line)

                if label == "Right": # take the gesture from the right hand to control the game
                    gesture,shoot = hand_gestures(hand_landmarks) 
                    open_right=checkpause(hand_landmarks)
                if label == "Left": 
                    open_left=checkpause(hand_landmarks)    
                if open_left and open_right : #if poth left and right hand are open , stop the game
                    stop=1
        
        else : #if camera detect no hands
            cv2.putText(frame,text='NO HANDS DETECTED',org=(f_width//8,f_hight//2), fontFace=font,fontScale=1.5 ,color=(0,0,255),thickness=3,lineType=cv2.LINE_AA)

        display_frame=cv2.resize(frame,(c_width,c_hight)) #this is the frame to be displayed
        display_frame = cv2.cvtColor(display_frame,cv2.COLOR_BGR2RGB)
        if cv2.waitKey(1) & 0xFF == 27:
            break
        return display_frame,stop,shoot,gesture                 


#test : process every single frame to return those three parames >> stop,shoot,gesture
#mp_hands,hands,mp_draw,font,cap = prepare_tracking()
#stop,shoot,gesture = process_frame(mp_hands,hands,mp_draw,font,cap)
#print(stop,shoot,gesture)


    