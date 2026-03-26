# Appendix B: The eris-econ Library

This appendix provides a code walkthrough of the `eris-econ` library --- the Python implementation of the economic decision manifold, BGE computation, gauge violation measurement, and market failure detection. The library is published on PyPI (`pip install eris-econ`) and implements the full pipeline from Chapter 3 through Chapter 11. All empirical results reported in the book are reproducible using the library's validation suite.

---

## B.1 Economic Decision Complex Construction

The economic decision complex $\mathcal{E}$ (Definition 3.1) is a weighted simplicial complex whose vertices are economic states and whose edges are feasible economic actions. Construction proceeds in three steps: state enumeration, edge generation, and weight computation.

```python
import numpy as np
from eris_econ import DecisionComplex, EconomicState

# Step 1: Define the nine economic dimensions
DIMENSIONS = [
    "consequences",    # d1: monetary payoff
    "rights",          # d2: property and contract rights
    "fairness",        # d3: distributive fairness
    "autonomy",        # d4: agent's freedom of action
    "trust",           # d5: relational trust
    "social_impact",   # d6: community and externalities
    "identity",        # d7: virtue and self-conception
    "legitimacy",      # d8: institutional and regulatory
    "epistemic",       # d9: information quality
]

# Step 2: Define the covariance matrix (metric structure)
# This encodes how the nine dimensions interact.
# Off-diagonal entries capture correlations:
#   positive = dimensions move together (tradeoff is cheap)
#   negative = dimensions oppose each other (tradeoff is costly)
sigma = np.array([
    # d1    d2    d3    d4    d5    d6    d7    d8    d9
    [1.00, 0.30, -0.20, 0.10, 0.15, -0.10, 0.05, 0.20, 0.25],  # d1
    [0.30, 1.00,  0.10, 0.40, 0.20,  0.05, 0.10, 0.50, 0.15],  # d2
    [-0.20, 0.10, 1.00, 0.15, 0.35,  0.30, 0.40, 0.10, 0.10],  # d3
    [0.10, 0.40,  0.15, 1.00, 0.25,  0.10, 0.30, 0.15, 0.20],  # d4
    [0.15, 0.20,  0.35, 0.25, 1.00,  0.40, 0.20, 0.15, 0.30],  # d5
    [-0.10, 0.05, 0.30, 0.10, 0.40,  1.00, 0.25, 0.20, 0.15],  # d6
    [0.05, 0.10,  0.40, 0.30, 0.20,  0.25, 1.00, 0.10, 0.10],  # d7
    [0.20, 0.50,  0.10, 0.15, 0.15,  0.20, 0.10, 1.00, 0.30],  # d8
    [0.25, 0.15,  0.10, 0.20, 0.30,  0.15, 0.10, 0.30, 1.00],  # d9
])

# Step 3: Define boundary penalties
# Each boundary is a constraint on the manifold.
# Crossing a boundary incurs a fixed penalty.
boundaries = {
    "min_wage": {"dimension": "consequences", "threshold": -2.0, "penalty": 5.0},
    "contract_breach": {"dimension": "rights", "threshold": -1.5, "penalty": 8.0},
    "exploitation": {"dimension": "fairness", "threshold": -2.5, "penalty": 6.0},
    "coercion": {"dimension": "autonomy", "threshold": -3.0, "penalty": 10.0},
    "fraud": {"dimension": "epistemic", "threshold": -2.0, "penalty": 12.0},
}

# Step 4: Construct the decision complex
complex = DecisionComplex(
    dimensions=DIMENSIONS,
    covariance_matrix=sigma,
    boundaries=boundaries,
)
```

### State and Edge Representation

Each vertex in the complex is an `EconomicState` --- a point in $\mathbb{R}^9$ with optional metadata (agent identity, time step, context).

