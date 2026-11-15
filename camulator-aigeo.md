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
      - { label: Motivation, start: 2, end: 3 }
      - { label: The emulator, start: 4, end: 7 }
      - { label: Performance, start: 8, end: 13 }
      - { label: Open questions, start: 14, end: 21 }
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

The Community Earth System Model (CESM) steps the atmosphere, ocean, land, sea ice and rivers forward together, with an atmospheric time step of 30 minutes.

- One simulated year of CESM2 costs 3,750 core-hours on Derecho; CESM3 costs 25,643.
- The CESM2 Large Ensemble has 100 members from 1850 to 2100, about 25,000 simulated years.
- At CESM2's cost that ensemble needs about 94 million core-hours.

</div>

<div class="cm-src">Costs: Derecho, fully coupled, nominal 1° grid. Ensemble: Rodgers et al. (2021).</div>

</div>
</div>

<!--
Climate projections need many long simulations: centuries of model time, repeated across ensemble members to separate the forced signal from internal variability. A coupled model such as CESM computes the atmosphere, ocean, land and ice on a global grid every half hour of model time. One simulated year of CESM2 costs 3,750 core-hours on NCAR's Derecho machine, and CESM3 costs about seven times more. The CESM2 Large Ensemble, one hundred members over 250 years, would cost around 94 million core-hours at that rate. The atmosphere is the most expensive component, so it is the component we emulate.
-->


---

# Autoregressive machine-learning models

A learned operator replaces the numerical solver for the equations of motion. The network takes the state vector $x_t$ and returns the next state, $x_{t+1} = F_\theta(x_t)$; applying the same network again gives $x_{t+2}$, and so on.

<img src="/camulator/rollout_diagram.png" class="cm-fig-rollout" alt="The same network F applied repeatedly: x at t to x at t plus one to x at t plus two" />

<div class="cm-src">Weather examples: GraphCast, Pangu-Weather, FourCastNet. Climate examples: ACE2, NeuralGCM, CAMulator.</div>

<!--
Before CAMulator itself, the general idea. A conventional model integrates the equations of motion with a numerical solver. An autoregressive machine-learning model keeps the same structure, a state vector advanced in time, but the step from one time to the next is a neural network trained on data. For multiple steps we feed the network its own prediction, so the same model is applied again and again. This is how the recent machine-learning weather models such as GraphCast work. Climate emulators such as ACE2, NeuralGCM and CAMulator use the same idea but have to stay stable for decades rather than days.
-->

---

# Advantages of autoregressive emulation

<div class="cm-cols">
<div>

- CAMulator steps the atmosphere forward six hours at a time; one step takes about 0.3 s on one GPU.
- Runs of any length and large ensembles become affordable.
- The network is differentiable end to end, so sensitivities come from one backward pass.
- The ocean, sea ice, sunlight and CO₂ enter as inputs, so the same network runs historical and scenario climates.

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

# Training data and network

Training data are one coupled CESM2.1.5 simulation, 1980 to 2048, saved every six hours on a 192 × 288 grid with 32 levels. Years 1980 to 2012 train the network; 2013 and 2014 validate it.

<img src="/camulator/architecture.png" class="cm-fig-wide" alt="CAMulator architecture: cross-embedding attention encoder, up-sampling decoder, conservation post-blocks" />

<div class="cm-src">874 M parameters: attention encoder at four scales and a U-Net-like decoder; 136 input and 147 output maps. Earth-aware padding wraps longitude and reflects across the poles.</div>

<!--
The training data come from one coupled CESM2 simulation from 1980 to 2048, with the SSP2-4.5 scenario after 2015, saved every six hours. The network sees 136 two-dimensional maps per step: winds, temperature and moisture on 32 levels, surface pressure, and the forcing fields. It predicts 147 maps, including precipitation and radiation. The encoder uses attention at four spatial scales and the decoder mirrors it, as in a U-Net. The loss is the mean squared error summed over three consecutive six-hour steps. Small blocks at the end rescale the output so that global mass, water and energy are conserved, and they are trained with the network.
-->

---

# Three-step rollout training with conservation

<img src="/camulator/three_step_loss.png" class="cm-fig-train" alt="Three-step rollout: the network applied three times, with a squared error against CESM at each step" />

<img src="/camulator/conservation_blocks.png" class="cm-fig-train cm-fig-train-b" alt="Network output passed through post-blocks that enforce tracer positivity, dry-air mass, water and energy conservation" />

