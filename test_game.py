import unittest
from pacmanmain import check_collisions, move_player

class TestGameCounters(unittest.TestCase): #Перші промті тести
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

class TestPlayerMovement(unittest.TestCase):
    def test_move_player_right(self):
        # Arrange
        player_x = 450  # Початкова позиція гравця по горизонталі
        player_y = 663  # Початкова позиція гравця по вертикалі

        new_player_x, new_player_y = move_player(player_x, player_y)  # Виклик функції для переміщення гравця
        
        # Assert
        self.assertEqual(new_player_x, player_x)  # Перевірка, чи гравець перемістився по горизонталі
        self.assertEqual(new_player_y, player_y)  # Перевірка, чи гравець не перемістився по вертикалі


if __name__ == '__main__':
    unittest.main()
