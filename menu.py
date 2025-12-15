import pygame

class Menu:
    def __init__(self, screen):
        self.menu_time = 0
        self.screen = screen
        self.time = 100
        self.menu = pygame.image.load("img/menu_principal.jpg").convert_alpha()
        self.menu = pygame.transform.scale(self.menu, self.screen.get_size())

    def run(self):
        if self.menu_time <= self.time:
            self.menu_time = self.menu_time + 1
            return self.screen.blit(self.menu, (0, 0))
