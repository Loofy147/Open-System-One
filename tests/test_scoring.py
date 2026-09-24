from open_system_one.scoring import cosine, pairwise_scores, set_aware_scores


def test_cosine_identity():
    assert abs(cosine([1.0, 0.0], [1.0, 0.0]) - 1.0) < 1e-9


def test_pairwise_preserves_candidate_identity():
    scores = pairwise_scores([1.0, 0.0], [[1.0, 0.0], [0.0, 1.0]])
    reversed_scores = pairwise_scores([1.0, 0.0], [[0.0, 1.0], [1.0, 0.0]])
    assert scores == list(reversed(reversed_scores))


def test_set_aware_returns_one_score_per_candidate():
    scores = set_aware_scores([1.0, 0.0], [[1.0, 0.0], [0.0, 1.0]])
    assert len(scores) == 2
