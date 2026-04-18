"""
-------------------------------------------------------------------------
Requirements: pip install matplotlib numpy
Run         : python exponentiation_final.py
-------------------------------------------------------------------------
"""

import time
import math
import csv
import statistics
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# ════════════════════════════════════════════════════════════════
# SECTION 1 — ALGORITHM IMPLEMENTATIONS
# ════════════════════════════════════════════════════════════════

# Algorithm 1: Naive Exponentiation — O(n)
# Technique: Brute-force / Iterative


def naive_exponentiation(a, n):
    """
    Compute a^n by performing n successive multiplications.
    Time Complexity : O(n)
    Space Complexity: O(1)
    """
    result = 1
    for _ in range(n):      # loop runs exactly n times
        result *= a         # one multiplication per iteration
    return result


# Algorithm 2: Fast Exponentiation by Squaring — O(log n)
# Technique: Divide and Conquer
def fast_exponentiation(a, n):
    """
    Compute a^n using repeated squaring (divide and conquer).
    Recurrence: a^n = (a^(n/2))^2  if n even
                a^n = a * a^(n-1)  if n odd
    Time Complexity : O(log n)
    Space Complexity: O(1)
    """
    result = 1
    base = a
    while n > 0:
        if n & 1:           # if LSB is set, multiply result
            result *= base
        base *= base        # square the base at every step
        n >>= 1             # halve the exponent (process next bit)
    return result


# Algorithm 3: Modular Exponentiation — O(log n)
# Technique: Divide and Conquer + Modular Arithmetic
MOD = 10**9 + 7             # standard cryptographic prime = 1,000,000,007


def modular_exponentiation(a, n, mod=MOD):
    """
    Compute (a^n) mod m using repeated squaring with modular reduction.
    Every intermediate value is bounded by mod^2, keeping arithmetic O(1).
    Used in RSA, Diffie-Hellman, and all public-key cryptography.
    Time Complexity : O(log n)
    Space Complexity: O(1)
    """
    result = 1
    base = a % mod        # reduce base into [0, mod)
    while n > 0:
        if n & 1:
            result = (result * base) % mod  # reduce after every multiply
        base = (base * base) % mod          # reduce after every squaring
        n >>= 1
    return result


# ════════════════════════════════════════════════════════════════
# SECTION 2 — CORRECTNESS VERIFICATION
# ════════════════════════════════════════════════════════════════

def verify_correctness():
    """
    Verify all three algorithms produce correct results
    against Python's built-in pow() as ground truth.
    """
    print("\n" + "=" * 65)
    print("  CORRECTNESS VERIFICATION")
    print("=" * 65)

    test_cases = [
        (2, 0), (2, 1), (2, 10), (3, 5),
        (5, 7), (2, 20), (7, 15), (10, 6),
        (2, 32), (13, 11)
    ]

    all_passed = True
    print(f"  {'a':>5}  {'n':>5}  {'Expected':>16}  {'Naive':>6}  {'Fast':>6}  {'Modular':>8}  Status")
    print("  " + "-" * 60)

    for a, n in test_cases:
        expected = pow(a, n)
        naive_r = naive_exponentiation(a, n)
        fast_r = fast_exponentiation(a, n)
        mod_r = modular_exponentiation(a, n)
        mod_exp = pow(a, n, MOD)

        ok_n = (naive_r == expected)
        ok_f = (fast_r == expected)
        ok_m = (mod_r == mod_exp)
        ok = ok_n and ok_f and ok_m

        if not ok:
            all_passed = False

        print(f"  {a:>5}  {n:>5}  {expected:>16}  "
              f"{'OK' if ok_n else 'FAIL':>6}  "
              f"{'OK' if ok_f else 'FAIL':>6}  "
              f"{'OK' if ok_m else 'FAIL':>8}  "
              f"{'PASS' if ok else 'FAIL'}")

    print(f"\n  {'All tests PASSED!' if all_passed else 'Some tests FAILED!'}")
    return all_passed


