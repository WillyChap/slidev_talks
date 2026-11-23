---
theme: cu-boulder
title: "Coupling a machine-learning atmosphere to an ocean"
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
      - { label: The emulator, start: 4, end: 6 }
      - { label: Coupling, start: 7, end: 12 }
      - { label: Coupled climate, start: 13, end: 16 }
      - { label: Next, start: 17, end: 19 }
    hideOnCover: true
---

# Coupling a machine-learning atmosphere to an ocean and sea ice

## CAMulator inside CESM: what works, what fails, and what comes next

<img src="/camulator/globe.png" class="cm-cover-globe" alt="Globe rendered from a CAMulator simulation" />

<!--
Thank you for having me. This talk is about one project in my group: replacing the atmosphere of the NCAR climate model with a neural network and running it together with the model's ocean and sea ice. I will show where that works, where it fails, and what we are changing so that the machine-learning model and the physical models agree. The audience spans several fields, so I will keep the machine-learning details short and spend the time on what happens when a neural network has to talk to forty-year-old Fortran.
-->

---

# Chapman Research Group, ATOC

<div class="cm-team">
  <div><img src="/camulator/team_li.jpg" alt="Yuanpu Li" /><b>Yuanpu Li</b><span>Postdoctoral scholar</span><em>Coupling to ocean and sea ice</em></div>
  <div><img src="/camulator/team_heslin.png" alt="Sean Heslin" /><b>Sean Heslin</b><span>Graduate student</span><em>Atmospheric rivers in emulators</em></div>
  <div><img src="/camulator/team_becker.jpg" alt="Charlie Becker" /><b>Charlie Becker</b><span>Graduate student; NCAR ML scientist</span><em>Training losses</em></div>
  <div><img src="/camulator/team_pape.png" alt="Aiden Pape" /><b>Aiden Pape</b><span>Graduate student</span></div>
  <div><img src="/camulator/team_melvin.png" alt="Ona Melvin" /><b>Ona Melvin</b><span>Graduate student</span></div>
  <div><img src="/camulator/team_gosnell.jpg" alt="Eric Gosnell" /><b>Eric Gosnell</b><span>CS master's student</span></div>
  <div><img src="/camulator/team_voeller.jpg" alt="Tate Voeller" /><b>Tate Voeller</b><span>Undergraduate student</span></div>
</div>

<div class="cm-src">The emulator is built on CREDIT, the NCAR MILES framework for machine-learning Earth system models.</div>

<!--
The coupled system was built by Yuanpu Li, a postdoc in the group, and most of the coupled results today are his runs or come from diagnosing them. The emulator is trained in CREDIT, the machine-learning framework of the NCAR MILES group, and the ocean and sea-ice models are the standard CESM components. The other students work on extremes, training losses and the cost of the models; I will point to their work where it connects to the coupled problem.
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

- CESM steps atmosphere, ocean, land and sea ice forward together, exchanging fluxes through a coupler.
- One simulated year of CESM2 costs 3,750 core-hours on Derecho.
- The CESM2 Large Ensemble, about 25,000 simulated years, would need about 94 million core-hours at that rate.
- The atmosphere is the most expensive component, so it is the one we emulate.

</div>

<div class="cm-src">Derecho, fully coupled, nominal 1° grid. Ensemble: Rodgers et al. (2021).</div>

</div>
</div>

<!--
Climate questions need many long simulations: centuries of model time, repeated across ensemble members to separate the forced signal from internal variability. CESM computes the atmosphere, ocean, land and ice on a global grid and lets them exchange heat, water and momentum through a component called the coupler. One simulated year of CESM2 costs 3,750 core-hours on NCAR's Derecho machine. A hundred-member ensemble over 250 years would cost around 94 million core-hours. The atmosphere dominates that cost, so the plan is to replace the atmosphere with a neural network and keep the physical ocean and sea ice.
-->

---

# CAMulator: a learned six-hour step

<div class="cm-cols">
<div>

<img src="/camulator/rollout_diagram.png" class="cm-fig-col" alt="The same network F applied repeatedly: x at t to x at t plus one to x at t plus two" />

</div>
<div>

<div class="cm-right">

- A neural network maps the global atmosphere now to the atmosphere six hours later.
- Feeding each prediction back in gives runs of any length.
- It was trained on one coupled CESM2 simulation, 1980 to 2012, on a 1° grid with 32 levels.
- One step takes about 0.3 s on one GPU.

</div>

<div class="cm-src">874 M parameters; ocean temperature, sea ice, sunlight and CO₂ enter as inputs.</div>

</div>
</div>

