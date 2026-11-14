---
theme: ./themes/atoc4870
title: "Gregory diagrams"
layout: cover
author: ["Will Chapman", "ATOC 4870 / 5870"]
tagline: "Estimating equilibrium warming from an unfinished simulation"
mdc: true
routerMode: hash
---

# Gregory diagrams

<!--
{{NOTE1}}
-->

---

# How much warming is still to come?

**Suppose we abruptly increase CO₂ in a coupled climate model and then hold it fixed. The model continues to warm for decades as the ocean takes up heat.**

After 150 years, the run tells us how much warming has occurred so far.

<div class="context">

The deep ocean adjusts over centuries to millennia, so a coupled model would need thousands of simulated years to reach equilibrium. Most CMIP abrupt-4×CO₂ runs stop at 150 years. The equilibrium warming for **doubled** CO₂ is the **equilibrium climate sensitivity (ECS)**.

</div>

<div class="ask">

How can we estimate the warming that would occur if we kept running the model?

</div>

<!--
{{NOTE2}}
-->

---

# Is the climate still gaining energy?

At the top of the atmosphere, Earth absorbs shortwave radiation and emits longwave radiation. The difference is the net energy flux into the climate system.

$$
R_{\mathrm{TOA}} = \mathrm{ASR} - \mathrm{OLR}
$$

- **ASR** is absorbed shortwave radiation, about 240 W m$^{-2}$.
- **OLR** is outgoing longwave radiation, also about 240 W m$^{-2}$.

A positive $R_{\mathrm{TOA}}$ means the climate system is gaining energy. Today the observed imbalance is about +1 W m$^{-2}$, less than 1% of either term.

<div class="ask">

Question: where does most of the extra energy go while the climate warms?

</div>

<div class="footnote">All fluxes are global means in W m⁻². At equilibrium, incoming and outgoing energy balance on average.</div>

<!--
{{NOTE3}}
-->

---

# Forcing and the response to warming

<div class="cols">
<div>

### CO₂ changes the energy budget

Less longwave radiation escapes to space. The planet gains energy before the surface has warmed.

### Warming changes it again

A warmer planet emits more longwave radiation. Clouds and surface reflectivity also change the net flux.

</div>
<div class="small-table">

| Feedback | Effect on B |
|---|---|
| Planck | about +3.2, stabilising |
| Water vapour | reduces B |
| Lapse rate | increases B |
| Surface albedo | reduces B |
| Clouds | reduces B in most models |

</div>
</div>

<div class="ask">

The TOA imbalance decreases as warming proceeds, even though CO₂ stays fixed.

</div>

<div class="footnote">B in W m⁻² K⁻¹. CMIP6 models give a net B of roughly 0.5 to 1.8 W m⁻² K⁻¹ (Zelinka et al. 2020).</div>

<!--
{{NOTE4}}
-->

---

# An abrupt CO₂ experiment

Start a **control** run at preindustrial CO₂ and an **abrupt-4×CO₂** run from the same state. Each year, $\Delta T$ is the change in surface air temperature (K) and $N$ the change in net downward TOA radiation (W m$^{-2}$).

<img src="/figures/cesm2_timeseries.png" class="fig-full" alt="CESM2 abrupt-4xCO2 global-mean surface warming and TOA imbalance for years 1 to 150" />

<div class="footnote">Annual global means, CESM2 abrupt-4×CO₂ minus the piControl mean (CMIP6).</div>

<!--
{{NOTE5}}
-->

---

# Two time series produce a Gregory diagram

**Each dot represents ΔT and N from the same year.**

| year | Surface warming, $\Delta T$ (K) | TOA imbalance, $N$ (W m$^{-2}$) |
|---|---:|---:|
| Year 1 | 1 | 6 |
| Year 50 | 3 | 2 |

Put $\Delta T$ on the horizontal axis and $N$ on the vertical axis.

<div class="ask">

Which way does the model move as it warms? Has it reached energy balance by year 50?

</div>

<div class="footnote">Rounded values. CESM2 gives year 1 at (0.8 K, 7.7 W m⁻²) and year 50 at (5.6 K, 2.7 W m⁻²).</div>

<!--
{{NOTE6}}
-->

---

# Linear fit

Recall the 0D energy balance model.

$$
C\frac{d\Delta T}{dt} = N = \Delta F - B\Delta T
$$

With fixed forcing $\Delta F$ and constant $B$, plotting $N$ against $\Delta T$ gives a straight line with slope $-B$. In a coupled model, we fit that line to the annual points.

At the start, $\Delta T = 0$ so $N = \Delta F$. At equilibrium, $N = 0$ so $\Delta T_{\mathrm{eq}} = \Delta F / B$.