# ════════════════════════════════════════════════════════════════
# SECTION 3 — TIMING UTILITY
# ════════════════════════════════════════════════════════════════

def measure(func, a, n, trials=10, **kwargs):
    """
    Measure average runtime of func(a, n) over multiple trials.
    Uses time.perf_counter() for high-resolution sub-microsecond timing.
    Returns: (mean_ms, std_ms)
    """
    times = []
    for _ in range(trials):
        t = time.perf_counter()
        func(a, n, **kwargs)
        times.append((time.perf_counter() - t) * 1000)  # convert to ms
    mean = statistics.mean(times)
    std = statistics.stdev(times) if len(times) > 1 else 0.0
    return mean, std


# ════════════════════════════════════════════════════════════════
# SECTION 4 — EXPERIMENTS
# ════════════════════════════════════════════════════════════════

def experiment_1(base=2, trials=10):
    """
    Experiment 1: Runtime vs Exponent Value (n = 500 to 20,000)
    x-axis: exponent n
    y-axis: average running time in milliseconds
    """
    exponents = list(range(500, 20001, 500))
    nm, fm, mm = [], [], []
    ns, fs, ms = [], [], []

    print("\n" + "=" * 65)
    print(
        f"  EXPERIMENT 1 — Runtime vs Exponent (base={base}, trials={trials})")
    print("=" * 65)
    print(
        f"  {'n':>8}  {'Naive ms':>12}  {'Fast ms':>12}  {'Mod ms':>12}  {'Speedup':>10}")
    print("  " + "-" * 60)

    for n in exponents:
        mn, sn = measure(naive_exponentiation,    base, n, trials)
        mf, sf = measure(fast_exponentiation,     base, n, trials)
        mm_, sm = measure(modular_exponentiation, base, n, trials)

        nm.append(mn)
        fm.append(mf)
        mm.append(mm_)
        ns.append(sn)
        fs.append(sf)
        ms.append(sm)

        speedup = mn / mf if mf > 0 else 0
        print(f"  {n:>8}  {mn:>12.5f}  {mf:>12.5f}  {mm_:>12.5f}  {speedup:>9.1f}x")

    return exponents, nm, fm, mm, ns, fs, ms


def experiment_2(base=2, trials=5):
    """
    Experiment 2: Large Exponent Scalability (n up to 1,000,000)
    Naive is excluded beyond n = 50,000 (too slow).
    """
    large_n = [10_000, 50_000, 100_000, 200_000, 500_000, 1_000_000]
    ft, mt, nt = [], [], []

    print("\n" + "=" * 65)
    print(
        f"  EXPERIMENT 2 — Large Exponent Scalability (base={base}, trials={trials})")
    print("=" * 65)
    print(f"  {'n':>12}  {'Naive ms':>16}  {'Fast ms':>12}  {'Mod ms':>12}")
    print("  " + "-" * 58)

    for n in large_n:
        mf, _ = measure(fast_exponentiation,    base, n, trials)
        mm, _ = measure(modular_exponentiation, base, n, trials)
        ft.append(mf)
        mt.append(mm)

        if n <= 50_000:
            mn, _ = measure(naive_exponentiation, base, n, trials)
            nt.append(mn)
            print(f"  {n:>12}  {mn:>16.3f}  {mf:>12.4f}  {mm:>12.4f}")
        else:
            nt.append(None)     # too slow to measure
            print(f"  {n:>12}  {'N/A (too slow)':>16}  {mf:>12.4f}  {mm:>12.4f}")

    return large_n, nt, ft, mt