<!--
CAMulator takes the state of the atmosphere, winds, temperature and moisture on thirty-two levels plus surface pressure, and predicts the state six hours later. The prediction becomes the next input, and the model is applied again, so a century is about 146,000 steps. It was trained on six-hourly output of one coupled CESM2 run. The ocean temperature, sea ice, sunlight and carbon dioxide are inputs. That design is what makes coupling possible: if the ocean is an input, a real ocean model can supply it.
-->

---

# The emulator tracks CAM6 for 35 years

<img src="/camulator/free_run_35yr.png" class="cm-fig-wide" alt="Annual global means 1980 to 2014 of five quantities for CAM6 and CAMulator" />

One continuous run of 51,100 steps from 1980. Annual means follow CAM6, including the warming trend. The lower stratosphere (b) drifts cold.

<div class="cm-src">Annual global means, 1980–2014: (a) 2-m temperature, (b) 52-hPa temperature, (c) 525-hPa temperature, (d) column water, (e) precipitation.</div>

<!--
Before coupling, the emulator has to run for decades on its own without drifting. Here the ocean is prescribed from the training simulation, and the emulator runs 51,100 steps from a single initial state. Surface temperature, mid-tropospheric temperature, column water and precipitation follow CAM6, the physical atmosphere model, year by year. One quantity is wrong: the lower stratosphere cools steadily. In broad terms the stand-alone emulator is a usable atmosphere, which is the precondition for everything that follows.
-->

---

# El Niño teleconnections in winter

<img src="/camulator/enso_teleconnections.png" class="cm-fig-wide" alt="Composite 500 hPa height and precipitation differences for warm minus cold tropical Pacific winters, CAM6 and CAMulator" />

The pattern correlation with CAM6 is 0.95 for tropical rainfall and 0.82 for the North Pacific wave train.

<div class="cm-src">Ten warmest minus ten coldest tropical Pacific winters of 34. Top: 500-hPa height. Bottom: precipitation. Left: CAM6. Right: CAMulator.</div>

<!--
The atmosphere's response to the tropical Pacific matters most for coupling, because that is how El Niño reaches the rest of the world and how the atmosphere feeds back on the ocean. With both models given the same ocean, the emulator shifts tropical rainfall east during warm winters with a pattern correlation of 0.95 against CAM6, and reproduces the North Pacific wave train with 0.82. So the emulator responds to the ocean in the right places. Whether it responds with the right strength is a question only a coupled run can answer.
-->

---
layout: section
---

# Coupling CAMulator to the CESM ocean and sea ice

A Python neural network on a GPU exchanges data with Fortran ocean and sea-ice models on CPUs every six model hours.

<!--
The second part of the talk is the coupled system itself: how the two halves talk, what physics sits between them, and what went wrong the first time.
-->

---

# Fortran and Python exchange files

<div class="cm-cols">
<div>

<div class="cm-couple cm-couple-big">
  <div class="box gpu">CAMulator server (Python, PyTorch)<br /><small>atmosphere · 1 GPU</small></div>
  <div class="arrows"><span>→ lowest-level wind, temperature, humidity, pressure</span><span>→ radiation and precipitation</span><span>← SST and sea-ice fraction</span></div>
  <div class="box">Data-atmosphere component (Fortran)<br /><small>reads and writes netCDF files, waits on a flag</small></div>
  <div class="arrows"><span>⇅ CESM coupler (Fortran, MPI)</span></div>
  <div class="box">POP2 ocean + CICE sea ice (Fortran)<br /><small>Derecho CPUs</small></div>
</div>

</div>
<div>

<div class="cm-right">

- CESM treats the emulator as a data atmosphere: a component that normally reads observations from files.
- A modified data atmosphere waits for a flag, reads the emulator's file, and writes the ocean state back.
- The Python server never calls Fortran, and CESM never imports PyTorch.
- 55–60 simulated years per day on 2 Derecho nodes and 1 GPU, about 10× faster than CESM2.

</div>

</div>
</div>

<div class="cm-src">Handshake files every six model hours; CESM2.1.5 GIAF configuration with POP2 and CICE5 on the 1° ocean grid.</div>

<!--
The two halves never share memory. CESM has a component called the data atmosphere, normally used to drive the ocean with observed weather read from files. We modified it so that every six model hours it writes the current sea-surface temperature and ice fraction to a file, sets a flag, and waits. The Python server sees the flag, runs one emulator step on the GPU, writes the atmospheric fields to a file and sets its own flag. The Fortran side reads them and hands them to the coupler. This file handshake is slow by software standards, but it keeps the two code bases independent, and the whole system runs 55 to 60 simulated years per day.
-->

