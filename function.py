from PIL import Image, ImageDraw
import pygame

import config


class Function:
    def __init__(self, screen):
        self.screen = screen

    def error(self, msg):
        img = Image.new('RGB', (200, 30), color=(0, 0, 0))
        d = ImageDraw.Draw(img)
        d.text((10, 10), msg, fill=(255, 0, 0))
        img.save('img/error.png')

        draw_image = pygame.image.load("img/error.png").convert_alpha()
        self.screen.blit(draw_image, (0, 0))

    def information(self, msg):
        img = Image.new('RGB', (150, 30), color=(0, 0, 0))
        d = ImageDraw.Draw(img)
        d.text((10, 10), msg, fill=(255, 165, 0))
        img.save('img/info.png')

        draw_image = pygame.image.load('img/info.png').convert_alpha()
        self.screen.blit(draw_image, (650, 1))

    def create(self, msg):
        img = Image.new('RGB', (80, 30), color=(255, 255, 255))
        d = ImageDraw.Draw(img)
        d.text((25, 10), msg, fill=(255, 50, 0))
        img.save('img/' + msg + '.png')

        draw = pygame.image.load('img/' + msg + '.png').convert_alpha()
        self.screen.blit(draw, (0, 0))

    def fps_stats(self, clock):
        self.clock = clock
        if config.Config.fps_show(self):
            try:
                draw_image_name = Image.new('RGB', (50, 30), color=(0, 0, 0))
                d_name = ImageDraw.Draw(draw_image_name)
                d_name.text((7, 7), self.clock + " FPS", fill=(135, 206, 250))
                draw_image_name.save('img/clock.png')
                draw_image_name_load = pygame.image.load('img/clock.png').convert_alpha()
                self.screen.blit(draw_image_name_load, (750, 575))
            except:
                print('ERROR FPS')

    #draw_image_name = Image.new('RGB', (120, 30), color=(255, 255, 255))
    #d_name = ImageDraw.Draw(draw_image_name)
    #d_name.text((10, 10), "Pokemon as healed", fill=(229, 52, 213))
    #draw_image_name.save('img/as_health.png')




