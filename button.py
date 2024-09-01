import pygame
pygame.init()  # initialize pygame

BLOCK_IMAGE = "assets/button.png"
FONT = pygame.font.Font('freesansbold.ttf', 24)

class Button(pygame.sprite.Sprite):
    def __init__(self, initial_x, initial_y, text, onclick_func):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(BLOCK_IMAGE)
        self.image = pygame.transform.smoothscale(self.image, (70, 40))  # (new width, new height)

        self.rect = self.image.get_rect()
        self.rect.x = initial_x
        self.rect.y = initial_y

        self.onclick_func = onclick_func

        self.text = text
        self.text = FONT.render(f"{self.text}", True, (255, 255, 255))
    
    # draw the sprite onto the screen
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))  # draw the image on the screen
        screen.blit(self.text, (self.rect.x+10, self.rect.y+7))

    # check collision with mouse
    def check_click(self, mouse):
        if self.rect.collidepoint(mouse):
            self.onclick_func()
            return True
    