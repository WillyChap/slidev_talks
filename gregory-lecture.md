---
theme: cu-boulder
title: "Gregory Diagrams"
coverAuthor: "Will Chapman"
coverDate: "Fall 2026"
mdc: true
routerMode: hash
themeConfig:
  showLogo: true
  department: "Department of Atmospheric & Oceanic Sciences"
  footerNav:
    sections:
      - { label: Energy budget, start: 2, end: 4 }
      - { label: Gregory diagram, start: 5, end: 9 }
      - { label: CESM2, start: 10, end: 12 }
    hideOnCover: true
---

# Gregory Diagrams

## Estimating equilibrium warming from an unfinished simulation

<!--
Lecture plan, about 50 minutes. Two discussion pauses (slides 3 and 6), one board exercise (slide 6),
and two interactive slides (8 and 10). Slides 8 and 10 need the dev server (npm run gregory);
the PDF export shows them at their default settings.
-->

---

# How much warming is still to come?

Suppose we abruptly increase CO₂ in a coupled climate model and then hold it fixed. The model continues to warm for decades as the ocean takes up heat.

After 150 years, the run tells us how much warming has occurred so far. How can we estimate the warming that would occur if we kept running the model?

<div class="context">

**Why not just keep running it?** The deep ocean adjusts over centuries to millennia. A coupled model would need thousands of simulated years to reach equilibrium, so most CMIP abrupt-4×CO₂ runs stop at 150 years.

The warming at equilibrium for **doubled** CO₂ is the **equilibrium climate sensitivity (ECS)**, the most widely quoted number about any climate model.

</div>

<!--
Set up the problem as a practical one. A 150-year coupled run at CMIP resolution costs months of
computer time, and a run to equilibrium would cost tens of times more. LongRunMIP (Rugenstein et al. 2019)
collected the few runs that went beyond 1000 years, and CESM2 is one of the models with a 999-year
abrupt-4xCO2 run, which we use at the end of the lecture to check the method we develop today.
Ask the class to guess what fraction of the equilibrium warming a model reaches in 150 years.
-->

---

# Is the climate still gaining energy?

At the top of the atmosphere, Earth absorbs shortwave radiation and emits longwave radiation. The difference is the net energy flux into the climate system.

$$
R_{\mathrm{TOA}} = \mathrm{ASR} - \mathrm{OLR}
$$

- **ASR** is absorbed shortwave radiation, about 240 W m$^{-2}$ in the global mean.
- **OLR** is outgoing longwave radiation, also about 240 W m$^{-2}$.

All fluxes are global means in W m$^{-2}$. A positive $R_{\mathrm{TOA}}$ means the climate system is gaining energy. At equilibrium, incoming and outgoing energy balance on average. Today the observed imbalance is about **+1 W m$^{-2}$**, less than 1% of either term.

**Discussion.** Where does most of the extra energy go while the climate warms?

<!--
Expected answer: into the ocean. About 91% of the heat gained since 1971 is stored in the ocean,
with the rest warming land, melting ice and warming the atmosphere (IPCC AR6 WG1, Chapter 7).
The ocean's large heat capacity is the reason the surface lags the forcing, and it is the reason
a 150-year run is far from equilibrium. The +1 W m-2 imbalance comes from CERES satellite fluxes
anchored to ocean heat content measurements (Loeb et al. 2021). Emphasise that the imbalance is a
small difference between two large numbers, so models are judged on changes, not absolute values.
-->

---
layout: two-cols
---

# Forcing and the response to warming

**CO₂ changes the energy budget.** Immediately after CO₂ increases, less longwave radiation escapes to space. The planet starts gaining energy before the surface has warmed appreciably.

**Warming changes the energy budget again.** A warmer planet tends to emit more longwave radiation. Changes in clouds and surface reflectivity also affect the net flux.

As warming proceeds, the net radiative response can offset more of the original forcing. The TOA imbalance then decreases even though CO₂ remains fixed.

::right::

<div class="side-box">

**The net response is a sum of feedbacks**, each in W m$^{-2}$ K$^{-1}$ of extra outgoing energy per kelvin:

| Process | Effect on B |
|---|---|
| Planck (hotter emits more) | about +3.2, stabilising |
| Water vapour | reduces B |
| Lapse rate | increases B |
| Surface albedo (snow, ice) | reduces B |
| Clouds | reduces B in most models |

CMIP6 models give a net $B$ of roughly 0.5 to 1.8 W m$^{-2}$ K$^{-1}$, so feedbacks cancel much of the Planck response.

</div>

<!--
Keep the sign convention explicit: B is positive when the system is stable, because more warming means
more energy lost to space. The Planck value comes from differentiating the Stefan-Boltzmann law at
the effective emission temperature, with a correction for the vertical structure of warming. Water vapour
and lapse rate feedbacks partly cancel. The spread between models is dominated by clouds, especially
low clouds over the subtropical oceans (Zelinka et al. 2020). The Gregory diagram measures the sum of
all these terms at once, which is why it is so widely used.
-->

