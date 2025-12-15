import pygame

import config
from config import Config
from sound import Sound

class Console:

    def __init__(self, screen, inventory):
        print('CONSOLE LOADED')
        self.screen = screen
        self.inventory = inventory
        self.run_console = False
        self.user_text = ''
        self.task_text = ''
        self.base_font = pygame.font.Font(None, 32)
        self.color = (98, 234, 39)
        self.config = Config()
        self.sound = Sound()

    def console_dec(self):
        text_explication = self.base_font.render('*************************', True, self.color)
        self.screen.blit(text_explication, (10, 10))
        text_explication = self.base_font.render('Type "exit" to quit', True, self.color)
        self.screen.blit(text_explication, (10, 25))
        text_explication = self.base_font.render('Type "help" for help', True, self.color)
        self.screen.blit(text_explication, (10, 55))
        text_explication = self.base_font.render('*************************', True, self.color)
        self.screen.blit(text_explication, (10, 85))
        text_explication = self.base_font.render('>>>', True, (243, 8, 33))
        self.screen.blit(text_explication, (10, 530))

    def quit_console(self):
        self.run_console = False
        self.inventory.inventory_is_open = False
        self.task_text = ''
        if self.tiledmap == 'world1':
            self.sound.create_sound('spawn_world.mp3')
        elif self.tiledmap == 'world2':
            self.sound.create_sound('spawn_world2.mp3')
        elif self.tiledmap == 'world3':
            self.sound.create_sound('spawn_world3.mp3')

    def get_events(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_p]:
            if self.run_console == False:
                self.run_console = True
        if self.run_console:
            console = pygame.image.load('img/console.jpg').convert_alpha()
            console = pygame.transform.scale(console, self.screen.get_size())
            self.screen.blit(console, (0, 0))
            self.console_dec()
            self.input_rect = pygame.Rect(45, 530, 0, 0)
            self.task_text_rect = pygame.Rect(10, 120, 0, 0)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_KP_ENTER:
                        command = self.user_text.lower().split(' ')[0]
                        if command == 'exit':
                            self.quit_console()
                        elif command == 'help':
                            self.task_text = ['- reset', '- inventory on/off', '- sound on/off', '- fight on/off', '- health on/off', '- fps on/off']
                        elif command == 'reset':
                            self.game.switch_world('map', 'enter_house', 'player')
                            self.task_text = ["The command reset as been success"]
                        elif command == 'inventory':
                            arg = self.user_text.lower().split(' ')[1]
                            if arg == 'on':
                                self.config.inventory_loaded = True
                                self.task_text = ["The command inventory as been load to on", "Reload the game"]
                            elif arg == 'off':
                                self.config.inventory_loaded = False
                                self.task_text = ["The command inventory as been load to off", "Reload the game"]
                            else:
                                self.task_text = ["Invalid argument, Type 'help' for help"]
                        elif command == 'sound':
                            arg = self.user_text.lower().split(' ')[1]
                            if arg == 'on':
                                self.config.soundload = True
                                self.task_text = ["The command sound as been load to on", "Reload the game"]
                            elif arg == 'off':
                                self.config.soundload = False
                                self.task_text = ["The command sound as been load to off", "Reload the game"]
                            else:
                                self.task_text = ["Invalid argument, Type 'help' for help"]
                        elif command == 'fight':
                            arg = self.user_text.lower().split(' ')[1]
                            if arg == 'on':
                                self.config.fight_loaded = True
                                self.task_text = ["The command fight as been load to on", "Reload the game"]
                            elif arg == 'off':
                                self.config.fight_loaded = False
                                self.task_text = ["The command fight as been load to off", "Reload the game"]
                            else:
                                self.task_text = ["Invalid argument, Type 'help' for help"]
                        elif command == 'health':
                            arg = self.user_text.lower().split(' ')[1]
                            if arg == 'on':
                                self.config.health_loaded = True
                                self.task_text = ["The command health as been load to on", "Reload the game"]
                            elif arg == 'off':
                                self.config.health_loaded = False
                                self.task_text = ["The command health as been load to off", "Reload the game"]
                            else:
                                self.task_text = ["Invalid argument, Type 'help' for help"]
                        elif command == 'fps':
                            arg = self.user_text.lower().split(' ')[1]
                            if arg == 'on':
                                self.config.fps = True
                                self.task_text = ["The command fps as been load to on", "Reload the game"]
                            elif arg == 'off':
                                self.task_text = ["The command fps as been load to off", "Reload the game"]
                            else:
                                self.task_text = ["Invalid argument, Type 'help' for help"]
                        else:
                            self.task_text = ["Invalid command, Type 'help' for help"]
                        print("Command console execute : " + command)
                        self.user_text = ''
                    if event.key == pygame.K_BACKSPACE:
                        self.user_text = self.user_text[:-1]
                    elif event.key != pygame.K_KP_ENTER:
                        self.user_text += event.unicode
                if len(self.user_text) >= 15:
                    self.user_text = self.user_text[:-1]
            text_surface = self.base_font.render(self.user_text, True, (255, 255, 255))
            self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
            y = 120
            for text in self.task_text:
                font = pygame.font.SysFont('Arial', 32)
                word_surface = font.render(text, 0, self.color)
                word_width, word_height = word_surface.get_size()
                self.screen.blit(word_surface, (20, y))
                y += word_height
            pygame.draw.rect(self.screen, pygame.Color(0, 0, 0, 0), self.input_rect)
    def run(self, game, tiledmap):
        if config.Config.console_active(self):
            self.game = game
            self.tiledmap = tiledmap
            self.get_events()