<div class="cm-src">Top: the loss sums the squared error over three consecutive six-hour steps, and gradients pass back through all three. Bottom: post-blocks rescale the output so that global dry-air mass, water and energy are conserved; they are trained with the network.</div>

<!--
Two choices in training matter for climate. First, the loss is not computed on one step. The network makes three six-hour steps from its own output, and the squared error at each step is summed, so the gradient teaches it to correct errors it introduces itself. Second, the last layers are not free. Small differentiable blocks clip negative moisture and rescale the global dry-air mass, the water budget and the energy budget so that they balance, and the network is trained through them. Without these constraints, runs of more than a few years drift in mass and energy and eventually fail.
-->

---

# Weather skill against CAM6 itself

<div class="cm-cols">
<div>

<img src="/camulator/z500_skill.png" class="cm-fig-col" alt="Anomaly correlation of 500 hPa height against lead time for CAMulator and CAM6" />

</div>
<div>

<div class="cm-right">

- 233 forecasts started from CAM6 states, 2013 to 2014.
- The correlation of 500-hPa height with CAM6 falls to 0.6 at 8.9 days.
- CAM6 forecasting a perturbed copy of itself falls to 0.6 at 7.4 days.

</div>

<div class="cm-src">Orange: CAMulator. Black: CESM2 subseasonal reforecasts, perturbed against unperturbed members (Richter et al. 2022).</div>

</div>
</div>

<!--
First, weather. We start CAMulator from CAM6 states and score its forecasts against what CAM6 did next. The anomaly correlation of the 500-hectopascal height field drops to 0.6, a common threshold for useful skill, at 8.9 days. The black curves are CAM6 forecasting itself from slightly perturbed initial states, which removes model error entirely, and they reach 0.6 at 7.4 days. The emulator does better than the model forecasting itself because a squared-error loss trains it to predict something close to an ensemble mean, and a mean tracks any single trajectory better than another trajectory does.
-->


---

# A 35-year run from one initial state

<img src="/camulator/free_run_35yr.png" class="cm-fig-wide" alt="Annual global means 1980 to 2014 of five quantities for CAM6 and CAMulator" />

One continuous run of 51,100 six-hour steps from 1980, with the ocean prescribed. Annual means follow CAM6 year by year, including the warming trend. The lower stratosphere (b) drifts cold.

<div class="cm-src">Annual global means, 1980–2014: (a) 2-m temperature, (b) 52-hPa temperature, (c) 525-hPa temperature, (d) column water, (e) precipitation.</div>

<!--
For climate, the emulator has to run for decades without blowing up or drifting. This is one continuous run of 51,100 steps started from a single CAM6 state in 1980, with the observed-like ocean from the training simulation prescribed. Surface temperature, mid-tropospheric temperature, column water and precipitation follow CAM6 year by year, including the trend. One quantity is clearly wrong: the lower stratosphere cools steadily. That error is systematic rather than random, and errors of that kind turn out to be the hardest problem we work on.
-->

---

# El Niño teleconnections in winter

<img src="/camulator/enso_teleconnections.png" class="cm-fig-wide" alt="Composite 500 hPa height and precipitation differences for warm minus cold tropical Pacific winters, CAM6 and CAMulator" />

The pattern correlation with CAM6 is 0.95 for tropical rainfall and 0.82 for the North Pacific wave train.

<div class="cm-src">Ten warmest minus ten coldest tropical Pacific winters of 34. Top: 500-hPa height. Bottom: precipitation. Left: CAM6. Right: CAMulator.</div>

<!--
El Niño is the largest source of year-to-year variability, and its effect on weather far from the tropical Pacific is a standard test for any climate model. Both models see the same ocean, so we can compare the same winters directly. During El Niño, tropical rainfall shifts east, and a wave train of pressure anomalies arches over the North Pacific and North America. The emulator reproduces the rainfall shift with a pattern correlation of 0.95 and the wave train with 0.82. Nothing in the training asked for this response; it comes from learning the six-hour dynamics.
-->

---

# Mean bias beside other climate emulators

<div class="cm-cols">
<div>

<img src="/camulator/aimip_bias.png" class="cm-fig-col" alt="Bar chart of 2-m temperature time-mean bias for machine-learning climate emulators in AIMIP phase 1" />

