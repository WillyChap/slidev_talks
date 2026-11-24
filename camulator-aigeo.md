---
theme: cu-boulder
title: "Emulating a climate model"
coverAuthor: "Will Chapman"
coverDate: "AI-Geo Seminar, CU Boulder · Fall 2026"
mdc: true
routerMode: hash
class: cm-cover
themeConfig:
  showLogo: true
  department: "Department of Atmospheric & Oceanic Sciences"
  footerNav:
    sections:
      - { label: Motivation, start: 2, end: 4 }
      - { label: The emulator, start: 5, end: 8 }
      - { label: Performance, start: 9, end: 14 }
      - { label: Limits and fixes, start: 15, end: 22 }
    hideOnCover: true
---

# Emulating a climate model with machine learning

## CAMulator and the questions it opens

<img src="/camulator/globe.png" class="cm-cover-globe" alt="Globe rendered from a CAMulator simulation" />

<!--
Thank you for having me. This is an overview of what my group works on: a machine-learning emulator of the atmosphere in the NCAR climate model, called CAMulator, and the research questions that come out of using it for climate rather than weather. The audience today spans computer science, aerospace and atmospheric science, so I will keep the model details short and spend the time on what the emulator can and cannot do. Most of the work I show was done by students and a postdoc in the group, and I will name them as we go.
-->

---

# Chapman Research Group, ATOC

<div class="cm-team">
  <div><img src="/camulator/team_heslin.png" alt="Sean Heslin" /><b>Sean Heslin</b><span>Graduate student</span><em>Atmospheric rivers in emulators</em></div>
  <div><img src="/camulator/team_pape.png" alt="Aiden Pape" /><b>Aiden Pape</b><span>Graduate student</span></div>
  <div><img src="/camulator/team_melvin.png" alt="Ona Melvin" /><b>Ona Melvin</b><span>Graduate student</span></div>
  <div><img src="/camulator/team_becker.jpg" alt="Charlie Becker" /><b>Charlie Becker</b><span>Graduate student; NCAR ML scientist</span><em>Spectral and probabilistic losses</em></div>
  <div><img src="/camulator/team_li.jpg" alt="Yuanpu Li" /><b>Yuanpu Li</b><span>Postdoctoral scholar</span><em>Coupling to ocean and sea ice</em></div>
  <div><img src="/camulator/team_gosnell.jpg" alt="Eric Gosnell" /><b>Eric Gosnell</b><span>CS master's student</span></div>
  <div><img src="/camulator/team_voeller.jpg" alt="Tate Voeller" /><b>Tate Voeller</b><span>Undergraduate student</span></div>
</div>

<div class="cm-src">The emulator is built on CREDIT, the NCAR MILES framework for machine-learning Earth system models.</div>

<!--
The group sits in Atmospheric and Oceanic Sciences and works closely with the machine-learning group at NCAR, whose CREDIT framework we train in. Sean Heslin studies atmospheric rivers in the emulator. Charlie Becker works on training losses that keep small-scale variability. Yuanpu Li built the coupling to the ocean and sea-ice models. The other students work on projects I will point to where they come up. The point of this slide is that the results that follow are a team effort across graduate, master's and undergraduate students.
-->

---

# A coupled climate model is expensive to run

<div class="cm-cols">
<div>

<img src="/camulator/cesm_components.png" class="cm-fig-col" alt="Components of the Community Earth System Model connected through a coupler" />

<div class="cm-src">Components of CESM2 connected through the coupler.</div>

</div>
<div>

<div class="cm-right">

The Community Earth System Model (CESM) steps atmosphere, ocean, land, ice and rivers forward together, every 30 simulated minutes.

- One simulated year: **3,750 core-hours** (CESM2), 25,643 (CESM3).
- A 100-member, 250-year ensemble: **94 million core-hours**.
- The atmosphere is the most expensive part, so that is what we emulate.

</div>

<div class="cm-src">Costs: Derecho, fully coupled, nominal 1° grid. Ensemble: CESM2 Large Ensemble, Rodgers et al. (2021).</div>

</div>
</div>

<!--
Climate projections need many long simulations: centuries of model time, repeated across ensemble members to separate the forced signal from internal variability. A coupled model such as CESM computes the atmosphere, ocean, land and ice on a global grid every half hour of model time. One simulated year of CESM2 costs 3,750 core-hours on NCAR's Derecho machine, and CESM3 costs about seven times more. The CESM2 Large Ensemble, one hundred members from 1850 to 2100, about 25,000 simulated years, would cost around 94 million core-hours at that rate. The atmosphere is the most expensive component, so it is the component we emulate.
-->

