"""Standalone verification of the finite functional-cycle predicate.

This module reimplements the executed predicate in Symlib's
symlib/kernel/verify.py. For each colour c, the source assigns the edge along
axis a to colour sigma[v][a], so a fixed colour selects the unique axis whose
permutation entry equals that colour.

No Symlib, NumPy, or Numba dependency is required here.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Tuple

Vertex = Tuple[int, ...]
Permutation = Tuple[int, ...]
Sigma = Mapping[Vertex, Permutation]


@dataclass(frozen=True)
class ColourResult:
    colour: int
    n_arcs: int
    n_vertices_reached: int
    n_components: int
    indegree_one: bool
    is_single_cycle: bool


@dataclass(frozen=True)
class VerificationResult:
    valid: bool
    m: int
    k: int
    n_vertices: int
    domain_valid: bool
    permutation_valid: bool
    colours: Tuple[ColourResult, ...]
    errors: Tuple[str, ...]


def _validate_parameters(m: int, k: int) -> Tuple[str, ...]:
    errors: list[str] = []
    if not isinstance(m, int) or isinstance(m, bool) or m < 1:
        errors.append("m must be a positive integer")
    if not isinstance(k, int) or isinstance(k, bool) or k < 1:
        errors.append("k must be a positive integer")
    return tuple(errors)


def _validate_sigma_shape(sigma: Sigma, m: int, k: int) -> Tuple[bool, bool, list[str]]:
    errors: list[str] = []
    domain_valid = True
    permutation_valid = True

    try:
        items = sigma.items()
    except AttributeError:
        return False, False, ["sigma must provide an items() mapping interface"]

    n = m ** k
    try:
        sigma_len = len(sigma)
    except TypeError:
        sigma_len = None

    if sigma_len != n:
        domain_valid = False
        errors.append(f"sigma must contain exactly {n} vertices; found {sigma_len}")

    for vertex, permutation in items:
        if not isinstance(vertex, tuple) or len(vertex) != k:
            domain_valid = False
            errors.append(f"invalid vertex key: {vertex!r}")
            continue
        if any(
            not isinstance(x, int) or isinstance(x, bool) or x < 0 or x >= m
            for x in vertex
        ):
            domain_valid = False
            errors.append(f"vertex outside Z_{m}^{k}: {vertex!r}")

        if not isinstance(permutation, tuple) or len(permutation) != k:
            permutation_valid = False
            errors.append(f"invalid permutation at {vertex!r}: {permutation!r}")
            continue
        if tuple(sorted(permutation)) != tuple(range(k)):
            permutation_valid = False
            errors.append(
                f"value at {vertex!r} is not a permutation of 0..{k-1}: {permutation!r}"
            )

    return domain_valid, permutation_valid, errors


def _analyse_colours(sigma: Sigma, m: int, k: int) -> tuple[ColourResult, ...]:
    n = m ** k
    vertices = tuple(sigma.keys())
    colours: list[ColourResult] = []

    for colour in range(k):
        func: dict[Vertex, Vertex] = {}
        indegree: dict[Vertex, int] = {v: 0 for v in vertices}

        for vertex, permutation in sigma.items():
            for axis in range(k):
                if permutation[axis] == colour:
                    neighbor = list(vertex)
                    neighbor[axis] = (neighbor[axis] + 1) % m
                    target = tuple(neighbor)
                    func[vertex] = target
                    indegree[target] += 1
                    break

        indegree_one = all(value == 1 for value in indegree.values())

        visited: set[Vertex] = set()
        components = 0
        for start in vertices:
            if start in visited:
                continue
            components += 1
            current = start
            while current not in visited:
                visited.add(current)
                current = func[current]

        colours.append(
            ColourResult(
                colour=colour,
                n_arcs=len(func),
                n_vertices_reached=len(visited),
                n_components=components,
                indegree_one=indegree_one,
                is_single_cycle=(len(func) == n and components == 1),
            )
        )

    return tuple(colours)


def verify_and_diagnose(sigma: Sigma, m: int, k: int = 3) -> VerificationResult:
    """Verify the exact single-cycle predicate executed by the legacy source."""
    parameter_errors = _validate_parameters(m, k)
    if parameter_errors:
        return VerificationResult(
            valid=False,
            m=m if isinstance(m, int) and not isinstance(m, bool) else 0,
            k=k if isinstance(k, int) and not isinstance(k, bool) else 0,
            n_vertices=0,
            domain_valid=False,
            permutation_valid=False,
            colours=(),
            errors=parameter_errors,
        )

    n = m ** k
    domain_valid, permutation_valid, errors = _validate_sigma_shape(sigma, m, k)
    if not domain_valid or not permutation_valid:
        return VerificationResult(
            valid=False,
            m=m,
            k=k,
            n_vertices=n,
            domain_valid=domain_valid,
            permutation_valid=permutation_valid,
            colours=(),
            errors=tuple(errors),
        )

    colours = _analyse_colours(sigma, m, k)
    for item in colours:
        if not item.is_single_cycle:
            errors.append(
                f"colour {item.colour}: induced function has {item.n_components} components"
            )

    return VerificationResult(
        valid=all(item.is_single_cycle for item in colours),
        m=m,
        k=k,
        n_vertices=n,
        domain_valid=True,
        permutation_valid=True,
        colours=colours,
        errors=tuple(errors),
    )


def verify_sigma(sigma: Sigma, m: int, k: int = 3) -> bool:
    """Return True exactly when the legacy predicate accepts sigma."""
    return verify_and_diagnose(sigma, m, k).valid


def verify_strict_hamiltonian(sigma: Sigma, m: int, k: int = 3) -> bool:
    """Require the legacy predicate plus indegree one for every colour."""
    result = verify_and_diagnose(sigma, m, k)
    return result.valid and all(
        colour.indegree_one and colour.n_vertices_reached == m ** k
        for colour in result.colours
    )
