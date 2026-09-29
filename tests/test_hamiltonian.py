from itertools import permutations, product

from open_system_one.verification.hamiltonian import verify_and_diagnose, verify_sigma


def find_small_valid_sigma(m: int = 2, k: int = 2):
    vertices = list(product(range(m), repeat=k))
    perms = list(permutations(range(k)))
    from itertools import product as cartesian_product

    for choices in cartesian_product(perms, repeat=len(vertices)):
        sigma = dict(zip(vertices, choices))
        if verify_sigma(sigma, m, k):
            return sigma
    raise AssertionError("no small valid sigma found")


def test_small_valid_instance():
    sigma = find_small_valid_sigma()
    result = verify_and_diagnose(sigma, 2, 2)
    assert result.valid
    assert result.n_vertices == 4
    assert all(c.is_hamiltonian for c in result.colours)
    assert all(c.n_vertices_reached == 4 for c in result.colours)


def test_incomplete_domain_is_rejected_without_exception():
    sigma = {(0, 0): (0, 1), (0, 1): (1, 0)}
    result = verify_and_diagnose(sigma, 2, 2)
    assert not result.valid
    assert not result.domain_valid
    assert any("exactly 4 vertices" in e for e in result.errors)


def test_non_permutation_value_is_rejected_without_exception():
    sigma = {
        (0, 0): (0, 0),
        (0, 1): (1, 0),
        (1, 0): (0, 1),
        (1, 1): (1, 0),
    }
    result = verify_and_diagnose(sigma, 2, 2)
    assert not result.valid
    assert not result.permutation_valid


def test_out_of_domain_vertex_is_rejected():
    sigma = {
        (9, 0): (0, 1),
        (0, 1): (1, 0),
        (1, 0): (1, 0),
        (1, 1): (0, 1),
    }
    result = verify_and_diagnose(sigma, 2, 2)
    assert not result.valid
    assert not result.domain_valid


def test_multi_component_case_is_rejected():
    sigma = find_small_valid_sigma()
    sigma = dict(sigma)
    sigma[(0, 0)] = sigma[(0, 1)]
    result = verify_and_diagnose(sigma, 2, 2)
    assert not result.valid
    assert any(c.n_components != 1 for c in result.colours) or result.errors


def test_parameter_validation():
    result = verify_and_diagnose({}, 0, 2)
    assert not result.valid
    assert result.n_vertices == 0


def independent_spec_checker(sigma, m=2, k=2):
    """Tiny independent reference implementation used only by the kill-test."""
    vertices = set(product(range(m), repeat=k))
    if set(sigma) != vertices:
        return False
    for p in sigma.values():
        if tuple(sorted(p)) != tuple(range(k)):
            return False
    n = m ** k
    for colour in range(k):
        f = {}
        for v in vertices:
            u = list(v)
            u[sigma[v][colour]] = (u[sigma[v][colour]] + 1) % m
            f[v] = tuple(u)
        seen = set()
        cur = min(vertices)
        while cur not in seen:
            seen.add(cur)
            cur = f[cur]
        if cur != min(vertices) or len(seen) != n:
            return False
    return True


def test_exhaustive_m2_k2_matches_independent_spec():
    vertices = list(product(range(2), repeat=2))
    perms = list(permutations(range(2)))
    checked = 0
    for choices in product(perms, repeat=len(vertices)):
        sigma = dict(zip(vertices, choices))
        assert verify_sigma(sigma, 2, 2) == independent_spec_checker(sigma, 2, 2)
        checked += 1
    assert checked == 16


def test_legacy_semantics_regression_boundary():
    """The extracted verifier preserves the positive assertion used by Symlib."""
    sigma = find_small_valid_sigma()
    assert verify_sigma(sigma, 2, 2)