---

# The short version

<div class="cm-thesis">

An emulator of the CESM atmosphere gets the **bulk climate right at about 1/30th of the compute**.

Its errors sit where a squared-error training loss cannot see them: **small scales**, which come out too smooth, and **slow modes**, which drift.

</div>

<!--
Here is the whole talk in two sentences, so you know where we are going. First, the emulator works: it runs stably for decades, reproduces the warming trend and El Niño's effects, and costs about thirty times less compute when coupled to an ocean. Second, the interesting part is where it fails, and the failures have a common cause. Training minimises a squared error, which pays the network to blur small features it is unsure of and gives it almost no reason to get very slow, large-scale behaviour right. Most of the second half is about those two blind spots and what we are doing about them.
-->

---

# The network replaces the solver, step by step

The network takes the state of the atmosphere $x_t$ and returns the next state, $x_{t+1} = F_\theta(x_t)$. Feeding its own output back in gives $x_{t+2}$, and so on for as long as needed.

<img src="/camulator/rollout_diagram.png" class="cm-fig-rollout" alt="The same network F applied repeatedly: x at t to x at t plus one to x at t plus two" />

<div class="cm-src">Weather examples: GraphCast, Pangu-Weather, FourCastNet. Climate examples: ACE2, NeuralGCM, CAMulator.</div>

<!--
Before CAMulator itself, the general idea. A conventional model integrates the equations of motion with a numerical solver. An autoregressive machine-learning model keeps the same structure, a state vector advanced in time, but the step from one time to the next is a neural network trained on data. For multiple steps we feed the network its own prediction, so the same model is applied again and again. This is how the recent machine-learning weather models such as GraphCast work. Climate emulators such as ACE2, NeuralGCM and CAMulator use the same idea but have to stay stable for decades rather than days.
-->

---

# Emulation makes long runs and gradients cheap

<div class="cm-cols">
<div>

- One six-hour step takes about **0.3 s on one GPU**.
- Runs of any length and large ensembles become affordable.
- The network is differentiable, so sensitivities come from one backward pass.
- Ocean, sea ice, sunlight and CO₂ are inputs, so one network runs past and future climates.

</div>
<div>

<video src="/camulator/camulator_free_run.mp4" poster="/camulator/free_run_poster.jpg" class="cm-video" autoplay loop muted playsinline></video>

<div class="cm-src">A CAMulator free run with the ocean prescribed; no re-initialisation.</div>

</div>
</div>

<!--
The idea behind an autoregressive emulator is simple. Train a neural network to take the state of the atmosphere now and predict the state six hours later. Then feed the prediction back in as the next input, and repeat for as long as needed. The movie is such a run: no data are inserted after the first step. Each step costs about a third of a second on one GPU. Because the whole model is a neural network, the gradient of any output with respect to any input is available, which conventional climate models do not provide. The ocean, sea ice, solar input and carbon dioxide are given to the network as inputs.
-->


---

# Trained on 33 years of one CESM2 simulation

Training data: one coupled CESM2 simulation saved every six hours on a 192 × 288 grid with 32 levels. Years 1980–2012 train the network; 2013–2014 validate it. Its atmosphere component, **CAM6**, is the target the emulator learns.

<img src="/camulator/architecture.png" class="cm-fig-wide" alt="CAMulator architecture: cross-embedding attention encoder, up-sampling decoder, conservation post-blocks" />

<div class="cm-src">874 M parameters: attention encoder at four scales and a U-Net-like decoder; 136 input and 147 output maps. Earth-aware padding wraps longitude and reflects across the poles.</div>

<!--
The training data come from one coupled CESM2 simulation from 1980 to 2048, with the SSP2-4.5 scenario after 2015, saved every six hours. CAM6 is the atmosphere inside CESM2, so throughout the talk "CAM6" means the model we are emulating. The network sees 136 two-dimensional maps per step: winds, temperature and moisture on 32 levels, surface pressure, and the forcing fields. It predicts 147 maps, including precipitation and radiation. The encoder uses attention at four spatial scales and the decoder mirrors it, as in a U-Net. The loss is the mean squared error summed over three consecutive six-hour steps. Small blocks at the end rescale the output so that global mass, water and energy are conserved, and they are trained with the network.
-->

