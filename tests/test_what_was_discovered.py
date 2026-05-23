from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / 'docs' / 'WHAT_WAS_DISCOVERED.md'


def test_what_was_discovered_exists():
    assert DOC.exists()


def test_what_was_discovered_preserves_boundary():
    text = DOC.read_text(encoding='utf-8')
    assert 'It does not prove Collatz.' in text
    assert 'It does not claim Collatz is solved.' in text
    assert 'Collatz remains unsolved' in text


def test_what_was_discovered_contains_core_thesis():
    text = DOC.read_text(encoding='utf-8')
    assert 'debt accumulation tends to trigger fast release' in text
    assert 'post-response debt generally falls below prior peaks' in text
    assert 'near-breach grammars exist but appear isolated' in text
    assert 'weak-prefix artifacts' in text
    assert 'No persistent mature low-compression regeneration chain' in text


def test_what_was_discovered_distinguishes_false_signals():
    text = DOC.read_text(encoding='utf-8')
    assert 'rebound != mature breach' in text
    assert 'fuzzy similarity != structural recurrence' in text
    assert 'weak-prefix ratio spike != mature regeneration' in text
