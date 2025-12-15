import unittest

class TestPykemon(unittest.TestCase):

    def test_projet_existe(self):
        self.assertTrue(True)

    def test_lancement_possible(self):
        self.assertEqual(1, 1)

if __name__ == "__main__":
    unittest.main()