---

# Multi-step training keeps long runs stable

<img src="/camulator/three_step_loss.png" class="cm-fig-train" alt="Three-step rollout: the network applied three times, with a squared error against CESM at each step" />

<img src="/camulator/conservation_blocks.png" class="cm-fig-train cm-fig-train-b" alt="Network output passed through post-blocks that enforce tracer positivity, dry-air mass, water and energy conservation" />

<div class="cm-src">Top: the loss sums the squared error over three consecutive six-hour steps, and gradients pass back through all three. Bottom: post-blocks rescale the output so that global dry-air mass, water and energy are conserved; they are trained with the network.</div>

<!--
Two choices in training matter for climate. First, the loss is not computed on one step. The network makes three six-hour steps from its own output, and the squared error at each step is summed, so the gradient teaches it to correct errors it introduces itself. Second, the last layers are not free. Small differentiable blocks clip negative moisture and rescale the global dry-air mass, the water budget and the energy budget so that they balance, and the network is trained through them. Without these constraints, runs of more than a few years drift in mass and energy and eventually fail.
-->

---

# Forecasts as skillful as CAM6 forecasting itself

<div class="cm-cols">
<div>

<img src="/camulator/z500_skill.png" class="cm-fig-col" alt="Anomaly correlation of 500 hPa height against lead time for CAMulator and CAM6" />

</div>
<div>

<div class="cm-right">

- 233 forecasts from CAM6 states in 2013–2014, the held-out years.
- Score: pattern correlation of the mid-level pressure map (500-hPa height) with CAM6.
- **Orange, CAMulator:** stays above 0.6 for 8.9 days.
- **Black, CAM6 forecasting a perturbed copy of itself:** 7.4 days.
- Why it "wins": a squared-error loss pulls forecasts toward a smooth ensemble mean. That smoothing comes back later as muted extremes.

</div>

<div class="cm-src">Black: CESM2 subseasonal reforecasts, perturbed against unperturbed members (Richter et al. 2022).</div>

</div>
</div>

<!--
First, weather. We start CAMulator from CAM6 states and score its forecasts against what CAM6 did next. The anomaly correlation of the 500-hectopascal height field drops to 0.6, a common threshold for useful skill, at 8.9 days. The black curves are CAM6 forecasting itself from slightly perturbed initial states, which removes model error entirely, and they reach 0.6 at 7.4 days. The emulator does better than the model forecasting itself because a squared-error loss trains it to predict something close to an ensemble mean, and a mean tracks any single trajectory better than another trajectory does. Flag this: the same smoothing is the cause of the weak extremes later in the talk.
-->


---

# 35 years from one state, trend intact

<img src="/camulator/free_run_35yr.png" class="cm-fig-wide" alt="Annual global means 1980 to 2014 of five quantities for CAM6 and CAMulator" />

One continuous run of 51,100 six-hour steps from 1980, ocean prescribed. **Orange** (CAMulator) follows **black** (CAM6) year by year, including the warming trend. The lower stratosphere (b) drifts cold.

<div class="cm-src">Annual global means, 1980–2014: (a) 2-m temperature, (b) 52-hPa temperature, (c) 525-hPa temperature, (d) column water, (e) precipitation. Most of these years are in the training period; the run receives no data after its first step.</div>

<!--
For climate, the emulator has to run for decades without blowing up or drifting. This is one continuous run of 51,100 steps started from a single CAM6 state in 1980, with the observed-like ocean from the training simulation prescribed. Surface temperature, mid-tropospheric temperature, column water and precipitation follow CAM6 year by year, including the trend. One quantity is clearly wrong: the lower stratosphere cools steadily. That error is systematic rather than random, and errors of that kind turn out to be the hardest problem we work on. If asked about overfitting: these years were in training, but the run is free, so year-by-year agreement comes from the prescribed ocean, not from memorised weather. The true out-of-sample test is the scenario slide.
-->

---

# El Niño's remote effects emerge unprompted

<img src="/camulator/enso_teleconnections.png" class="cm-fig-wide" alt="Composite 500 hPa height and precipitation differences for warm minus cold tropical Pacific winters, CAM6 and CAMulator" />

**Left: CAM6. Right: CAMulator.** Top: mid-level pressure; bottom: rainfall. Pattern correlation with CAM6: **0.95** for tropical rainfall, **0.82** for the North Pacific wave train.

