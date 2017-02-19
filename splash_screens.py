import pygame

'''
class: screen/menu with the option of buttons
parameters:
    loc: tuple location of the screen
    ani_time: integer cycles between animation
    bg_frames: list of string paths to frames used in the background
    images: list of tuples containing first a string path to the image and second, the location for the image to be displayed on the screen
    buttons: list of tuples containing first a string path to the button image and second, the location for the button to be displayed on the screen
'''
class Splash_Screen():
    def __init__(self,loc,ani_time,bg_frames,images,buttons):
        self.background_ani_idx = 0
        self.ani_time = ani_time
        self.current_ani_time = ani_time
        self.frames = self.init_frames(bg_frames)
        self.images = self.init_images(images)
        self.loc = loc
        self.buttons = self.init_images(buttons)
        self.button_disp = []

    '''
    function: display frames, images and buttons on the screem
        screen: pygame.display to display on
        dt: float time in a cycle
    '''
    def display(self,screen,dt):
        if self.ani_time > 0 and len(self.frames) > 1:

            if self.current_ani_time >= self.ani_time:
                self.current_ani_time = 0
                screen.blit(self.frames[self.background_ani_idx],self.loc)
                self.display_buttons(screen)
                for i in self.images:
                    screen.blit(i[0],i[1])

                self.background_ani_idx += 1
            else:
                self.current_ani_time += dt

            if self.background_ani_idx >= len(self.frames):
                self.background_ani_idx = 0

        else:
            screen.blit(self.frames[0],self.loc)
            self.display_buttons(screen)
            self.display_images(screen)

    '''
    function: display buttons on the screen
        screen: pygame.display to display the buttons on
    '''
    def display_buttons(self,screen):
        for b in self.buttons:
            self.button_disp.append(screen.blit(b[0],b[1]))

    '''
    function: display images on the screen
        screen: pygame.display to display the images on
    '''
    def display_images(self,screen):
        for i in self.images:
            screen.blit(i[0],i[1])

    '''
    function: convert paths to images to pygame images
        images: list of tuples first containing string paths to images, second a tuple of the location of the images
    '''
    def init_images(self, images):
        result  = []
        for i in images:
            result.append((pygame.image.load(i[0]), i[1]))

        return result

    '''
    function: convert paths to background animation frames to pygame images
        frames: list of string paths to frames
    '''
    def init_frames(self, frames):
        result = []
        for f in frames:
            result.append(pygame.image.load(f))

        return result