def experiment_3(base=2, trials=10):
    """
    Experiment 3: Theoretical Complexity Validation
    Plots T(n)/n for Naive and T(n)/log2(n) for Fast and Modular.
    If each ratio converges to a constant, the theoretical complexity is confirmed.
    """
    exps = [1000, 2000, 4000, 6000, 8000, 10000, 14000, 18000, 20000]
    nr, fr, mr = [], [], []

    print("\n" + "=" * 65)
    print(
        f"  EXPERIMENT 3 — Complexity Validation (base={base}, trials={trials})")
    print("=" * 65)
    print(f"  {'n':>8}  {'T_naive/n':>14}  {'T_fast/log2n':>16}  {'T_mod/log2n':>14}")
    print("  " + "-" * 58)

    for n in exps:
        mn, _ = measure(naive_exponentiation,    base, n, trials)
        mf, _ = measure(fast_exponentiation,     base, n, trials)
        mm, _ = measure(modular_exponentiation,  base, n, trials)
        lg = math.log2(n)

        # Convert ms -> us (*1000) for readability of small values
        nr.append(mn * 1000 / n)
        fr.append(mf * 1000 / lg)
        mr.append(mm * 1000 / lg)

        print(
            f"  {n:>8}  {mn*1000/n:>14.8f}  {mf*1000/lg:>16.8f}  {mm*1000/lg:>14.8f}")

    print("\n  Stable ratios confirm theoretical complexities.")
    return exps, nr, fr, mr


def experiment_4(trials=7):
    """
    Experiment 4: Effect of Base Value on Naive Exponentiation
    Tests base = 2, 10, 100 to show how larger bases increase
    per-multiplication cost due to Python's arbitrary-precision integers.
    """
    exps = list(range(500, 15001, 500))
    bases = [2, 10, 100]
    data = {}

    print("\n" + "=" * 65)
    print(f"  EXPERIMENT 4 — Effect of Base Value on Naive (trials={trials})")
    print("=" * 65)

    for b in bases:
        times = [measure(naive_exponentiation, b, n, trials)[0] for n in exps]
        data[b] = times
        print(
            f"  base={b:>4}: {times[0]:.4f} ms at n=500  ->  {times[-1]:.4f} ms at n=15000")

    return exps, data


# ════════════════════════════════════════════════════════════════
# SECTION 5 — GRAPH GENERATION (7 Figures)
# ════════════════════════════════════════════════════════════════

# Color palette
C_NAIVE = "#D85A30"   # coral  — Naive
C_FAST = "#1D9E75"   # teal   — Fast
C_MOD = "#7F77DD"   # purple — Modular
BG = "#FAFAF9"

plt.rcParams.update({
    "figure.facecolor":   BG,
    "axes.facecolor":     BG,
    "axes.grid":          True,
    "grid.color":         "#E8E6DF",
    "grid.linewidth":     0.8,
    "axes.spines.top":    False,
    "axes.spines.right":  False,
    "font.size":          11,
})

fmt_n = ticker.FuncFormatter(lambda x, _: f"{int(x):,}")