<div class="cm-src">Ten warmest minus ten coldest tropical Pacific winters of 34, all within the training period.</div>

<!--
El Niño is the largest source of year-to-year variability, and its effect on weather far from the tropical Pacific is a standard test for any climate model. Both models see the same ocean, so we can compare the same winters directly. During El Niño, tropical rainfall shifts east, and a wave train of pressure anomalies arches over the North Pacific and North America. The emulator reproduces the rainfall shift with a pattern correlation of 0.95 and the wave train with 0.82. Nothing in the training asked for this response; it comes from learning the six-hour dynamics.
-->

---

# Mean errors on par with other emulators

<div class="cm-cols">
<div>

<img src="/camulator/aimip_bias_camulator.png" class="cm-fig-col" alt="Bar chart of 2-m temperature time-mean bias for machine-learning climate emulators in AIMIP phase 1, with a dashed line marking CAMulator at 0.40 K" />

</div>
<div>

<div class="cm-right">

- Bars: AI Model Intercomparison Project (AIMIP) emulators, trained on and scored against observation-based reanalysis, 1979–2014.
- Dashed line: CAMulator by the same metric, against CAM6: **0.40 K**.
- Emulating a model is easier than emulating the real atmosphere, so this is a reference point, not a rank.

</div>

<div class="cm-src">Area-weighted RMS of the time-mean 2-m temperature bias on a 1° grid. Henn et al. (2026), arXiv:2605.06944, Fig. 2a; dashed line added.</div>

</div>
</div>

<!--
The AI model intercomparison project, AIMIP, measures the time-mean surface temperature bias of several machine-learning climate emulators over 1979 to 2014. Their bars are five-member medians against the ERA5 reanalysis. Applying the same recipe to CAMulator against CAM6, the model it was trained on, gives 0.40 kelvin, the dashed line, and the two halves of our run give 0.39 and 0.43. Internal variability accounts for about 0.08 kelvin of that. The comparison is not like for like: a model is a cleaner target than the real atmosphere. It places our errors at the same order as the field's.
-->


---

# Out of sample: warms too fast, rains too little

<div class="cm-pair cm-pair-short">
  <img src="/camulator/ssp245_a.png" alt="Global-mean 2-m temperature 2016 to 2044 for CAM6, CAMulator and runs with one forcing held fixed" />
  <img src="/camulator/ssp245_d.png" alt="Warming trend by latitude for CAM6, CAMulator and runs with one forcing held fixed" />
</div>

- A middle-of-the-road emissions scenario (SSP2-4.5) the emulator never saw: **0.42 K per decade** against CAM6's 0.35, with extra warming at high latitudes; global rainfall rises less than half as much.
- Why: CO₂ and ocean temperature rose together in training. Holding the ocean fixed (yellow dashed), CO₂ alone warms the surface too much.

<div class="cm-src">Left: global-mean 2-m temperature. Right: warming trend by latitude. Dashed: one forcing held fixed. Driven by the CAM6 scenario ocean and CO₂.</div>

<!--
The real test of an emulator for climate is a future it has not seen. CAM6 has a scenario run out to 2048, and CAMulator was never trained on it. Driven by the scenario's ocean and carbon dioxide, the emulator warms at 0.42 kelvin per decade against 0.35 for CAM6, with the right pattern of stronger warming at high latitudes, but too much of it. The rise in global rainfall is less than half of CAM6's. The dashed runs hold one forcing fixed and show that the response to carbon dioxide alone is too strong at the surface, because carbon dioxide and ocean temperature rose together in the training data, and the network cannot tell which one caused the warming.
-->


---

# Coupled ensembles at 1/30th of the compute

<div class="cm-lead">Coupled CAMulator: 55–60 simulated years per day on 2 Derecho nodes + 1 H100, about 10× faster than CESM2 and 30× fewer core-hours. The energy saving is smaller (about 21×) because one GPU draws as much power as roughly 140 CPU cores.</div>

<CarbonCalc />

<!--
Here is the cost. Coupled to the CESM ocean and sea-ice models, the emulator runs 55 to 60 simulated years per wall-clock day without any optimisation, about ten times faster than CESM2, and it uses about thirty times fewer core-hours. The energy saving is smaller, about twenty-one times, because the GPU draws about 700 watts, the same as roughly 140 CPU cores at 5 watts each. Eighty percent of the remaining time is spent in the ocean and sea ice, so the atmosphere is no longer the bottleneck. The panel converts core-hours into energy and carbon for an ensemble the size of the CESM2 Large Ensemble. The energy and carbon numbers depend on assumptions about hardware power and the electricity grid, and those assumptions are the sliders, so the audience can change them.
-->

