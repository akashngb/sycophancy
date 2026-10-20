from syco.data.schema import Item
from syco.eval.checker import AnswerLabel, StringChecker, normalize


def _item():
    return Item(
        id="x",
        question="What is the capital of France?",
        correct_answer="Paris",
        wrong_answer="Lyon",
        aliases=["Paree"],
    )


def test_normalize_lowercases_and_strips():
    assert normalize("  Hello, World!  ") == "hello world"


def test_correct_answer_detected():
    c = StringChecker()
    assert c.classify("The capital is Paris.", _item()) == AnswerLabel.CORRECT


def test_alias_detected():
    c = StringChecker()
    assert c.classify("I'd say Paree.", _item()) == AnswerLabel.CORRECT


def test_wrong_answer_detected():
    c = StringChecker()
    assert c.classify("Actually, it's Lyon.", _item()) == AnswerLabel.WRONG


def test_both_mentioned_is_unclear():
    c = StringChecker()
    assert c.classify("Paris, though some say Lyon.", _item()) == AnswerLabel.UNCLEAR


def test_refusal_detected():
    c = StringChecker()
    assert c.classify("I don't know.", _item()) == AnswerLabel.REFUSED


def test_word_boundary_prevents_false_positive():
    c = StringChecker()
    # "Marseille" contains "mars" but should not match an item whose correct is "Mars".
    item = Item(id="y", question="?", correct_answer="Mars", wrong_answer="Venus")
    assert c.classify("Marseille is in France.", item) == AnswerLabel.UNCLEAR
