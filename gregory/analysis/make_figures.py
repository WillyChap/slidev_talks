"""Build slide data and figures from cesm2_global_annual.csv (written by global_means.py).

Anomalies: abrupt-4xCO2 minus the piControl mean over the parallel control years.
CESM2 abrupt-4xCO2 r1i1p1f1 branches from piControl at the start of control year 502.

Outputs
  ../data/cesm2_gregory.json       year, dT, N used by the Vue components
  ../data/fit_summary.json         numbers quoted on the slides
  ../../public/figures/*.png       static figures
"""
import json, os
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
FIGS = os.path.join(HERE, "..", "..", "public", "figures")
os.makedirs(DATA, exist_ok=True); os.makedirs(FIGS, exist_ok=True)

ACCENT, BLUE, INK, GREY = "#B5473A", "#2E6F95", "#222222", "#9A9A9A"
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 15, "axes.labelsize": 16, "xtick.labelsize": 14,
    "ytick.labelsize": 14, "axes.spines.top": False, "axes.spines.right": False,
    "lines.linewidth": 2.5, "legend.frameon": False, "legend.fontsize": 14,
    "figure.constrained_layout.use": True, "savefig.dpi": 200,
})

df = pd.read_csv(os.path.join(HERE, "cesm2_global_annual.csv"))
a = df[df.experiment == "abrupt-4xCO2"].set_index("year").sort_index()
c = df[df.experiment == "piControl"].set_index("year").sort_index()
ctrl = c.loc[502:]                       # control years parallel to the 4xCO2 run
drift_T = np.polyfit(ctrl.index, ctrl.tas, 1)[0] * 100
drift_N = np.polyfit(ctrl.index, ctrl.N, 1)[0] * 100
yr = a.index.values
dT = (a.tas - ctrl.tas.mean()).values
N = (a.N - ctrl.N.mean()).values

json.dump({"year": yr.tolist(), "dT": np.round(dT, 3).tolist(), "N": np.round(N, 3).tolist()},
          open(os.path.join(DATA, "cesm2_gregory.json"), "w"))

def fit(y0, y1):
    m = (yr >= y0) & (yr <= y1)
    s, F = np.polyfit(dT[m], N[m], 1)
    return dict(F=F, B=-s, Teq=F / -s)

fits = {k: fit(*v) for k, v in {"1-150": (1, 150), "1-20": (1, 20), "21-150": (21, 150),
                                "151-999": (151, yr.max())}.items()}
late = (yr > yr.max() - 50)
summary = dict(
    control_years=[int(ctrl.index.min()), int(ctrl.index.max())],
    control_drift_T_per_century=drift_T, control_drift_N_per_century=drift_N,
    year1=dict(dT=dT[0], N=N[0]), year50=dict(dT=dT[49], N=N[49]),
    year150_dT=float(dT[149]), mean_last50=dict(dT=dT[late].mean(), N=N[late].mean(),
                                               years=[int(yr[late][0]), int(yr[late][-1])]),
    fits=fits,
)
json.dump(summary, open(os.path.join(DATA, "fit_summary.json"), "w"), indent=2, default=float)
print(json.dumps(summary, indent=2, default=float))

# ---- Figure 1: time series, years 1-150 --------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.0, 4.4))
m150 = yr <= 150
for ax, v, lab in [(ax1, dT, "Surface warming ΔT (K)"), (ax2, N, "TOA imbalance N (W m⁻²)")]:
    ax.plot(yr[m150], v[m150], color=INK, lw=1.8)
    for y, col in [(1, BLUE), (50, ACCENT)]:
        ax.plot(y, v[y - 1], "o", ms=10, color=col, zorder=3)
        ax.annotate(f"year {y}", (y, v[y - 1]), textcoords="offset points",
                    xytext=((12, 2) if y == 1 else (10, -18)) if ax is ax1 else (6, 24), color=col, fontsize=14)
    ax.set_xlabel("Year after CO₂ quadrupling"); ax.set_ylabel(lab); ax.set_xlim(0, 150)
ax2.axhline(0, color=GREY, lw=1.2, ls="--"); ax1.set_ylim(0, 8.5); ax2.set_ylim(-0.5, 9)
ax1.text(0.02, 0.95, "(a)", transform=ax1.transAxes, fontsize=16, va="top")
ax2.text(0.92, 0.95, "(b)", transform=ax2.transAxes, fontsize=16, va="top")
fig.savefig(os.path.join(FIGS, "cesm2_timeseries.png"))

# ---- Figure 2: board example ------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6.0, 4.6))
x = np.linspace(0, 4, 50)
ax.plot(x, 8 - 2 * x, color=ACCENT, label="N = 8 − 2ΔT")
ax.axhline(0, color=GREY, lw=1.2, ls="--")
ax.plot([1, 3], [6, 2], "o", ms=11, color=INK, zorder=3)
ax.annotate("year 1", (1, 6), xytext=(10, 6), textcoords="offset points", fontsize=14)
ax.annotate("year 50", (3, 2), xytext=(10, 6), textcoords="offset points", fontsize=14)
ax.plot(0, 8, "o", ms=11, mfc="none", mec=ACCENT, mew=2.5)
ax.plot(4, 0, "o", ms=11, mfc="none", mec=ACCENT, mew=2.5)
ax.annotate("forcing\n8 W m⁻²", (0, 8), xytext=(14, 0), textcoords="offset points", fontsize=14, color=ACCENT)
ax.annotate("equilibrium\n4 K", (4, 0), xytext=(10, 12), textcoords="offset points", fontsize=14, color=ACCENT)
ax.set_xlim(-0.1, 5.4); ax.set_ylim(-1, 9)
ax.set_xlabel("Surface warming ΔT (K)"); ax.set_ylabel("TOA imbalance N (W m⁻²)")
fig.savefig(os.path.join(FIGS, "board_example.png"))

# ---- Figure 3: 999-year check of the 150-year extrapolation --------------------------------
f150 = fits["1-150"]
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.0, 4.6))
sc = ax1.scatter(dT, N, c=yr, s=9, cmap="cividis", zorder=2)
xx = np.array([0, f150["Teq"]])
ax1.plot(xx, f150["F"] - f150["B"] * xx, color=ACCENT, label="fit to years 1–150")
ax1.axhline(0, color=GREY, lw=1.2, ls="--")
ax1.set_xlabel("Surface warming ΔT (K)"); ax1.set_ylabel("TOA imbalance N (W m⁻²)")
ax1.set_xlim(0, 13.5); ax1.set_ylim(-1, 10); ax1.legend(loc="upper right")
cb = fig.colorbar(sc, ax=ax1, pad=0.01); cb.set_label("Year"); cb.outline.set_visible(False)
ax2.plot(yr, dT, color=INK, lw=1.2)
ax2.axhline(f150["Teq"], color=ACCENT, ls="--", label=f"years 1–150 estimate, {f150['Teq']:.1f} K")
ax2.axvline(150, color=GREY, lw=1.2, ls=":")
ax2.set_xlabel("Year after CO₂ quadrupling"); ax2.set_ylabel("Surface warming ΔT (K)")
ax2.set_xlim(0, yr.max()); ax2.set_ylim(0, 13); ax2.legend(loc="lower right")
ax1.text(0.02, 0.97, "(a)", transform=ax1.transAxes, fontsize=16, va="top")
ax2.text(0.02, 0.97, "(b)", transform=ax2.transAxes, fontsize=16, va="top")
fig.savefig(os.path.join(FIGS, "cesm2_999yr_check.png"))
