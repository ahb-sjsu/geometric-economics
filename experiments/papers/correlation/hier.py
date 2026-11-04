"""Hierarchical GEO for the population kappa (DESIGN.md, secondary analysis; REHEARSAL.md, the kappa bias).

A per-person kappa fitted from a feasible number of choices is biased upward, and pooling profile
estimates does not fix it, because each person's other parameters are maximized over rather than
integrated out (the incidental-parameter problem). This module fits GEO hierarchically and samples it
by NUTS (NumPyro), so every person's parameters are integrated out:

  theta_i = mu + sigma * z_i,  z_i ~ N(0, I)          (non-centred), theta = (l1, l21, l2, lk, bias)
  kappa_i = 0.5 + exp(lk_i),   P_i = L_i L_i', L_i = [[e^l1, 0], [l21, e^l2]]
  P(left) = LAPSE/2 + (1 - LAPSE) * sigmoid(V_left - V_right + bias_i),  V = -sum_s p_s C_s^kappa_i

The reported quantity is the population median of kappa, 0.5 + exp(mu_lk): its posterior median and
95% interval. Hyperpriors are weak: mu ~ N((0, 0, -1, 0, 0), (3, 5, 3, 1, 1)), so the population median
kappa is centred at 1.5 a priori; sigma ~ HalfNormal((2, 3, 2, 1, 0.5)).
"""
from __future__ import annotations

import os

os.environ.setdefault("XLA_FLAGS", "--xla_cpu_multi_thread_eigen=false intra_op_parallelism_threads=1")

import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402
import numpyro  # noqa: E402
import numpyro.distributions as dist  # noqa: E402
from numpyro.infer import MCMC, NUTS, init_to_value  # noqa: E402

LAPSE = 0.04
MU0 = jnp.array([0.0, 0.0, -1.0, 0.0, 0.0])
MU_SD = jnp.array([3.0, 5.0, 3.0, 1.0, 1.0])
SIGMA_SD = jnp.array([2.0, 3.0, 2.0, 1.0, 0.5])


def model(p, a, b, y):
    n = y.shape[0]
    mu = numpyro.sample("mu", dist.Normal(MU0, MU_SD).to_event(1))
    sigma = numpyro.sample("sigma", dist.HalfNormal(SIGMA_SD).to_event(1))
    with numpyro.plate("people", n):
        z = numpyro.sample("z", dist.Normal(jnp.zeros(5), 1.0).to_event(1))
    th = mu + sigma * z
    l1, l21, l2, lk = (th[:, i][:, None, None, None] for i in range(4))
    bias = th[:, 4][:, None]
    kappa = 0.5 + jnp.exp(lk)
    e1 = jnp.exp(l1)
    P11, P12, P22 = e1 * e1, e1 * l21, l21 * l21 + jnp.exp(2 * l2)
    log_c = 0.5 * jnp.log(jnp.maximum(P11 * a * a + 2 * P12 * a * b + P22 * b * b, 1e-12))
    # C^kappa in log space, capped: at an extreme draw (kappa in the tens) C^kappa overflowed to inf and
    # inf - inf gave a NaN probability (the first version-3 NRP run, 2026-11-02). The cap binds only
    # where C^kappa > 1e26, far outside any fitted region.
    V = -(p * jnp.exp(jnp.minimum(kappa * log_c, 60.0))).sum(-1)
    logit = jnp.clip(V[..., 0] - V[..., 1] + bias, -60.0, 60.0)
    prob = LAPSE / 2 + (1 - LAPSE) * jax.nn.sigmoid(logit)
    numpyro.sample("y", dist.Bernoulli(probs=prob, validate_args=False), obs=y)


def fit(data, Y, seed=0, warmup=500, samples=500):
    """data = (p, a, b) of the calibration trials, shared by everyone; Y = choices, people x trials.
    The chain starts at the hyperprior centre (everyone at the population mean, sigma 0.3), not at a
    random draw."""
    p, a, b = (jnp.asarray(x, dtype=jnp.float32) for x in data)
    start = init_to_value(values={"mu": MU0, "sigma": jnp.full(5, 0.3), "z": jnp.zeros((Y.shape[0], 5))})
    mcmc = MCMC(NUTS(model, target_accept_prob=0.9, init_strategy=start), num_warmup=warmup,
                num_samples=samples, num_chains=1, progress_bar=False)
    mcmc.run(jax.random.PRNGKey(seed), p, a, b, jnp.asarray(Y, dtype=jnp.float32), extra_fields=("diverging",))
    s = mcmc.get_samples()
    mu_lk = np.asarray(s["mu"][:, 3])
    k_med = 0.5 + np.exp(mu_lk)
    # q80 was the version 5 rule's kappa (the smallest tabulated kappa at or above it), and the first version 6
    # pilot rehearsal's rule read the draws. At pilot size both sat 0.1 to 0.2 below a common kappa, so the rule
    # now reads kappa from the lottery-choice rate against simulated pilots (pilot_analysis.kappa_belt, PILOT.md).
    return {"kappa_median": float(np.median(k_med)), "lo": float(np.quantile(k_med, 0.025)),
            "hi": float(np.quantile(k_med, 0.975)), "q80": float(np.quantile(k_med, 0.8)),
            "draws": [round(float(x), 5) for x in k_med],
            "sigma_lk": float(np.median(np.asarray(s["sigma"][:, 3]))),
            "divergences": int(np.asarray(mcmc.get_extra_fields()["diverging"]).sum()),
            "ess_mu_lk": float(numpyro.diagnostics.effective_sample_size(mu_lk[None, :]))}