---

# An abrupt CO₂ experiment

Start a **control** run at preindustrial CO₂ and an **abrupt-4×CO₂** run from the same state, with CO₂ quadrupled and held fixed. Each year, $\Delta T$ is the change in global surface air temperature (K) and $N$ the change in net downward TOA radiation (W m$^{-2}$), relative to the control.

<img src="/figures/cesm2_timeseries.png" class="fig-full" alt="CESM2 abrupt-4xCO2 global-mean surface warming and TOA imbalance for years 1 to 150" />

<div class="caption">

Annual global means from CESM2 abrupt-4×CO₂ minus the piControl mean (CMIP6, r1i1p1f1). Year 1 and year 50 are marked in both panels.

</div>

<!--
Ask what the time series show before saying it. After the initial jump in N, surface temperature
rises quickly for about two decades and then much more slowly, while N falls from 7.7 W m-2 in year 1
to 2.7 W m-2 in year 50. Year 1 already shows 0.8 K of warming because the land and ocean
mixed layer respond within months. The slow part of the warming is set by heat exchange with the
deep ocean. The same panels are Figure 1 of He et al. (2026) if you prefer to show the published version.
These data are the CMIP6 archive on Glade; see gregory/analysis/ for the scripts.
-->

---

# From two time series to one Gregory diagram

Each dot pairs $\Delta T$ and $N$ from **the same year**.

| Illustrative year | Surface warming, $\Delta T$ (K) | TOA imbalance, $N$ (W m$^{-2}$) |
|---|---:|---:|
| Year 1 | 1 | 6 |
| Year 50 | 3 | 2 |

Put $\Delta T$ on the horizontal axis and $N$ on the vertical axis. Plot both years and label them.

**Which way does the model move as it warms? Has it reached energy balance by year 50?**

<div class="context small">

The numbers are rounded for the board. CESM2 gives year 1 at (0.8 K, 7.7 W m⁻²) and year 50 at (5.6 K, 2.7 W m⁻²).

</div>

<!--
Draw N = 0 on the board. Year 50 is farther right and lower, but still above the zero line, so the
model is still gaining energy and will keep warming. Time is not an axis on this plot, which is the
step students find hardest. Point out that a model moves down and to the right along a path, and the
speed along the path slows with time. Ask what the point for equilibrium would look like: it sits on
the N = 0 line and stops moving.
-->

---
class: dense
---

# Why fit a straight line?

Recall the 0D energy balance model from Lecture 3.

$$
C\frac{d\Delta T}{dt} = N = \Delta F - B\Delta T
$$

$\Delta F$ is the imposed radiative forcing in W m$^{-2}$. The restoring coefficient $B$ is the decrease in net downward radiation per kelvin of warming, in W m$^{-2}$ K$^{-1}$. $C$ is the heat capacity per unit area, in J m$^{-2}$ K$^{-1}$.

With fixed forcing and constant $B$, plotting $N$ against $\Delta T$ gives a straight line with slope $-B$. In a coupled model, we fit that line to the annual points and use the slope to estimate the net radiative response to warming.

<div class="context">

**Two limits fix the line.** At the start, $\Delta T = 0$ so $N = \Delta F$. At equilibrium, $N = 0$ so $\Delta T_{\mathrm{eq}} = \Delta F / B$. The heat capacity $C$ sets how fast the model moves along the line, not where the line is.

</div>

<!--
The relation N = dF - B dT does not contain time or heat capacity, which is why the diagram works for
a model whose ocean we do not need to describe. Solving the ODE gives an exponential approach with
timescale C/B, a few years for a 75 m mixed layer. A real ocean has a deep reservoir as well, which
gives a second timescale of centuries. Both are explored on the next slide. Stress that the straight
line is an assumption about B, and we will test it with CESM2.
-->

---

# The 0D model under abrupt forcing

<EBMExplorer />

<div class="caption">

Mixed-layer model of Lecture 3 with an optional deep ocean, $C\,d\Delta T/dt = \Delta F - B\Delta T - \gamma(\Delta T - \Delta T_D)$ (Held et al. 2010). Dots on the right panel mark every 10 years.

</div>

<!--
Live demonstration. First change the mixed-layer depth: the curve on the left speeds up or slows down,
and the line on the right does not change. Then change B and show that the horizontal intercept moves
to dF/B. Then turn on deep-ocean uptake gamma: warming has a fast and a slow part, as in CESM2, but the
Gregory line stays straight because N still equals dF - B dT. Finally overlay CESM2. With gamma near
0.7 the time series can be made to look like CESM2, but the CESM2 points curve on the Gregory diagram,
which no setting of this model can reproduce. That curvature is the subject of the last part.
-->

