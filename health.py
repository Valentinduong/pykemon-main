import pygame

import config
from sound import Sound
import time

class Health:
    def __init__(self, screen):
        print('HEALTH LOADED')
        self.screen = screen
        self.heath_zone = []
        self.sound = Sound()


    def get_map(self):
        if self.map == 'house':
            for obj in self.tmx_data.objects:
                if obj.name == 'health_zone':
                    self.heath_zone.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
                    for sprite in self.group.sprites():
                        if sprite.feet.collidelist(self.heath_zone) > -1:
                            self.create_heath()

    def create_heath(self):
        pressed = pygame.key.get_pressed()
        draw_image_info_health = pygame.image.load('img/info_health.png').convert_alpha()
        self.screen.blit(draw_image_info_health, (350, 0))

        if pressed[pygame.K_f]:
            self.inventory.life = [100, 100, 100, 100, 100, 100, 100, 100]
            self.inventory.pokeball = 50
            self.sound.create_sound('healing-pokemon.mp3')
            time.sleep(7)
            draw_image_ashealth_load = pygame.image.load('img/as_health.png').convert_alpha()
            self.screen.blit(draw_image_ashealth_load, (350, 0))
            self.sound.create_sound('spawn_house.mp3')



    def run(self, tmx_data, group, map, player, inventory):
        if config.Config.health(self):
            self.tmx_data = tmx_data
            self.group = group
            self.map = map
            self.player = player
            self.inventory = inventory

            self.get_map()

