from itertools import permutations, product

from open_system_one.verification.hamiltonian import (
    verify_and_diagnose,
    verify_sigma,
    verify_strict_hamiltonian,
)


M3_LEVELS = (
    {0: (1, 0, 2), 1: (1, 0, 2), 2: (1, 0, 2)},
    {0: (0, 1, 2), 1: (2, 1, 0), 2: (2, 1, 0)},
    {0: (0, 2, 1), 1: (1, 2, 0), 2: (1, 2, 0)},
)


def symlib_m3_fixture():
    return {
        (i, j, k): M3_LEVELS[(i + j + k) % 3][j]
        for i, j, k in product(range(3), repeat=3)
    }


def independent_legacy_checker(sigma, m, k):
    vertices = set(product(range(m), repeat=k))
    if set(sigma) != vertices:
        return False
    if any(tuple(sorted(p)) != tuple(range(k)) for p in sigma.values()):
        return False

    n = m ** k
    for colour in range(k):
        func = {}
        for v in vertices:
            u = list(v)
            axis = sigma[v][colour]
            u[axis] = (u[axis] + 1) % m
            func[v] = tuple(u)

        seen = set()
        cycles = 0
        for start in vertices:
            if start in seen:
                continue
            cycles += 1
            cur = start
            while cur not in seen:
                seen.add(cur)
                cur = func[cur]
        if len(func) != n or cycles != 1:
            return False
    return True


def test_m3_legacy_fixture_is_accepted():
    sigma = symlib_m3_fixture()
    result = verify_and_diagnose(sigma, 3, 3)
    assert result.valid
    assert result.n_vertices == 27
    assert all(c.is_single_cycle for c in result.colours)


def test_m3_fixture_is_not_strict_hamiltonian():
    sigma = symlib_m3_fixture()
    assert verify_sigma(sigma, 3, 3)
    assert not verify_strict_hamiltonian(sigma, 3, 3)
    assert any(not c.indegree_one for c in verify_and_diagnose(sigma, 3, 3).colours)


def test_exhaustive_m2_k2_matches_independent_legacy_spec():
    vertices = list(product(range(2), repeat=2))
    perms = list(permutations(range(2)))
    checked = 0
    for choices in product(perms, repeat=len(vertices)):
        sigma = dict(zip(vertices, choices))
        assert verify_sigma(sigma, 2, 2) == independent_legacy_checker(sigma, 2, 2)
        checked += 1
    assert checked == 16


def test_m3_single_entry_mutation_is_rejected():
    sigma = symlib_m3_fixture()
    original = sigma[(0, 0, 0)]
    sigma[(0, 0, 0)] = (0, 1, 2)
    assert original != sigma[(0, 0, 0)]
    assert not verify_sigma(sigma, 3, 3)


def test_incomplete_domain_is_rejected_without_exception():
    sigma = {(0, 0): (0, 1), (0, 1): (1, 0)}
    result = verify_and_diagnose(sigma, 2, 2)
    assert not result.valid
    assert not result.domain_valid


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