---

# The coupler computes the surface fluxes

<div class="cm-cols">
<div>

$$
\tau = \rho \, C_D(\text{stability}, |V|) \, |V| \, (u_{\text{air}} - u_{\text{ocean}})
$$

$$
H = \rho \, c_p \, C_H \, |V| \, (T_{\text{sea}} - \theta_{\text{air}})
$$

<div class="cm-src">Bulk formulas of the CESM coupler (Large and Yeager). τ: wind stress; H: sensible heat flux; ρ: air density; |V|: wind speed; C_D, C_H: exchange coefficients that depend on near-surface stability.</div>

</div>
<div>

<div class="cm-right">

- The network predicts its own surface fluxes, but over the ocean the coupler ignores them.
- The coupler recomputes stress, heat and evaporation from the lowest-level air the network predicts.
- So the network's state must be physically right, not only its flux outputs.
- Errors in near-surface wind or temperature reach the ocean directly.

</div>

</div>
</div>

<!--
This is the most important physical point of the talk. The neural network predicts surface heat fluxes and wind stress, because CAM6 had them in its output and the network was trained on everything. But in the coupled system those predictions are never used over the ocean. The coupler takes the network's air temperature, humidity and wind at the lowest model level, about sixty metres up, combines them with the ocean's surface temperature and currents, and computes the fluxes itself with these bulk formulas. A network can have good flux outputs and still drive the ocean wrongly, if its near-surface state is inconsistent with them.
-->

---

# Stable coupled runs for decades

<div class="cm-cols">
<div>

<video src="/camulator/coupled_sst_precip_2028.mp4" poster="/camulator/coupled_poster.jpg" class="cm-video" autoplay loop muted playsinline></video>

<div class="cm-src">Coupled run, 2028. Colour: SST anomaly; white: sea ice; cyan: precipitation. Yuanpu Li and Will Chapman.</div>

</div>
<div>

<div class="cm-right">

- The coupled system has run 1981 to 2040 without a crash or a runaway drift.
- Ocean, sea ice and atmosphere exchange heat, water and momentum every six hours.
- No flux adjustment is applied in the main run.

</div>

</div>
</div>

<!--
The first success is simply that it runs. The coupled system has gone from 1981 to 2040 without blowing up, which was not guaranteed: an emulator trained with a prescribed ocean has never seen its own errors fed back through an ocean. The movie shows one year of the coupled run, with sea-surface temperature anomalies, sea ice in white and rain in cyan. El Niño events develop and decay, storms track across the oceans, and the ice edge moves with the seasons. No correction to the fluxes is applied in the main run.
-->

---

# The first coupled runs failed at the interface

| What was wrong at the interface | Effect on the ocean |
|---|---:|
| Air temperature handed over from the wrong level, 0.6 K too cold | −6 W m⁻² sensible heat |
| Ocean albedo fixed instead of varying with the sun angle | about −3 W m⁻² sunlight |
| Winds interpolated twice through a coarser grid, 2.2 % too weak | −1.3 W m⁻² latent heat |

Each error was in the exchange code. Correcting the first one moved SST (60°S–60°N) from −0.71 to +0.14 K against CESM2.

<div class="cm-src">Diagnosis: Yuanpu Li and Will Chapman, from coupler restart files and an offline copy of the coupler's flux code checked to 1 %.</div>

<!--
The first coupled runs were too cold everywhere, and the natural suspect was the neural network. It was not. Each of these errors sat in the code that passes fields between Python and Fortran. Potential temperature was taken from the wrong level, the ocean albedo was a constant, and the winds were interpolated twice through a coarser grid, which shortens them. For comparison, the warming signal of the last century is a few watts per square metre, so each of these is large. We found them by rebuilding the coupler's flux calculation offline and checking it against the coupler's own output.
-->

---

# Coupled sea ice in the Arctic

<div class="cm-cols">
<div>

<video src="/camulator/coupled_arctic_seaice_2028.mp4" class="cm-video" autoplay loop muted playsinline></video>

<div class="cm-src">Coupled run, 2028: sea-ice thickness, SST anomaly and precipitation over the Arctic.</div>

</div>
<div class="cm-right">

- CICE grows and melts ice from the fluxes the coupler computes from CAMulator's state.
- Correcting the temperature hand-over moved September Arctic ice from 8.8 to 6.5 million km².
- Sea ice is where small flux errors become large state errors.

</div>
</div>

<div class="cm-src">Scores against CESM2, 37-year runs.</div>