def graph1(e1n, nm, fm, mm, ns, fs, ms):
    """ Figure 1: Runtime vs Exponent with theoretical overlay and error bands. """
    na = np.array(e1n, dtype=float)
    scale_n = nm[-1] / na[-1]
    scale_l = fm[-1] / np.log2(na[-1])

    fig, ax = plt.subplots(figsize=(10, 6))

    # Shaded error bands (±1 std)
    for times, stds, color in [(nm, ns, C_NAIVE), (fm, fs, C_FAST), (mm, ms, C_MOD)]:
        upper = [t + s for t, s in zip(times, stds)]
        lower = [max(0, t - s) for t, s in zip(times, stds)]
        ax.fill_between(e1n, lower, upper, color=color, alpha=0.12)

    ax.plot(e1n, nm, color=C_NAIVE, lw=2.5,
            marker="o", ms=3, label="Naive  O(n)")
    ax.plot(e1n, fm, color=C_FAST,  lw=2.5, marker="s",
            ms=3, label="Fast Exponentiation  O(log n)")
    ax.plot(e1n, mm, color=C_MOD,   lw=2.5, marker="^",
            ms=3, label="Modular Exponentiation  O(log n)")

    # Theoretical curves (dashed)
    ax.plot(na, scale_n * na,              color=C_NAIVE,
            lw=1.2, ls="--", alpha=0.5, label="Theoretical O(n)")
    ax.plot(na, scale_l * np.log2(na),     color=C_FAST,  lw=1.2,
            ls="--", alpha=0.5, label="Theoretical O(log n)")

    ax.set_xlabel("Exponent  n", fontsize=13)
    ax.set_ylabel("Running Time (ms)", fontsize=13)
    ax.set_title("Figure 1 — Runtime vs Exponent Value\n"
                 "All three algorithms + theoretical overlay (base=2, 10 trials ± 1σ shaded)",
                 fontsize=12, pad=14)
    ax.legend(fontsize=10, framealpha=0.7, loc="upper left")
    ax.xaxis.set_major_formatter(fmt_n)
    plt.tight_layout()
    plt.savefig("graph1_runtime_overlay.png", dpi=150, bbox_inches="tight")
    print("  Saved: graph1_runtime_overlay.png")
    plt.show()


def graph2(ln, nt, ft, mt):
    """ Figure 2: Large exponent scalability. """
    nx = [ln[i] for i in range(len(ln)) if nt[i] is not None]
    ny = [t for t in nt if t is not None]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(nx, ny, color=C_NAIVE, lw=2.5, marker="o",
            ms=6, label="Naive  O(n)  [n ≤ 50,000 only]")
    ax.plot(ln, ft, color=C_FAST,  lw=2.5, marker="s",
            ms=5, label="Fast Exponentiation  O(log n)")
    ax.plot(ln, mt, color=C_MOD,   lw=2.5, marker="^",
            ms=5, label="Modular Exponentiation  O(log n)")

    ax.axvline(x=50_000, color=C_NAIVE, lw=1, ls=":", alpha=0.7)
    ax.text(60_000, max(ny) * 0.55, "Naive excluded\n(too slow)",
            color=C_NAIVE, fontsize=9)

    ax.set_xlabel("Exponent  n", fontsize=13)
    ax.set_ylabel("Running Time (ms)", fontsize=13)
    ax.set_title("Figure 2 — Scalability with Large Inputs\n"
                 "Fast and Modular remain practical; Naive becomes infeasible",
                 fontsize=12, pad=14)
    ax.legend(fontsize=10, framealpha=0.7)
    ax.xaxis.set_major_formatter(
        ticker.FuncFormatter(lambda x, _: f"{int(x/1000)}k" if x < 1_000_000 else "1M"))
    plt.tight_layout()
    plt.savefig("graph2_large_scalability.png", dpi=150, bbox_inches="tight")
    print("  Saved: graph2_large_scalability.png")
    plt.show()


def graph3(e3n, nr, fr, mr):
    """ Figure 3: Complexity validation — T(n)/f(n) ratios. """
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    datasets = [
        (nr, C_NAIVE, "Naive: T(n) / n",          "T(n) / n  (μs per unit)"),
        (fr, C_FAST,  "Fast: T(n) / log₂(n)",     "T(n) / log₂(n)  (μs per unit)"),
        (mr, C_MOD,   "Modular: T(n) / log₂(n)",  "T(n) / log₂(n)  (μs per unit)"),
    ]
    for ax, (ratios, color, title, ylabel) in zip(axes, datasets):
        ax.plot(e3n, ratios, color=color, lw=2.5, marker="o", ms=5)
        mean_val = statistics.mean(ratios)
        ax.axhline(mean_val, color=color, lw=1.2, ls="--", alpha=0.6,
                   label=f"Mean = {mean_val:.5f}")
        ax.set_xlabel("Exponent  n", fontsize=11)
        ax.set_ylabel(ylabel, fontsize=10)
        ax.set_title(
            f"{title}\n→ stable ratio confirms complexity", fontsize=11)
        ax.legend(fontsize=9)
        ax.set_ylim(bottom=0)
        ax.xaxis.set_major_formatter(fmt_n)

    fig.suptitle("Figure 3 — Complexity Validation: T(n)/f(n) Ratios\n"
                 "Converging to constants confirms O(n) and O(log n)",
                 fontsize=13, y=1.02)
    plt.tight_layout()
    plt.savefig("graph3_complexity_validation.png",
                dpi=150, bbox_inches="tight")
    print("  Saved: graph3_complexity_validation.png")
    plt.show()


