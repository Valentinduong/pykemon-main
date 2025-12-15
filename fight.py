import pygame
import random
from PIL import Image, ImageDraw
import time

import config
from function import Function
from sound import Sound


class Fight:

    def __init__(self, screen):
        print("FIGHT LOADED")
        self.screen = screen
        self.function = Function(self.screen)

        self.in_fight = False
        self.zone = []
        self.capa = []

        self.pokemon = [
            "florizarre", "dracaufeu", "tortank", "papilusion", "roucool", "rattata",
            "onix", "smogogo", "arcanin", "akwakwak", "triopikeur", "nosferalto",
            "staross", "insecateur", "ptera", "ronflex", "evoli", "sulfura"
        ]

        self.capacity = [
            "charge", "Acid", "Acrobatics", "Aeroblast", "MaxAirstream", "GrassPledge",
            "WaterPledge", "AquaJet", "Assurance", "MorningSun", "PyroBall", "Sing",
            "DefenseCurl", "ElectroBall", "BugBuzz", "BrutalSwing", "Tickle"
        ]

        self.wait = 250
        self.in_attak = True
        self.change = False

        self.transition = False
        self.transitionWait = 0

        self.no_capture = False
        self.errorMess = ""

        self.active_slot = 0  # Pokémon actif côté joueur

        self.sound = Sound()

    # =========================
    # Utils
    # =========================
    def first_alive_slot(self):
        # Si tu as choisi un slot vivant, on le garde
        if 0 <= self.active_slot < len(self.inventory.inv):
            if self.active_slot < len(self.inventory.life) and self.inventory.life[self.active_slot] > 0:
                return self.active_slot

        # Sinon premier vivant
        for i in range(min(len(self.inventory.inv), len(self.inventory.life))):
            if self.inventory.life[i] > 0:
                self.active_slot = i
                return i
        return None

    def remove_dead(self, idx):
        if idx is None:
            return
        if idx < 0 or idx >= len(self.inventory.inv):
            return
        if self.inventory.life[idx] > 0:
            return
        # Utilise ta fonction existante dans inventory.py
        self.inventory.remove_inventory(self.inventory.inv[idx], idx)

    # =========================
    # Capacity images (FIX)
    # =========================
    def get_capacity(self):
        # Crée une image pour la dernière capacité ajoutée
        self.number_capa += 1

        capa_one = Image.new('RGB', (100, 40), color=(255, 255, 255))
        one_draw = ImageDraw.Draw(capa_one)

        last_capa = self.capa[-1]
        print('Capacity "' + last_capa + '" as create.')

        one_draw.text((100 / 4, 40 / 4), last_capa, fill=(192, 192, 192))
        capa_one.save('img/charge' + str(self.number_capa) + '.png')

    # =========================
    # Fight trigger
    # =========================
    def get_fight(self):
        if self.map == 'world':
            for obj in self.tmx_data.objects:
                if obj.name == "fight_zone":
                    self.zone.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
                    for sprite in self.group.sprites():
                        if sprite.feet.collidelist(self.zone) > -1:
                            if random.randint(1, 1000) == 1000:
                                self.in_attak = True
                                self.transition = True
                                self.transitionWait = 0

                                self.life_battle = 100
                                self.pokemon_number = random.randint(1, len(self.pokemon))

                                self.capa = []
                                self.number_capa = 0

                                print("FIGHT VERSUS", self.pokemon[self.pokemon_number - 1])

                                for _ in range(4):
                                    cap = random.choice(self.capacity)
                                    self.capa.append(cap)
                                    self.get_capacity()
                                    self.sound.create_sound('pokemon-battle.mp3')

    # =========================
    # Draw fight
    # =========================
    def for_fight(self):
        for sprite in self.group.sprites():
            sprite.move_back()

        bg = pygame.image.load("img/battle.png").convert_alpha()
        bg = pygame.transform.scale(bg, self.screen.get_size())
        self.screen.blit(bg, (0, 0))

        enemy_img = pygame.image.load(f"img/{self.pokemon[self.pokemon_number - 1]}.png").convert_alpha()
        enemy_img = pygame.transform.scale(enemy_img, (154, 154))
        self.screen.blit(enemy_img, (510, 90))

        self.draw_enemy_life()
        self.get_inv()
        self.item_battle()

    def draw_enemy_life(self):
        img = Image.new('RGB', (295, 35), (255, 255, 255))
        d = ImageDraw.Draw(img)

        if self.life_battle > 50:
            color = (50, 202, 50)
        elif self.life_battle >= 20:
            color = (255, 105, 180)
        else:
            color = (255, 0, 0)

        d.text((95, 12), f'Life : {self.life_battle}/100', fill=color)
        img.save('img/life.png')

        self.screen.blit(pygame.image.load('img/life.png').convert_alpha(), (50, 105))

        img2 = Image.new('RGB', (295, 40), (255, 255, 255))
        d2 = ImageDraw.Draw(img2)
        d2.text((95, 12), self.pokemon[self.pokemon_number - 1], fill=(135, 206, 250))
        img2.save('img/name.png')
        self.screen.blit(pygame.image.load('img/name.png').convert_alpha(), (50, 65))

    # =========================
    # Player Pokémon display
    # =========================
    def get_inv(self):
        # Nettoie les morts (au cas où)
        i = 0
        while i < min(len(self.inventory.inv), len(self.inventory.life)):
            if self.inventory.life[i] <= 0 and len(self.inventory.inv) > 1:
                self.remove_dead(i)
                continue
            i += 1

        idx = self.first_alive_slot()
        if idx is None:
            self.function.error("You don't have Pokemon")
            self.Quit_fight()
            return

        self.draw_player(self.inventory.inv[idx], self.inventory.life[idx])

    def draw_player(self, item, life):
        img = pygame.image.load(f'img/{item}.png').convert_alpha()
        img = pygame.transform.scale(img, (154, 154))
        img = pygame.transform.flip(img, True, False)
        self.screen.blit(img, (100, 265))

        self.draw_life_box(life, 450, 385, 'life_set.png')
        self.draw_text_box(item, 450, 355, 'name_battle.png')

    def draw_life_box(self, life, x, y, filename):
        img = Image.new('RGB', (100, 30), (255, 255, 255))
        d = ImageDraw.Draw(img)

        if life > 50:
            color = (50, 202, 50)
        elif life >= 20:
            color = (255, 105, 180)
        else:
            color = (255, 0, 0)

        d.text((10, 10), f'Life : {life}/100', fill=color)
        img.save(f'img/{filename}')
        self.screen.blit(pygame.image.load(f'img/{filename}').convert_alpha(), (x, y))

    def draw_text_box(self, text, x, y, filename):
        img = Image.new('RGB', (100, 30), (255, 255, 255))
        d = ImageDraw.Draw(img)
        d.text((10, 10), text, fill=(135, 206, 250))
        img.save(f'img/{filename}')
        self.screen.blit(pygame.image.load(f'img/{filename}').convert_alpha(), (x, y))

    # =========================
    # Change Pokémon menu
    # =========================
    def Change(self):
        bg = pygame.image.load("img/menu.jpg").convert_alpha()
        bg = pygame.transform.scale(bg, self.screen.get_size())
        self.screen.blit(bg, (0, 0))

        pokeball_img = Image.new('RGB', (160, 30), color=(255, 255, 255))
        draw_pokeball = ImageDraw.Draw(pokeball_img)
        draw_pokeball.text((10, 8), 'Pokéball : ' + str(self.inventory.pokeball), fill=(229, 100, 52))
        pokeball_img.save('img/pokeball.png')
        self.screen.blit(pygame.image.load('img/pokeball.png').convert_alpha(), (320, 0))

        for i, item in enumerate(self.inventory.inv):
            x = 180 if i < 4 else 425
            y = 140 + (i % 4) * 80

            rect = pygame.Rect(x, y, 220, 70)
            if pygame.mouse.get_pressed()[0] and rect.collidepoint(pygame.mouse.get_pos()):
                if self.inventory.life[i] > 0:
                    self.active_slot = i
                    self.change = False

            self.draw_item(item, x, y, self.inventory.life[i])

    def draw_item(self, item, x, y, life):
        self.draw_life_box(life, x + 80, y + 25, 'life.png')
        self.draw_text_box(item, x + 80, y, 'name.png')

        poke = pygame.image.load(f'img/{item}.png').convert_alpha()
        poke = pygame.transform.scale(poke, (65, 50))
        self.screen.blit(poke, (x, y))

    # =========================
    # Fight menu
    # =========================
    def item_battle(self):
        if pygame.mouse.get_pressed()[0]:
            if pygame.Rect(90, 450, 80, 30).collidepoint(pygame.mouse.get_pos()):
                self.Quit_fight()
            elif pygame.Rect(90, 485, 80, 30).collidepoint(pygame.mouse.get_pos()):
                self.change = True
            elif pygame.Rect(90, 520, 80, 30).collidepoint(pygame.mouse.get_pos()):
                self.capture()
            elif pygame.Rect(470, 450, 210, 110).collidepoint(pygame.mouse.get_pos()) or self.in_attak is False:
                self.attack()

        self.screen.blit(pygame.image.load('img/Fuir.png').convert_alpha(), (90, 450))
        self.screen.blit(pygame.image.load('img/Change.png').convert_alpha(), (90, 485))
        self.screen.blit(pygame.image.load('img/Capture.png').convert_alpha(), (90, 520))

        self.screen.blit(pygame.image.load('img/charge1.png').convert_alpha(), (470, 450))
        self.screen.blit(pygame.image.load('img/charge2.png').convert_alpha(), (470, 520))
        self.screen.blit(pygame.image.load('img/charge3.png').convert_alpha(), (580, 450))
        self.screen.blit(pygame.image.load('img/charge4.png').convert_alpha(), (580, 520))

    # =========================
    # Fight logic
    # =========================
    def attack(self):
        if self.in_attak:
            # toi tu tapes plus fort
            dmg = random.randint(20, 40)
            self.life_battle -= dmg
            print("Life pokemon :", self.life_battle)
            self.in_attak = False

            if self.life_battle <= 0:
                self.Quit_fight()
        else:
            idx = self.first_alive_slot()
            if idx is None:
                self.Quit_fight()
                return

            # ennemi tape moins fort
            dmg = random.randint(5, 15)
            self.inventory.life[idx] -= dmg
            print("Attack pokemon to player : -" + str(dmg))

            # si ton pokémon meurt -> remove inventaire
            if self.inventory.life[idx] <= 0:
                self.inventory.life[idx] = 0
                if len(self.inventory.inv) > 1:
                    self.remove_dead(idx)

            self.in_attak = True

    # =========================
    # Capture
    # =========================
    def capture(self):
        self.no_capture = False
        self.errorMess = ""

        if self.inventory.pokeball > 0:
            self.inventory.pokeball -= 1

            # 50% environ
            if random.randint(1, 10) >= 6:
                if len(self.inventory.inv) < 8:
                    self.inventory.add_inventory(self.pokemon[self.pokemon_number - 1])
                    # auto-select le dernier capturé
                    self.active_slot = len(self.inventory.inv) - 1
                    self.Quit_fight()
                else:
                    self.errorMess = "No space"
                    self.no_capture = True
            else:
                self.errorMess = "Capture failed"
                self.no_capture = True
        else:
            self.errorMess = "No Pokeball"
            self.no_capture = True

    # =========================
    # Exit
    # =========================
    def Quit_fight(self):
        self.in_attak = True
        self.in_fight = False
        self.change = False
        self.no_capture = False
        self.errorMess = ""
        self.sound.create_sound('escape_pokemon.mp3')
        time.sleep(1)
        self.sound.create_sound('spawn_world.mp3')

    # =========================
    # Main loop
    # =========================
    def run(self, tmx_data, group, map, player, inventory):
        if config.Config.fight(self):
            self.tmx_data = tmx_data
            self.group = group
            self.map = map
            self.player = player
            self.inventory = inventory

            if not self.in_fight:
                self.get_fight()
            else:
                self.for_fight()

            if self.change:
                self.Change()

            if self.transition:
                if self.transitionWait <= self.wait:
                    self.transitionWait += 1
                    transition = pygame.image.load('img/noir.jpg').convert_alpha()
                    transition = pygame.transform.scale(transition, self.screen.get_size())
                    self.transition = False
                    self.in_fight = True
                    return self.screen.blit(transition, (0, 0))

            if self.no_capture:
                img = Image.new('RGB', (155, 30), color=(0, 0, 0))
                d = ImageDraw.Draw(img)
                d.text((10, 10), self.errorMess, fill=(255, 0, 0))
                img.save('img/error.png')
                self.screen.blit(pygame.image.load('img/error.png').convert_alpha(), (350, 0))
