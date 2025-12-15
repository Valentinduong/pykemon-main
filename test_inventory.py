import unittest
import pygame
from inventory import Inventory

pygame.init()
pygame.display.set_mode((1, 1))


class FakeGroup:
    def sprites(self):
        return []


class FakeTmxData:
    objects = []


class TestInventory(unittest.TestCase):

    def setUp(self):
        fake_screen = pygame.display.get_surface()
        fake_group = FakeGroup()
        fake_tmx_data = FakeTmxData()

        self.inventory = Inventory(fake_screen, fake_group, fake_tmx_data)

        self.inventory.inv = []
        self.inventory.life = []
        self.inventory.pokeball = 0

    def test_add_inventory_adds_pokemon(self):
        self.inventory.add_inventory("pikachu")
        self.assertEqual(self.inventory.inv, ["pikachu"])

    def test_add_inventory_increases_inventory_size(self):
        self.inventory.add_inventory("pikachu")
        self.inventory.add_inventory("salameche")
        self.assertEqual(len(self.inventory.inv), 2)

    def test_remove_inventory_when_multiple_pokemon(self):
        # Préparation cohérente de l'état interne
        self.inventory.inv = ["pikachu", "salameche"]
        self.inventory.life = [100, 100]

        self.inventory.remove_inventory("pikachu", 0)

        self.assertNotIn("pikachu", self.inventory.inv)
        self.assertEqual(len(self.inventory.inv), 1)


if __name__ == "__main__":
    unittest.main()