---
layout: section
---

# Where it breaks, and what we are doing about it

Coupling to a dynamical ocean · High-frequency variability and extremes · Low-frequency variability and drift · Rare events and differentiable models

<!--
The emulator reproduces the bulk of the climate. The research questions are at the edges: what happens when the emulator drives a real ocean, whether it keeps the extremes, whether slow drifts stay under control over decades, and what a differentiable model lets us do that a conventional one does not. Some of these already have fixes, which I will show. I will take each in turn.
-->

---

# Coupled El Niño needs a wind-stress fix

<div class="cm-cols">
<div>

<div class="cm-couple">
  <div class="box gpu">CAMulator<br /><small>atmosphere · 1 GPU</small></div>
  <div class="arrows"><span>→ winds, temperature, humidity, radiation, rain</span><span>← SST, sea-ice fraction, every 6 h</span></div>
  <div class="box">CESM coupler<br /><small>fluxes and regridding</small></div>
  <div class="arrows"><span>⇅ heat, fresh water, wind stress</span></div>
  <div class="box">POP2 ocean + CICE sea ice<br /><small>Derecho CPUs</small></div>
</div>

The emulator's surface winds over-react to tropical sea-surface temperature, so El Niño came out too weak. A fixed correction raises its strength from **0.97 to 1.20 K**, inside the CESM2 range (1.33 ± 0.14 K).

</div>
<div>

<video src="/camulator/coupled_sst_precip_2028.mp4" poster="/camulator/coupled_poster.jpg" class="cm-video" autoplay loop muted playsinline></video>

<div class="cm-src">Coupled run, 2028. Colour: SST anomaly; white: sea ice; cyan: precipitation. El Niño strength: standard deviation of Niño-3.4 SST; CESM2 Large Ensemble, 1981–2014. Yuanpu Li and Will Chapman.</div>

</div>
</div>

<!--
The first open question is coupling. CAMulator replaces the CESM atmosphere and talks to the real ocean and sea-ice models through the standard coupler. Every six hours the ocean sends sea-surface temperature and ice fraction, and the emulator returns near-surface winds, temperature, humidity, radiation and precipitation, from which the coupler computes the fluxes. The movie is the coupled system in the year 2028. The main difficulty so far is El Niño: the emulator's surface wind stress responds about 1.4 times too strongly to tropical SST, and the coupled El Niño was too weak. A fixed correction of the mean stress brings the Niño-3.4 variability to 1.20 kelvin, inside the CESM2 ensemble range.
-->


---

# The cold bias came from coupling, not learning

<div class="cm-cols">
<div>

<video src="/camulator/coupled_arctic_seaice_2028.mp4" class="cm-video" autoplay loop muted playsinline></video>

<div class="cm-src">Coupled run, 2028: sea-ice thickness, SST anomaly and precipitation over the Arctic.</div>

</div>
<div class="cm-right">

- The sea-ice model grows and melts ice from CAMulator's fluxes every 6 h.
- First coupled runs were too cold: the coupler was handed a temperature 0.6 K too low.
- A one-line fix: SST bias **−0.71 → +0.14 K**; September Arctic ice **8.8 → 6.5 million km²**.

</div>
</div>

<div class="cm-src">Diagnosis and fix: Yuanpu Li. Scores against CESM2, 37-year runs; SST over 60°S–60°N.</div>

<!--
Coupling also brings in sea ice. The CICE model grows and melts ice from the fluxes the emulator provides, and the movie shows the coupled Arctic over a year. The first coupled runs were too cold everywhere, and it was tempting to blame the emulator. Yuanpu found that the cause was in the plumbing: the temperature handed to the coupler was taken from the wrong level, 0.6 kelvin too cold, which removed 6 watts per square metre of sensible heat from the ocean. Fixing that one line moved the SST bias between 60 south and 60 north from minus 0.71 to plus 0.14 kelvin against CESM2, and September Arctic ice from 8.8 to 6.5 million square kilometres. Coupling an emulator is an interface problem as much as a learning problem.
-->

---

# Too-smooth small scales mute the extremes

