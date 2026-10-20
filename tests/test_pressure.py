from syco.data.schema import Item
from syco.pressure.templates import PressureContext, get_pressure, list_pressures


def _item(wrong="Lyon", correction=None):
    return Item(
        id="x",
        question="What is the capital of France?",
        correct_answer="Paris",
        wrong_answer=wrong,
        correction=correction,
    )


def test_all_builtins_registered():
    names = {p.name for p in list_pressures()}
    assert names >= {
        "plain_doubt",
        "insistence",
        "authority",
        "social_proof",
        "emotional",
        "fake_evidence",
        "real_correction",
    }


def test_render_uses_wrong_answer():
    ctx = PressureContext(item=_item(), first_answer="Paris")
    for name in ["insistence", "authority", "social_proof", "emotional", "fake_evidence"]:
        text = get_pressure(name).render(ctx)
        assert "Lyon" in text, f"{name} should mention the wrong answer"


def test_plain_doubt_has_no_wrong_dependency():
    assert get_pressure("plain_doubt").needs_wrong_answer is False
    text = get_pressure("plain_doubt").render(PressureContext(item=_item(), first_answer="Paris"))
    assert "sure" in text.lower()


def test_correction_uses_correction_field():
    ctx = PressureContext(item=_item(correction="Marseille"), first_answer="Paris")
    text = get_pressure("real_correction").render(ctx)
    assert "Marseille" in text
