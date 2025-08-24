from coin import Coin
from monster import Monster
from door import Door

class Spawn:
    def __init__(self, spawn_interval=500, min_spawn_interval=300):
        self.spawn_counter = 200
        self.spawn_interval = spawn_interval
        self.min_spawn_interval = min_spawn_interval
        self.spawn_position = 0

    def update(self):
        self.spawn_counter += 1

class CoinSpawn(Spawn):
    def __init__(self):
        super().__init__(spawn_interval=200, min_spawn_interval=150)
        self.spawn_position = 0

    def generate(self, window, image, robot, **kwargs):
        if self.spawn_counter >= self.spawn_interval:
            self.spawn_interval = max(
                self.min_spawn_interval,
                self.spawn_interval - 5
            )
            self.spawn_counter = 0

            self.spawn_position = (self.spawn_position * 3 + robot.x + 150) % (window.get_width() - image.get_width())

            return self._create_object(
                self.spawn_position,
                0,
                image,
                window,
                **kwargs
            )
        return None

    def _create_object(self, x, y, image, window):
        return Coin(x, y, image, window)

class MonsterSpawn(Spawn):
    def __init__(self):
        super().__init__(spawn_interval=300, min_spawn_interval=200)
        self.spawn_position = 300

    def generate(self, window, image, robot, **kwargs):
        if self.spawn_counter >= self.spawn_interval:
            self.spawn_interval = max(
                self.min_spawn_interval,
                self.spawn_interval - 10
            )
            self.spawn_counter = 0

            self.spawn_position = (self.spawn_position * 2 + robot.x + 200) % (window.get_width() - image.get_width())

            return self._create_object(
                self.spawn_position,
                0,
                image,
                window,
                **kwargs
            )
        return None

    def _create_object(self, x, y, image, window):
        return Monster(x, y, image, window)

class DoorSpawn(Spawn):
    def __init__(self):
        super().__init__(spawn_interval=3000, min_spawn_interval=1000)
        self.spawn_position = 0

    def generate(self, window, image, robot, **kwargs):
        if self.spawn_counter >= self.spawn_interval:
            self.spawn_interval = max(
                self.min_spawn_interval,
                self.spawn_interval - 200
            )
            self.spawn_counter = 0

            self.spawn_position = (self.spawn_position * 2 + robot.x + 250) % (window.get_width() - image.get_width())

            return self._create_object(
                self.spawn_position,
                0,
                image,
                window,
                **kwargs
            )
        return None

    def _create_object(self, x, y, image, window):
        return Door(x, y, image, window)