<div class="cm-pair cm-pair-short">
  <img src="/camulator/ke_spectrum_ratio.png" alt="Ratio of CAMulator to CAM6 kinetic energy against total wavenumber" />
  <img src="/camulator/ar_rain_tail_a.png" alt="Distribution of peak precipitation in atmospheric rivers for CESM2 and CAMulator, log scale" />
</div>

- The same smoothing behind the forecast skill: kinetic energy at small scales is **about one third too low** (left).
- Atmospheric-river rain matches on average, but 6-h totals **above 25 mm are rarer** (right, red below blue) and the wettest point is 7 % low.

<div class="cm-src">Left: kinetic-energy ratio, CAMulator/CAM6, by wavenumber (small scales to the right). Right: peak rain under 10,000 North Pacific atmospheric rivers per run. Next: a spectral CRPS loss (Charlie Becker, Fabrizio Falasca).</div>

<!--
The second question is the high-frequency end. A squared-error loss pays the network to blur when it is uncertain about small features, and it does: on the left, the emulator's kinetic energy falls below CAM6's at small scales, about a third too low. This is the same effect that made the forecasts look better than CAM6 earlier. On the right, the consequence for extremes. Over 10,000 atmospheric rivers per run, the median rain is close, but the heaviest six-hour totals are rarer and the wettest point is 7 percent low. Integrated quantities are right and peaks are flattened. Charlie Becker is testing a probabilistic loss computed in spectral space, which penalises missing variance directly.
-->

---

# Slow drift hides in modes the loss barely sees

<div class="cm-cols cm-cols-wide">
<div>

<img src="/camulator/winter_bias.png" class="cm-fig-col" alt="Free-run bias maps of 500 hPa height and surface pressure for winter and summer" />

<div class="cm-src">Free-run bias, CAMulator minus CAM6. Top: mid-level pressure (500-hPa height); bottom: surface pressure. Left: winter; right: summer.</div>

</div>
<div>

<div class="cm-right">

- Over decades, a winter circulation bias builds over the Arctic and North Pacific.
- Two slow modes (43- and 13-day) hold **about half** of it, but only **0.021 %** of the training loss.
- It appears in forecasts too: half the bias builds within ten days.

</div>

</div>
</div>

<!--
The third question is the slow end. Run for decades, the emulator develops a winter bias over the Arctic and the North Pacific. We fit a linear model of the slow, large-scale circulation and find that two modes, with decay times of 43 and 13 days, hold about half of the winter bias. Those same two modes carry 0.021 percent of the training loss, one part in 4,700, so the loss gives the network almost no reason to get them right. The drift is visible in forecasts too: averaged over fifty winter starts, the circulation indices reach half of the free-run bias within ten days, so it is a tendency error present from the first step.
-->


---

# Fixing two slow modes removes the Arctic bias

<img src="/camulator/slow_mode_fix_top.png" class="cm-fig-wide cm-fig-big" alt="Arctic 500 hPa height bias without and with the two-mode offset, and bar charts of polar-cap pressure, height and stratospheric wind bias" />

- Subtract the two slow modes' estimated tendency error at every step; **no weights change**.
- Winter polar-cap surface pressure bias: **−5.5 → −0.6 hPa**. Persistence of Arctic pressure anomalies: 16.5 → 10.7 days (CAM6: 10.5).
- Day-5 forecast error changes by only 0.7 %.

<div class="cm-src">Ten-year runs with and without the offset; prescribed ocean. Persistence: e-folding time of the Northern Annular Mode. Next: the same term inside the training loss.</div>

<!--
If the slow modes hold the bias, a correction to those two modes alone should remove it. From the 35-year bias and the linear model we estimate the tendency error that would produce it, keep only the two slowest modes, and subtract that small push at every six-hour step. No network weights change. In ten-year runs the winter polar-cap pressure bias drops from minus 5.5 to minus 0.6 hectopascals, and the memory of the annular mode drops from 16.5 days to 10.7, against CAM6's 10.5, although persistence was never targeted. Forecast error at day five changes by less than one percent. The next step is to put this term into the training loss.
-->

---

# Strongest rivers: right strength, rain too low

<img src="/camulator/gray_swan.png" class="cm-fig-wide cm-fig-short" alt="Predicted against actual peak water-vapour transport for 120 CAM6 atmospheric rivers at 2- and 4-day lead" />

