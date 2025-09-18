import pygame
import random
import gameplay
import json
import cv2
#################this class for make a button wether u have a image or u will write 
class button (pygame.sprite.Sprite) :
    def __init__(self,pos,display_surface, text_button=None, size=None ,font_path=None,color="white", surface=False ,hover_surface=False,bg_color=None, groups=None):
        super().__init__(groups)
        #check if there surface or will creat one form a text
        self.checking_surface = False
        # for general surface or image it is visual layer u see but rect it is a invisible rectangle known its points to use for format or collosions 
        if surface :
            self.image= surface
            self.hover_surface= hover_surface
            self.checking_surface = True
        else :
            my_font= pygame.font.Font(font_path, size )
            self.image=my_font.render(text_button , True,color ,bg_color) 
        self.pos =pos
        self.rect= self.image.get_frect(center=self.pos)
        self.rect_collosion=self.rect #this made to chech with that the collosion between button and the mouse
        self.has_border=False
        self.clicked=False #this is to check if the button clicked or not 
        self.display_surface= display_surface
        self.display_surface.blit(self.image, self.rect) #blit methode to put layer argyment on layer variable
    def make_borders(self, surface_display ,thickness=0 ,color="white", border_radius=-1) :
        self.has_border=pygame.draw.rect(surface_display ,color , self.rect.inflate(5*thickness, (3.75*thickness) + 15) ,thickness ,border_radius)
    def check_input(self, click): #check is it clicked or not 
        self.clicked=click
    def update(self, *args, **kwargs): #this for updating state of the any spirit becaue it are frames that drwan frame by frame 
        mouse_position= pygame.mouse.get_pos()
        if self.has_border: #because i want to cover the border also when i hover but it has a bigger rect 
                self.rect_collosion = self.has_border
        if self.rect_collosion.collidepoint(mouse_position):# checking if mouse im area of button to make hover
            if self.checking_surface:
                self.display_surface.blit(self.hover_surface , self.rect)
                self.check_input(click= pygame.mouse.get_just_pressed()[0])
            else :
                #i make a black surface has a low opacity to show i hover on the button
                darkening_surface = pygame.Surface((self.rect_collosion.width, self.rect_collosion.height))
                darkening_surface.fill((0, 0, 0))
                dark_rect=darkening_surface.get_frect(center=self.pos)
                darkening_surface.set_alpha(50)
                self.display_surface.blit(self.image, self.rect)
                self.display_surface.blit(darkening_surface,dark_rect)
                self.check_input(click= pygame.mouse.get_just_pressed()[0])
        else :
            #for return the button like before
            self.clicked=False
            self.display_surface.blit(self.image, self.rect)
class weapon ():
    def __init__(self ,pos,groups, weapon_num, price,bought, equip):
        self.equip=equip
        self.bought=bought
        self.button =button(display_surface=display_surface,surface=pygame.image.load(r"attachment\buy_button.png").convert_alpha(),hover_surface=pygame.image.load(r"attachment\buy_button_pressed.png").convert_alpha(),pos=pos, groups=groups)
        self.equip_button=pygame.image.load(r"attachment\equip_button.png").convert_alpha()
        self.equip_button_pressed=pygame.image.load(r"attachment\equip_button_pressed.png").convert_alpha()
        self.equiped_button=pygame.image.load(r"attachment\equiped_button.png").convert_alpha()
        self.equiped_button_pressed=pygame.image.load(r"attachment\equiped_button_pressed.png").convert_alpha()
        if self.bought:
            if equip:
                self.button.image=self.equiped_button
                self.button.hover_surface=self.equiped_button_pressed
            else :
                self.button.image=self.equip_button
                self.button.hover_surface=self.equip_button_pressed
        self.weapon =weapon_num
        self.price=price
        self.equip=equip
    def equip_func (self) :
        if self.bought:
            if self.equip:
                self.button.image=self.equiped_button
                self.button.hover_surface=self.equiped_button_pressed
            else :
                self.button.image=self.equip_button
                self.button.hover_surface=self.equip_button_pressed

######################################################
#u will notice in most funcs that represent a windows i pass a cap object that response of capture the camera we made this to use one cap obj
#to reduce the delay and any wasting processoring and the strem will mot walk smoth
def animat (dt,surfaces,i) :
    i += 32*dt
    surface=surfaces[int(i) % len(surfaces)]
    return surface ,i
