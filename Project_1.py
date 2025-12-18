import tkinter
import tkinter.messagebox
import random

WORDS = [
    # "кот"
    "мост", "свет", "лодка", "пирог", "яблоко",
    "машина", "стол", "ручка", "книга", "звезда", "планета", "огонь",
    "время", "птица", "рыба", "небо", "ветер", "солнце", "луна",
    "окно", "дверь", "стена", "поле", "река", "гора", "лиса"
]

ALPHABET = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"


def get_random_word():
    """
    Возвращает случайное слово длиной от 4 до 8 символов из списка WORDS.

    :return: Случайное слово в нижнем регистре.
    :rtype: str
    :raises ValueError: Если нет слов подходящей длины.
    """
    valid_words = [word for word in WORDS if 4 <= len(word) <= 8]
    if not valid_words:
        raise ValueError("Нет подходящих слов в списке WORDS.")
    return random.choice(valid_words).lower()


class Game:
    """
    Класс для управления игрой "Виселица" в графическом интерфейсе Tkinter.

    :ivar root: Корневое окно Tkinter.
    :type root: tk.Tk

    :ivar word: Загаданное слово.
    :type word: str

    :ivar guessed_letters: Множество угаданных букв.
    :type guessed_letters: set[str]

    :ivar used_letters: Множество всех использованных букв.
    :type used_letters: set[str]

    :ivar attempts_left: Оставшееся количество попыток.
    :type attempts_left: int

    :ivar game_over: Флаг, указывающий, завершена ли игра.
    :type game_over: bool

    :ivar alphabet_labels: Словарь, связывающий букву алфавита с её меткой на экране.
    :type alphabet_labels: dict[str, tk.Label]

    :ivar word_label: Метка для отображения загаданного слова.
    :type word_label: tk.Label

    :ivar attempts_label: Метка для отображения количества оставшихся попыток.
    :type attempts_label: tk.Label

    :ivar result_label: Метка для отображения результата игры.
    :type result_label: tk.Label

    :ivar reset_button: Кнопка "Заново", сбрасывающая игру.
    :type reset_button: tk.Button
    """

    def __init__(self, root):
        """
        Инициализирует окно и игровые переменные.

        :param root: Корневое окно Tkinter.
        :type root: tkinter.Tk
        """
        self.root = root
        self.root.title("Виселица")
        self.root.geometry("720x380")
        self.root.resizable(False, False)

        try:
            self.word = get_random_word()
        except ValueError:
            tkinter.messagebox.showerror(
                "Критическая ошибка",
                "Список слов не содержит подходящих вариантов (длина 4–8 букв)"
            )
            self.root.destroy()

        self.guessed_letters = set()
        self.used_letters = set()
        self.attempts_left = 5
        self.game_over = False
        self.alphabet_labels = {}

        self.setup_ui()
        self.update_display()
        self.root.bind("<Key>", self.on_key_press)

    def setup_ui(self):
        """Создаёт графический интерфейс игры."""
        main = tkinter.Frame(self.root)
        main.pack(fill="both", expand=True, padx=20, pady=20)

        left = tkinter.Frame(main)
        left.pack(side="left", fill="y")

        tkinter.Label(left, text="Виселица", font=("Arial", 16, "bold")).pack(
            pady=(0, 15)
        )

        self.word_label = tkinter.Label(left, text="", font=("Courier", 24))
        self.word_label.pack(pady=10, padx=(80, 80))

        self.attempts_label = tkinter.Label(left, text="", font=("Arial", 12))
        self.attempts_label.pack(pady=5)

        self.result_label = tkinter.Label(
            left, text="", font=("Arial", 12, "bold")
        )
        self.result_label.pack(pady=15)

        self.reset_button = tkinter.Button(
            left, text="Заново", command=self.reset_game
        )
        self.reset_button.pack(pady=10)

        right = tkinter.Frame(main)
        right.pack(side="right", fill="y", padx=(20, 0))

        tkinter.Label(
            right, text="Алфавит", font=("Arial", 10, "underline")
        ).pack(pady=(5, 10))

        grid = tkinter.Frame(right)
        grid.pack(padx=10)

        for i, letter in enumerate(ALPHABET):
            row = i // 6
            col = i % 6
            lbl = tkinter.Label(
                grid, text=letter.upper(), font=("Courier", 11), width=2
            )
            lbl.grid(row=row, column=col, padx=3, pady=2)
            self.alphabet_labels[letter] = lbl

        for j in range(3):
            tkinter.Label(grid, text="", width=2).grid(
                row=5, column=3 + j, padx=3, pady=2
            )

    def on_key_press(self, event):
        """
        Обрабатывает нажатие клавиши на клавиатуре.

        :param event: Событие нажатия клавиши.
        :type event: tkinter.Event
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
        Зачёркивает указанную букву в алфавите на экране.

        :param letter: Буква для зачёркивания.
        :type letter: str
        """
        lbl = self.alphabet_labels.get(letter)
        if lbl:
            lbl.config(font=("Courier", 11, "overstrike"))

    def update_display(self):
        """Обновляет отображение слова и количества оставшихся попыток."""
        displayed = " ".join(
            letter.upper() if letter in self.guessed_letters else "_"
            for letter in self.word
        )
        self.word_label.config(text=displayed)
        self.attempts_label.config(text=f"Попыток: {self.attempts_left}")
        self.check_game_end()

    def check_game_end(self):
        """Проверяет, завершена ли игра (победа или поражение)."""
        if all(letter in self.guessed_letters for letter in self.word):
            self.result_label.config(text="ПОБЕДА!")
            self.game_over = True
        elif self.attempts_left <= 0:
            self.result_label.config(
                text=f"ПОРАЖЕНИЕ! Слово: {self.word.upper()}"
            )
            self.game_over = True
        else:
            self.result_label.config(text="")

    def reset_game(self):
        """Сбрасывает игру к начальному состоянию."""
        try:
            self.word = get_random_word()
        except ValueError:
            tkinter.messagebox.showerror(
                "Критическая ошибка",
                "Список слов не содержит подходящих вариантов (длина 4–8 букв)"
            )
            self.root.destroy()

        self.guessed_letters.clear()
        self.used_letters.clear()
        self.attempts_left = 5
        self.game_over = False

        for lbl in self.alphabet_labels.values():
            lbl.config(font=("Courier", 11))

        self.update_display()
        self.result_label.config(text="")


if __name__ == "__main__":
    root = tkinter.Tk()
    Game(root)
    root.mainloop()
