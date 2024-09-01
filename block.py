import pygame
pygame.init()  # initialize pygame

BLOCK_IMAGE = "assets/block.png"
FONT = pygame.font.Font('freesansbold.ttf', 32)

class Block(pygame.sprite.Sprite):
    def __init__(self, initial_x, initial_y, value):
        pygame.sprite.Sprite.__init__(self)

        if (value != 0):
            self.image = pygame.image.load(BLOCK_IMAGE)
            self.image = pygame.transform.smoothscale(self.image, (60, 60))  # (new width, new height)
        else:
            self.image = pygame.Surface((60, 60), pygame.SRCALPHA)

        self.rect = self.image.get_rect()
        self.rect.x = initial_x
        self.rect.y = initial_y
        self.value = value

        self.value_image = FONT.render(f"{self.value}", True, (255, 255, 255))
    
    # draw the sprite onto the screen
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))  # draw the image on the screen
        if (self.value != 0):
            screen.blit(self.value_image, (self.rect.x + 22, self.rect.y + 15))

    # check collision with mouse
    def check_click(self, mouse):
        if self.rect.collidepoint(mouse):
            print(f"clicked {self.value}")
            return True

    # method for swapping the block and the zero block
    def swap(self, zero_block):
        old_self_x = self.rect.x
        old_self_y = self.rect.y

        self.rect.x = zero_block.rect.x
        self.rect.y = zero_block.rect.y

        zero_block.rect.x = old_self_x
        zero_block.rect.y = old_self_y
    