def store (cap) :
    font0=pygame.font.Font(r"attachment\jungle-adventurer\JungleAdventurer.otf",30)
    font1=pygame.font.Font(r"attachment\jungle-adventurer\JungleAdventurer.otf",20)
    coin_text = font0.render(f"your coins : {my_data['coins']}",True,(221,243,231))
    weapon_0_text = font1.render(f"1 shoot\ncall down :\n  500 msec",True,(137,75,0))
    weapon_1_text = font1.render(f"1 shoot\ncall down :\n  250 msec",True,(137,75,0))
    weapon_2_text = font1.render(f"3 shoots\ncall down :\n  500 msec",True,(137,75,0))
    weapon_3_text = font1.render(f"11 shoots\ncall down :\n  2000 msec",True,(137,75,0))
    rect_coin_text =coin_text.get_frect(center=(w_width-120,50))
    #spirit its a class but with common init attribute like surface and rect
    button_groups=pygame.sprite.Group() # to use some spirt in mu opinion are belong together
    back_button=button( display_surface=display_surface,surface=pygame.image.load(r"attachment\back_button.png").convert_alpha(),hover_surface=pygame.image.load(r"attachment\back_button_pressed.png").convert_alpha(),pos=((w_width-250)/2,w_hight-120), groups=button_groups)
    weapon_0=weapon(pos=(232,440),groups=button_groups, weapon_num=1, price=0 , bought=my_data["weapon_0"]["bought"], equip=my_data["weapon_0"]["equip"])
    weapon_1=weapon(pos=(442,440),groups=button_groups, weapon_num=1, price=300 , bought=my_data["weapon_1"]["bought"], equip=my_data["weapon_1"]["equip"])
    weapon_2=weapon(pos=(652,440),groups=button_groups, weapon_num=2, price=400 , bought=my_data["weapon_2"]["bought"], equip=my_data["weapon_2"]["equip"])
    weapon_3=weapon(pos=(860,440),groups=button_groups, weapon_num=3, price=500 , bought=my_data["weapon_3"]["bought"], equip=my_data["weapon_3"]["equip"])
    weapon_1_price = font1.render(f"price is : {weapon_1.price}",True,(137,75,0))
    weapon_2_price = font1.render(f"price is : {weapon_2.price}",True,(137,75,0))
    weapon_3_price = font1.render(f"price is : {weapon_3.price}",True,(137,75,0))
    #import hands
    surface_0=surface_animation_steady[0][0]
    surface_1=surface_animation_steady[1][1]
    surface_2=surface_animation_steady[2][2]
    surface_3=surface_animation_steady[3][3]
    #counter for the animation
    counter=0
    store_window=pygame.image.load(r"attachment\store_window.png").convert_alpha()
    BG_store=pygame.image.load(r"attachment\general_BG.jPg").convert_alpha()
    store_rect=store_window.get_frect(center=((w_width-250)/2 ,w_hight/2 ))
    BG_store.blit(store_window,store_rect)
    running=True
    clock = pygame.time.Clock()
    FPS = 30
    while running :
        dt = clock.tick(FPS)/1000
        ret,frame=cap.read()
        display_frame=cv2.resize(frame,(300,220)) #this is the frame to be displayed
        display_frame = cv2.cvtColor(display_frame,cv2.COLOR_BGR2RGB)
        coin_text = font.render(f"your coins : {my_data['coins']}",True,(221,243,231))
        pygame.display.set_caption("Store")
        display_surface.fill("black")
        display_surface.blit(BG_store, (-10,0))
        display_surface.blit(label_coins,rect_label_coins)
        display_surface.blit(coin_text,rect_coin_text)
        surface_0 , counter= animat(dt,surface_animation_steady[0],counter) 
        surface_1 , counter= animat(dt,surface_animation_steady[1],counter+1)
        surface_2 , counter= animat(dt,surface_animation_steady[2],counter+2) 
        surface_3 , counter= animat(dt,surface_animation_steady[3],counter+3) 
        display_surface.blit(surface_0,(160,170)) 
        display_surface.blit(surface_1,(370,175))
        display_surface.blit(surface_2,(580,175))
        display_surface.blit(surface_3,(787,175))
        display_surface.blit(weapon_0_text,(170,340)) 
        display_surface.blit(weapon_1_text,(380,340))
        display_surface.blit(weapon_2_text,(590,340))
        display_surface.blit(weapon_3_text,(797,340))
        if not weapon_1.bought:
            display_surface.blit(weapon_1_price,(380,320))
        if not weapon_2.bought:
            display_surface.blit(weapon_2_price,(590,320))
        if not weapon_3.bought:
            display_surface.blit(weapon_3_price,(797,320))
        if back_button.clicked:
            for key, value in my_data.items():
                    if key.startswith("weapon_"):  # Only process weapon-related keys
                            if value["equip"] == True:  # Check if equip is True
                                my_data["selected_weapon"] = int(key[-1])  # Update selected_weapon with weapon index
                                break  # Exit after finding the first equipped weapon
            with open(r"data\data.txt", "w") as coin_file :
                        json.dump(my_data, coin_file , indent=4)
            running=False
        elif weapon_0.button.clicked :
            if not weapon_0.equip:
                weapon_0.equip=True
                my_data["weapon_0"]["equip"]=True
                weapon_0.equip_func()
                weapon_1.equip=False
                my_data["weapon_1"]["equip"]=False
                weapon_1.equip_func()
                weapon_2.equip=False
                my_data["weapon_2"]["equip"]=False
                weapon_2.equip_func()
                weapon_3.equip=False
                my_data["weapon_3"]["equip"]=False
                weapon_3.equip_func()
        elif weapon_1.button.clicked :
            if weapon_1.bought :
                if weapon_1.equip:
                    weapon_1.equip=False
                    my_data["weapon_1"]["equip"]=False
                    weapon_1.equip_func()
                    weapon_0.equip=True
                    my_data["weapon_0"]["equip"]=True
                    weapon_0.equip_func()
                else:
                    weapon_1.equip=True
                    my_data["weapon_1"]["equip"]=True
                    weapon_1.equip_func()
                    weapon_0.equip=False
                    my_data["weapon_0"]["equip"]=False
                    weapon_0.equip_func()
                    weapon_2.equip=False
                    my_data["weapon_2"]["equip"]=False
                    weapon_2.equip_func()
                    weapon_3.equip=False
                    my_data["weapon_3"]["equip"]=False
                    weapon_3.equip_func()
            else :
                if my_data["coins"] >= weapon_1.price :
                    my_data['coins'] -=weapon_1.price
                    weapon_1.bought= True
                    weapon_1.button.image=weapon_1.equip_button
                    weapon_1.button.hover_surface=False
                    my_data["weapon_1"]["bought"]=True
        elif weapon_2.button.clicked :
            if weapon_2.bought :
                if weapon_2.equip:
                    weapon_2.equip=False
                    my_data["weapon_2"]["equip"]=False
                    weapon_2.equip_func()
                    weapon_0.equip=True
                    my_data["weapon_0"]["equip"]=True
                    weapon_0.equip_func()
                else:
                    weapon_2.equip=True
                    my_data["weapon_2"]["equip"]=True
                    weapon_2.equip_func()
                    weapon_0.equip=False
                    my_data["weapon_0"]["equip"]=False
                    weapon_0.equip_func()
                    weapon_1.equip=False
                    my_data["weapon_1"]["equip"]=False
                    weapon_1.equip_func()
                    weapon_3.equip=False
                    my_data["weapon_3"]["equip"]=False
                    weapon_3.equip_func()
            else :
                if my_data["coins"] >= weapon_2.price :
                    my_data['coins'] -=weapon_2.price
                    weapon_2.bought= True
                    weapon_2.button.image=weapon_2.equip_button
                    weapon_2.button.hover_surface=False
                    my_data["weapon_2"]["bought"]=True
        elif weapon_3.button.clicked :
            if weapon_3.bought :
                if weapon_3.equip:
                    weapon_3.equip=False
                    my_data["weapon_3"]["equip"]=False
                    weapon_3.equip_func()
                    weapon_0.equip=True
                    my_data["weapon_0"]["equip"]=True
                    weapon_0.equip_func()
                else:
                    weapon_3.equip=True
                    my_data["weapon_3"]["equip"]=True
                    weapon_3.equip_func()
                    weapon_0.equip=False
                    my_data["weapon_0"]["equip"]=False
                    weapon_0.equip_func()
                    weapon_2.equip=False
                    my_data["weapon_2"]["equip"]=False
                    weapon_2.equip_func()
                    weapon_1.equip=False
                    my_data["weapon_1"]["equip"]=False
                    weapon_1.equip_func()
            else :
                if my_data["coins"] >= weapon_3.price :
                    my_data['coins'] -=weapon_3.price
                    weapon_3.bought= True
                    weapon_3.button.image=weapon_3.equip_button
                    weapon_3.button.hover_surface=False
                    my_data["weapon_3"]["bought"]=True
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                for key, value in my_data.items():
                    if key.startswith("weapon_"):  # Only process weapon-related keys
                            if value["equip"] == True:  # Check if equip is True
                                my_data["selected_weapon"] = int(key[-1])  # Update selected_weapon with weapon index
                                break  # Exit after finding the first equipped weapon
                with open(r"data\data.txt", "w") as data_file :
                        json.dump(my_data, data_file , indent=4)
                running=False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    for key, value in my_data.items():
                        if key.startswith("weapon_"):  # Only process weapon-related keys
                                if value["equip"] == True:  # Check if equip is True
                                    my_data["selected_weapon"] = int(key[-1])  # Update selected_weapon with weapon index
                                    break  # Exit after finding the first equipped weapon
                    with open(r"data\data.txt", "w") as data_file :
                        json.dump(my_data, data_file , indent=4)
                    running=False
        frame_surface = pygame.surfarray.make_surface(display_frame)
        frame_surface = pygame.transform.rotate(frame_surface,-90)
        display_surface.blit(frame_surface,(w_width-305,w_hight-230))
        button_groups.update()
        pygame.display.update() 
