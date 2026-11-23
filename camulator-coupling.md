---
theme: cu-boulder
title: "Trained open-loop, run closed-loop"
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
      - { label: The emulator, start: 4, end: 5 }
      - { label: Coupling, start: 6, end: 9 }
      - { label: Results, start: 10, end: 13 }
      - { label: Next, start: 14, end: 15 }
    hideOnCover: true
---

# Trained open-loop, run closed-loop

## A neural-network atmosphere coupled to a physical ocean and sea ice

<img src="/camulator/globe.png" class="cm-cover-globe" alt="Globe rendered from a CAMulator simulation" />

<!--
Thank you for having me. This talk is about one project in my group: a neural network that replaces the atmosphere of NCAR's climate model, run together with the model's physical ocean and sea ice. The machine-learning question underneath it is what happens when a model trained on fixed inputs is placed inside a feedback loop with a physics code that consumes its outputs. I will show what works, what failed, and how we are changing the training as a result.
-->

---

# CAMulator driving the CESM ocean

<div class="cm-cols">
<div>

<video src="/camulator/coupled_sst_precip_2028.mp4" poster="/camulator/coupled_poster.jpg" class="cm-video" autoplay loop muted playsinline></video>

<div class="cm-src">Coupled run, 2028. Colour: sea-surface temperature anomaly; white: sea ice; cyan: precipitation. Yuanpu Li and Will Chapman.</div>

</div>
<div>

<div class="cm-right">

- The ocean and sea ice are the standard CESM models, written in Fortran.
- The atmosphere is CAMulator, a neural network trained on CESM output.
- This coupled run covers 1981 to 2040 with no flux correction.

</div>

</div>
</div>

<!--
This is one year of a coupled simulation. The ocean and sea-ice components are the standard physical models of the Community Earth System Model, CESM, written in Fortran. The atmosphere above them is not the physical atmosphere model. It is a neural network, CAMulator, that predicts the global atmosphere six hours ahead and is applied over and over. The ocean temperatures, sea ice and rainfall you see all come from the two systems responding to each other. The run has gone sixty years without a correction to the exchanged fluxes.
-->

---

# A coupled climate model is expensive to run

<div class="cm-cols">
<div>

<img src="/camulator/cesm_components.png" class="cm-fig-col" alt="Components of the Community Earth System Model connected through a coupler" />

<div class="cm-src">Components of CESM2, connected through the coupler.</div>

</div>
<div>

<div class="cm-right">

- One simulated year of CESM2 costs 3,750 CPU core-hours.
- Climate studies need ensembles of many 100-year runs to separate signal from internal noise.
- The atmosphere is the most expensive component, so it is the one we emulate.
- Coupled with CAMulator: 55–60 simulated years per day, about 10× faster than CESM2.

</div>

<div class="cm-src">Derecho supercomputer, nominal 1° grid. Coupled speed: 2 CPU nodes and 1 GPU.</div>

</div>
</div>

<!--
Climate models are expensive because the questions need many long runs. The climate in any one simulation is a mix of the response to forcing and internal noise, so studies run ensembles of tens to hundreds of century-long simulations. One simulated year of CESM2 costs 3,750 core-hours on NCAR's Derecho machine. The atmosphere is the most expensive component. Replacing it with a neural network and keeping the physical ocean gives 55 to 60 simulated years per day, about ten times faster than CESM2.
-->

---

# CAMulator: a learned six-hour step

<div class="cm-cols">
<div>

<img src="/camulator/rollout_diagram.png" class="cm-fig-col" alt="The same network F applied repeatedly: x at t to x at t plus one to x at t plus two" />

</div>
<div>

<div class="cm-right">

- The network maps the global atmosphere now to the atmosphere six hours later.
- Feeding each prediction back in gives runs of any length.
- Training data: one CESM2 simulation, 1980–2012; tests use later years.
- Ocean temperature, sea ice, sunlight and CO₂ are inputs, not predictions.

</div>

<div class="cm-src">874 M parameters; 192 × 288 grid (about 100 km), 32 vertical levels; 0.3 s per step on one GPU.</div>

</div>
</div>

<!--
CAMulator is an autoregressive model. The state is the global atmosphere on a grid of about 100 kilometres with 32 vertical levels: winds, temperature, humidity and surface pressure. The network predicts the state six hours ahead, and the prediction becomes the next input. It was trained on six-hourly output of one CESM2 simulation from 1980 to 2012. The important design choice for this talk is that the ocean surface temperature, sea ice, sunlight and carbon dioxide are inputs. In training they come from a file.
-->