</div>
<div>

<div class="cm-right">

- AIMIP Phase 1 scores emulators trained on reanalysis over 1979–2014.
- By the same metric, CAMulator's bias against its own training model is 0.40 K.
- Emulating a model is easier than emulating reanalysis, so this value is a reference point, not a rank.

</div>

<div class="cm-src">Area-weighted RMS of the time-mean 2-m temperature bias on a 1° grid. Henn et al. (2026), arXiv:2605.06944, Fig. 2a.</div>

</div>
</div>

<!--
The AI model intercomparison project, AIMIP, measures the time-mean surface temperature bias of several machine-learning climate emulators over 1979 to 2014. Their bars are five-member medians against the ERA5 reanalysis. Applying the same recipe to CAMulator against CAM6, the model it was trained on, gives 0.40 kelvin, and the two halves of our run give 0.39 and 0.43. Internal variability accounts for about 0.08 kelvin of that. The comparison is not like for like: a model is a cleaner target than the real atmosphere. It places our errors at the same order as the field's.
-->


---

# Out of sample: SSP2-4.5, 2016–2044

<div class="cm-cols">
<div>

<img src="/camulator/ssp245_out_of_sample.png" class="cm-fig-col" alt="Global 2-m temperature, precipitation and warming profiles for CAMulator and CAM6 under SSP2-4.5" />

</div>
<div>

<div class="cm-right">

- The emulator never saw these years.
- It warms 0.42 K per decade against CAM6's 0.35 K, with polar amplification in the right place.
- Global rainfall rises less than half as much as in CAM6.

</div>

<div class="cm-src">Dashed: runs with one forcing held fixed. Driven by the CAM6 scenario ocean and CO₂.</div>

</div>
</div>

<!--
The real test of an emulator for climate is a future it has not seen. CAM6 has a scenario run out to 2048, and CAMulator was never trained on it. Driven by the scenario's ocean and carbon dioxide, the emulator warms at 0.42 kelvin per decade against 0.35 for CAM6, with the right pattern of stronger warming at high latitudes. The rise in global rainfall is less than half of CAM6's. The dashed runs hold one forcing fixed and show that the response to carbon dioxide alone is too strong at the surface, because carbon dioxide and ocean temperature rose together in the training data.
-->


---

# Cost and energy of a coupled ensemble

<div class="cm-lead">Coupled CAMulator: 55–60 simulated years per day on 2 Derecho nodes + 1 H100, about 10× faster than CESM2 and 30× fewer core-hours.</div>

<CarbonCalc />

<!--
Here is the cost. Coupled to the CESM ocean and sea-ice models, the emulator runs 55 to 60 simulated years per wall-clock day without any optimisation, about ten times faster than CESM2, and it uses about thirty times fewer core-hours. Eighty percent of the remaining time is spent in the ocean and sea ice, so the atmosphere is no longer the bottleneck. The panel converts core-hours into energy and carbon for an ensemble the size of the CESM2 Large Ensemble. The energy and carbon numbers depend on assumptions about hardware power and the electricity grid, and those assumptions are the sliders, so the audience can change them.
-->

---
layout: section
---

# Questions we are working on

Coupling to a dynamical ocean · High-frequency variability and extremes · Low-frequency variability and drift · Rare events and differentiable models

<!--
The emulator reproduces the bulk of the climate. The research questions are at the edges: what happens when the emulator drives a real ocean, whether it keeps the extremes, whether slow drifts stay under control over decades, and what a differentiable model lets us do that a conventional one does not. I will take each in turn with one slide.
-->

---

# Coupling CAMulator to the CESM ocean

<div class="cm-cols">
<div>

<div class="cm-couple">
  <div class="box gpu">CAMulator<br /><small>atmosphere · 1 GPU</small></div>
  <div class="arrows"><span>→ winds, temperature, humidity, radiation, rain</span><span>← SST, sea-ice fraction, every 6 h</span></div>
  <div class="box">CESM coupler<br /><small>fluxes and regridding</small></div>
  <div class="arrows"><span>⇅ heat, fresh water, wind stress</span></div>
  <div class="box">POP2 ocean + CICE sea ice<br /><small>Derecho CPUs</small></div>
</div>

With a fixed tropical wind-stress correction, the Niño-3.4 SST standard deviation rises from 0.97 to 1.20 K (CESM2 Large Ensemble: 1.33 ± 0.14 K, 1981–2014).