def pause (display_surface , w_width,w_hight,cap) :
    # i made this because we drawing frames on other so when u clicked by accidant quit button and decide that u want back the effect of are_u_sure will be there
    my_surface= display_surface.copy() 
    BG_check= pygame.Surface((w_width,w_hight))
    BG_check.fill("gray")
    BG_check.set_alpha(80)
    my_surface.blit(BG_check,(0,0))
    button_groups=pygame.sprite.Group()
    resume_button=button(display_surface=display_surface,surface=pygame.image.load(r"attachment\resume_button.png").convert_alpha(),hover_surface=pygame.image.load(r"attachment\resume_button_pressed.png").convert_alpha(),pos=(640,280), groups=button_groups)
    back_to_main_button=button(display_surface=display_surface,surface=pygame.image.load(r"attachment\back_MM_button.png").convert_alpha(),hover_surface=pygame.image.load(r"attachment\back_MM_button_pressed.png").convert_alpha(),pos=(640,420), groups=button_groups)
    pause_window=pygame.image.load(r"attachment\pause_window.png").convert_alpha()
    rect_pause_window=pause_window.get_frect(center=((w_width-80)/2,w_hight/2))
    running=True
    while running :
        ret,frame =cap.read()
        display_frame=cv2.resize(frame,(300,220)) #this is the frame to be displayed
        display_frame = cv2.cvtColor(display_frame,cv2.COLOR_BGR2RGB)
        display_surface.blit(my_surface,(0 ,0))
        pygame.display.set_caption("pause")
        display_surface.blit(pause_window,rect_pause_window)
        if back_to_main_button.clicked:
            check=are_u_sure(display_surface , w_width-80,w_hight,cap)
            if not check:
                return False #when u decide a no choice it will return to the runnig variable of while loop of func play to terminate it 
        elif resume_button.clicked:
            return True #when u decide a yes choice it will return to the runnig variable of while loop of func play to continue playing
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                return True #when u don't need this window it will return to the runnig variable of while loop of func play to continue playing
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    #this for issue because i use the same key in affect in the main loop so it seems like it gitting not unpaused
                    while pygame.key.get_pressed()[pygame.K_ESCAPE]:
                        pygame.event.pump()
                    return True
        frame_surface = pygame.surfarray.make_surface(display_frame)
        frame_surface = pygame.transform.rotate(frame_surface,-90)
        display_surface.blit(frame_surface,(w_width-305,w_hight-230))
        button_groups.update()
        pygame.display.update() 