---

# The emulator alone tracks CESM

<img src="/camulator/free_run_35yr.png" class="cm-fig-wide" alt="Annual global means 1980 to 2014 of five quantities for CAM6 and CAMulator" />

51,100 autoregressive steps without blow-up. Annual means follow the physics model, including the warming trend; one upper layer (b) drifts cold.

<div class="cm-src">Global annual means, 1980–2014: (a) near-surface temperature, (b) temperature at about 20 km, (c) at about 5 km, (d) total water vapour, (e) precipitation. Black: CESM atmosphere (CAM6).</div>

<!--
Before coupling, the emulator has to run for decades on its own. Here the ocean is read from the training simulation, and the network runs 51,100 steps from one initial state. Near-surface temperature, mid-level temperature, water vapour and precipitation follow the physical model year by year, including the warming trend. One quantity drifts: the layer near 20 kilometres cools steadily. With fixed ocean inputs the emulator is a usable atmosphere. The rest of the talk asks what changes when the ocean is no longer fixed.
-->

---

# Trained open-loop, run closed-loop

<div class="cm-cols">
<div>

<div class="cm-couple cm-couple-big">
  <div class="arrows"><span><b>Training</b></span></div>
  <div class="box">Ocean and sea ice from the CESM run (a file)</div>
  <div class="arrows"><span>↓ input</span></div>
  <div class="box gpu">CAMulator</div>
  <div class="arrows"><span>↓ loss against the CESM atmosphere, six hours later</span></div>
</div>

</div>
<div>

<div class="cm-couple cm-couple-big">
  <div class="arrows"><span><b>Coupled</b></span></div>
  <div class="box gpu">CAMulator</div>
  <div class="arrows"><span>↓ near-surface wind, temperature, humidity, radiation</span></div>
  <div class="box">Ocean and sea-ice models (Fortran)</div>
  <div class="arrows"><span>↺ new ocean state returned to CAMulator</span></div>
</div>

</div>
</div>

When coupled, the network's errors change its future inputs. Three questions follow: does the system stay stable, is the mean climate right, and does it respond correctly to the ocean and to CO₂?

<!--
This is the central point for a machine-learning audience. In training, the ocean is a fixed input read from the physical simulation, so the network never sees the consequences of its own errors on the ocean. In the coupled system the ocean responds to what the network predicts, and its new state comes back as the next input. That is a distribution shift with feedback. A small bias in the network can push the ocean somewhere the network was never trained, and the error can grow. The rest of the talk takes the three questions in turn.
-->

---

# Fortran and Python exchange files

<div class="cm-cols">
<div>

<div class="cm-couple cm-couple-big">
  <div class="box gpu">CAMulator server (Python, PyTorch)<br /><small>1 GPU</small></div>
  <div class="arrows"><span>→ near-surface state, radiation, precipitation</span><span>← sea-surface temperature, sea-ice fraction</span></div>
  <div class="box">Data-atmosphere component (Fortran)<br /><small>reads and writes netCDF files, waits on a flag</small></div>
  <div class="arrows"><span>⇅ CESM coupler (Fortran, MPI)</span></div>
  <div class="box">Ocean + sea-ice models (Fortran)<br /><small>CPU nodes</small></div>
</div>

</div>
<div>

<div class="cm-right">

- CESM has a "data atmosphere" component that normally reads observed weather from files.
- We modified it to wait for a flag, read the network's output file, and write the ocean state back.
- The two code bases stay independent: no Fortran–Python bindings.
- The exchange happens every six model hours.

</div>

</div>
</div>

<div class="cm-src">CESM2.1.5 with the POP2 ocean and CICE5 sea-ice models. Server and handshake: Yuanpu Li and Will Chapman.</div>

<!--
The two halves never share memory. CESM already has a component that drives the ocean with observed weather read from files, called the data atmosphere. We modified it so that every six model hours it writes the ocean surface temperature and ice fraction to a file, sets a flag, and waits. A Python server sees the flag, runs one network step on the GPU, writes its output and sets its own flag. The Fortran side reads the file and hands the fields to the coupler. Files are slow by software standards, but this keeps a large Fortran code base and a PyTorch model independent and easy to debug.
-->

---

# The network's flux predictions are not used

<div class="cm-cols">
<div>

$$
H = \rho \, c_p \, C_H \, |V| \, (T_{\text{sea}} - \theta_{\text{air}})
$$