</div>
<div>

<video src="/camulator/coupled_sst_precip_2028.mp4" poster="/camulator/coupled_poster.jpg" class="cm-video" autoplay loop muted playsinline></video>

<div class="cm-src">Coupled run, 2028. Colour: SST anomaly; white: sea ice; cyan: precipitation. Yuanpu Li and Will Chapman.</div>

</div>
</div>

<!--
The first open question is coupling. CAMulator replaces the CESM atmosphere and talks to the real ocean and sea-ice models through the standard coupler. Every six hours the ocean sends sea-surface temperature and ice fraction, and the emulator returns near-surface winds, temperature, humidity, radiation and precipitation, from which the coupler computes the fluxes. The movie is the coupled system in the year 2028. The main difficulty so far is El Niño: the emulator's surface wind stress responds about 1.4 times too strongly to tropical SST, and the coupled El Niño was too weak. A fixed correction of the mean stress brings the Niño-3.4 variability to 1.20 kelvin, inside the CESM2 ensemble range.
-->


---

# Coupled sea ice in the Arctic

<div class="cm-cols">
<div>

<video src="/camulator/coupled_arctic_seaice_2028.mp4" class="cm-video" autoplay loop muted playsinline></video>

<div class="cm-src">Coupled run, 2028: sea-ice thickness, SST anomaly and precipitation over the Arctic.</div>

</div>
<div class="cm-right">

- CICE grows and melts ice in response to CAMulator's surface fluxes, exchanged every six hours.
- The first coupled runs were too cold. The cause was in the coupling: the temperature passed to the coupler was 0.6 K low, removing 6 W m⁻² of sensible heat from the ocean.
- Fixing it moved SST (60°S–60°N) from −0.71 to +0.14 K against CESM2, and September Arctic ice from 8.8 to 6.5 million km².

</div>
</div>

<div class="cm-src">Diagnosis and fix: Yuanpu Li. Scores against CESM2, 37-year runs.</div>

<!--
Coupling also brings in sea ice. The CICE model grows and melts ice from the fluxes the emulator provides, and the movie shows the coupled Arctic over a year. The first coupled runs were too cold everywhere, and it was tempting to blame the emulator. Yuanpu found that the cause was in the plumbing: the temperature handed to the coupler was taken from the wrong level, 0.6 kelvin too cold, which removed 6 watts per square metre of sensible heat from the ocean. Fixing that one line removed the global cold bias and most of the excess September sea ice. Coupling an emulator is an interface problem as much as a learning problem.
-->

---

# High-frequency variability and extremes

<div class="cm-pair">
  <img src="/camulator/ke_spectrum_ratio.png" alt="Ratio of CAMulator to CAM6 kinetic energy against total wavenumber" />
  <img src="/camulator/ar_rain_tail.png" alt="Distributions of peak precipitation in atmospheric rivers for CESM2 and CAMulator" />
</div>

- The squared-error loss rewards smoothing: kinetic energy at small scales is about one third too low.
- Atmospheric-river rain matches CAM6 on average, but 6-h totals above 25 mm are rarer and the wettest point is 7 % low.

<div class="cm-src">Left: kinetic-energy ratio, CAMulator/CAM6, by wavenumber. Right: peak rain under 10,000 North Pacific ARs per run. Next: a spectral CRPS loss (Charlie Becker, Fabrizio Falasca).</div>

<!--
The second question is the high-frequency end. A squared-error loss pays the network to blur when it is uncertain about small features, and it does: on the left, the emulator's kinetic energy falls below CAM6's at small scales, about a third too low. On the right, the consequence for extremes. Over 10,000 atmospheric rivers per run, the median rain is close, but the heaviest six-hour totals are rarer and the wettest point is 7 percent low. Integrated quantities are right and peaks are flattened. Charlie Becker is testing a probabilistic loss computed in spectral space, which penalises missing variance directly.
-->

---

# Low-frequency variability and drift

<div class="cm-cols">
<div>

<img src="/camulator/winter_bias.png" class="cm-fig-col" alt="Free-run bias maps of 500 hPa height and surface pressure for winter and summer" />

<div class="cm-src">Free-run bias, CAMulator minus CAM6. Top: 500-hPa height; bottom: surface pressure. Left: winter; right: summer.</div>

</div>
<div>