def are_u_sure (display_surface ,w_width,w_hight, cap) :
    BG_check=pygame.image.load(r"attachment\are_u_sure.png").convert_alpha()
    rect_BG_check=BG_check.get_frect(center=(w_width/2,w_hight/2))
    # display_surface.blit(BG_check,rect_BG_check)
    button_groups=pygame.sprite.Group()
    yes_button=button(display_surface=display_surface,surface=pygame.image.load(r"attachment\yes_button.png").convert_alpha(),hover_surface=pygame.image.load(r"attachment\yes_button_pressed.png").convert_alpha(),pos=((w_width/2)+100,w_hight/2), groups=button_groups)
    no_button=button(display_surface=display_surface,surface=pygame.image.load(r"attachment\no_button.png").convert_alpha(),hover_surface=pygame.image.load(r"attachment\no_button_pressed.png").convert_alpha(),pos=((w_width/2)-100,w_hight/2), groups=button_groups)
    running=True
    while running :
        ret,frame=cap.read()
        display_frame=cv2.resize(frame,(300,220)) #this is the frame to be displayed
        display_frame = cv2.cvtColor(display_frame,cv2.COLOR_BGR2RGB)
        display_surface.blit(BG_check,rect_BG_check)
        if yes_button.clicked :
            print("yes")
            return False # this mean u sure want to quit 
        elif no_button.clicked :
            print("no")
            return True
        for event in pygame.event.get() :
            if event.type == pygame.QUIT: 
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running=False
        frame_surface = pygame.surfarray.make_surface(display_frame)
        frame_surface = pygame.transform.rotate(frame_surface,-90)
        display_surface.blit(frame_surface,(1055,w_hight-230))
        button_groups.update()
        pygame.display.update()
