from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor, QFont
from PyQt5.QtWidgets import QMessageBox, QGraphicsRectItem, QGraphicsTextItem, QGraphicsScene, \
    QGraphicsView


class GameView(QGraphicsView):
    def __init__(self, model, score_labels, current_word_label):
        super().__init__()
        self.model = model
        self.score_labels = score_labels
        self.current_word_label = current_word_label
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.init_ui()

        self.selected_cells = []
        self.editing_text_item = None

        self.set_font_size(20)

    def set_font_size(self, size):
        font = QFont()
        font.setPointSize(size)

        for row in self.cells:
            for rect, text_item in row:
                text_item.setFont(font)

    def init_ui(self):
        self.setFixedSize(502, 502)
        self.scene.setSceneRect(0, 0, 500, 500)

        self.cells = []
        for y in range(5):
            row = []
            for x in range(5):
                rect = QGraphicsRectItem(x * 100, y * 100, 100, 100)
                rect.setBrush(QBrush(QColor("white")))
                rect.setPen(QColor("black"))
                self.scene.addItem(rect)

                text_item = QGraphicsTextItem()
                text_item.setDefaultTextColor(Qt.black)
                text_item.setPos(x * 100 + 40, y * 100 + 40)
                text_item.setTextInteractionFlags(Qt.NoTextInteraction)
                self.scene.addItem(text_item)

                if self.model.board[y][x]:
                    text_item.setPlainText(self.model.board[y][x])

                row.append((rect, text_item))
            self.cells.append(row)

    def mousePressEvent(self, event):
        x = int(event.x() // 100)
        y = int(event.y() // 100)

        if 0 <= x < 5 and 0 <= y < 5:
            if self.model.board[y][x] == "":
                self.start_text_editing(x, y)
            else:
                try:
                    self.model.add_letter_to_word(x, y)
                    self.update_current_word()
                except ValueError as e:
                    QMessageBox.warning(self, "Ошибка", str(e))

    def start_text_editing(self, x, y):
        rect, text_item = self.cells[y][x]
        if self.editing_text_item:
            self.finish_text_editing()
            return

        text_item.setTextInteractionFlags(Qt.TextEditorInteraction)
        text_item.setFocus()
        self.editing_text_item = (x, y, text_item)

    def finish_text_editing(self):
        if not self.editing_text_item:
            return

        x, y, text_item = self.editing_text_item
        letter = text_item.toPlainText().strip().upper()

        if len(letter) != 1 or not letter.isalpha():
            QMessageBox.warning(self, "Ошибка", "Некорректный ввод! Введите одну букву.")
            text_item.setPlainText("")
        else:
            try:
                self.model.add_letter_to_board(x, y, letter)
            except ValueError as e:
                    QMessageBox.warning(self, "Ошибка", str(e))

        text_item.setTextInteractionFlags(Qt.NoTextInteraction)
        self.editing_text_item = None
        self.refresh_board()

    def refresh_board(self):
        self.scene.clear()
        self.init_ui()

    def update_scores(self):
        self.score_labels[0].setText(f"Игрок 1: {self.model.scores[0]} очков")
        self.score_labels[1].setText(f"Игрок 2: {self.model.scores[1]} очков")

    def update_current_word(self):
        self.current_word_label.setText(f"Текущее слово: {self.model.current_word}")