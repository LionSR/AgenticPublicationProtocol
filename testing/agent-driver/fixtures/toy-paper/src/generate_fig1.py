"""Reproduce Figure 1: direct sum vs. closed form for the first N integers.

Usage:
    python src/generate_fig1.py            # writes paper/figures/fig1.png
"""
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def direct_sum(n: int) -> int:
    return sum(range(1, n + 1))


def closed_form(n: int) -> int:
    return n * (n + 1) // 2


def main() -> None:
    ns = list(range(1, 101))
    direct = [direct_sum(n) for n in ns]
    closed = [closed_form(n) for n in ns]
    max_diff = max(abs(a - b) for a, b in zip(direct, closed))
    print(f"max abs difference between direct and closed form: {max_diff}")

    fig, ax = plt.subplots(figsize=(5, 3.2))
    ax.plot(ns, closed, "-", label="closed form N(N+1)/2")
    ax.plot(ns[::5], direct[::5], "o", ms=4, label="direct sum")
    ax.set_xlabel("N")
    ax.set_ylabel("sum of first N integers")
    ax.legend()
    fig.tight_layout()

    out = os.path.join(os.path.dirname(__file__), "..", "paper", "figures", "fig1.png")
    out = os.path.abspath(out)
    fig.savefig(out, dpi=120)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