<div class="cm-src">Heat flux from ocean to air, as the coupler computes it. From the network: air density ρ, wind speed |V|, air temperature θ. From the ocean model: sea-surface temperature. The exchange coefficient C_H depends on both.</div>

</div>
<div>

<div class="cm-right">

- The network also predicts surface heat fluxes and wind stress directly.
- Over the ocean, the coupler discards them and recomputes the fluxes from the predicted near-surface state.
- A loss on the flux outputs alone is not enough: the predicted state must be consistent with them.

</div>

</div>
</div>

<!--
The network was trained to predict every field the physical atmosphere wrote out, including the heat flux and wind stress at the surface. In the coupled system those predictions are thrown away over the ocean. The coupler takes the network's air temperature, humidity and wind at the lowest level, about sixty metres up, and the ocean's surface temperature, and computes the fluxes with formulas like this one. So the model is used at deployment through a different function from the one it was scored on in training. Accurate flux outputs do not help if the predicted state that produces them is inconsistent.
-->

---

# The first failures were integration bugs

| Error in the exchange code | Energy error at the ocean surface |
|---|---:|
| Air temperature passed from the wrong level, 0.6 K too cold | −6 W m⁻² |
| Ocean reflectivity held fixed instead of varying with sun angle | about −3 W m⁻² |
| Winds interpolated twice through a coarser grid, 2.2 % too weak | −1.3 W m⁻² |

Fixing the first error moved the ocean from 0.71 K too cold to 0.14 K too warm, and cut September Arctic sea ice from 8.8 to 6.5 million km². We found the errors by re-implementing the coupler's flux code in Python and comparing it with the coupler's own output, which agreed to 1 %.

<div class="cm-src">For scale, the present energy imbalance of the climate system is about 1 W m⁻². Ocean: 60°S–60°N mean against CESM2.</div>

<!--
The first coupled runs were too cold everywhere, and the obvious suspect was the network. It was not. Each of these errors sat in the code that passes fields between Python and Fortran: a temperature taken from the wrong level, a constant ocean reflectivity, and winds weakened by interpolating them twice. Each is comparable to or larger than the energy imbalance that drives present-day warming. We found them by writing a Python copy of the coupler's flux calculation and comparing it with the coupler's output field by field. In a hybrid system, the interface needs the same testing as the model.
-->

---

# Mean surface temperature of the coupled run

<img src="/coupling/coupled_t2m_bias.png" class="cm-fig-wide" alt="Map of near-surface temperature of the coupled run minus the mean of 30 CESM2 runs, 1981 to 2014" />

The global-mean difference is +0.12 K. Most of the ocean is within 1 K; the largest errors are over Antarctica and northern Asia.

<div class="cm-src">Near-surface air temperature, coupled CAMulator minus the mean of 30 CESM2 runs that differ only in their initial state, 1981–2014.</div>

<!--
With the interface corrected, the coupled system's mean climate is close to the physical model's. The reference is a set of thirty CESM2 simulations that differ only in tiny changes to their initial state, so their spread measures the internal noise of the climate system. This map is the coupled run minus their mean. The global mean differs by 0.12 kelvin, and most of the ocean is within one kelvin. The largest errors are over Antarctica, northern Asia and the North Pacific.
-->

---

# Out-of-sample forcing: warming follows CO₂

<img src="/coupling/t2m_forced_response.png" class="cm-fig-wide cm-fig-tall" alt="Four panels of near-surface temperature anomaly 1981 to 2040 for global, land, ocean and Arctic; coupled runs with full scenario, forcing held at 2014 and constant 1990 forcing, against CESM2 runs" />

With 1990 forcing held fixed the system does not drift. Holding the forcing at 2014 stops the warming; a moderate-emissions scenario continues it past the training years.

<div class="cm-src">Temperature anomaly from 1981–1990: (a) global, (b) land, (c) ocean, (d) Arctic. Grey: 30 CESM2 runs, which follow a higher-emissions scenario after 2015.</div>

<!--
This is the test I find most convincing, an ablation on the forcing. Three coupled runs differ only in greenhouse gases and the other external drivers. With those held at 1990 values, the orange line, the system does not drift for sixty years. With them held at 2014, the pink line, warming stops. With a moderate-emissions scenario, the blue line, warming continues past the end of the training data. The grey band follows a higher-emissions scenario after 2015, so the two are not directly comparable after that year.
-->

---

# El Niño in the coupled system is too weak

<div class="cm-cols">
<div>