---
layout: two-cols
class: dense
---

# Reading the Gregory diagram

| Feature | Physical interpretation |
|---|---|
| **Vertical intercept** at $\Delta T=0$ | Estimate of the effective radiative forcing. |
| **Slope** $-B$ | Change in the TOA imbalance per kelvin of warming. |
| **Horizontal intercept** at $N=0$ | Estimate of the equilibrium warming for this CO₂ increase. |

In the board example, the two points give $N=8-2\Delta T$. The line reaches $N=0$ at **4 K**. At year 50, the model has warmed by 3 K, so the line projects another 1 K of warming.

**Prediction.** If a second model has the same forcing and a shallower negative slope, where will its line cross $N=0$?

::right::

<img src="/figures/board_example.png" class="fig-side" alt="Board example Gregory diagram with two points and the line N = 8 minus 2 delta T" />

<div class="caption">

The two board points and the line through them. The open circles mark the two intercepts.

</div>

<!--
Prediction answer: it crosses farther to the right. Each kelvin of warming offsets less of the forcing,
so more warming is needed to restore balance. The vertical intercept is called the effective radiative
forcing because it includes the rapid adjustments of the atmosphere and land that happen within the
first months, before the global surface has warmed. For 4xCO2, ECS is usually taken as half of the
horizontal intercept, because the forcing grows roughly with the logarithm of CO2 concentration.
B = 2 W m-2 K-1 in this example is larger than in any CMIP6 model, chosen to keep the numbers simple.
-->

---

# A Gregory diagram from CESM2

<GregoryExplorer />

<div class="caption">

Each point is one year of CESM2 abrupt-4×CO₂. The red line is a least-squares fit to the selected years, extended to $N = 0$.

</div>

<!--
Start with the fit for years 1-150, which gives 6.5 W m-2, B = 0.63 W m-2 K-1 and an equilibrium
warming of 10.3 K, so ECS of about 5.2 K. This matches the 5.2 K that Zelinka et al. (2020) report
for CESM2 with the same method. Then click 1-20 and 21-150.
The early years give a steeper slope (B = 1.14) and the later years a shallower one (B = 0.41). The
later fit crosses N = 0 at 12.5 K. Why is the crossing only an estimate? As the geographic pattern of
surface warming changes, the global radiative response per kelvin can change as well. He et al. (2026),
Figure 2, shows the same comparison.
-->

---

# The 150-year estimate against 999 years

<img src="/figures/cesm2_999yr_check.png" class="fig-full" alt="CESM2 Gregory diagram for all 999 years with the years 1 to 150 fit, and the warming time series against the estimate" />

<div class="caption">

CESM2 abrupt-4×CO₂ continued to year 999. By years 950–999 the model has warmed 11.3 K and still gains 0.8 W m⁻², above the 10.3 K given by the fit to years 1–150.

</div>

<!--
This is the test students cannot usually do, because few models were run this long. The points after
year 150 lie above the line fitted to years 1-150, so the linear extrapolation underestimates the
eventual warming. A fit to years 151-999 alone gives B = 0.35 W m-2 K-1 and an equilibrium warming
of 13.3 K. Rugenstein et al. (2020) found the same behaviour in most LongRunMIP models. The cause is the
pattern effect: warming slowly spreads to the eastern Pacific and the Southern Ocean, where the local
radiative response per kelvin is weak, so the global B decreases with time.
-->

---

# References

<div class="refs">

- Gregory, J. M., et al. (2004). A new method for diagnosing radiative forcing and climate sensitivity. *Geophys. Res. Lett.*, 31, L03205. [doi:10.1029/2003GL018747](https://doi.org/10.1029/2003GL018747)
- He, et al. (2026). CESM2 time series and Gregory diagram, Figures 1 and 2. *J. Geophys. Res. Atmos.* [doi:10.1029/2026JD046855](https://doi.org/10.1029/2026JD046855)
- Held, I. M., et al. (2010). Probing the fast and slow components of global warming by returning abruptly to preindustrial forcing. *J. Climate*, 23, 2418–2427.
- Gettelman, A., et al. (2019). High climate sensitivity in the Community Earth System Model version 2 (CESM2). *Geophys. Res. Lett.*, 46, 8329–8337.
- Rugenstein, M., et al. (2020). Equilibrium climate sensitivity estimated by equilibrating climate models. *Geophys. Res. Lett.*, 47, e2019GL083898.
- Zelinka, M. D., et al. (2020). Causes of higher climate sensitivity in CMIP6 models. *Geophys. Res. Lett.*, 47, e2019GL085782.
- Data: CESM2 abrupt-4×CO₂ and piControl, r1i1p1f1, CMIP6 archive (Danabasoglu, 2019).

</div>

<!--
Check the He et al. (2026) author list and title before distributing the slides.
-->