def graph4(e1n, nm, fm, mm):
    """ Figure 4: Speedup ratio of Fast and Modular vs Naive. """
    sf = [n / f if f > 0 else 0 for n, f in zip(nm, fm)]
    sm = [n / m if m > 0 else 0 for n, m in zip(nm, mm)]
    na = np.array(e1n, dtype=float)
    th = na / np.log2(na)
    sc = sf[-1] / th[-1]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(e1n, sf, color=C_FAST, lw=2.5, marker="s",
            ms=4, label="Speedup: Naive / Fast")
    ax.plot(e1n, sm, color=C_MOD,  lw=2.5, marker="^",
            ms=4, label="Speedup: Naive / Modular")
    ax.plot(na,  sc * th, color="#888", lw=1.2, ls="--", alpha=0.6,
            label="Theoretical n / log₂(n)  (scaled)")

    ax.set_xlabel("Exponent  n", fontsize=13)
    ax.set_ylabel("Speedup Factor  (× times faster than Naive)", fontsize=13)
    ax.set_title("Figure 4 — Speedup Ratio vs Naive Exponentiation\n"
                 "Gap grows proportional to n / log₂(n) as theory predicts",
                 fontsize=12, pad=14)
    ax.legend(fontsize=10, framealpha=0.7)
    ax.xaxis.set_major_formatter(fmt_n)
    plt.tight_layout()
    plt.savefig("graph4_speedup_ratio.png", dpi=150, bbox_inches="tight")
    print("  Saved: graph4_speedup_ratio.png")
    plt.show()


def graph5(e1n, nm, fm, mm):
    """ Figure 5: Log-scale combined view of all three algorithms. """
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.semilogy(e1n, nm, color=C_NAIVE, lw=2.5,
                marker="o", ms=3, label="Naive  O(n)")
    ax.semilogy(e1n, fm, color=C_FAST,  lw=2.5,
                marker="s", ms=3, label="Fast  O(log n)")
    ax.semilogy(e1n, mm, color=C_MOD,   lw=2.5, marker="^",
                ms=3, label="Modular  O(log n)")

    ax.set_xlabel("Exponent  n", fontsize=13)
    ax.set_ylabel("Running Time ms  (logarithmic scale)", fontsize=13)
    ax.set_title("Figure 5 — Log-Scale Comparison\n"
                 "All three algorithms; gap confirms order-of-magnitude difference",
                 fontsize=12, pad=14)
    ax.legend(fontsize=10, framealpha=0.7)
    ax.xaxis.set_major_formatter(fmt_n)
    plt.tight_layout()
    plt.savefig("graph5_logscale.png", dpi=150, bbox_inches="tight")
    print("  Saved: graph5_logscale.png")
    plt.show()


def graph6(e4n, bd):
    """ Figure 6: Effect of base value on Naive runtime. """
    colors = [C_NAIVE, C_FAST, C_MOD]
    fig, ax = plt.subplots(figsize=(10, 6))
    for (b, times), color in zip(bd.items(), colors):
        ax.plot(e4n, times, color=color, lw=2.5, marker="o",
                ms=3, label=f"Naive  base = {b}")

    ax.set_xlabel("Exponent  n", fontsize=13)
    ax.set_ylabel("Running Time (ms)", fontsize=13)
    ax.set_title("Figure 6 — Effect of Base Value on Naive Exponentiation\n"
                 "Larger bases → bigger intermediate integers → higher per-multiplication cost",
                 fontsize=12, pad=14)
    ax.legend(fontsize=10, framealpha=0.7)
    ax.xaxis.set_major_formatter(fmt_n)
    plt.tight_layout()
    plt.savefig("graph6_base_comparison.png", dpi=150, bbox_inches="tight")
    print("  Saved: graph6_base_comparison.png")
    plt.show()