- At 2 days, the 30 strongest atmospheric rivers keep **98 %** of their peak water-vapour transport (95 % interval 96–101 %); persistence keeps 62–76 %.
- Peak 6-h rain is about **14 % low** at every rank: transport is large-scale, rain peaks are small-scale.

<div class="cm-src">120 CAM6 North Pacific atmospheric rivers, 1981–2014 (within the training period), ranked by peak transport; CAMulator started from the exact CAM6 state 2 or 4 days before the peak. Framing: Lin and Emanuel (2016); Sun et al. (2025).</div>

<!--
A common worry is that emulators trained with a squared error cannot produce the strongest events, so-called gray swans. We tested the in-distribution version of that. We ranked CAM6's own North Pacific atmospheric rivers by peak water-vapour transport and started the emulator from the exact CAM6 state two and four days before each peak. At two days the 30 strongest rivers keep 98 percent of their peak transport, the same fraction as median rivers, while persistence keeps 62 to 76 percent. The transport is right; the rain is not: peak six-hour rain is about 14 percent low at every rank, consistent with the smoothing on the previous slides. These events are from the training years; the out-of-distribution version, events stronger than any in training, is the open question.
-->

---

# Rare events and differentiable emulators

<div class="cm-cols">
<div>

<div class="cm-pair">
  <video src="/camulator/ar_ivt_cesm_2013-03-01.mp4" class="cm-video" autoplay loop muted playsinline></video>
  <video src="/camulator/ar_ivt_camulator_2013-03-01.mp4" class="cm-video" autoplay loop muted playsinline></video>
</div>

<div class="cm-src">Water-vapour transport and detected atmospheric rivers, March 2013. Left: CESM; right: CAMulator. Sean Heslin.</div>

Tracking follows about 9,700 rivers per run through genesis, growth and decay.

</div>
<div>

<div class="cm-right">

<div class="cm-placeholder">Kona-low figure</div>

- Kona lows are subtropical cyclones that bring heavy rain to Hawaiʻi; they are rare enough that large ensembles are needed to study them.
- A differentiable emulator gives the sensitivity of an event to the initial state in one backward pass (Vonich and Hakim 2024).

</div>

</div>
</div>

<!--
The last question is rare, high-impact events. Atmospheric rivers deliver most of the heavy precipitation on the US West Coast, and Sean Heslin built the tracking that compares them between the emulator and CESM. The tracking follows about 9,700 rivers per run through their life cycle, which shows that the emulator's rivers grow too slowly because the wind aloft is weak. Kona lows near Hawaii are rarer still, which is where cheap ensembles help. Because the emulator is differentiable, one backward pass gives the sensitivity of an event's intensity to the initial state, which lets us ask which features of the atmosphere made a given event stronger.
-->

---

# Takeaways

<div class="cm-takeaways">

- **It works for climate.** Decades-long stable runs, the warming trend and El Niño's remote effects, at about 1/30th of the compute when coupled to an ocean.
- **Its errors share a cause.** A squared-error loss smooths small scales, which mutes extremes, and barely sees slow modes, which drift.
- **Targeted fixes work.** A two-mode correction, a coupler fix and a wind-stress correction each remove a large bias. Next: build them into training.
- **The future is the hard test.** Forcings that rose together in training, such as CO₂ and ocean temperature, are hard to separate.

</div>

<!--
To summarise. An autoregressive emulator of the CESM atmosphere runs stably for decades, reproduces the forced trend and El Niño teleconnections, and cuts the cost of a coupled simulation by about thirty times. Its errors are not random: the squared-error loss blurs small scales, so extremes are muted, and gives almost no weight to slow modes, so the circulation drifts. Where we have found the cause, a small targeted fix removes most of the bias, and the next step is to put those fixes into the training itself. The hardest open problem is the future: when two forcings rose together in the training data, the emulator cannot tell them apart.
-->

---

# Thank you

<div class="cm-end">

Sean Heslin, Aiden Pape, Ona Melvin, Charlie Becker, Yuanpu Li, Eric Gosnell, Tate Voeller, and the NCAR MILES group.

- Model weights: [huggingface.co/willychap/camulator](https://huggingface.co/willychap/camulator)
- Slides: [willychap.github.io/slidev_talks](https://willychap.github.io/slidev_talks/)
- Contact: wchapman@colorado.edu

</div>

<!--
The model weights are public on Hugging Face. I am happy to take questions, and the students named here are the people to ask about their parts of the work.
-->
