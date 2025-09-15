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
    return mp_hands,hands,mp_draw

               


#test : process every single frame to return those three parames >> stop,shoot,gesture
#mp_hands,hands,mp_draw,font,cap = prepare_tracking()
#stop,shoot,gesture = process_frame(mp_hands,hands,mp_draw,font,cap)
#print(stop,shoot,gesture)


    