<div class="cm-right">

- Over decades, a winter circulation bias builds over the Arctic and North Pacific.
- Two slow modes (43-day and 13-day) hold about half of it, but 0.021 % of the training loss.
- The same drift appears in forecasts: winter circulation indices reach half of the free-run bias within ten days.

</div>

</div>
</div>

<!--
The third question is the slow end. Run for decades, the emulator develops a winter bias over the Arctic and the North Pacific. We fit a linear model of the slow, large-scale circulation and find that two modes, with decay times of 43 and 13 days, hold about half of the winter bias. Those same two modes carry 0.021 percent of the training loss, one part in 4,700, so the loss gives the network almost no reason to get them right. The drift is visible in forecasts too: averaged over fifty winter starts, the circulation indices reach half of the free-run bias within ten days, so it is a tendency error present from the first step.
-->


---

# A two-mode correction removes the Arctic bias

<div class="cm-cols cm-cols-wide">
<div>

<img src="/camulator/slow_mode_fix.png" class="cm-fig-col" alt="Arctic 500 hPa height bias without and with the two-mode offset, zonal-mean wind bias, and annular-mode autocorrelation" />

</div>
<div class="cm-right">

- The tendency error of the two slowest modes is estimated from the 35-year bias and subtracted at every step; no weights change.
- Winter polar-cap surface pressure bias: −5.5 → −0.6 hPa.
- Annular-mode memory: 16.5 → 10.7 days (CAM6: 10.5).
- Day-5 forecast error changes by 0.7 %.

</div>
</div>

<div class="cm-src">Ten-year runs with and without the offset; prescribed ocean. Next: the same term inside the training loss.</div>

<!--
If the slow modes hold the bias, a correction to those two modes alone should remove it. From the 35-year bias and the linear model we estimate the tendency error that would produce it, keep only the two slowest modes, and subtract that small push at every six-hour step. No network weights change. In ten-year runs the winter polar-cap pressure bias drops from minus 5.5 to minus 0.6 hectopascals, and the memory of the annular mode drops from 16.5 days to 10.7, against CAM6's 10.5, although persistence was never targeted. Forecast error at day five changes by less than one percent. The next step is to put this term into the training loss.
-->

---

# Hindcasts of the strongest atmospheric rivers

<img src="/camulator/gray_swan.png" class="cm-fig-wide cm-fig-short" alt="Predicted against actual peak water-vapour transport for 120 CAM6 atmospheric rivers at 2- and 4-day lead" />

- At 2 days the 30 strongest rivers keep 98 % of their peak water-vapour transport (95 % interval 96–101 %); persistence keeps 62–76 %.
- Peak 6-h rain is about 14 % low at every rank.

<div class="cm-src">120 CAM6 North Pacific ARs, 1981–2014, ranked by peak IVT; CAMulator started from the exact CAM6 state 2 or 4 days before the peak. Framing: Lin and Emanuel (2016); Sun et al. (2025).</div>

<!--
A common worry is that emulators trained with a squared error cannot produce the strongest events, so-called gray swans. We tested the in-distribution version of that. We ranked CAM6's own North Pacific atmospheric rivers by peak water-vapour transport and started the emulator from the exact CAM6 state two and four days before each peak. At two days the 30 strongest rivers keep 98 percent of their peak transport, the same fraction as median rivers, while persistence keeps 62 to 76 percent. The transport is right; the rain is not: peak six-hour rain is about 14 percent low at every rank, consistent with the smoothing on the previous slides.
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

# Thank you

<div class="cm-end">

Sean Heslin, Aiden Pape, Ona Melvin, Charlie Becker, Yuanpu Li, Eric Gosnell, Tate Voeller, and the NCAR MILES group.

- Model weights: [huggingface.co/willychap/camulator](https://huggingface.co/willychap/camulator)
- Slides: [willychap.github.io/slidev_talks](https://willychap.github.io/slidev_talks/)
- Contact: wchapman@colorado.edu

</div>

<!--
To summarise: an autoregressive emulator of the CESM atmosphere runs stably for decades, reproduces the forced trend and El Niño teleconnections, and cuts the cost of a coupled simulation by about thirty times. The open problems are the coupled tropical response, smoothed extremes, and slow drifts that the training loss barely sees. The model weights are public on Hugging Face. I am happy to take questions, and the students named here are the people to ask about their parts of the work.
-->