<div class="ask">

The heat capacity C sets how fast the model moves along the line, not where the line is.

</div>

<div class="footnote">ΔF: forcing (W m⁻²). B: restoring coefficient (W m⁻² K⁻¹). C: heat capacity per unit area (J m⁻² K⁻¹).</div>

<!--
{{NOTE7}}
-->

---

# 1. Why does mixed-layer depth matter?

The upper ocean exchanges heat with the atmosphere. In the 0D model, we represent it as a single layer with a uniform temperature. Its heat capacity per unit area is

$$
C = \rho_w c_{p,w} h,
$$

where $h$ is the layer depth, $\rho_w$ is seawater density, and $c_{p,w}$ is the specific heat capacity of seawater.

With deep-ocean heat exchange turned off, the surface warming rate is

$$
\frac{d\Delta T}{dt}
= \frac{N}{C}
= \frac{\Delta F-B\Delta T}{\rho_w c_{p,w}h}.
$$

A deeper layer has more water to warm. Immediately after the forcing is applied, $\Delta T=0$, so the warming rate is $\Delta F/C$. **Doubling the depth halves the initial warming rate.**

<!-- Both have N = ΔF − B × 3 K. The deeper run takes longer to reach 3 K. -->

---

# 2. Adding a deep ocean

When the upper ocean transfers heat to the deep ocean, its warming rate becomes

$$
\frac{d\Delta T}{dt}
= \frac{\underbrace{\Delta F-B\Delta T}_{\text{TOA imbalance }N}
-\underbrace{\gamma(\Delta T-\Delta T_D)}_{\text{heat transfer to the deep ocean}}}{C}.
$$

$\Delta T_D$ is the deep-ocean warming, and $\gamma$ controls heat exchange between the layers. Heat transferred to the deep ocean still counts toward the climate system’s energy gain.

---

# 3. From surface warming to the Gregory diagram

<EBMExplorer />

**Fast timescale** $\tau = C/(B+\gamma)$ is the e-folding time of the surface layer before the deep ocean warms. A deeper mixed layer (larger $C$) slows it; stronger restoring $B$ or deep-ocean uptake $\gamma$ speeds it up.

<div class="footnote">Left: surface warming over time. Right: ΔT against the TOA imbalance N. Red dots mark 10-year intervals.</div>

<!--
{{NOTE8}}
-->



---

# Reading the Gregory diagram

<div class="cols">
<div class="small-table">

| Feature | Interpretation |
|---|---|
| Vertical intercept | Effective radiative forcing |
| Slope $-B$ | Change in $N$ per kelvin |
| Horizontal intercept | Equilibrium warming |

The board points give $N=8-2\Delta T$, which reaches $N=0$ at **4 K**. At year 50 the model has warmed 3 K, so 1 K more is to come.

</div>
<div>

<img src="/figures/board_example.png" class="fig-col" alt="Board example Gregory diagram with two points and the line N = 8 minus 2 delta T" />

</div>
</div>

<div class="ask">

Predict: with the same forcing and a shallower slope, where does the line cross N = 0?

</div>

<!--
{{NOTE9}}
-->

---

# A Gregory diagram from CESM2

<GregoryExplorer />

<div class="ask">

Why is the crossing at N = 0 only an estimate?

</div>

<!--
{{NOTE10}}
-->

---

# The 150-year estimate against 999 years

<img src="/figures/cesm2_999yr_check.png" class="fig-full" alt="CESM2 Gregory diagram for all 999 years with the years 1 to 150 fit, and the warming time series against the estimate" />

<div class="ask">

By years 950–999 CESM2 has warmed 11.3 K, above the 10.3 K from years 1–150.

</div>

<div class="footnote">CESM2 abrupt-4×CO₂, years 1–999. The model still gains 0.8 W m⁻² at the end of the run.</div>

<!--
{{NOTE11}}
-->

---

# Sources and data

<div class="refs">

### Methods

Gregory et al. (2004), *GRL* 31, L03205. Held et al. (2010), *J. Climate* 23, 2418–2427.

### CESM2 and model sensitivity

Gettelman et al. (2019), *GRL* 46, 8329–8337. Zelinka et al. (2020), *GRL* 47, e2019GL085782. Rugenstein et al. (2020), *GRL* 47, e2019GL083898. He et al. (2026), *JGR Atmospheres*, [doi:10.1029/2026JD046855](https://doi.org/10.1029/2026JD046855).

### Data

CESM2 abrupt-4×CO₂ and piControl, r1i1p1f1, CMIP6 archive (Danabasoglu, 2019).

</div>

<!--
{{NOTE12}}
-->
