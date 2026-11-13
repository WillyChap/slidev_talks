# How much warming is still to come?

Suppose we abruptly increase CO₂ in a coupled climate model and then hold it fixed. The model continues to warm for decades as the ocean takes up heat.

After 150 years, the run tells us how much warming has occurred so far. How can we estimate the warming that would occur if we kept running the model?

---

# Is the climate still gaining energy?

At the top of the atmosphere, Earth absorbs shortwave radiation and emits longwave radiation. The difference is the net energy flux into the climate system.

$$
R_{\mathrm{TOA}} = \mathrm{ASR} - \mathrm{OLR}
$$

- **ASR** is absorbed shortwave radiation.
- **OLR** is outgoing longwave radiation.

All fluxes are global means in W m$^{-2}$. A positive $R_{\mathrm{TOA}}$ means the climate system is gaining energy. At equilibrium, incoming and outgoing energy balance on average.

**Discussion.** Where does most of the extra energy go while the climate warms?

<!-- Expected answer. Into the ocean. -->

---

# Forcing and the response to warming

**CO₂ changes the energy budget.** Immediately after CO₂ increases, less longwave radiation escapes to space. The planet starts gaining energy before the surface has warmed appreciably.

**Warming changes the energy budget again.** A warmer planet tends to emit more longwave radiation. Changes in clouds and surface reflectivity also affect the net flux.

As warming proceeds, the net radiative response can offset more of the original forcing. The TOA imbalance then decreases even though CO₂ remains fixed.

---

# An abrupt CO₂ experiment

Start two simulations from the same climate state. In the **control**, keep CO₂ at its preindustrial concentration. In the **abrupt-4×CO₂ run**, quadruple CO₂ at the start and hold it there.

For each year, calculate two global-mean quantities relative to the control:

- $\Delta T$ is the change in surface air temperature, in K.
- $N$ is the change in net downward TOA radiation, in W m$^{-2}$.

**What do the time series show?** After the initial jump in $N$, surface temperature generally rises and the energy imbalance declines.

<!-- Insert He et al. (2026), Figure 1. Mark one early year and one later year on both time series. -->

---

# From two time series to one Gregory diagram

Each dot pairs $\Delta T$ and $N$ from **the same year**.

| Illustrative year | Surface warming, $\Delta T$ (K) | TOA imbalance, $N$ (W m$^{-2}$) |
|---|---:|---:|
| Year 1 | 1 | 6 |
| Year 50 | 3 | 2 |

Put $\Delta T$ on the horizontal axis and $N$ on the vertical axis. Plot both years and label them.

**Which way does the model move as it warms? Has it reached energy balance by year 50?**

<!-- Draw N = 0 on the board. Year 50 is farther right and lower, but still above the zero line. -->

---

# Why fit a straight line?

Recall the 0D energy balance model from Lecture 3.

$$
C\frac{d\Delta T}{dt} = N = \Delta F - B\Delta T
$$

$\Delta F$ is the imposed radiative forcing in W m$^{-2}$. The restoring coefficient $B$ is the decrease in net downward radiation per kelvin of warming, in W m$^{-2}$ K$^{-1}$.

With fixed forcing and constant $B$, plotting $N$ against $\Delta T$ gives a straight line with slope $-B$. In a coupled model, we fit that line to the annual points and use the slope to estimate the net radiative response to warming.

---

# Reading the Gregory diagram

| Feature | Physical interpretation |
|---|---|
| **Vertical intercept** at $\Delta T=0$ | Estimate of the effective radiative forcing. |
| **Slope** $-B$ | Change in the TOA imbalance per kelvin of warming. |
| **Horizontal intercept** at $N=0$ | Estimate of the equilibrium warming for this CO₂ increase. |

In the board example, the two points give $N=8-2\Delta T$. The line reaches $N=0$ at **4 K**. At year 50, the model has warmed by 3 K, so the line projects another 1 K of warming.

**Prediction.** If a second model has the same forcing and a shallower negative slope, where will its line cross $N=0$?

<!-- It crosses farther to the right. Each kelvin of warming offsets less of the forcing. -->

---

# A Gregory diagram from CESM2

<!-- Insert He et al. (2026), Figure 2. Start with the annual points and the black fit for years 1–150. Then compare the fits for different periods. -->

Each point is one year of the abrupt-4×CO₂ simulation. Follow the points from the early years to the later years. Then trace the fit for years 1–150 to $N=0$.

**Why is that crossing an estimate?** The early and late years give different slopes. As the geographic pattern of surface warming changes, the global radiative response per kelvin can change as well.

[CESM2 time series and Gregory diagram, He et al. (2026), Figures 1 and 2](https://doi.org/10.1029/2026JD046855)