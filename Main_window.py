import pygame
import random
import gameplay
class button (pygame.sprite.Sprite) :
    def __init__(self,pos,display_surface, text_button=None, size=None ,font_path=None,color="white", surface=False ,hover_surface=False,bg_color=None, groups=None):
        super().__init__(groups)
        #check if there surface or will creat one form a text
        self.checking_surface = False
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
        self.display_surface.blit(self.image, self.rect)
    def make_borders(self, surface_display ,thickness=0 ,color="white", border_radius=-1) :
        self.has_border=pygame.draw.rect(surface_display ,color , self.rect.inflate(5*thickness, (3.75*thickness) + 15) ,thickness ,border_radius)
    def check_input(self, click):
        self.clicked=click
    def update(self, *args, **kwargs):
        mouse_position= pygame.mouse.get_pos()
        if self.has_border: #because i want to cober the border also when i hover but it has a bigger rect 
                self.rect_collosion = self.has_border
        if self.rect_collosion.collidepoint(mouse_position):
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
            self.clicked=False
            self.display_surface.blit(self.image, self.rect)
def store () :
    button_groups=pygame.sprite.Group()
    back_button=button( display_surface=display_surface,surface=pygame.image.load(r"attachment\back_button.png").convert_alpha(),hover_surface=pygame.image.load(r"attachment\back_button_pressed.png").convert_alpha(),pos=(w_width/2,w_hight-120), groups=button_groups)
    buy_button_1=button(display_surface=display_surface,surface=pygame.image.load(r"attachment\buy_button.png").convert_alpha(),hover_surface=pygame.image.load(r"attachment\buy_button_pressed.png").convert_alpha(),pos=(630,440), groups=button_groups)
    buy_button_2=button(display_surface=display_surface,surface=pygame.image.load(r"attachment\buy_button.png").convert_alpha(),hover_surface=pygame.image.load(r"attachment\buy_button_pressed.png").convert_alpha(),pos=(415,440), groups=button_groups)
    buy_button_2=button(display_surface=display_surface,surface=pygame.image.load(r"attachment\buy_button.png").convert_alpha(),hover_surface=pygame.image.load(r"attachment\buy_button_pressed.png").convert_alpha(),pos=(845,440), groups=button_groups)
    store_window=pygame.image.load(r"attachment\store_window.png").convert_alpha()
    BG_store=pygame.image.load(r"attachment\general_BG.png").convert_alpha()
    store_rect=store_window.get_frect(center=(w_width/2 ,w_hight/2 ))
    BG_store.blit(store_window,store_rect)
    running=True
    while running :
        pygame.display.set_caption("Store")
        display_surface.fill("black")
        display_surface.blit(BG_store, (0,0))
        if back_button.clicked:
            running=False
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                running=False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running=False
        button_groups.update()
        pygame.display.update() 
def pause (display_surface , w_width,w_hight) :
    # i made this because we drawing frames on other so when u clicked by accidant quit button and decide that u want back the effect of are_u_sure will be there
    my_surface= display_surface.copy() 
    BG_check= pygame.Surface((w_width,w_hight))
    BG_check.fill("gray")
    BG_check.set_alpha(50)
    my_surface.blit(BG_check,(0,0))
    button_groups=pygame.sprite.Group()
    resume_button=button(display_surface=display_surface,surface=pygame.image.load(r"attachment\resume_button.png").convert_alpha(),hover_surface=pygame.image.load(r"attachment\resume_button_pressed.png").convert_alpha(),pos=(640,280), groups=button_groups)
    back_to_main_button=button(display_surface=display_surface,surface=pygame.image.load(r"attachment\back_MM_button.png").convert_alpha(),hover_surface=pygame.image.load(r"attachment\back_MM_button_pressed.png").convert_alpha(),pos=(640,420), groups=button_groups)
    pause_window=pygame.image.load(r"attachment\pause_window.png").convert_alpha()
    rect_pause_window=pause_window.get_frect(center=(w_width/2,w_hight/2))
    running=True
    while running :
        display_surface.blit(my_surface,(0 ,0))
        pygame.display.set_caption("pause")
        display_surface.blit(my_surface,(0 ,0))
        display_surface.blit(pause_window,rect_pause_window)
        if back_to_main_button.clicked:
            check=are_u_sure(display_surface , w_width,w_hight)
            if not check:
                return False #when u decide a no choice it will return to the runnig variable of while loop of func play to terminate it 
        elif resume_button.clicked:
            return True #when u decide a yes choice it will return to the runnig variable of while loop of func play to continue playing
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                return True #when u don't need this window it will return to the runnig variable of while loop of func play to continue playing
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
        button_groups.update()
        pygame.display.update() 
def are_u_sure (display_surface ,w_width,w_hight) :
    BG_check=pygame.image.load(r"attachment\are_u_sure.png").convert_alpha()
    rect_BG_check=BG_check.get_frect(center=(w_width/2,w_hight/2))
    # display_surface.blit(BG_check,rect_BG_check)
    button_groups=pygame.sprite.Group()
    yes_button=button(display_surface=display_surface,surface=pygame.image.load(r"attachment\yes_button.png").convert_alpha(),hover_surface=pygame.image.load(r"attachment\yes_button_pressed.png").convert_alpha(),pos=((w_width/2)+100,w_hight/2), groups=button_groups)
    no_button=button(display_surface=display_surface,surface=pygame.image.load(r"attachment\no_button.png").convert_alpha(),hover_surface=pygame.image.load(r"attachment\no_button_pressed.png").convert_alpha(),pos=((w_width/2)-100,w_hight/2), groups=button_groups)
    running=True
    while running :
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
        button_groups.update()
        pygame.display.update() 
if __name__ =="__main__" :    
    pygame.init()
    w_width= 1280 
    w_hight= 720
    display_surface = pygame.display.set_mode((w_width,w_hight))
    button_groups=pygame.sprite.Group()
    play_button=button(display_surface=display_surface,surface=pygame.image.load(r"attachment\play_button.png").convert_alpha(),hover_surface=pygame.image.load(r"attachment\play_button_preessed.png").convert_alpha(),pos=(200,330), groups=button_groups)
    store_button=button(display_surface=display_surface,surface=pygame.image.load(r"attachment\store_button.png").convert_alpha(),hover_surface=pygame.image.load(r"attachment\store_button_pressed.png").convert_alpha(),pos=(180,420), groups=button_groups)
    quit_button =button(display_surface=display_surface,surface=pygame.image.load(r"attachment\quit_button.png").convert_alpha(),hover_surface=pygame.image.load(r"attachment\quit_button_pressed.png").convert_alpha(),pos=(160,500), groups=button_groups)
    BG_MM=pygame.image.load(r"attachment\BG_MM.png").convert_alpha()
    running_main=True
    while running_main :
        pygame.display.set_caption("Main Menu")
        display_surface.fill("black")
        display_surface.blit(BG_MM, (0,0))
        if play_button.clicked:
            gameplay.start_game()
        elif store_button.clicked :
            store()
        elif quit_button.clicked:
            running_main=are_u_sure(display_surface , w_width,w_hight)
        for event in pygame.event.get() :
            if event.type == pygame.QUIT : 
                running_main=False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running_main=False
        button_groups.update()
        pygame.display.update() 
    pygame.quit()