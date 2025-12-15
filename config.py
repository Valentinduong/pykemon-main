class Config:
    def __init__(self):
        print('CONFIG LOADED')

    def screen(self):
        self.screen = (800, 600)
        return self.screen

    def system_speed(self):
        self.system_speed = (20**2)/6.6
        return self.system_speed

    def console_active(self):
        self.console_active = True
        return self.console_active

    def sound_loaded(self):
        self.soundload = True
        return self.soundload

    def fight(self):
        self.fight_loaded = True
        return self.fight_loaded

    def health(self):
        self.health_loaded = True
        return self.health_loaded

    def inventory(self):
        self.inventory_loaded = True
        return self.inventory_loaded

    def fps_show(self):
        self.fps = False
        return self.fps