def game_mode(cap) :
    my_surface= display_surface.copy() 
    button_groups=pygame.sprite.Group() # to use some spirt in mu opinion are belong together
    pvp_button=button(display_surface=display_surface,surface=pygame.image.load(r"attachment\pvp_button.png").convert_alpha(),hover_surface=pygame.image.load(r"attachment\pvp_button_pressed.png").convert_alpha(),pos=((w_width/2),300), groups=button_groups)
    normal_button=button(display_surface=display_surface,surface=pygame.image.load(r"attachment\normal_button.png").convert_alpha(),hover_surface=pygame.image.load(r"attachment\normal_button_pressed.png").convert_alpha(),pos=((w_width/2),370), groups=button_groups)
    back_button=button(display_surface=display_surface,surface=pygame.image.load(r"attachment\back_GM_button.png").convert_alpha(),hover_surface=pygame.image.load(r"attachment\back_GM_button_pressed.png").convert_alpha(),pos=((w_width/2),450), groups=button_groups)
    mode_window=pygame.image.load(r"attachment\game_mode_window.png").convert_alpha()
    mode_rect=mode_window.get_frect(center=(w_width/2 ,w_hight/2 ))
    running=True
    while running :
        ret,frame=cap.read()
        display_frame=cv2.resize(frame,(300,220)) #this is the frame to be displayed
        display_frame = cv2.cvtColor(display_frame,cv2.COLOR_BGR2RGB)
        pygame.display.set_caption("mode")
        display_surface.fill("black")
        display_surface.blit(my_surface, (0,0))
        display_surface.blit(mode_window,mode_rect)
        if back_button.clicked:
            return False,None
        elif normal_button.clicked :
            return True , 0
        elif pvp_button.clicked:
            return True , 1
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                return False , None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False , None 
        frame_surface = pygame.surfarray.make_surface(display_frame)
        frame_surface = pygame.transform.rotate(frame_surface,-90)
        display_surface.blit(frame_surface,(w_width-305,w_hight-230))
        button_groups.update()
        pygame.display.update() 