<!--
Sea ice is the most sensitive part of the system to a small flux error, because ice responds to the energy balance accumulated over a season. With the cold hand-over the Arctic had 8.8 million square kilometres of ice in September; after the correction it had 6.5. The movie shows the coupled Arctic over a year, with ice thinning in summer and refreezing in autumn. Here the ice model is entirely physical, and it is reacting only to what the emulator and the coupler give it.
-->

---

# Mean surface temperature of the coupled run

<img src="/coupling/coupled_t2m_bias.png" class="cm-fig-wide" alt="Map of 2-m temperature of the coupled run minus the CESM2 Large Ensemble mean, 1981 to 2014" />

The global-mean bias is +0.12 K. Most of the ocean is within 1 K of the ensemble mean; the largest errors are over Antarctica and northern Asia.

<div class="cm-src">2-m temperature, coupled CAMulator minus the CESM2 Large Ensemble mean (30 members), 1981–2014. Dots: outside the member range.</div>

<!--
With the interface corrected, the mean climate of the coupled run is close to that of the full physical model. This map is the 2-metre temperature of the coupled run minus the mean of thirty members of the CESM2 Large Ensemble, the reference we compare against throughout. The global mean differs by 0.12 kelvin. Most of the ocean is within one kelvin. The largest errors are cold Antarctica, cold northern Asia and a warm North Pacific, and several of these are already present in the emulator with a prescribed ocean.
-->

---

# Forced warming in the coupled system

<img src="/coupling/t2m_forced_response.png" class="cm-fig-wide cm-fig-tall" alt="Four panels of 2-m temperature anomaly 1981 to 2040 for global, land, ocean and Arctic; coupled runs with full scenario, forcing held at 2014 and constant 1990 forcing, against the CESM2 Large Ensemble" />

With constant 1990 forcing the coupled system does not drift. Holding the forcing at 2014 stops the warming, and SSP2-4.5 continues it beyond the training years.

<div class="cm-src">2-m temperature anomaly from 1981–1990: (a) global, (b) land, (c) ocean, (d) Arctic. Grey: CESM2 Large Ensemble, 30 members (SSP3-7.0 after 2015).</div>

<!--
This is the test I find most convincing. Three coupled runs differ only in their forcing. With carbon dioxide and other forcings held at 1990 values, the orange line, the system does not drift for sixty years, so the warming in the other runs is not a numerical drift. With the forcing held at 2014, the pink line, warming stops. With the SSP2-4.5 scenario, the blue line, warming continues past the end of the training data at roughly the rate of the ensemble, which follows a stronger scenario after 2015. The coupled system responds to forcing, not to the calendar.
-->

---

# El Niño in the coupled system is too weak

<div class="cm-cols">
<div>

<img src="/coupling/enso_sd.png" class="cm-fig-col" alt="Nino-3.4 standard deviation of two coupled runs against 50 CESM2 Large Ensemble members" />

</div>
<div>

<div class="cm-right">

- The Niño-3.4 SST standard deviation is 0.97 K against 1.33 ± 0.14 K in the Large Ensemble.
- A fixed monthly correction of the tropical wind stress raises it to 1.20 K, inside the ensemble range.
- The correction is a patch: it does not respond to the state of the atmosphere.

</div>

<div class="cm-src">Monthly anomalies, 1981–2014. Grey band: 5–95 % of 50 members.</div>

</div>
</div>

<!--
The main failure is El Niño. In the coupled emulator the sea-surface temperature in the central Pacific varies about three quarters as much as in the physical model, 0.97 kelvin against 1.33 plus or minus 0.14 across fifty ensemble members. A fixed monthly correction added to the wind stress the ocean receives brings it to 1.20 kelvin, inside the ensemble. That tells us the defect is in the winds over the tropical Pacific. It does not fix the emulator, because the correction is the same every year whatever the atmosphere does.
-->

---

# The emulator's trade winds are too strong

<div class="cm-cols">
<div>

<img src="/coupling/wind_stress.png" class="cm-fig-col" alt="Stress change per wind change against mean easterly wind; ensemble members on a line, coupled runs further along it" />

</div>
<div>

<div class="cm-right">

- Mean near-surface easterlies are 5.7 m s⁻¹ in the coupled emulator against 4.9 m s⁻¹ in CAM6.
- Stress rises with the square of the wind, so stronger mean winds give a larger stress response.
- The ensemble members follow one line, and the coupled runs sit on its extension.
- The training target is the near-surface wind, not the stress.

</div>

<div class="cm-src">Central equatorial Pacific (5°S–5°N, 160°E–150°W), 1981–2014; ± 1 s.d. over years.</div>

</div>
</div>

