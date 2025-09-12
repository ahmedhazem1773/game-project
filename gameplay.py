import pygame
import random 
import Main_window
import json
class Player(pygame.sprite.Sprite):
    def __init__(self,groups,width,hight): 
        super().__init__(groups)
        #itialize the player size,color,speed and direction.
        self.image = pygame.Surface((30,50))
        self.image.fill((0,0,255))
        self.w_width = width
        self.w_hight = hight        
        self.rect = self.image.get_rect(midleft =(0,self.w_hight//2)) 
        self.direction = pygame.Vector2(0,0) 
        self.speed = 800


    def update(self,dt):
        keys = pygame.key.get_pressed()
        self.direction.y=0  
        if keys[pygame.K_UP]:
            self.direction.y=-1
        if keys[pygame.K_DOWN]:  
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
        self.rect=self.image.get_rect(bottomleft=(self.w_width+200,y_pos))
        self.x_speed=  500 
        if y_speed == None:  
            y_speed = 0           
        self.y_speed = y_speed
        self.direction = pygame.Vector2(-1,random.choice([-1,1])) #obstacle move to lift with random vertical initial direction 


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
    def check_passing_screen(self):
        if self.rect.x <-100:
            self.kill()
            return True
        else : 
            False    

class Wipons(pygame.sprite.Sprite):
    def __init__(self,player,groups,width,hight):
        super().__init__(groups)
        self.image=pygame.Surface((10,10))
        self.image.fill((255,0,0))
        self.rect=self.image.get_rect(midleft = player.rect.midright)
        self.speed = 2000
        self.direction = pygame.Vector2(1,0)
        self.w_width = width
        self.w_hight = hight

    def update(self,dt):
        keys = pygame.key.get_pressed()
        self.rect.x += self.direction.x*self.speed*dt
        if self.rect.x >self.w_width:
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
                float_text = Floating_text("+5",pos,all_sprites) #display +5 score when bullet collide to obstacle
            return True
        else :     
            self.hit=0
        return False
    
class Score_counter:
    def __init__(self,width,hight,surf):
        self.total_score = 0 
        self.time_score=0
        self.hit_score=[] 
        self.w_width = width
        self.w_hight = hight
        self.board_counter=pygame.image.load(r"attachment\empty_window_show_score.png").convert_alpha()
        self.rect_board_counter=self.board_counter.get_rect(center = (self.w_width//2,self.w_hight-self.w_hight//8))
        self.display_surface = surf

    def update_score(self,hit):
        self.display_surface.blit(self.board_counter ,self.rect_board_counter)
        self.time_score = pygame.time.get_ticks()//500  #score increase by 2 every second
        self.hit_score.append(1) if hit else 0
        self.total_score =len(self.hit_score)*5  #score increase by 5 every correct hit
        # i made 2 func in 1 instead of calling twice
        font = pygame.font.Font(r"attachment\jungle-adventurer\JungleAdventurer.otf",50)
        score_text = font.render(f"{self.total_score}",True,(221,243,231))
        text_rect = score_text.get_rect(center = (self.w_width//2,self.w_hight-self.w_hight//8))
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
        self.alpha = self.lifetime*4        
        self.image.set_alpha(self.alpha)
        if self.lifetime < 1:
            self.kill()
        
def end_game(display_surface,w_width,w_hight, score):
    font = pygame.font.Font(r"attachment\jungle-adventurer\JungleAdventurer.ttf", 60)
    game_over_window=pygame.image.load(r"attachment\gawme_over_window.png").convert_alpha()
    rect_game_over=game_over_window.get_frect(center =(w_width/2,w_hight/2))
    showing_the_score= font.render(f"your score is : {score}",True,(221,243,231)) 
    text_rect = showing_the_score.get_rect(center = (w_width//2,250))
    button_groups=pygame.sprite.Group()
    play_again_button=Main_window.button(display_surface=display_surface,surface=pygame.image.load(r"attachment\play_again_button.png").convert_alpha(),hover_surface=pygame.image.load(r"attachment\play_again_button_pressed.png").convert_alpha(),pos=(800,400), groups=button_groups)
    back_MM_button=Main_window.button(display_surface=display_surface,surface=pygame.image.load(r"attachment\back_MM_inverted_button.png").convert_alpha(),hover_surface=pygame.image.load(r"attachment\back_MM_inverted_button_pressed.png").convert_alpha(),pos=(500,400), groups=button_groups)
    running = True
    while running :
        display_surface.blit(game_over_window,rect_game_over)
        display_surface.blit(showing_the_score,text_rect)
        if play_again_button.clicked :
            return True , score
        elif back_MM_button.clicked :
            running=False
            return False , score
        for event in pygame.event.get() :
            if event.type == pygame.QUIT : 
                running=False
                return False , score
        button_groups.update()
        pygame.display.update()
        

def start_game():
    #pygame.init() >>> not needed , already called in the menu module
    #screen initialization
    w_width,w_hight = 1280,720 #window width and hight
    display_surface = pygame.display.set_mode((w_width,w_hight))
    pygame.display.set_caption("first prototype")
    play_board=pygame.image.load(r"attachment\play_board.png").convert_alpha()
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
    pygame.time.set_timer(obstacle_event,300)
    num_in_wave=1 
    num_created=0
    all_dead=0
    #other parameters
    last_shoot_time=0
    time_delay=500 #delay between every single shoot
    clock = pygame.time.Clock()
    FPS = 120
    running = True
    pause_checker = False
    while running:
        #delta time 
        dt = clock.tick(FPS)/1000
        #events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE :
                    now = pygame.time.get_ticks()
                    if now - last_shoot_time > time_delay:
                        shoot = Wipons(player,[all_sprites,shoots],w_width,w_hight) 
                        last_shoot_time = now
                if event.key == pygame.K_ESCAPE:
                    pause_checker = True
                    running= Main_window.pause(display_surface, w_width,w_hight)
                    pause_checker = False
        if num_created < num_in_wave  :
            chance = random. randint(0,3) #random generator to detect the type of obstacle that will be generated every single event , 50% chance to generate one obstacle
            if chance == 3:
                y_speed = 300
                obstacle2 = Obstacle([all_sprites,obstacles],None,y_speed,2,w_width,w_hight)
            elif chance : 
                obstacle = Obstacle([all_sprites,obstacles],None,None,1,w_width,w_hight)
            else :
                obstacle = Obstacle([all_sprites,obstacles],None,None,1,w_width,w_hight)   
                y2 = obstacle.y_pos+random.randint(100,400) #the distance between the two obstacles
                y2 = obstacle.check_y2(y2)  
                obstacle = Obstacle([all_sprites,obstacles],y2,None,1,w_width,w_hight)
        #collisions
        if collisions.check_collisions():
            checker=end_game(display_surface,w_width,w_hight , score.total_score)
            return checker
        checker_for_killed_enemy =collisions.bullet_collision(all_sprites)
        if checker_for_killed_enemy or any( obs.check_passing_screen() for obs in obstacles) :
            all_dead +=1
        if all_dead ==num_in_wave :
            all_dead=0
            num_created = 0 
        elif num_created < num_in_wave :
            num_created += 1
        #update and display screen    
        display_surface.blit(play_board, (0,0))
        all_sprites.draw(display_surface)
        #update score
        score.update_score(collisions.hit) #collisions.hit is 1 if a bullet hit an obstacle, else 0
        all_sprites.update(dt)
        pygame.display.update()

#pygame.quit() >>> not needed , already called in the menu module

#test :
#pygame.init()
#start_game()
#pygame.quit()