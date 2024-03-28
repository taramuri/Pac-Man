import unittest
from pacmanmain import move_player

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