<!--
To find out why, we ran the coupler's stress formula offline on every six-hour state of the emulator and of CAM6. The answer is simple. The emulator's mean trade winds near the surface are too strong, 5.7 metres per second against 4.9. Because stress grows with the square of the wind, a stronger mean wind makes the stress respond more to each change in wind, and the ocean feels a stronger push. The fifty-member ensemble shows the same relation among its own members. The fix belongs in the emulator's winds, which is a training target, not in the stress.
-->

---
layout: section
---

# Keeping the network consistent with the physics

The next training round takes its targets from the physical model's equations, not only from its output.

<!--
The last part is where the group is going. Everything so far points the same way: the coupled system is only as good as the physical consistency of the emulator's state.
-->

---

# The network uses CO₂ as a clock

<img src="/coupling/co2_ts_response_3col.png" class="cm-fig-wide" alt="Maps of the six-hour land surface temperature response to a CO2 increase for CAM6, CAMulator and a smaller convolutional emulator, in two seasons" />

In the training run CO₂ and temperature rise together, so a network can use CO₂ to tell the year. CAMulator overreacts in places, and a smaller, faster emulator (DCN6) overreacts everywhere.

<div class="cm-src">Land surface temperature change in the first six hours after a CO₂ increase, K per ln CO₂. Rows: Nov–Feb, May–Aug. DCN6: 173 M-parameter convolutional emulator.</div>

<!--
Here is the next problem, which we are working on now. In the training simulation, carbon dioxide and temperature both rise from 1980 to 2014, so a network can learn that more carbon dioxide means a later, warmer year, without learning the radiative physics. The maps show what each model does in the first six hours after carbon dioxide is raised. In CAM6 the land warms a little. CAMulator overreacts in places and has the wrong sign over East Asia in summer. A smaller emulator we are developing, DCN6, with five times fewer parameters, overreacts everywhere, about five times CAM6 averaged over land.
-->

---

# Next: targets from the physical model

<div class="cm-cols">
<div>

<div class="cm-couple cm-couple-big">
  <div class="box">CESM physics (Fortran)<br /><small>radiation code, coupler flux formulas</small></div>
  <div class="arrows"><span>↓ responses to CO₂, SST and wind, computed offline</span></div>
  <div class="box gpu">Training targets (PyTorch)<br /><small>a checked copy of the Fortran flux code</small></div>
  <div class="arrows"><span>↓ train CAMulator</span></div>
  <div class="box">Coupled test (CESM + CAMulator)<br /><small>inside the 50-member Large Ensemble?</small></div>
  <div class="arrows"><span>↺ coupled failures become new targets</span></div>
</div>

</div>
<div>

<div class="cm-right">

- Train on randomly perturbed CO₂, with targets from the radiation code, so CO₂ stops acting as a clock.
- Compute surface-flux targets with a PyTorch copy of the coupler's Fortran flux code, checked against the original.
- Add coupled targets: mean tropical winds and their response to SST.
- Accept a model only when its coupled climate falls inside the 50-member Large Ensemble.

</div>

</div>
</div>

<div class="cm-src">Perturbed-CO₂ training and the PyTorch flux code are in progress; the coupled acceptance test uses the CESM2 Large Ensemble, 1981–2014.</div>

<!--
The direction of the group is to make the emulator learn the physical model's responses, not only its trajectory. For carbon dioxide we perturb the input during training and take the target change from the radiation code. For the surface we use a PyTorch copy of the coupler's flux code, checked against the Fortran, so that the network is trained on the same physics the ocean will feel. The coupled diagnosis adds targets of its own, starting with the tropical winds. A model is accepted only when its coupled climate sits inside the fifty-member ensemble, with the sampling noise stated.
-->

---

# Thank you

<div class="cm-end">

Yuanpu Li, Sean Heslin, Charlie Becker, Aiden Pape, Ona Melvin, Eric Gosnell, Tate Voeller, and the NCAR MILES and CESM groups.

- Model weights: [huggingface.co/willychap/camulator](https://huggingface.co/willychap/camulator)
- Slides: [willychap.github.io/slidev_talks](https://willychap.github.io/slidev_talks/)
- Contact: wchapman@colorado.edu

</div>

<!--
To summarise: a neural-network atmosphere can drive the CESM ocean and sea ice for decades, with a mean climate close to the physical model and a forced warming that responds to the forcing rather than to the calendar. Most early failures were in the interface between Python and Fortran. The remaining ones, El Niño and the carbon dioxide response, come from physical inconsistencies in the network's state, and the next round trains against targets computed from the physical model's own equations. I am happy to take questions.
-->
