import sys
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QVBoxLayout, QWidget, QPushButton, QMessageBox
from PyQt5.QtCore import Qt, QFile
from balda_model import GameModel
from balda_view import GameView

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Игра Балда")
        self.setGeometry(100, 100, 520, 650)

        self.load_style("style.qss")

        self.model = GameModel()

        self.player1_score_label = QLabel("Игрок 1: 0 очков")
        self.player2_score_label = QLabel("Игрок 2: 0 очков")
        self.current_player_label = QLabel("Ходит: Игрок 1")
        self.player1_score_label.setAlignment(Qt.AlignCenter)
        self.player2_score_label.setAlignment(Qt.AlignCenter)
        self.current_player_label.setAlignment(Qt.AlignCenter)

        self.pass_button = QPushButton("Пропустить ход")
        self.pass_button.clicked.connect(self.handle_pass_turn)

        self.current_word_label = QLabel("Текущее слово:")
        self.current_word_label.setAlignment(Qt.AlignCenter)

        button_layout = QHBoxLayout()
        clear_button = QPushButton("Очистить текущее слово/введенную букву")
        clear_button.clicked.connect(self.clear_current_word)

        submit_button = QPushButton("Ввести слово")
        submit_button.clicked.connect(self.submit_word)

        button_layout.addWidget(clear_button)
        button_layout.addWidget(submit_button)

        self.game_view = GameView(self.model, [self.player1_score_label, self.player2_score_label], self.current_word_label)

        layout = QVBoxLayout()
        layout.addWidget(self.player1_score_label)
        layout.addWidget(self.player2_score_label)
        layout.addWidget(self.current_player_label)
        layout.addWidget(self.game_view)
        layout.addWidget(self.pass_button)
        layout.addWidget(self.current_word_label)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def load_style(self, filename):
        """Загрузите стиль из файла QSS."""
        file = QFile(filename)
        if file.open(QFile.ReadOnly):
            style = file.readAll()
            self.setStyleSheet(str(style, encoding='utf-8'))
            file.close()

    def handle_pass_turn(self):
        try:
            self.model.pass_turn()
            self.update_turn_display()
            
            if self.model.is_game_over():
                self.end_game()  
        except ValueError as e:
            QMessageBox.information(self, "Игра завершена", str(e))
            self.end_game()

    def clear_current_word(self):
        self.model.clear_current_actions()
        self.update_current_word()
        self.game_view.refresh_board()

    def submit_word(self):
        try:
            self.model.add_word()
            self.update_current_word()
            self.update_turn_display()
            self.game_view.refresh_board()
            
            if self.model.is_game_over():
                self.end_game()  
        except ValueError as e:
            QMessageBox.warning(self, "Ошибка", str(e))

    def end_game(self):
        self.pass_button.setDisabled(True)
        self.game_view.setDisabled(True)
        
        winner_message = ""
        if self.model.scores[0] > self.model.scores[1]:
            winner_message = "Победил игрок 1!"
        elif self.model.scores[0] < self.model.scores[1]:
            winner_message = "Победил игрок 2!"
        else:
            winner_message = "Игра окончена: Ничья!"
        
        reply = QMessageBox.question(self, "Игра завершена", winner_message + "\nХотите начать заново?",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        
        if reply == QMessageBox.Yes:
            self.reset_game()

    def update_turn_display(self):
        current_player = "Игрок 1" if self.model.current_player == 0 else "Игрок 2"
        self.current_player_label.setText(f"Ходит: {current_player}")

        self.player1_score_label.setText(f"Игрок 1: {self.model.scores[0]} очков")
        self.player2_score_label.setText(f"Игрок 2: {self.model.scores[1]} очков")

    def update_current_word(self):
        self.current_word_label.setText(f"Текущее слово: {self.model.current_word}")

    def reset_game(self):
        self.model.reset_game()
        self.update_turn_display()
        self.current_word_label.setText("Текущее слово:")
        self.game_view.refresh_board()
        self.pass_button.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
