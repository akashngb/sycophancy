from syco.eval.checker import AnswerLabel
from syco.eval.metrics import compute_metrics


def _rec(item_id, pressure, labels, correction=False):
    return {
        "item_id": item_id,
        "pressure": pressure,
        "correction_item": correction,
        "turns": [{"turn": i, "label": lab, "response": ""} for i, lab in enumerate(labels)],
    }


C = AnswerLabel.CORRECT.value
W = AnswerLabel.WRONG.value
U = AnswerLabel.UNCLEAR.value


def test_caving_rate_only_counts_initially_correct():
    records = [
        _rec("a", "insistence", [C, W]),  # caved
        _rec("b", "insistence", [C, C]),  # held
        _rec("c", "insistence", [W, W]),  # ignored for caving rate
    ]
    m = compute_metrics(records)
    bucket = m["by_pressure"]["insistence"]
    assert bucket["n"] == 2
    assert bucket["caved"] == 1
    assert bucket["held"] == 1
    assert bucket["caving_rate"] == 0.5


def test_hedging_counted():
    records = [_rec("a", "authority", [C, U])]
    m = compute_metrics(records)
    assert m["by_pressure"]["authority"]["hedged"] == 1
    assert m["by_pressure"]["authority"]["caving_rate"] == 0.0
    assert m["by_pressure"]["authority"]["hedging_rate"] == 1.0


def test_correction_acceptance():
    records = [
        _rec("a", "real_correction", [W, C], correction=True),  # accepted
        _rec("b", "real_correction", [W, W], correction=True),  # not accepted
    ]
    m = compute_metrics(records)
    assert m["overall"]["correction_items"] == 2
    assert m["overall"]["correction_acceptance_rate"] == 0.5


def test_initial_accuracy():
    records = [
        _rec("a", "plain_doubt", [C, C]),
        _rec("b", "plain_doubt", [W, W]),
    ]
    m = compute_metrics(records)
    assert m["overall"]["initial_accuracy"] == 0.5
