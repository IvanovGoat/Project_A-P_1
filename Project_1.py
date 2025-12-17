import tkinter as tk
import random

WORDS = [
    "кот", "дом", "лес", "мост", "свет", "лодка", "пирог", "яблоко",
    "машина", "стол", "ручка", "книга", "звезда", "планета", "огонь",
    "время", "птица", "рыба", "небо", "ветер", "солнце", "луна",
    "окно", "дверь", "стена", "поле", "река", "гора", "лиса"
]

ALPHABET = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"


def get_random_word():
    """
    Возвращает случайное слово длиной от 4 до 8 символов из списка WORDS.

    :return: Случайное слово в нижнем регистре
    :rtype: str
    :raises ValueError: Если в WORDS нет слов длиной от 4 до 8 символов
    """
    valid_words = [word for word in WORDS if 4 <= len(word) <= 8]
    if not valid_words:
        raise ValueError("Нет подходящих слов в списке WORDS.")
    return random.choice(valid_words).lower()


class Game:
    def __init__(self, root):
        """
        Инициализирует окно и игровые переменные.

        :param root: Корневое окно Tkinter
        :type root: tk.Tk
        """
        self.root = root
        self.root.title("Виселица")
        self.root.geometry("720x380")
        self.root.resizable(False, False)

        try:
            self.word = get_random_word()
        except ValueError as e:
            self.word = "ошибка"
            print(f"Ошибка при выборе слова: {e}")

        self.guessed_letters = set()
        self.used_letters = set()
        self.attempts_left = 5
        self.game_over = False
        self.alphabet_labels = {}

        self.setup_ui()
        self.update_display()
        self.root.bind("<Key>", self.on_key_press)

    def setup_ui(self):
        """
        Создаёт интерфейс игры: отображение слова, попыток, результата,
        кнопки «Заново» и алфавита в сетке 6×6 справа.
        """
        main = tk.Frame(self.root)
        main.pack(fill="both", expand=True, padx=20, pady=20)

        left = tk.Frame(main)
        left.pack(side="left", fill="y")

        tk.Label(left, text="Виселица", font=("Arial", 16, "bold")).pack(pady=(0, 15))

        self.word_label = tk.Label(left, text="", font=("Courier", 24))
        self.word_label.pack(pady=10, padx=(80, 80))

        self.attempts_label = tk.Label(left, text="", font=("Arial", 12))
        self.attempts_label.pack(pady=5)

        self.result_label = tk.Label(left, text="", font=("Arial", 12, "bold"))
        self.result_label.pack(pady=15)

        self.reset_button = tk.Button(left, text="Заново", command=self.reset_game)
        self.reset_button.pack(pady=10)

        right = tk.Frame(main, relief="sunken", borderwidth=1)
        right.pack(side="right", fill="y", padx=(20, 0))

        tk.Label(right, text="Алфавит", font=("Arial", 10, "underline")).pack(pady=(5, 10))

        grid = tk.Frame(right)
        grid.pack(padx=10)

        for i, letter in enumerate(ALPHABET):
            row = i // 6
            col = i % 6
            lbl = tk.Label(grid, text=letter.upper(), font=("Courier", 11), width=2)
            lbl.grid(row=row, column=col, padx=3, pady=2)
            self.alphabet_labels[letter] = lbl

        for j in range(3):
            row = 5
            col = 3 + j
            tk.Label(grid, text="", width=2).grid(row=row, column=col, padx=3, pady=2)

    def on_key_press(self, event):
        """
        Обрабатывает нажатие клавиши: принимает только русские буквы,
        игнорирует всё остальное, повторные вводы и ввод после окончания игры.

        :param event: Событие нажатия клавиши
        :type event: tk.Event
        """
        if self.game_over:
            return

        char = event.char.lower()
        if len(char) != 1 or char not in ALPHABET:
            return
        if char in self.used_letters:
            return

        self.used_letters.add(char)
        self.update_alphabet_display(char)

        if char in self.word:
            self.guessed_letters.add(char)
        else:
            self.attempts_left -= 1

        self.update_display()

    def update_alphabet_display(self, letter):
        """
        Вычёркивает букву в алфавите, применяя overstrike к соответствующей метке.

        :param letter: Буква для зачёркивания
        :type letter: str
        """
        lbl = self.alphabet_labels.get(letter)
        if lbl:
            lbl.config(font=("Courier", 11, "overstrike"))

    def update_display(self):
        """
        Обновляет отображение слова и количества оставшихся попыток.
        """
        displayed = " ".join(letter.upper() if letter in self.guessed_letters else "_" for letter in self.word)
        self.word_label.config(text=displayed)
        self.attempts_label.config(text=f"Попыток: {self.attempts_left}")
        self.check_game_end()

    def check_game_end(self):
        """
        Проверяет, завершена ли игра: победа (все буквы угаданы) или поражение (попытки закончились).
        Устанавливает флаг game_over при завершении.
        """
        if all(letter in self.guessed_letters for letter in self.word):
            self.result_label.config(text="ПОБЕДА!")
            self.game_over = True
        elif self.attempts_left <= 0:
            self.result_label.config(text=f"ПОРАЖЕНИЕ! Слово: {self.word.upper()}")
            self.game_over = True
        else:
            self.result_label.config(text="")

    def reset_game(self):
        """
        Сбрасывает игру: выбирает новое слово, очищает состояния,
        снимает зачёркивание с букв алфавита и обновляет интерфейс.
        """
        try:
            self.word = get_random_word()
        except ValueError as e:
            self.word = "ошибка"
            print(f"Ошибка при сбросе: {e}")

        self.guessed_letters.clear()
        self.used_letters.clear()
        self.attempts_left = 5
        self.game_over = False

        for lbl in self.alphabet_labels.values():
            lbl.config(font=("Courier", 11))

        self.update_display()
        self.result_label.config(text="")


if __name__ == "__main__":
    root = tk.Tk()
    Game(root)
    root.mainloop()