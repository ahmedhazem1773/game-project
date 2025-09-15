import pygame
import random 
import hand_tracking as ht
import cv2

class Player(pygame.sprite.Sprite):
    def __init__(self,groups,width,hight): 
        super().__init__(groups)
        #itialize the player size,color,speed and direction.
        self.image = pygame.Surface((30,50))
        self.image.fill((0,0,255))
        self.w_width = width
        self.w_hight = hight        
        self.rect = self.image.get_rect(midright =(self.w_width,self.w_hight//2)) 
        self.direction = pygame.Vector2(0,0) 
        self.speed = 500


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

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,groups,y_pos,y_speed,obstacle_type,width,hight):   #y_pos is the vertical position for the obstacle #y_speed is the speed in y axis 
        super().__init__(groups)
        #initialize the obstacle size,color,speed and direction.
        o_width , o_hight =70,70  #obstacle width and hight
        self.image = pygame.Surface((o_width,o_hight))
        if obstacle_type == 1:
            self.image.fill((0,0,0))
        elif obstacle_type == 2 :
            self.image.fill((255,0,0))    
        self.w_width = width
        self.w_hight = hight            
        if y_pos == None:
            y_pos=random.randint(o_hight//2,self.w_hight-2*o_hight)  # another obstacle will be under the first one , they must not enteract
        self.y_pos = y_pos    
        self.rect=self.image.get_rect(bottomleft=(-200,y_pos))
        self.x_speed=  500 
        if y_speed == None:  
            y_speed = 0           
        self.y_speed = y_speed
        self.direction = pygame.Vector2(1,random.choice([-1,1])) #obstacle move to right with random vertical initial direction 


    def check_y2(self,y2):  #check if y2 is not on the screen 
        if y2 > self.w_hight:    #y2 is the vertical coordinate for the second obstacle (if two obstacles get generated together)
            y2=self.w_hight 
        return y2           

    def update(self,dt):
        #when obstacle hit the top or bottom of the screen , it bounces and changes its direction.
        if self.rect.top <= 0:
            self.rect.top = 0 #that fixed some bugs here 
            self.direction.y*=-1
        if self.rect.bottom >= self.w_hight:
            self.rect.bottom = self.w_hight
            self.direction.y*=-1
        self.rect.x += self.direction.x*self.x_speed*dt    
        self.rect.y += self.direction.y*self.y_speed*dt      
        #the obstacle dissapper when get out of the screen        
        if self.rect.x >self.w_width+100:
            self.kill()    

class Wipons(pygame.sprite.Sprite):
    def __init__(self,player,groups,width,hight):
        super().__init__(groups)
        self.image=pygame.Surface((20,10))
        self.image.fill((169,169,169))
        self.rect=self.image.get_rect(midright = player.rect.midleft)
        self.speed = 1000
        self.direction = pygame.Vector2(-1,0)
        self.w_width = width
        self.w_hight = hight

    def update(self,dt):
        self.rect.x += self.direction.x*self.speed*dt
        if self.rect.x <0:
            self.kill()    

class Collisions:
    def __init__(self,player,obstacles,shoots):
        self.player=player
        self.obstacles=obstacles
        self.shoots=shoots
        self.hit=0 #if an collision occur between a bullet and an obstacle >> hit=1 >> score increase

    def check_collisions(self): #check if player collide to an obstacle
        if pygame.sprite.spritecollide(self.player,self.obstacles,False):
            return True
        return False
    
    def bullet_collision(self,all_sprites): #check if bullet collide to an obstacle
        hits = pygame.sprite.groupcollide(self.shoots,self.obstacles,True,True) #if no collision happened , hits equal to zero
        if hits:
            self.hit=1 
            for bullet,obstacles in hits.items():
                pos = obstacles[0].rect.center
                Floating_text("+5",pos,all_sprites) #display +5 score when bullet collide to obstacle
        else :     
            self.hit=0
        return 0
    
class Score_counter:
    def __init__(self,width,hight,surf):
        self.total_score = 0 
        self.time_score=0
        self.hit_score=[] 
        self.w_width = width
        self.w_hight = hight
        self.display_surface = surf

    def update_score(self,hit):
        self.time_score =(pygame.time.get_ticks()//500-8)  #score increase by 2 every second , this (-8) because the camera and other modules take some time to get prepared
        if self.time_score<0: # if the camera get prepared faster than expected , sore cant be negative
            self.time_score=0
        self.hit_score.append(1) if hit else 0
        self.total_score = self.time_score + len(self.hit_score)*5  #score increase by 5 every correct hit

    def draw_score(self):   
        font = pygame.font.Font(None,80)
        score_text = font.render(f"{self.total_score}",True,(200,200,200))
        text_rect = score_text.get_rect(center = (self.w_width//2,self.w_hight-self.w_hight//6))
        text_box = text_rect.inflate(15,10)
        pygame.draw.rect(self.display_surface,(200,200,200),text_box,5,border_radius=10)
        self.display_surface.blit(score_text,text_rect) # display the score within a rectangle

class Floating_text(pygame.sprite.Sprite): #display floating text
    def __init__(self,text,pos,groups):
        super().__init__(groups)
        font = pygame.font.Font(None,40)
        self.image = font.render(text,True,(150,150,150))
        self.rect = self.image.get_rect(center = pos)
        self.lifetime = 60

    def update(self,dt):
        self.rect.y-=1
        self.lifetime-=1
        self.alpha = self.lifetime*4 #the text fade out with its lifetime       
        self.image.set_alpha(self.alpha)
        if self.lifetime < 1:
            self.kill()

def shooting(time_delay,last_shoot_time,player,group1,group2):
    now = pygame.time.get_ticks()
    if now - last_shoot_time > time_delay:
        Wipons(player,[group1,group2],player.w_width,player.w_hight) 
        last_shoot_time = now
    return last_shoot_time    

def end_game(display_surface,w_width,w_hight):
    font = pygame.font.SysFont(None,180,True)
    game_over_text = font.render("GAME OVER",True,(50,205,50)) 
    text_rect = game_over_text.get_rect(center = (w_width//2,w_hight//2))
    display_surface.blit(game_over_text,text_rect)

def controller(mp_hands,hands,mp_draw,font,cap,c_width,c_hight):
    frame,move,fire,pause=None,0,False,False
    keys = pygame.key.get_pressed()
    frame,stop,shoot,gesture = ht.process_frame(mp_hands,hands,mp_draw,font,cap,c_width,c_hight)
    if keys[pygame.K_UP]:
        move=1
    elif keys[pygame.K_DOWN]:    
        move=-1
    elif gesture==1:
        move=1
    elif gesture==-1:
        move=-1
    if keys[pygame.K_SPACE] or shoot:
        fire=True
    if keys[pygame.K_ESCAPE] or stop:
        pause = True    
    return frame,move,fire,pause   

def start_game():

    #pygame.init() >>> not needed , already called in the menu module
    #screen initialization
    w_width,w_hight = 1067,600 #window width and hight
    c_width,c_hight = 300,220 #camera width and hight
    display_surface = pygame.display.set_mode((w_width+c_width,w_hight))
    c_surface = display_surface.subsurface(pygame.Rect(w_width,0,c_width,w_hight)) #camera surface
    pygame.display.set_caption("first prototype") #this line mostly will be deleted later
    #camera initialization
    mp_hands,hands,mp_draw,font,cap = ht.prepare_tracking()
    #groups
    all_sprites = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    shoots = pygame.sprite.Group()
    #objects
    player = Player(all_sprites,w_width,w_hight)
    collisions=Collisions(player,obstacles,shoots)
    score = Score_counter(w_width,w_hight,display_surface)
    #events
    obstacle_event = pygame.event.custom_type()
    pygame.time.set_timer(obstacle_event,600)
    #other parameters
    last_shoot_time=0
    y_speed = 300 #verticales speed for obstacles
    time_delay=500 #delay between every single shoot
    clock = pygame.time.Clock()
    FPS = 120
    running = True

    while running:
        #delta time 
        dt = clock.tick(FPS)/1000
        #actions
        frame,move,fire,pause = controller(mp_hands,hands,mp_draw,font,cap,c_width,c_hight)
        #events
        for event in pygame.event.get():
            #out game
            if event.type == pygame.QUIT:
                running = False
            #create obstacles    
            if event.type == obstacle_event:
                chance = random. randint(0,3) #random generator to detect the type of obstacle that will be generated every single event , 50% chance to generate one obstacle
                if chance == 3:
                    obstacle2 = Obstacle([all_sprites,obstacles],None,y_speed,2,w_width,w_hight)
                elif chance : 
                    obstacle = Obstacle([all_sprites,obstacles],None,None,1,w_width,w_hight)
                else :
                    obstacle = Obstacle([all_sprites,obstacles],None,None,1,w_width,w_hight)   
                    y2 = obstacle.y_pos+random.randint(100,400) #the distance between the two obstacles
                    y2 = obstacle.check_y2(y2)  
                    obstacle = Obstacle([all_sprites,obstacles],y2,None,1,w_width,w_hight)
        #pause
        if pause:
            running=False            
        #shooting
        if fire:
            last_shoot_time = shooting(time_delay,last_shoot_time,player,all_sprites,shoots)
        #player moving
        player.update(dt,move) 
        #collisions
        if collisions.check_collisions():
            running=0
        collisions.bullet_collision(all_sprites)
        #update score
        score.update_score(collisions.hit) #collisions.hit is 1 if a bullet hit an obstacle, else 0
        #prepare screen    
        display_surface.fill((255,255,153)) 
        all_sprites.draw(display_surface)
        c_surface.fill((0,0,0))
        #display frame
        frame_surface = pygame.surfarray.make_surface(frame)
        frame_surface = pygame.transform.rotate(frame_surface,-90)
        frame_surface = pygame.transform.flip(frame_surface,True,False)
        display_surface.blit(frame_surface,(w_width,w_hight-c_hight))
        #draw score and update screen
        score.draw_score()
        all_sprites.update(dt)
        if not running:
            end_game(display_surface,w_width,w_hight)  #display game_over text 
        #display screen    
        pygame.display.update() 
        #close the game 
        if not running:
            pygame.time.delay(1500)  
            cap.release()
            cv2.destroyAllWindows()  

#pygame.quit() >>> not needed , already called in the menu module

#test :
#pygame.init()
#start_game()
#pygame.quit()


