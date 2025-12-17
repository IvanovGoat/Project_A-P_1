import Project_1


def test_get_random_word_length():
    word = Project_1.get_random_word()
    assert 4 <= len(word) <= 8


def test_get_random_word_is_lowercase():
    word = Project_1.get_random_word()
    assert word == word.lower()


def test_get_random_word_in_word_list():
    word = Project_1.get_random_word()
    original_words_lower = [w.lower() for w in Project_1.WORDS]
    assert word in original_words_lower


def test_get_random_word_empty_valid_list_raises_value_error():
    original = Project_1.WORDS.copy()
    Project_1.WORDS = ["а", "бы", "в"]
    try:
        Project_1.get_random_word()
        assert False, "Expected ValueError"
    except ValueError:
        pass
    finally:
        Project_1.WORDS[:] = original


def test_alphabet_has_33_letters():
    assert len(Project_1.ALPHABET) == 33


def test_alphabet_letters_are_unique():
    assert len(Project_1.ALPHABET) == len(set(Project_1.ALPHABET))