<img src="/coupling/enso_hist.png" class="cm-fig-col" alt="Histogram of tropical Pacific SST variability across 50 CESM2 runs, with lines for the coupled run and the corrected run" />

</div>
<div>

<div class="cm-right">

- Tropical Pacific variability is 0.97 K, below all 50 CESM2 runs (1.33 ± 0.14 K).
- The emulator's trade winds are 16 % too strong: 5.7 against 4.9 m s⁻¹.
- A fixed correction to the wind stress the ocean receives raises the variability to 1.20 K.
- The correction is fixed in time; the winds themselves need correcting in training.

</div>

<div class="cm-src">El Niño: the year-to-year warming and cooling of the tropical Pacific. Standard deviation of monthly anomalies, Niño-3.4 region, 1981–2014.</div>

</div>
</div>

<!--
The main failure is El Niño, the irregular warming and cooling of the tropical Pacific every few years that shifts weather worldwide. Its size in the coupled emulator is 0.97 kelvin, below every one of fifty physical simulations. The emulator's mean trade winds over the Pacific are about sixteen percent too strong. A fixed monthly correction added to the wind stress the ocean receives brings the variability to 1.20 kelvin, inside the range. That correction is a patch: it is the same every year whatever the atmosphere does. The fix belongs in training.
-->

---

# Shortcut learning: CO₂ as a time stamp

<img src="/coupling/co2_maps_mjja.png" class="cm-fig-wide" alt="Maps of the six-hour land surface temperature change per CO2 doubling for CAM6, CAMulator and DCN6, May to August" />

In the training run CO₂ and temperature rise together. Raising only CO₂ gives land-mean warming of 0.17 K in the physics model, 0.12 K in CAMulator (with cooling over East Asia), and 0.69 K in a smaller emulator.

<div class="cm-src">First six hours after CO₂ is raised, May–August, ocean held fixed. Emulators: 16 held-out states; CESM atmosphere: 10 starts. DCN6: 173 M-parameter convolutional emulator.</div>

<!--
The next failure is a familiar one in machine learning. In the training simulation, carbon dioxide and temperature both rise from 1980 to 2012, so a network can use carbon dioxide as a time stamp: more carbon dioxide means a later and warmer year. We test this by changing only carbon dioxide and looking at the first six hours. The physical model warms the land a little. CAMulator gets the average roughly right but with the wrong pattern, including cooling over East Asia. A smaller emulator we are developing warms about four times too much everywhere. Both learned part of the correlation instead of the physics.
-->

---

# Next: train against the physics

<div class="cm-cols">
<div>

<div class="cm-couple cm-couple-big">
  <div class="box">CESM physics (Fortran)<br /><small>radiation code, coupler flux formulas</small></div>
  <div class="arrows"><span>↓ responses to CO₂, sea temperature and wind</span></div>
  <div class="box gpu">Training targets (PyTorch)<br /><small>a checked copy of the Fortran flux code</small></div>
  <div class="arrows"><span>↓ train CAMulator</span></div>
  <div class="box">Coupled test<br /><small>inside the spread of 50 CESM2 runs?</small></div>
  <div class="arrows"><span>↺ coupled failures become new targets</span></div>
</div>

</div>
<div>

<div class="cm-right">

- Perturbed-CO₂ training samples, labelled by the radiation code, to break the CO₂–time correlation.
- Sensitivity matching: the network's response to sea temperature and CO₂ is trained toward the physics response.
- A differentiable PyTorch copy of the coupler's flux code, so training scores the outputs the ocean will see.
- Acceptance: coupled statistics inside the spread of 50 CESM2 runs.

</div>

</div>
</div>

<div class="cm-src">Perturbed-CO₂ training and the PyTorch flux code are in progress.</div>

<!--
The direction of the group follows from these failures. To remove the carbon dioxide shortcut, we perturb carbon dioxide during training and take the correct response from the physical model's radiation code. More generally, we train the network's sensitivity to its inputs, not only its predictions, toward the physical model's sensitivity. For the surface, we use a differentiable copy of the coupler's flux code, checked against the Fortran, so the loss sees the same function the ocean does. A model is accepted only when its coupled statistics sit inside the spread of fifty physical simulations, which sets the noise floor.
-->

---

# Thank you