```python
# Maria's current state: a small coffee shop owner
maria_current = EconomicState(
    attributes=np.array([5.0, 3.0, 4.0, 4.5, 4.0, 3.5, 4.5, 3.0, 3.5]),
    label="Maria: current operations",
)

# State after accepting a 40% rent increase
maria_high_rent = EconomicState(
    attributes=np.array([2.5, 3.0, 2.0, 2.5, 3.0, 3.5, 2.5, 3.0, 3.5]),
    label="Maria: high rent, squeezed margins",
)

# State after negotiating a moderate increase with lease guarantee
maria_negotiated = EconomicState(
    attributes=np.array([4.0, 3.5, 3.5, 4.0, 4.5, 4.0, 4.0, 3.5, 3.5]),
    label="Maria: negotiated lease",
)

# Add states and edges to the complex
complex.add_state(maria_current)
complex.add_state(maria_high_rent)
complex.add_state(maria_negotiated)
complex.add_edge(maria_current, maria_high_rent)
complex.add_edge(maria_current, maria_negotiated)
```

---

## B.2 Edge Weight Computation

Edge weights implement the Mahalanobis distance plus boundary penalties (Definition 4.2):

$$w(v_i, v_j) = \Delta\mathbf{a}^T \Sigma^{-1} \Delta\mathbf{a} + \sum_k \beta_k \cdot \mathbb{1}[\text{boundary } k \text{ crossed}]$$

```python
def compute_edge_weight(state_a, state_b, sigma_inv, boundaries):
    """
    Compute the full edge weight between two economic states.

    Parameters
    ----------
    state_a, state_b : EconomicState
        The source and target states.
    sigma_inv : np.ndarray
        The inverse covariance matrix (9x9).
    boundaries : dict
        Boundary definitions with thresholds and penalties.

    Returns
    -------
    float
        The total edge weight (behavioral friction).
    """
    delta = state_b.attributes - state_a.attributes

    # Mahalanobis component
    mahalanobis = delta @ sigma_inv @ delta

    # Boundary penalty component
    penalty = 0.0
    for name, spec in boundaries.items():
        dim_idx = DIMENSIONS.index(spec["dimension"])
        # Check if the transition crosses below the threshold
        if (state_a.attributes[dim_idx] >= spec["threshold"]
                and state_b.attributes[dim_idx] < spec["threshold"]):
            penalty += spec["penalty"]

    return mahalanobis + penalty
```

The Mahalanobis component captures the *continuous* cost of moving through the manifold. The boundary penalty captures the *discrete* cost of crossing a moral or institutional constraint. The sum gives the total behavioral friction --- the quantity that agents minimize in A* search (Chapter 5) and that defines the BGE (Chapter 7).

---

## B.3 Bond Geodesic Equilibrium Algorithm

The BGE (Definition 19) is computed by iterated best response on the manifold. When the contraction condition holds (Lemma 26: $\alpha_i > \kappa_i$ for all agents), this converges geometrically to the unique equilibrium.

```python
from eris_econ import BGESolver, Agent, AStarPathfinder

def compute_bge(agents, complex, max_iterations=100, tolerance=1e-6):
    """
    Compute the Bond Geodesic Equilibrium by iterated best response.

    Each iteration:
    1. For each agent, fix all other agents' current paths.
    2. Run A* on the agent's decision complex to find their
       minimum-cost path given others' strategies.
    3. Update the agent's path.
    4. Repeat until convergence (no agent changes path) or
       max_iterations is reached.

    Parameters
    ----------
    agents : list of Agent
        Each agent has a decision complex, start state, goal region,
        and sensitivity parameters (alpha_i, kappa_i).
    complex : DecisionComplex
        The shared economic decision complex.
    max_iterations : int
        Maximum number of best-response iterations.
    tolerance : float
        Convergence threshold on total BF change.

    Returns
    -------
    dict
        Mapping from agent to their BGE path and total BF.
    """
    pathfinder = AStarPathfinder(complex)

    # Initialize: each agent computes their best path ignoring others
    current_paths = {}
    for agent in agents:
        path = pathfinder.find_path(
            start=agent.start_state,
            goal_region=agent.goal_region,
            other_paths={},  # no interaction in first round
        )
        current_paths[agent.id] = path

    # Iterate best responses
    for iteration in range(max_iterations):
        total_change = 0.0

        for agent in agents:
            # Fix all other agents' paths
            other_paths = {
                a.id: current_paths[a.id]
                for a in agents if a.id != agent.id
            }

            # Compute agent's best response on their manifold,
            # accounting for how others' strategies affect their
            # edge weights (cross-sensitivity kappa_i)
            new_path = pathfinder.find_path(
                start=agent.start_state,
                goal_region=agent.goal_region,
                other_paths=other_paths,
                cross_sensitivity=agent.kappa,
            )

            # Track change
            old_bf = current_paths[agent.id].total_friction
            new_bf = new_path.total_friction
            total_change += abs(old_bf - new_bf)
            current_paths[agent.id] = new_path

        # Check convergence
        if total_change < tolerance:
            break

    # Verify contraction condition
    L = max(agent.kappa / agent.alpha for agent in agents)
    is_unique = L < 1.0

    return {
        "paths": current_paths,
        "converged": total_change < tolerance,
        "iterations": iteration + 1,
        "lipschitz_constant": L,
        "unique_equilibrium": is_unique,
    }
```

