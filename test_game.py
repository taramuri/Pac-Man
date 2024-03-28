import unittest
from pacmanmain import check_collisions

class TestGameCounters(unittest.TestCase): #Перші прото тести
    def test_counter_update(self):
        # Початкові значення лічильників
        scor = 0
        power = False
        power_counter = 0
        eaten_ghosts = [False, False, False, False]

        # Створення гри і оновлення її стану
        updated_scor, updated_power, updated_power_counter, updated_eaten_ghosts = check_collisions(scor, power, power_counter, eaten_ghosts)

        # Перевірка, чи збільшився лічильник на 1
        self.assertEqual(updated_scor, 0)  # Очікуємо, що scor залишиться незмінним на цьому кроці

        # Перевірка, чи лічильник "power" оновлено вірно
        self.assertFalse(updated_power)

        # Перевірка, чи лічильник "power_counter" оновлено вірно
        self.assertEqual(updated_power_counter, 0)  # Очікуємо, що power_counter залишиться незмінним на цьому кроці

        # Перевірка, чи список "eaten_ghosts" оновлено вірно
        self.assertEqual(updated_eaten_ghosts, [False, False, False, False])  # Очікуємо, що eaten_ghosts залишиться незмінним на цьому кроці

if __name__ == '__main__':
    unittest.main()