<div class="cm-team">
  <div><img src="/camulator/team_li.jpg" alt="Yuanpu Li" /><b>Yuanpu Li</b><span>Postdoctoral scholar</span><em>Coupling to ocean and sea ice</em></div>
  <div><img src="/camulator/team_heslin.png" alt="Sean Heslin" /><b>Sean Heslin</b><span>Graduate student</span></div>
  <div><img src="/camulator/team_becker.jpg" alt="Charlie Becker" /><b>Charlie Becker</b><span>Graduate student; NCAR</span></div>
  <div><img src="/camulator/team_pape.png" alt="Aiden Pape" /><b>Aiden Pape</b><span>Graduate student</span></div>
  <div><img src="/camulator/team_melvin.png" alt="Ona Melvin" /><b>Ona Melvin</b><span>Graduate student</span></div>
  <div><img src="/camulator/team_gosnell.jpg" alt="Eric Gosnell" /><b>Eric Gosnell</b><span>CS master's student</span></div>
  <div><img src="/camulator/team_voeller.jpg" alt="Tate Voeller" /><b>Tate Voeller</b><span>Undergraduate student</span></div>
</div>

<div class="cm-src">Built on CREDIT (NCAR MILES group). Weights: huggingface.co/willychap/camulator. Slides: willychap.github.io/slidev_talks. Contact: wchapman@colorado.edu</div>

<!--
To summarise: a neural-network atmosphere can drive a physical ocean and sea ice for decades, with a mean climate close to the physical model and warming that follows the forcing rather than the calendar. The first failures were in the interface. The remaining ones, a weak El Niño and a carbon dioxide shortcut, come from responses the network learned from correlations in a single training run. The next round trains those responses against the physics directly. The coupled system is Yuanpu Li's work, and the students here work on extremes, training losses and smaller emulators. I am happy to take questions.
-->

---

# Backup: trade winds and wind stress

<div class="cm-cols">
<div>

<img src="/coupling/wind_stress.png" class="cm-fig-col" alt="Stress change per wind change against mean easterly wind; CESM2 runs on a line, coupled runs further along it" />

</div>
<div>

<div class="cm-right">

- Stress grows with the square of the wind, so a stronger mean wind gives a larger stress change per wind change.
- The 30 CESM2 runs follow one line; the coupled runs sit on its extension.
- The excess comes from the mean wind, not from the stress formula.

</div>

<div class="cm-src">Central equatorial Pacific (5°S–5°N, 160°E–150°W), 1981–2014; ± 1 s.d. over years. Coupler stress formula run offline on every six-hour state.</div>

</div>
</div>

<!--
Backup for questions about the El Niño result. We ran the coupler's stress formula offline on every six-hour state of the emulator and of the physical model. The emulator's mean trade winds are stronger, and because stress grows with the square of the wind, the stress responds more to each change in wind. The thirty physical runs show the same relation among themselves, and the coupled emulator runs fall on its extension. So the stress formula is not the problem; the mean wind is.
-->

---

# Backup: El Niño teleconnections

<img src="/camulator/enso_teleconnections.png" class="cm-fig-wide" alt="Composite 500 hPa height and precipitation differences for warm minus cold tropical Pacific winters, CAM6 and CAMulator" />

Pattern correlation with the physics model: 0.95 for tropical rainfall, 0.82 for the North Pacific pressure pattern.

<div class="cm-src">Ten warmest minus ten coldest tropical Pacific winters of 34. Top: pressure pattern at about 5 km. Bottom: precipitation. Left: CESM atmosphere. Right: CAMulator.</div>

<!--
Backup for questions about whether the emulator responds to the ocean in the right places. With the ocean prescribed, the emulator shifts tropical rainfall during warm Pacific winters with a pattern correlation of 0.95 against the physical model, and reproduces the pressure pattern over the North Pacific with 0.82. The coupled problem is the strength of the response near the surface, not its location.
-->

---

# Backup: coupled sea ice in the Arctic

<div class="cm-cols">
<div>

<video src="/camulator/coupled_arctic_seaice_2028.mp4" class="cm-video" autoplay loop muted playsinline></video>

<div class="cm-src">Coupled run, 2028: sea-ice thickness, sea-surface temperature anomaly and precipitation over the Arctic.</div>

</div>
<div class="cm-right">

- The sea-ice model grows and melts ice from fluxes the coupler computes from CAMulator's state.
- Correcting the temperature hand-over cut September Arctic ice from 8.8 to 6.5 million km².

</div>
</div>

<!--
Backup for questions about sea ice. The sea-ice model is fully physical and responds only to the fluxes the coupler computes from the emulator's state. It integrates the energy balance over a season, so small flux errors become large differences in ice. The temperature hand-over error alone added more than two million square kilometres of September ice.
-->