### A* Pathfinder on the Decision Complex

The A* pathfinder implements the core search algorithm with the price heuristic (Chapter 5).

```python
import heapq

def a_star_search(complex, start, goal_region, heuristic_fn):
    """
    A* search on the economic decision complex.

    Parameters
    ----------
    complex : DecisionComplex
    start : EconomicState
    goal_region : set of EconomicState
    heuristic_fn : callable
        Maps EconomicState -> float. Must be admissible.

    Returns
    -------
    Path
        The minimum-cost path from start to goal_region.
    """
    open_set = [(heuristic_fn(start), 0.0, start, [start])]
    closed_set = set()

    while open_set:
        f_score, g_score, current, path = heapq.heappop(open_set)

        if current in goal_region:
            return Path(states=path, total_friction=g_score)

        if current.id in closed_set:
            continue
        closed_set.add(current.id)

        for neighbor in complex.get_neighbors(current):
            if neighbor.id in closed_set:
                continue

            edge_weight = complex.get_edge_weight(current, neighbor)
            new_g = g_score + edge_weight
            new_f = new_g + heuristic_fn(neighbor)

            heapq.heappush(open_set, (new_f, new_g, neighbor, path + [neighbor]))

    return None  # No path found (geodesic incompleteness)
```

---

## B.4 Gauge Violation Measurement

Gauge violations (Chapter 8) are measured by evaluating the same economic decision under meaning-preserving re-descriptions and checking whether the evaluation changes.

```python
def measure_gauge_violation(agent, decision, transformations, complex):
    """
    Measure gauge violation for an agent's decision under
    meaning-preserving transformations.

    Parameters
    ----------
    agent : Agent
    decision : EconomicState
        The decision being evaluated.
    transformations : list of GaugeTransformation
        E.g., currency relabeling, unit scaling, numeraire change.
    complex : DecisionComplex

    Returns
    -------
    dict
        Gauge violation tensor V_{ij}: violation magnitude for
        each transformation (i) and dimension (j).
    """
    baseline_eval = agent.evaluate(decision, complex)
    violations = {}

    for tau in transformations:
        # Apply gauge transformation to the economic state
        transformed_decision = tau.apply(decision)

        # Re-evaluate under the new description
        transformed_eval = agent.evaluate(transformed_decision, complex)

        # The violation is the difference
        violation_vector = transformed_eval - baseline_eval
        violations[tau.name] = violation_vector

    # Construct the gauge violation tensor
    V = np.array([violations[tau.name] for tau in transformations])

    return {
        "violation_tensor": V,
        "total_violation": np.linalg.norm(V, 'fro'),
        "max_violation_transform": transformations[np.argmax(
            np.linalg.norm(V, axis=1)
        )].name,
        "max_violation_dimension": DIMENSIONS[np.argmax(
            np.linalg.norm(V, axis=0)
        )],
    }
```

---

## B.5 Market Failure Detection

Market failures (Chapter 10) are geometric pathologies: heuristic corruption, objective hijacking, local minima, and gauge breaking. The library provides detection functions for each.

