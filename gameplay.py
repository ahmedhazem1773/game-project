import pygame
import random 
import Main_window
import hand_tracking as ht
import cv2
import math

class Player(pygame.sprite.Sprite):
    def __init__(self,groups,width,hight,is_flipped=True): 
        super().__init__(groups)
        #itialize the player size,color,speed and direction.
        self.surfaces=surface_animation_steady=[]
        self.i=0
        for i in range(11) :
            if i < 10 :
                surface=pygame.image.load(f"attachment/hand/steady_hand/hand0{i}.gif").convert_alpha()
                surface=pygame.transform.scale(surface,(surface.get_size()[0]/13,surface.get_size()[1]/13))
                if is_flipped:
                    surface=pygame.transform.flip(surface,True,False)
                self.surfaces.append(surface)
            else :
                surface=pygame.image.load(f"attachment/hand/steady_hand/hand{i}.gif").convert_alpha()
                surface=pygame.transform.scale(surface,(surface.get_size()[0]/13,surface.get_size()[1]/13))
                if is_flipped:
                    surface=pygame.transform.flip(surface,True,False)
                self.surfaces.append(surface)
        self.image=self.surfaces[0]
        self.w_width = width
        self.w_hight = hight        
        self.rect = self.image.get_rect(midright =(self.w_width,self.w_hight//2)) 
        self.direction = pygame.Vector2(0,0) 
        self.speed = 800

    def update(self,dt,move=0):
        self.direction.y=0  
        if move==1:
            self.direction.y=-1
        if move==-1:  
            self.direction.y=1     
        self.rect.y += self.direction.y*self.speed*dt  #the player only move verticaly     
        #the player must be within the window.
        if self.rect.top<0:
            self.rect.top=0
        if self.rect.bottom>self.w_hight:
            self.rect.bottom=self.w_hight
        self.image, self.i = animat(dt,self.surfaces,self.i) 
        
class Obstacle(pygame.sprite.Sprite):
    def __init__(self,groups,y_pos,obstacle_type,width,hight):   #y_pos is the vertical position for the obstacle #y_speed is the speed in y axis 
        super().__init__(groups)
        #initialize the obstacle size,color,speed and direction.
        o_width , o_hight =64,64  #obstacle width and hight
        self.obstacle_type = obstacle_type
        self.image = pygame.Surface((o_width,o_hight))
        if self.obstacle_type == 1:
            sheet_bug=pygame.image.load(r"attachment\Scorpion.png").convert_alpha()
            self.surfaces_bug=creat_animation(8,(64,64),5,sheet_bug,True,1.5)
            self.i=0
            self.image=self.surfaces_bug[0]
            self.y_speed = 0
        elif self.obstacle_type == 2 :
            sheet_bug=pygame.image.load(r"attachment\Clampbeetle.png").convert_alpha()
            self.surfaces_bug=creat_animation(8,(64,64),5,sheet_bug,True,1.5)
            self.i=0
            self.image=self.surfaces_bug[0] 
            self.y_speed = 300
        self.w_width = width
        self.w_hight = hight            
        if y_pos == None:
            y_pos=random.randint(o_hight//2,self.w_hight-2*o_hight)  # another obstacle will be under the first one , they must not enteract
        self.y_pos = y_pos    
        self.rect=self.image.get_rect(bottomleft=(-200,y_pos))
        self.x_speed=  500           
        self.direction = pygame.Vector2(1,random.choice([-1,1])) #obstacle move to lift with random vertical initial direction 

    def check_y2(self,y2):  #check if y2 is not on the screen 
        if y2 > self.w_hight:    #y2 is the vertical coordinate for the second obstacle (if two obstacles get generated together)
            y2=self.w_hight 
        return y2           

    def update(self,dt ):
        #when obstacle hit the top or bottom of the screen , it bounces and changes its direction.
        if self.rect.top <= 0:
            self.rect.top = 0 #that fixed some bugs here 
            self.direction.y*=-1
        if self.rect.bottom >= self.w_hight:
            self.rect.bottom = self.w_hight
            self.direction.y*=-1
        self.rect.x += self.direction.x*self.x_speed* dt
        self.rect.y += self.direction.y*self.y_speed* dt 
        self.image, self.i = animat(dt,self.surfaces_bug,self.i)  
  
        #the obstacle dissapper when get out of the screen and seperate it for my waves of enemy to increase numbers of enemy in the wave 
               
    def check_passing_screen(self):
        if self.rect.right >= self.w_width:
            self.kill()
            return True
        else : 
            return False    

class Bullet(pygame.sprite.Sprite):
    def __init__(self,player,groups,surfaces,bullet_direction,p2_fire):
        super().__init__(groups)
        self.w_width=1360
        self.surfaces=surfaces
        self.image=surfaces[0]
        self.i=0
        self.rect=self.image.get_rect(midright = player.rect.midleft)
        if p2_fire:
            self.rect=self.image.get_rect(midleft = player.rect.midright)
        self.bullet_direction = bullet_direction
        self.x_speed = 1000
        self.y_speed = 0
        self.direction = pygame.Vector2(0,0)
        #bullet vertical speed >> detect the angle that bullet shooten with
        if self.bullet_direction in (-1,1):
            self.y_speed = 90 #makes an angle of 5 degrees with the horizontal
        elif self.bullet_direction in (-2,2):
            self.y_speed = 180 #makes an angle of 10 degrees with the horizontal
        elif self.bullet_direction in (-3,3):    
            self.y_speed = 270 #makes an angle of 15 degrees with the horizontal
        elif self.bullet_direction in (-4,4):    
            self.y_speed = 360 #makes an angle of 20 degrees with the horizontal   
        elif self.bullet_direction in (-5,5):    
            self.y_speed = 470 #makes an angle of 25 degrees with the horizontal              
        #bullet direction         
        if not p2_fire:
            if self.bullet_direction == 0:
                self.direction = pygame.Vector2(-1,0)
            elif self.bullet_direction > 0:
                self.direction = pygame.Vector2(-1,-1) 
            elif self.bullet_direction < 0:
                self.direction = pygame.Vector2(-1,1) 
        else:
            if self.bullet_direction == 0:
                self.direction = pygame.Vector2(1,0)
            elif self.bullet_direction > 0:
                self.direction = pygame.Vector2(1,-1) 
            elif self.bullet_direction < 0:
                self.direction = pygame.Vector2(1,1)
    def update(self,dt):
        self.rect.x += self.direction.x*self.x_speed*dt
        self.rect.y += self.direction.y*self.y_speed*dt
        self.image, self.i = animat(dt,self.surfaces,self.i) 
        if self.rect.x <0:
            self.kill()   
        if self.rect.x >self.w_width-320:     
            self.kill() 

class Collisions:
    def __init__(self,player,obstacles,shoots):
        self.player=player
        self.obstacles=obstacles
        self.shoots=shoots
        self.hit=0 #if an collision occur between a bullet and an obstacle >> hit=1 >> score increase

    def check_collisions(self): #check if player collide to an obstacle
        for obs in self.obstacles:
           dx = self.player.rect.centerx - obs.rect.centerx
           dy = self.player.rect.centery - obs.rect.centery
           d = (dx**2 + dy**2)**0.5 #distance
           collision_radius = 40 #this number represent the min distance between the player and obstacle before git collision
           if d<collision_radius :
                return True
        return False
       
    def bullet_collision(self,all_sprites,obstacle): #check if bullet collide to an obstacle
        hits = pygame.sprite.groupcollide(self.shoots,self.obstacles,True,True) #if no collision happened , hits equal to zero
        if hits:
            self.hit=1 
            for bullet,obstacles in hits.items():
                pos = obstacles[0].rect.center
                if obstacle.obstacle_type == 1:
                    float_text = Floating_text("+3",pos,all_sprites) #display +3
                elif obstacle.obstacle_type == 2:
                    float_text = Floating_text("+5",pos,all_sprites) #display +5 score when bullet collide to obstacle   
            return True #it for my waves of enemy to increase numbers of enemy in the wave
        else :     
            self.hit=0
        return False #it for my waves of enemy to increase numbers of enemy in the wave

class PVP_collisions:
    def __init__(self,player1,player2,p1_shoots1,p2_shoots):
        self.player1 = player1
        self.player2 = player2
        self.p1_shoots = p1_shoots1
        self.p2_shoots = p2_shoots

    def player1_win(self):
        for shoot in self.p1_shoots:
           dx = self.player2.rect.centerx - shoot.rect.centerx
           dy = self.player2.rect.centery - shoot.rect.centery
           d = (dx**2 + dy**2)**0.5 #distance
           collision_radius = 25 
           if d<collision_radius :
               return True
        return False

    def player2_win(self):
        for shoot in self.p2_shoots:
           dx = self.player1.rect.centerx - shoot.rect.centerx
           dy = self.player1.rect.centery - shoot.rect.centery
           d = (dx**2 + dy**2)**0.5 #distance
           collision_radius = 25
           if d<collision_radius :
               return True
        return False

    def barriers_collisions(self,p1_shoots,p2_shoots,barriers_group):
        pygame.sprite.groupcollide(barriers_group,p1_shoots,False,True) 
        pygame.sprite.groupcollide(barriers_group,p2_shoots,False,True)       
      
class Score_counter:
    def __init__(self,width,hight,surf):
        self.total_score = 0 
        self.hit_score_type1=[] 
        self.hit_score_type2=[]
        self.w_width = width
        self.w_hight = hight
        self.board_counter=pygame.image.load(r"attachment\empty_window_show_score.png").convert_alpha()
        self.rect_board_counter=self.board_counter.get_rect(center = (self.w_width//2,self.w_hight-self.w_hight//8))
        self.display_surface = surf

    def update_score(self,hit,obstacle_type):
        self.display_surface.blit(self.board_counter ,self.rect_board_counter)
        if hit and obstacle_type==1:
            self.hit_score_type1.append(1)
        if hit and obstacle_type==2:   
            self.hit_score_type2.append(1) 
        self.total_score =len(self.hit_score_type1)*3 + len(self.hit_score_type2)*5 #score increase by 5 every correct hit for obstacle type 2 , by 3 for type 1
        # i made 2 func in 1 instead of calling twice
        font = pygame.font.Font(r"attachment\jungle-adventurer\JungleAdventurer.otf",50)
        score_text = font.render(f"{self.total_score}",True,(221,243,231))
        text_rect = score_text.get_rect(center = (self.w_width//2,self.w_hight-self.w_hight//8))
        self.display_surface.blit(score_text,text_rect) # display the score within a rectangle

class Floating_text(pygame.sprite.Sprite): #display floating text
    def __init__(self,text,pos,groups):
        super().__init__(groups)
        font = pygame.font.Font(None,40)
        self.image = font.render(text,True,(255,69,0))
        self.rect = self.image.get_rect(center = pos)
        self.lifetime = 60

    def update(self,dt):
        self.rect.y-=1
        self.lifetime-=1
        self.alpha = self.lifetime*4        
        self.image.set_alpha(self.alpha)
        if self.lifetime < 1:
            self.kill()

class Barriers(pygame.sprite.Sprite):
    def __init__(self,groups,width,hight,pos,angle,barrier_type):
        super().__init__(groups)
        self.width=width
        self.hight=hight
        self.image = pygame.Surface((10,80))
        self.image.fill((0,0,0))
        self.barrier_type = barrier_type
        self.center_of_motion = [(self.width-300)/2,self.hight/2]
        self.radius = 300
        self.angle = angle
        if self.barrier_type == 1:
            self.rect = self.image.get_frect(center = pos)
        elif self.barrier_type == 2:
            x=(self.center_of_motion[0] + self.radius*math.cos(self.angle))
            y=(self.center_of_motion[1] + self.radius*math.sin(self.angle))
            self.rect = self.image.get_frect(center = (x,y))    
        self.direction = pygame.Vector2(0,1) 
        self.y_speed = 300
        self.cicular_speed = 1.2

    def update(self,dt):
        if self.barrier_type==1:
            self.rect.y += self.direction.y*self.y_speed*dt
            if self.rect.top<=0:
                self.rect.top=0 
                self.direction.y*=-1
            if self.rect.bottom>=self.hight:
                self.rect.bottom=self.hight 
                self.direction.y*=-1
        elif self.barrier_type==2:
            self.angle+=self.cicular_speed*dt
            self.rect.centerx = self.center_of_motion[0] + self.radius*math.cos(self.angle)
            self.rect.centery = self.center_of_motion[1] + self.radius*math.sin(self.angle)

def end_game(display_surface,w_width,w_hight,cap, score=False, winner=False):
    font = pygame.font.Font(r"attachment\jungle-adventurer\JungleAdventurer.ttf", 60)
    game_over_window=pygame.image.load(r"attachment\gawme_over_window.png").convert_alpha()
    rect_game_over=game_over_window.get_frect(center =((w_width-80)/2,w_hight/2))
    if score:
        showing_the_text= font.render(f"your score is : {score}",True,(221,243,231)) 
    elif winner:
        showing_the_text= font.render(f"the winner is : {winner}",True,(221,243,231)) 
    text_rect = showing_the_text.get_rect(center = ((w_width-80)//2,250))
    button_groups=pygame.sprite.Group()
    play_again_button=Main_window.button(display_surface=display_surface,surface=pygame.image.load(r"attachment\play_again_button.png").convert_alpha(),hover_surface=pygame.image.load(r"attachment\play_again_button_pressed.png").convert_alpha(),pos=(800,400), groups=button_groups)
    back_MM_button=Main_window.button(display_surface=display_surface,surface=pygame.image.load(r"attachment\back_MM_inverted_button.png").convert_alpha(),hover_surface=pygame.image.load(r"attachment\back_MM_inverted_button_pressed.png").convert_alpha(),pos=(500,400), groups=button_groups)
    running = True
    while running :
        ret,frame=cap.read()
        display_frame=cv2.resize(frame,(300,220)) #this is the frame to be displayed
        display_frame = cv2.cvtColor(display_frame,cv2.COLOR_BGR2RGB)
        display_surface.blit(game_over_window,rect_game_over)
        display_surface.blit(showing_the_text,text_rect)
        if play_again_button.clicked :
            if score :
                return True , score
            else :
                return True
        elif back_MM_button.clicked :
            running=False
            if score:
                return False , score
            else :
                return False
        for event in pygame.event.get() :
            if event.type == pygame.QUIT : 
                running=False
                return False , score
        frame_surface = pygame.surfarray.make_surface(display_frame)
        frame_surface = pygame.transform.rotate(frame_surface,-90)
        display_surface.blit(frame_surface,(w_width-305,w_hight-230))
        button_groups.update()
        pygame.display.update()

def round_ended(display_surface,score_text,w_width,w_hight, player,cap):
    players_score=pygame.image.load(r"attachment\players_score_board.png").convert_alpha()
    label_players=pygame.image.load(r"attachment\players_board.png").convert_alpha()
    rect_score_text =score_text.get_frect(center=(w_width-160,145))
    rect_label_players=label_players.get_frect(center=(w_width-160,50))
    rect_players_score=players_score.get_frect(center=(w_width-160,140))
    font = pygame.font.Font(r"attachment\jungle-adventurer\JungleAdventurer.ttf", 35)
    round_ended_window=pygame.image.load(r"attachment\round_ended_window.png").convert_alpha()
    rect_round_ended=round_ended_window.get_frect(center =((w_width-80)/2,w_hight/2))
    showing_the_winner= font.render(f"the winner is : {player}",True,(221,243,231)) 
    winner_rect = showing_the_winner.get_rect(center = ((w_width-80)//2,270))
    button_groups=pygame.sprite.Group()
    next_round_button=Main_window.button(display_surface=display_surface,surface=pygame.image.load(r"attachment\next_round_button.png").convert_alpha(),hover_surface=pygame.image.load(r"attachment\next_round_button_pressed.png").convert_alpha(),pos=(640,330), groups=button_groups)
    back_MM_button=Main_window.button(display_surface=display_surface,surface=pygame.image.load(r"attachment\Back_MM_round_button.png").convert_alpha(),hover_surface=pygame.image.load(r"attachment\Back_MM_round_button_pressed.png").convert_alpha(),pos=(640,440), groups=button_groups)
    running = True
    while running :
        ret,frame=cap.read()
        display_frame=cv2.resize(frame,(300,220)) #this is the frame to be displayed
        display_frame = cv2.cvtColor(display_frame,cv2.COLOR_BGR2RGB)
        display_surface.blit(round_ended_window,rect_round_ended)
        display_surface.blit(showing_the_winner,winner_rect)
        if next_round_button.clicked :
            return True 
        elif back_MM_button.clicked :
            running=False
            return False 
        for event in pygame.event.get() :
            if event.type == pygame.QUIT : 
                running=False
                return False 
        frame_surface = pygame.surfarray.make_surface(display_frame)
        frame_surface = pygame.transform.rotate(frame_surface,-90)
        display_surface.blit(frame_surface,(w_width-305,w_hight-230))
        display_surface.blit(label_players,rect_label_players) 
        display_surface.blit(players_score,rect_players_score)
        display_surface.blit(score_text,rect_score_text)  
        button_groups.update()
        pygame.display.update()

def controller(mp_hands,hands,mp_draw,cap,c_width,c_hight):
    #this function take the porocessed frame and convert it to hame actions
    frame,move,fire,pause=None,0,False,False
    keys = pygame.key.get_pressed()
    frame,stop,shoot,gesture,l_gesture,l_shoot = process_frame(mp_hands,hands,mp_draw,cap,c_width,c_hight)
    frame= cv2.flip(frame , 1 )
    if keys[pygame.K_UP]:
        move=1
    elif keys[pygame.K_DOWN]:    
        move=-1
    elif gesture==1:
        move=1
    elif gesture==-1:
        move=-1
    if keys[pygame.K_SPACE] or keys[pygame.K_KP_ENTER] or shoot:
        fire=True
    if keys[pygame.K_ESCAPE] or stop:
        pause = True    
    return frame,move,fire,pause,l_gesture,l_shoot

def left_hand_controller(l_gesture,l_shoot):
    l_move,l_fire = 0,False
    keys = pygame.key.get_pressed()          
    if keys[pygame.K_w]:
        l_move=1
    elif keys[pygame.K_s]:    
        l_move=-1
    elif l_gesture==1:
        l_move=1
    elif l_gesture==-1:
        l_move=-1
    if keys[pygame.K_c] or l_shoot:
        l_fire=True
    return l_move,l_fire

def shooting(weapons,last_shoot_time,player,group1,group2,surfaces_bullets,weapon,p2_fire=False):
    now = pygame.time.get_ticks()
    if now - last_shoot_time > weapons[weapon]:
        use_weapon(weapon,player,group1,group2,surfaces_bullets,p2_fire)
        last_shoot_time = now
    return last_shoot_time 

def creat_animation (num_frames,size,row,surface_sheet,flip=False,factor_scale=False) :
    surface_animation=[]
    for i in range(num_frames ) :
        rect=pygame.Rect(0+size[1]*i , 0+row*size[0] ,size[0] ,size[1])
        bug= surface_sheet.subsurface(rect)
        if flip:
            bug=pygame.transform.flip(bug,True,False)
        if factor_scale:
            bug=pygame.transform.scale(bug,(64*factor_scale,64*factor_scale))
        surface_animation.append(bug)
    return surface_animation

def animat (dt,surfaces,i) :
    i += 20*dt
    surface=surfaces[int(i) % len(surfaces)]
    return surface ,i
  
def process_frame(mp_hands,hands,mp_draw,cap,c_width,c_hight):
    # move this fun here from hand_travking_module to reduce camera startup time and make game faster
    font = cv2.FONT_HERSHEY_SIMPLEX
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
        l_gesture,l_shoot = None,False #added for pvp mode >> left hand gesture and shoot
        if results.multi_hand_landmarks: #if camera detect a hand >> true
            open_right,open_left=False,False
            for hand_landmarks,handness in zip(results.multi_hand_landmarks,results.multi_handedness):
                label = handness.classification[0].label #classify the hands to left and right
                c_color,l_color = ht.label_color(label)
                draw_circle=mp_draw.DrawingSpec(color=c_color,thickness=2,circle_radius=4)
                draw_line=mp_draw.DrawingSpec(color=l_color,thickness=2)
                mp_draw.draw_landmarks(frame,hand_landmarks,mp_hands.HAND_CONNECTIONS,draw_circle,draw_line)

                if label == "Right": # take the gesture from the right hand to control the game
                    gesture,shoot =ht.hand_gestures(hand_landmarks) 
                    open_right=ht.checkpause(hand_landmarks)
                if label == "Left": 
                    l_gesture,l_shoot =ht.hand_gestures(hand_landmarks,left_hand=True) 
                    open_left=ht.checkpause(hand_landmarks)    
                if open_left and open_right : #if poth left and right hand are open , stop the game
                    stop=1
        
        else : #if camera detect no hands
            cv2.putText(frame,text='NO HANDS DETECTED',org=(f_width//8,f_hight//2), fontFace= font ,fontScale=1.5 ,color=(0,0,255),thickness=3,lineType=cv2.LINE_AA)
        display_frame=cv2.resize(frame,(c_width,c_hight)) #this is the frame to be displayed
        display_frame = cv2.cvtColor(display_frame,cv2.COLOR_BGR2RGB)
        if cv2.waitKey(1) & 0xFF == 27:
            break
        return display_frame,stop,shoot,gesture,l_gesture,l_shoot

def use_weapon(weapon,player,group1,group2,surfaces_bullets,p2_fire):
    if weapon==0:
        Bullet(player,[group1,group2],surfaces_bullets,0,p2_fire)
    if weapon==1:
        Bullet(player,[group1,group2],surfaces_bullets,0,p2_fire)    
    if weapon==2:
        for i in [-2,0,2]:
            Bullet(player,[group1,group2],surfaces_bullets,i,p2_fire)
    if weapon==3:
        for i in range(-5,6): 
            Bullet(player,[group1,group2],surfaces_bullets,i,p2_fire)  
    if weapon==4:
        Bullet(player,[group1,group2],surfaces_bullets,0,p2_fire)

def start_game(cap,your_weapon):
    #pygame.init() >>> not needed , already called in the menu module
    #screen initialization
    w_width,w_hight = 1360,720#window width and hight
    display_surface = pygame.display.set_mode((w_width,w_hight))
    pygame.display.set_caption("good game")
    play_board=pygame.image.load(r"attachment\play_board.png").convert_alpha()
    player_back=pygame.image.load(r"attachment\BG_player.png").convert_alpha()
    mp_hands,hands,mp_draw = ht.prepare_tracking()
    #import surfaces
    sheet_bullets=pygame.image.load(r"attachment\Bullet 24x24 Free Part 2B.png")
    surfaces_bullets=creat_animation(8,(24,24),4,sheet_bullets,True)
    #groups
    all_sprites = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    shoots = pygame.sprite.Group()
    #objects
    player = Player(all_sprites,w_width-300,w_hight)
    collisions=Collisions(player,obstacles,shoots)
    score = Score_counter(w_width,w_hight,display_surface)
    #obstacles respone params : those for my waves to increase smothly in number of enemy in one wave
    num_in_wave=1 
    num_created=0
    all_dead=0
    #select your weapon
    weapons = [500,250,500,2000] # this list have a unique time_delay for each weapon
    #other parameters
    last_shoot_time=0
    clock = pygame.time.Clock()
    FPS = 60
    running = True
    just_unpaused = False
    while running:
        #delta time 
        dt = clock.tick(FPS)/1000
        if just_unpaused and dt > 0.06:  # Skip large dt after unpause
            dt = 0
            just_unpaused = False
        #take game actions params from controller fun
        frame,move,fire,pause,_,_ = controller(mp_hands,hands,mp_draw,cap,300,220)
        #events
        for event in pygame.event.get():
            #quit game
            if event.type == pygame.QUIT:
                running = False
                return False,0 
            #pause game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running= Main_window.pause(display_surface, w_width,w_hight,cap)
                    just_unpaused = True
                    if not running :
                        return False,0 
        #respone obstacles            
        if num_created < num_in_wave and abs(num_created - round(num_created)) < 1e-6 : # it for creat enemys untel reach the max number in the and don't others untel all enemies in brevious wave dead
            chance = random. randint(0,3) #random generator to detect the type of obstacle that will be generated every single event , 50% chance to generate one obstacle
            if chance == 3:
                y_speed = 300
                obstacle = Obstacle([all_sprites,obstacles],None,2,w_width-320,w_hight)
            elif chance : 
                obstacle = Obstacle([all_sprites,obstacles],None,1,w_width-320,w_hight)
            else :
                obstacle = Obstacle([all_sprites,obstacles],None,1,w_width-320,w_hight)   
                y2 = obstacle.y_pos+random.randint(100,400) #the distance between the two obstacles
                y2 = obstacle.check_y2(y2)  
                obstacle = Obstacle([all_sprites,obstacles],y2,1,w_width-320,w_hight)
        # fire        
        if fire:
            last_shoot_time = shooting(weapons,last_shoot_time,player,all_sprites,shoots,surfaces_bullets,your_weapon)
        #player moving
        player.update(dt,move)
        #pause
        if pause:
            running= Main_window.pause(display_surface, w_width,w_hight,cap)
            just_unpaused = True
            if not running :
                return False,0 
        #upgrade-weapon text  >> this option no longer available
        #if your_score >= threshold_score and show_upgrade_text:
        #   float_text2 = Floating_text("weapon upgraded!!",(500,500),all_sprites)
        #   show_upgrade_text=False
        #==========================
        #update and display screen
        display_surface.blit(player_back,(1030,-20))    
        display_surface.blit(play_board, (-240,0))
        #display frame
        frame_surface = pygame.surfarray.make_surface(frame)
        frame_surface = pygame.transform.rotate(frame_surface,-90)
        display_surface.blit(frame_surface,(w_width-305,w_hight-230))
        #update and display sprites
        all_sprites.update(dt)
        all_sprites.draw(display_surface)
        #collisions
        if collisions.check_collisions():
            checker=end_game(display_surface=display_surface,w_width=w_width,w_hight=w_hight,score=score.total_score,cap=cap)
            return checker
        checker_for_killed_enemy =collisions.bullet_collision(all_sprites,obstacle)
        if checker_for_killed_enemy : # to count for obscals that are  dead or pass 
            all_dead +=1
        for obs in obstacles :
            if obs.check_passing_screen() :
                all_dead +=1
        if all_dead >=num_in_wave :
            all_dead=0
            num_created = 0 
            num_in_wave+=1
        elif num_created < num_in_wave :
            num_created += 0.1
        #update score
        score.update_score(collisions.hit,obstacle.obstacle_type) #collisions.hit is 1 if a bullet hit an obstacle, else 0
        pygame.display.update()

def pvp_mode(cap):
    #screen initialization
    w_width,w_hight = 1360,720#window width and hight
    display_surface = pygame.display.set_mode((w_width,w_hight))
    font=pygame.font.Font(r"attachment\jungle-adventurer\JungleAdventurer.otf",70)
    score_text = font.render(f"{0} : {0}",True,(221,243,231))
    rect_score_text =score_text.get_frect(center=(w_width-160,145))
    pygame.display.set_caption("pvp game")
    player_back=pygame.image.load(r"attachment\BG_player.png").convert_alpha()
    label_players=pygame.image.load(r"attachment\players_board.png").convert_alpha()
    rect_label_players=label_players.get_frect(center=(w_width-160,50))
    players_score=pygame.image.load(r"attachment\players_score_board.png").convert_alpha()
    rect_players_score=players_score.get_frect(center=(w_width-160,140))
    mp_hands,hands,mp_draw = ht.prepare_tracking()
    #import surfaces
    sheet_bullets=pygame.image.load(r"attachment\Bullet 24x24 Free Part 2B.png")
    surfaces_bullets1=creat_animation(8,(24,24),4,sheet_bullets,True)
    surfaces_bullets2=creat_animation(8,(24,24),4,sheet_bullets,False)
    #groups
    all_sprites = pygame.sprite.Group()
    p1_shoots = pygame.sprite.Group()
    p2_shoots = pygame.sprite.Group() 
    barriers_group = pygame.sprite.Group()
    #objects
    player1 = Player(all_sprites,w_width-300,w_hight)
    player2 = Player(all_sprites,64,w_hight,False)
    pvp_collisions = PVP_collisions(player1,player2,p1_shoots,p2_shoots)
    #select weapons
    weapons = [500,250,500,2000,100] # this list have a unique time_delay for each weapon
    player1_weapon = 0
    player2_weapon = 0
    #other parameters
    last_shoot_time1=0
    last_shoot_time2=0
    p1_wins=0
    p2_wins=0
    who_won=0
    round=1
    create_barriers=True
    clock = pygame.time.Clock()
    FPS = 60
    running = True
    just_unpaused = False
    while running:
        #delta time 
        dt = clock.tick(FPS)/1000
        if just_unpaused and dt > 0.06:  # Skip large dt after unpause
            dt = 0
            just_unpaused = False
        #take game actions params from controller fun
        frame,move,fire,pause,l_gesture,l_shoot = controller(mp_hands,hands,mp_draw,cap,300,220)
        l_move,l_fire = left_hand_controller(l_gesture,l_shoot)
        #events
        for event in pygame.event.get():
            #quit game
            if event.type == pygame.QUIT:
                running = False
                return False
            #pause game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running= Main_window.pause(display_surface, w_width,w_hight,cap)
                    just_unpaused = True
                    if not running :
                        return False
        #fire
        if fire:
             last_shoot_time1 = shooting(weapons,last_shoot_time1,player1,all_sprites,p1_shoots,surfaces_bullets1,player1_weapon)
        if l_fire:
             last_shoot_time2 = shooting(weapons,last_shoot_time2,player2,all_sprites,p2_shoots,surfaces_bullets2,player2_weapon,True)
        #player moving
        player1.update(dt,move)
        player2.update(dt,l_move)
        #barriers
        if round%2==1 and create_barriers:
            barriers = Barriers((barriers_group,all_sprites),w_width,w_hight,((w_width-250)//2,0),None,1)
            barriers = Barriers((barriers_group,all_sprites),w_width,w_hight,((w_width-350)//2,w_hight),None,1)
            create_barriers=False
        elif round%2==0 and create_barriers:
            for i in range(0,246,45):
                barriers = Barriers((barriers_group,all_sprites),w_width,w_hight,None,i,2)
            create_barriers=False
        #pause
        if pause:
            running= Main_window.pause(display_surface, w_width,w_hight,cap)
            just_unpaused = True
            if not running :
                return False        
        #update and display screen
        display_surface.fill((58,27,30))         
        display_surface.blit(player_back,(1030,-20))   
                #display frame
        frame_surface = pygame.surfarray.make_surface(frame)
        frame_surface = pygame.transform.rotate(frame_surface,-90)
        display_surface.blit(frame_surface,(w_width-305,w_hight-230))
        #update and display sprites
        all_sprites.update(dt)
        all_sprites.draw(display_surface)
        #player collisions
        if pvp_collisions.player1_win():
           who_won=1           
           # >>> function to say play 1 win and start the next round after small timedelay
        elif pvp_collisions.player2_win():    
           who_won=2           
           # >>> function to say play 2 win and start the next round after small timedelay
        #barriers collisions
        pvp_collisions.barriers_collisions(p1_shoots,p2_shoots,barriers_group)
        #round counter
        if who_won==1:
            p1_wins+=1
            round+=1
            player1_weapon+=1
            player2_weapon+=1
            who_won=0
            create_barriers=True
            score_text = font.render(f"{p2_wins} : {p1_wins}",True,(221,243,231))
            if p1_wins<3:
                running=round_ended(display_surface,score_text,w_width,w_hight,"p1",cap)
                if not running :
                    return False    
        elif who_won==2:
            p2_wins+=1
            round+=1
            player1_weapon+=1
            player2_weapon+=1 
            who_won=0           
            create_barriers=True
            score_text = font.render(f"{p2_wins} : {p1_wins}",True,(221,243,231))
            if p2_wins<3:
                running=round_ended(display_surface,score_text,w_width,w_hight,"p2",cap)
                if not running :
                    return False    
        #update score
        display_surface.blit(label_players,rect_label_players) 
        display_surface.blit(players_score,rect_players_score)
        display_surface.blit(score_text,rect_score_text)   
        if p1_wins==3:
            checker=checker=end_game(display_surface=display_surface,w_width=w_width,w_hight=w_hight,winner="player 1",cap=cap)
            return checker
        elif p2_wins==3:  
            checker=checker=end_game(display_surface=display_surface,w_width=w_width,w_hight=w_hight,winner="player 2",cap=cap)
            return checker     
        pygame.display.update()

#pygame.quit() >>> not needed , already called in the menu module

#test :
#pygame.init()
#pvp_mode()
#pygame.quit()