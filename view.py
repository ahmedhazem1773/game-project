import cv2
import mediapipe as mp 
class visual :
    def __init__(self ):
        self.position = 0
        self.recording = False
        self.mp_hands = mp.solutions.hands #choose hand detector class
        self.hands = self.mp_hands.Hands(max_num_hands=1) #creat hand detector obj and it has default values  def __init__(self,static_image_mode=False,max_num_hands=2,model_complexity=1,min_detection_confidence=0.5,min_tracking_confidence=0.5)
        self.drawing_mp=mp.solutions.drawing_utils #choose frawing class
    def check_for_detector (self , results , frame) :
        if results.multi_hand_landmarks: #checks if there hand or not 
            for hand_landmarks in results.multi_hand_landmarks:
                for index , lm in enumerate(hand_landmarks.landmark ):
                    if index ==0 :
                        self.palm = lm
                    if index == 9:
                        self.bottom = lm
                    if index == 12:
                        self.top = lm
                        #draw lines between point in each hand it tkes 
                        # frame u will show (bgr) , indevual hand as set of points , method of class hand called hand_connection  
                        # if i didn't pass last para it will draw only points without connecting them 
                        #we can access each point by call attribute of hand (hand_landmarks.landmark )it will return something like list of coordinates of each point all as a one ele is a list

                        # u notice each point its coordinates in decimal because it reperesented in  relative to width and height
                        #to access to one coordinate call it as attribute because it don"t has slicing 
                        # notice that y represennted as in plt so the highest point is closest to zero
                self.drawing_mp.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
        else :
            self.palm= False
        return frame , self.palm
    def checker_for_opening (self , frame) :
        font = cv2.FONT_HERSHEY_SIMPLEX
        if (self.bottom.y> self.top.y )and (self.palm.y > self.top.y) :
            cv2.putText(frame,text='opened',org=(150,50), fontFace=font,fontScale= 1,color=(0,255,0),thickness=2,lineType=cv2.LINE_AA)
        else :
            cv2.putText(frame,text='closed',org=(150,50), fontFace=font,fontScale= 1,color=(0,0,255),thickness=2,lineType=cv2.LINE_AA)
        return frame