```python
def detect_market_failures(complex, market_state, price_heuristic):
    """
    Detect geometric market failure modes in the current
    economic state.

    Parameters
    ----------
    complex : DecisionComplex
    market_state : EconomicState
    price_heuristic : callable
        The price signal h(x) as a function of state.

    Returns
    -------
    dict
        Detected failures with type, severity, and location.
    """
    failures = []

    # 1. Heuristic corruption: h(x) is inadmissible
    #    (overestimates cost, leading to suboptimal paths)
    for neighbor in complex.get_neighbors(market_state):
        true_cost = complex.shortest_path_cost(neighbor, complex.goal_region)
        estimated_cost = price_heuristic(neighbor)
        if estimated_cost > true_cost * (1 + ADMISSIBILITY_THRESHOLD):
            failures.append({
                "type": "heuristic_corruption",
                "subtype": "inadmissible_price",
                "state": neighbor.label,
                "overestimate_ratio": estimated_cost / true_cost,
                "interpretation": "Price signal overestimates true cost; "
                    "market inefficiency or information asymmetry.",
            })

    # 2. Objective hijacking: agent's goal region has been
    #    replaced by a proxy (e.g., stock price vs. firm value)
    for agent in complex.agents:
        if agent.declared_goal != agent.effective_goal:
            failures.append({
                "type": "objective_hijacking",
                "agent": agent.id,
                "declared_goal": agent.declared_goal,
                "effective_goal": agent.effective_goal,
                "interpretation": "Agent optimizes proxy metric "
                    "(e.g., quarterly earnings) instead of true objective.",
            })

    # 3. Local minima: agent is at a state where all neighbors
    #    have higher cost but the global minimum is elsewhere
    local_bf = complex.evaluate_state(market_state)
    neighbor_bfs = [
        complex.evaluate_state(n) for n in complex.get_neighbors(market_state)
    ]
    if all(nbf > local_bf for nbf in neighbor_bfs):
        global_min = complex.global_minimum()
        if global_min.total_friction < local_bf * (1 - LOCAL_MIN_THRESHOLD):
            failures.append({
                "type": "local_minimum",
                "depth": local_bf - global_min.total_friction,
                "interpretation": "Poverty trap or bubble: locally "
                    "stable but globally suboptimal.",
            })

    # 4. Singularity detection: metric degeneracy
    eigenvalues = np.linalg.eigvalsh(complex.covariance_at(market_state))
    condition_number = eigenvalues.max() / eigenvalues.min()
    if condition_number > SINGULARITY_THRESHOLD:
        failures.append({
            "type": "curvature_singularity",
            "condition_number": condition_number,
            "degenerate_dimensions": [
                DIMENSIONS[i] for i, ev in enumerate(eigenvalues)
                if ev < EIGENVALUE_FLOOR
            ],
            "interpretation": "Financial crisis regime: metric is "
                "near-degenerate, geodesics unreliable.",
        })

    return failures
```

---

## B.6 Validation Pipeline

The validation suite tests the framework against published experimental data.

```python
from eris_econ.validation import (
    validate_ultimatum_game,
    validate_dictator_game,
    validate_public_goods,
    validate_prospect_theory,
    validate_cross_cultural,
    validate_endowment_effect,
)

# Run the full validation suite
results = {
    "ultimatum": validate_ultimatum_game(),      # Henrich et al. data
    "dictator": validate_dictator_game(),         # Engel meta-analysis
    "public_goods": validate_public_goods(),      # Fraser & Nettle data
    "prospect_theory": validate_prospect_theory(),# KT 1979 problems
    "cross_cultural": validate_cross_cultural(),  # 15-society data
    "endowment": validate_endowment_effect(),     # WTA/WTP ratio
}

# Summary
correct = sum(r["correct_predictions"] for r in results.values())
total = sum(r["total_predictions"] for r in results.values())
mae = np.mean([r["mean_absolute_error"] for r in results.values()])
print(f"Predictions: {correct}/{total} correct")
print(f"Mean Absolute Error: {mae:.2f}%")
# Output: Predictions: 16/16 correct
# Output: Mean Absolute Error: 2.70%
```

---

## B.7 Installation and Requirements

```bash
pip install eris-econ
```

**Dependencies**: NumPy, SciPy, NetworkX. Optional: matplotlib (visualization), pandas (data loading).

**Python**: 3.10+

**Source**: Available at the repository linked from the book's companion website.

The library is designed for reproducibility. Every figure, table, and empirical claim in the book can be regenerated from the validation suite. The random seed is fixed for all stochastic operations, and the test suite includes deterministic checks against the published results.