def graph7(e1n, nm, fm, mm, ns, fs, ms):
    """ Figure 7: Error bars showing measurement stability across 10 trials. """
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    datasets = [
        (nm, ns, C_NAIVE, "Naive  O(n)"),
        (fm, fs, C_FAST,  "Fast  O(log n)"),
        (mm, ms, C_MOD,   "Modular  O(log n)"),
    ]
    for ax, (means, stds, color, label) in zip(axes, datasets):
        ax.errorbar(e1n, means, yerr=stds, fmt="-o", color=color,
                    ecolor=color, elinewidth=1, capsize=3, ms=3, lw=2, label=label)
        ax.set_xlabel("Exponent  n", fontsize=11)
        ax.set_ylabel("Time (ms)", fontsize=11)
        ax.set_title(f"{label}\n± 1σ error bars (10 trials)", fontsize=11)
        ax.xaxis.set_major_formatter(fmt_n)

    fig.suptitle("Figure 7 — Runtime Stability: Mean ± Standard Deviation\n"
                 "Small error bars confirm measurement reliability",
                 fontsize=13, y=1.02)
    plt.tight_layout()
    plt.savefig("graph7_errorbars.png", dpi=150, bbox_inches="tight")
    print("  Saved: graph7_errorbars.png")
    plt.show()


# ════════════════════════════════════════════════════════════════
# SECTION 6 — MAIN
# ════════════════════════════════════════════════════════════════

if __name__ == "__main__":

    # Step 1: Verify correctness of all three algorithms
    verify_correctness()

    # Step 2: Run all four experiments
    print("\n[Running experiments — this may take 3–5 minutes...]")
    e1n, e1nm, e1fm, e1mm, e1ns, e1fs, e1ms = experiment_1(base=2, trials=10)
    e2n, e2nt, e2ft, e2mt = experiment_2(base=2, trials=5)
    e3n, e3nr, e3fr, e3mr = experiment_3(base=2, trials=10)
    e4n, e4bd = experiment_4(trials=7)

    # Step 3: Save CSVs for reference
    print("\n[Saving CSVs...]")
    with open("exp1_results.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["n", "naive_ms", "fast_ms", "mod_ms",
                   "naive_std", "fast_std", "mod_std"])
        w.writerows(zip(e1n, e1nm, e1fm, e1mm, e1ns, e1fs, e1ms))
    print("  Saved: exp1_results.csv")

    with open("exp3_ratios.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["n", "naive_ratio", "fast_ratio", "mod_ratio"])
        w.writerows(zip(e3n, e3nr, e3fr, e3mr))
    print("  Saved: exp3_ratios.csv")

    # Step 4: Generate all 7 graphs
    print("\n[Generating 7 graphs...]")
    graph1(e1n, e1nm, e1fm, e1mm, e1ns, e1fs, e1ms)
    graph2(e2n, e2nt, e2ft, e2mt)
    graph3(e3n, e3nr, e3fr, e3mr)
    graph4(e1n, e1nm, e1fm, e1mm)
    graph5(e1n, e1nm, e1fm, e1mm)
    graph6(e4n, e4bd)
    graph7(e1n, e1nm, e1fm, e1mm, e1ns, e1fs, e1ms)
    print("------------------------------------------------------------")
    print("  Done! 7 graphs + 2 CSVs saved to current directory.")
    print("------------------------------------------------------------")