if __name__ =="__main__" :    
    pygame.init()
    w_width,w_hight = 1360,720 #window width and hight
    # c_width,c_hight = 300,220 #camera width and hight
    display_surface = pygame.display.set_mode((w_width,w_hight))
    #this is for the data file
    try :
        with open(r"data\data.txt") as data_file :
            my_data=json.load(data_file)
    except:
        my_data = {"coins": 0,"weapon_0":{"bought":True , "equip":True},"weapon_1":{"bought":False , "equip":False},"weapon_2":{"bought":False , "equip":False},"weapon_3":{"bought":False , "equip":False},"selected_weapon":0}
    surface_animation_steady=[[],[],[],[]]
    for c in range(4):
        for i in range(11):
            if i < 10 :
                surface=pygame.image.load(f"attachment/hand/{c}/hand0{i}.gif").convert_alpha()
                surface=pygame.transform.scale(surface,(surface.get_size()[0]/6,surface.get_size()[1]/6))
                surface_animation_steady[c].append(surface)
            else :
                surface=pygame.image.load(f"attachment/hand/{c}/hand{i}.gif").convert_alpha()
                surface=pygame.transform.scale(surface,(surface.get_size()[0]/6,surface.get_size()[1]/6))
                surface_animation_steady[c].append(surface)
    font=pygame.font.Font(r"attachment\jungle-adventurer\JungleAdventurer.otf",30)
    font2=pygame.font.Font(r"attachment\jungle-adventurer\JungleAdventurer.otf",20)
    coin_text = font.render(f"your coins : {my_data['coins']}",True,(221,243,231))
    ahmed= font2.render(f"made by :\nahmed hazem linkedin : www.linkedin.com/in/ahmed-hazem-7730262b9",True,(221,243,231))
    abdo= font2.render(f"abdelrahman ehab linkedin : www.linkedin.com/in/abdelrahman-ehab-636275327",True,(221,243,231))
    rect_coin_text =coin_text.get_frect(center=(w_width-120,50))
    display_surface = pygame.display.set_mode((w_width,w_hight))
    button_groups=pygame.sprite.Group()
    play_button=button(display_surface=display_surface,surface=pygame.image.load(r"attachment\play_button.png").convert_alpha(),hover_surface=pygame.image.load(r"attachment\play_button_preessed.png").convert_alpha(),pos=(190,350), groups=button_groups)
    store_button=button(display_surface=display_surface,surface=pygame.image.load(r"attachment\store_button.png").convert_alpha(),hover_surface=pygame.image.load(r"attachment\store_button_pressed.png").convert_alpha(),pos=(170,440), groups=button_groups)
    quit_button =button(display_surface=display_surface,surface=pygame.image.load(r"attachment\quit_button.png").convert_alpha(),hover_surface=pygame.image.load(r"attachment\quit_button_pressed.png").convert_alpha(),pos=(150,520), groups=button_groups)
    BG_MM=pygame.image.load(r"attachment\BG_MM.png").convert_alpha()
    label_coins=pygame.image.load(r"attachment\empty_window_show_coins.png").convert_alpha()
    rect_label_coins=label_coins.get_frect(center=(w_width-120,50))
    running_main=True
    play_again=True
    cap = cv2.VideoCapture(0)
    while running_main :
        ret, frame = cap.read()
        if not ret :
            print("i don't capture")
            break
        display_frame=cv2.resize(frame,(300,220)) #this is the frame to be displayed
        display_frame = cv2.cvtColor(display_frame,cv2.COLOR_BGR2RGB)
        pygame.display.set_caption("Main Menu")
        coin_text = font.render(f"your coins : {my_data['coins']}",True,(221,243,231))
        display_surface.fill("black")
        display_surface.blit(BG_MM, (0,0))
        display_surface.blit(label_coins,rect_label_coins)
        display_surface.blit(coin_text,rect_coin_text)
        display_surface.blit(ahmed,(50,650))
        display_surface.blit(abdo,(50,690))
        if play_button.clicked:
            check_game , type = game_mode(cap)
            if check_game:
                if type ==0 :
                    while play_again:
                        play_again , score=gameplay.start_game(cap,my_data["selected_weapon"])
                        my_data['coins'] +=score
                        with open(r"data\data.txt", "w") as coin_file :
                            json.dump(my_data, coin_file , indent=4)
                    play_again= True
                elif type ==1 :
                    while play_again:
                        play_again =gameplay.pvp_mode(cap)
                    play_again= True
        elif store_button.clicked :
            store(cap)
        elif quit_button.clicked:
            running_main=are_u_sure(display_surface , w_width,w_hight, cap)
        for event in pygame.event.get() :
            if event.type == pygame.QUIT : 
                running_main=False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running_main=False
        frame_surface = pygame.surfarray.make_surface(display_frame)
        frame_surface = pygame.transform.rotate(frame_surface,-90)
        # frame_surface = pygame.transform.flip(frame_surface,True,False)
        display_surface.blit(frame_surface,(w_width-305,w_hight-230))
        button_groups.update()
        pygame.display.update() 
    pygame.quit()