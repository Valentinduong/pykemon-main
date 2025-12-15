import pygame
import config

class Sound:

    def __init__(self):
        print('SOUND LOADED')

    def create_sound(self, sound):
        if config.Config.sound_loaded(self):
            pygame.mixer.music.load('sound/' + sound)
            pygame.mixer.music.play(0)
            print('SOUND PLAYED : ' + sound)

