import unittest

from balda_model import GameModel

class TestGameModel(unittest.TestCase):
    def setUp(self):
        """Создаем экземпляр GameModel перед каждым тестом."""
        self.model = GameModel()

    def test_initial_board(self):
        """Проверяем, что начальная доска содержит правильное слово."""
        expected_board = [
            ["", "", "", "", ""],
            ["", "", "", "", ""],
            ["Б", "А", "Л", "Д", "А"],
            ["", "", "", "", ""],
            ["", "", "", "", ""]
        ]
        self.assertEqual(self.model.board, expected_board)

    def test_add_letter_to_board(self):
        """Проверяем добавление буквы на доску."""
        self.model.add_letter_to_board(0, 0, 'К')
        self.assertEqual(self.model.board[0][0], 'К')

    def test_is_valid_letter(self):
        """Проверяем, что метод is_valid_letter работает правильно."""
        self.model.add_letter_to_board(0, 0, 'К')
        self.model.current_letter_pos = [0, 0]
        self.assertTrue(self.model.is_valid_letter(0, 1))  
        self.assertFalse(self.model.is_valid_letter(2, 2))  

    def test_add_letter_to_word(self):
        """Проверяем добавление буквы к текущему слову."""
        self.model.add_letter_to_board(0, 0, 'К')
        self.model.current_letter_pos = [0, 0]
        self.model.add_letter_to_word(0, 0) 
        self.assertEqual(self.model.current_word, 'К')

    def test_add_word(self):
        """Проверяем добавление слова в список использованных слов."""
        self.model.add_letter_to_board(0, 0, 'К')
        self.model.current_letter_pos = [0, 0]
        self.model.add_letter_to_word(0, 0)  
        self.model.add_word()  
        self.assertIn('к', self.model.word_list)  

    def test_reset_game(self):
        """Проверяем сброс состояния игры."""
        self.model.add_letter_to_board(0, 0, 'К')
        self.model.add_letter_to_word(0, 0)
        self.model.add_word()
        self.model.reset_game()
        self.assertEqual(self.model.scores, [0, 0])
        self.assertEqual(self.model.word_list, set())
        self.assertEqual(self.model.pass_count, 0)
        self.assertEqual(self.model.current_player, 0)
        self.assertEqual(self.model.board[2], ["Б", "А", "Л", "Д", "А"])

    def test_word_already_used(self):
        """Проверяем, что повторное использование слова вызывает ошибку."""
        self.model.add_letter_to_board(0, 0, 'К')
        self.model.current_letter_pos = [0, 0]
        self.model.add_letter_to_word(0, 0)
        self.model.add_word()
        with self.assertRaises(ValueError):
            self.model.add_word()

if __name__ == '__main__':
    unittest.main()
