---
theme: cu-boulder
title: "A neural-network atmosphere in a coupled climate model"
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
      - { label: Background, start: 2, end: 5 }
      - { label: The emulator, start: 6, end: 9 }
      - { label: Coupling, start: 10, end: 15 }
      - { label: Coupled climate, start: 16, end: 21 }
      - { label: Next, start: 22, end: 23 }
    hideOnCover: true
---

# A neural-network atmosphere in a coupled climate model

## CAMulator with the CESM ocean and sea ice

<img src="/camulator/globe.png" class="cm-cover-globe" alt="Globe rendered from a CAMulator simulation" />

<!--
Thank you for having me. This talk is about one project in my group: replacing the atmosphere of NCAR's climate model with a neural network and running it together with the model's physical ocean and sea ice. The question running through the talk is whether a network trained on one simulation can stand in for the atmosphere when a real ocean responds to it. I will show where the answer is yes, where it is not yet, and what we are changing as a result.
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
The coupled system was built by Yuanpu Li, a postdoc in the group, and most of the coupled results today are his runs or come from diagnosing them. The emulator is trained in CREDIT, the machine-learning framework of the NCAR MILES group, and the ocean and sea-ice models are the standard CESM components. The other students work on extremes, training losses and the cost of the models.
-->

---

# What a coupled climate model is

<div class="cm-cols">
<div>

<img src="/camulator/cesm_components.png" class="cm-fig-col" alt="Components of the Community Earth System Model connected through a coupler" />

<div class="cm-src">Components of CESM2, connected through the coupler.</div>

</div>
<div>

<div class="cm-right">

- The globe is divided into boxes about 100 km wide, stacked in layers.
- Separate programs for the atmosphere, ocean, land and sea ice step the physics forward and exchange heat, water and momentum through a coupler.
- One simulated year of CESM2 costs 3,750 core-hours; the atmosphere is the most expensive part.
- With CAMulator as the atmosphere, the coupled model runs 55–60 simulated years per day, about 10× faster than CESM2.

</div>

<div class="cm-src">CESM2 on NCAR's Derecho supercomputer, nominal 1° grid. Coupled CAMulator: 2 CPU nodes and 1 GPU.</div>

</div>
</div>

<!--
A climate model divides the globe into boxes, about a hundred kilometres across here, stacked in layers from the ocean floor to the upper atmosphere. Separate programs solve the physics of the atmosphere, the ocean, the land and the sea ice, each stepping forward in time. A component called the coupler passes heat, water and momentum between them. One simulated year of NCAR's model, CESM2, costs 3,750 core-hours, and climate questions need hundreds or thousands of simulated years. The atmosphere is the most expensive component, so we replace it with a neural network. With the emulator as the atmosphere, the coupled model runs 55 to 60 simulated years per day on two CPU nodes and one GPU, about ten times faster than CESM2. The rest of the talk is about whether that faster model gives the right climate.
-->

---

# The ocean is where climate variability lives

<div class="cm-cols">
<div>

<div class="cm-couple cm-couple-big">
  <div class="box">Trade winds weaken</div>
  <div class="arrows"><span>↓</span></div>
  <div class="box">Warm water spreads east across the Pacific</div>
  <div class="arrows"><span>↓</span></div>
  <div class="box">Rainfall and heating move east with it</div>
  <div class="arrows"><span>↺ winds weaken further: El Niño grows</span></div>
</div>

</div>
<div>

<div class="cm-right">

- The ocean stores most of the climate system's heat and changes slowly.
- El Niño, the largest year-to-year swing in climate, exists only because winds and ocean push on each other.
- It shifts rainfall and temperature around the world every few years.
- An atmosphere model that runs only over a prescribed ocean never has to get this loop right.

</div>

</div>
</div>

<!--
The ocean matters for two reasons. It holds most of the heat in the climate system and changes slowly, so it is the system's memory. And the largest year-to-year swing in climate, El Niño, is a conversation between the atmosphere and the ocean. When the trade winds over the Pacific weaken, warm water spreads east, rainfall and heating follow it, and the winds weaken further. Neither the atmosphere nor the ocean produces El Niño alone. So coupling is a real test of an atmosphere model, not a formality.
-->

---

# One model, many possible histories

<img src="/coupling/le_nino34_three.png" class="cm-fig-wide" alt="Tropical Pacific SST anomaly from 1981 to 2014 in three CESM2 runs that differ only in their initial state" />

Three CESM2 runs with identical physics and forcing, started from slightly different states, produce different El Niño histories.

<div class="cm-src">Red: El Niño (warm); blue: La Niña (cold). Tropical Pacific (Niño-3.4) SST anomaly, 3-month mean. The CESM2 Large Ensemble has 50 such runs over 1981–2014.</div>

<!--
One more idea is needed to read the results. Weather is chaotic, so the same climate model started from two almost identical states produces different histories. These are three runs of CESM2 with the same physics and the same greenhouse gases. Their El Niño events come in different years. The CESM2 Large Ensemble has fifty such runs. Their spread tells us how much any statistic varies by chance, and that is the yardstick for the emulator: we ask whether it falls inside the range of the physical model, not whether it matches any one history.
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
- It was trained on one CESM2 simulation, 1980 to 2012: about 48,000 six-hour samples.
- Ocean temperature, sea ice, sunlight and CO₂ are inputs; in training they come from that simulation.

</div>

<div class="cm-src">874 M parameters; 192 × 288 grid, 32 levels; 0.3 s per step on one GPU.</div>

</div>
</div>

<!--
CAMulator takes the state of the atmosphere, winds, temperature and moisture on thirty-two levels plus surface pressure, and predicts the state six hours later. The prediction becomes the next input, and the model is applied again, so a century is about 146,000 steps. It was trained on six-hourly output of one CESM2 run, about 48,000 samples from a single history. The ocean temperature, sea ice, sunlight and carbon dioxide are inputs. That design is what makes coupling possible: if the ocean is an input, a real ocean model can supply it.
-->

---

# Training for stability over long runs

<img src="/camulator/three_step_loss.png" class="cm-fig-train" alt="Three-step rollout: the network applied three times, with a squared error against CESM at each step" />

<img src="/camulator/conservation_blocks.png" class="cm-fig-train cm-fig-train-b" alt="Network output passed through post-blocks that enforce tracer positivity, dry-air mass, water and energy conservation" />

<div class="cm-src">Top: the loss sums the squared error over three consecutive six-hour steps. Bottom: final layers rescale the output so that global dry-air mass, water and energy are conserved; they are trained with the network.</div>

<!--
Two choices in training matter for climate. First, the loss is not computed on one step. The network makes three six-hour steps from its own output, and the error at each step is summed, so training sees the errors the network feeds itself. Second, the last layers enforce physics. Small blocks rescale the global dry-air mass, the water budget and the energy budget so that they balance, and the network is trained through them. Without these constraints, runs of more than a few years drift and eventually fail.
-->

---

# With a prescribed ocean, 35 years track CESM

<img src="/camulator/free_run_35yr.png" class="cm-fig-wide" alt="Annual global means 1980 to 2014 of five quantities for CAM6 and CAMulator" />

One continuous run of 51,100 steps from 1980. Annual means follow the physical model, including the warming trend. The layer near 20 km (b) drifts cold.

<div class="cm-src">Global annual means, 1980–2014: (a) near-surface temperature, (b) temperature near 20 km, (c) near 5 km, (d) total water vapour, (e) precipitation. Black: CESM atmosphere (CAM6).</div>

<!--
Before coupling, the emulator has to run for decades on its own. Here the ocean is read from the training simulation, and the emulator runs 51,100 steps from a single initial state. Surface temperature, mid-level temperature, water vapour and precipitation follow the physical atmosphere year by year, including the trend. One quantity is wrong: the layer near twenty kilometres cools steadily. In broad terms the stand-alone emulator is a usable atmosphere, which is the precondition for everything that follows.
-->

---

# The response to El Niño, ocean prescribed

<img src="/camulator/enso_teleconnections.png" class="cm-fig-wide" alt="Composite 500 hPa height and precipitation differences for warm minus cold tropical Pacific winters, CAM6 and CAMulator" />

Pattern correlation with the physical model: 0.95 for tropical rainfall and 0.82 for the North Pacific pressure pattern.

<div class="cm-src">Ten warmest minus ten coldest tropical Pacific winters of 34, ocean prescribed. Top: pressure pattern near 5 km. Bottom: precipitation. Left: CESM atmosphere. Right: CAMulator.</div>

<!--
With the ocean prescribed, we can ask whether the emulator responds to El Niño correctly. During warm Pacific winters tropical rainfall shifts east, and a chain of high and low pressure arches over the North Pacific and North America. The emulator reproduces the rainfall shift with a pattern correlation of 0.95 against the physical model and the pressure pattern with 0.82. So the emulator responds to the ocean in the right places. Whether it responds with the right strength is a question only a coupled run can answer.
-->

---
layout: section
---

# Coupling CAMulator to the ocean and sea ice

Can a network trained on one simulation stand in for the atmosphere when a real ocean responds to it?

<!--
That brings us to the main question. In training, the ocean was a fixed record. In the coupled system, the ocean reacts to whatever the emulator does, and the emulator then sees the ocean it helped create. The next part is how the two codes talk, what physics sits between them, and what went wrong the first time.
-->

---

# Fortran and Python exchange files

<div class="cm-cols">
<div>

<div class="cm-couple cm-couple-big">
  <div class="box gpu">CAMulator server (Python)<br /><small>atmosphere · 1 GPU</small></div>
  <div class="arrows"><span>→ near-surface wind, temperature, humidity, radiation, rain</span><span>← sea-surface temperature, sea-ice fraction</span></div>
  <div class="box">Data-atmosphere component (Fortran)<br /><small>reads and writes files, waits on a flag</small></div>
  <div class="arrows"><span>⇅ CESM coupler (Fortran)</span></div>
  <div class="box">Ocean + sea-ice models (Fortran)<br /><small>CPU nodes</small></div>
</div>

</div>
<div>

<div class="cm-right">

- CESM has a data atmosphere: a component that normally reads observed weather from files.
- We modified it to wait for a flag, read the emulator's file, and write the ocean state back.
- The Python server never calls Fortran, and CESM never imports PyTorch.
- Most of the wall-clock time is now spent in the ocean and sea-ice models.

</div>

</div>
</div>

<div class="cm-src">CESM2.1.5 with the POP2 ocean and CICE5 sea-ice models. Server and handshake: Yuanpu Li and Will Chapman.</div>

<!--
The two halves never share memory. CESM has a component called the data atmosphere, normally used to drive the ocean with observed weather read from files. We modified it so that every six model hours it writes the sea-surface temperature and ice fraction to a file, sets a flag, and waits. The Python server sees the flag, runs one emulator step on the GPU, writes the atmospheric fields to a file and sets its own flag. The Fortran side reads them and hands them to the coupler. This keeps the two code bases independent, and most of the wall-clock time is now spent in the Fortran ocean and sea ice rather than in the atmosphere.
-->

---

# The coupler computes the surface fluxes

<div class="cm-cols">
<div>

$$
\tau = \rho \, C_D \, |V| \, (u_{\text{air}} - u_{\text{ocean}})
$$

$$
H = \rho \, c_p \, C_H \, |V| \, (T_{\text{sea}} - \theta_{\text{air}})
$$

<div class="cm-src">The coupler's formulas for wind stress τ and heat flux H. From the emulator: air density ρ, wind speed |V|, wind u_air, air temperature θ_air. From the ocean: surface current and temperature.</div>

</div>
<div>

<div class="cm-right">

- The emulator also predicts its own surface fluxes, but over the ocean the coupler does not use them.
- The coupler recomputes stress, heat and evaporation from the emulator's air near the surface.
- So the emulator's near-surface state must be physically right, not only its flux outputs.

</div>

</div>
</div>

<!--
This is the main physical point of the coupling. The neural network predicts surface heat fluxes and wind stress, because the physical atmosphere had them in its output and the network was trained on everything. In the coupled system those predictions are never used over the ocean. The coupler takes the emulator's air temperature, humidity and wind at the lowest level, about sixty metres up, combines them with the ocean's surface temperature and currents, and computes the fluxes itself with these formulas. An emulator can have good flux outputs and still drive the ocean wrongly, if the air near the surface is wrong.
-->

---

# Stable coupled runs for decades

<div class="cm-cols">
<div>

<video src="/camulator/coupled_sst_precip_2028.mp4" poster="/camulator/coupled_poster.jpg" class="cm-video" autoplay loop muted playsinline></video>

<div class="cm-src">Coupled run, 2028. Colour: sea-surface temperature anomaly; white: sea ice; cyan: precipitation. Yuanpu Li and Will Chapman.</div>

</div>
<div>

<div class="cm-right">

- The coupled system has run from 1981 to 2040 without failing or drifting away.
- Ocean, sea ice and atmosphere exchange heat, water and momentum every six hours.
- No correction to the exchanged fluxes is applied in the main run.

</div>

</div>
</div>

<!--
The first result is that it runs. The coupled system has gone from 1981 to 2040 without blowing up, which was not guaranteed: an emulator trained over a prescribed ocean has never seen its own errors fed back through an ocean. The movie shows one year of the coupled run, with sea-surface temperature anomalies, sea ice in white and rain in cyan. El Niño events develop and decay, storms cross the oceans, and the ice edge moves with the seasons.
-->

---

# The first coupled runs failed at the interface

| Error in the exchange code | Energy error at the ocean surface |
|---|---:|
| Air temperature passed from the wrong level, 0.6 K too cold | −6 W m⁻² |
| Ocean reflectivity fixed instead of varying with the sun angle | about −3 W m⁻² |
| Winds interpolated twice through a coarser grid, 2.2 % too weak | −1.3 W m⁻² |

Fixing the first error moved the ocean from 0.71 K too cold to 0.14 K too warm, and September Arctic sea ice from 8.8 to 6.5 million km².

<div class="cm-src">For scale, the present energy imbalance of the climate system is about 1 W m⁻². Diagnosis: Yuanpu Li and Will Chapman, with a Python copy of the coupler's flux code checked against the coupler to 1 %.</div>

<!--
The first coupled runs were too cold everywhere, and the natural suspect was the neural network. It was not. Each of these errors sat in the code that passes fields between Python and Fortran: a temperature taken from the wrong level, a constant ocean reflectivity, and winds weakened by interpolating them twice. Each is comparable to or larger than the energy imbalance behind present-day warming. We found them by rebuilding the coupler's flux calculation in Python and checking it against the coupler's own output. Coupling an emulator is an interface problem as much as a learning problem.
-->

---

# Coupled sea ice in the Arctic

<div class="cm-cols">
<div>

<video src="/camulator/coupled_arctic_seaice_2028.mp4" class="cm-video" autoplay loop muted playsinline></video>

<div class="cm-src">Coupled run, 2028: sea-ice thickness, sea-surface temperature anomaly and precipitation over the Arctic.</div>

</div>
<div class="cm-right">

- The sea-ice model grows and melts ice from the fluxes the coupler computes from CAMulator's state.
- Ice thins in summer, opens along the coasts, and refreezes in autumn.
- Correcting the temperature hand-over moved September Arctic ice from 8.8 to 6.5 million km².

</div>
</div>

<!--
Sea ice is where the interface errors showed most clearly. The sea-ice model is fully physical and responds only to the fluxes the coupler computes from the emulator's state. The movie shows one year of the coupled Arctic: the ice thins through the summer, open water appears along the coasts, and the pack refreezes in autumn. Because the ice accumulates the energy balance over a whole season, small flux errors become large differences in ice. The temperature hand-over error alone added more than two million square kilometres of September ice.
-->

---
layout: section
---

# The coupled climate

Mean state and warming are close to CESM2; El Niño and the response to CO₂ are not yet.

<!--
With the interface fixed, here is what the coupled system does, compared each time with the range of the fifty physical runs.
-->

---

# Mean surface temperature of the coupled run

<img src="/coupling/coupled_t2m_bias.png" class="cm-fig-wide" alt="Map of near-surface temperature of the coupled run minus the mean of 30 CESM2 runs, 1981 to 2014" />

The global-mean difference is +0.12 K. Most of the ocean is within 1 K; the largest errors are over Antarctica and northern Asia.

<div class="cm-src">Near-surface air temperature, coupled CAMulator minus the mean of 30 CESM2 Large Ensemble runs, 1981–2014.</div>

<!--
With the interface corrected, the mean climate of the coupled run is close to the physical model's. This map is the near-surface temperature of the coupled run minus the average of thirty Large Ensemble runs. The global mean differs by 0.12 kelvin, and most of the ocean is within one kelvin. The largest errors are a cold Antarctica, a cold northern Asia and a warm North Pacific, and several of these are already present in the emulator with a prescribed ocean.
-->

---

# Warming follows the forcing

<img src="/coupling/t2m_forced_response.png" class="cm-fig-wide cm-fig-tall" alt="Four panels of near-surface temperature anomaly 1981 to 2040 for global, land, ocean and Arctic; coupled runs with full scenario, forcing held at 2014 and constant 1990 forcing, against CESM2 runs" />

With 1990 forcing the coupled system does not drift. Holding the forcing at 2014 stops the warming; the SSP2-4.5 scenario continues it past the training data.

<div class="cm-src">Temperature anomaly from 1981–1990: (a) global, (b) land, (c) ocean, (d) Arctic. Grey: 30 CESM2 runs, which follow a higher-emissions scenario (SSP3-7.0) after 2015.</div>

<!--
Three coupled runs differ only in their forcing, meaning greenhouse gases and the other external drivers. With the forcing held at 1990 values, the orange line, the system does not drift for sixty years, so the warming in the other runs is not a numerical drift. With the forcing held at 2014, the pink line, warming stops. With the SSP2-4.5 scenario, the blue line, warming continues past the end of the training data. The grey band follows a stronger scenario after 2015, so the comparison after that year is approximate.
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
- A fixed correction to the wind stress the ocean receives raises it to 1.20 K, inside their range.
- The correction is the same every year; it shows where the problem is but does not fix the emulator.

</div>

<div class="cm-src">Standard deviation of monthly Niño-3.4 SST anomalies, 1981–2014.</div>

</div>
</div>

<!--
The main failure is El Niño. In the coupled emulator the tropical Pacific varies about three quarters as much as in the physical model, 0.97 kelvin, below every one of the fifty Large Ensemble runs. A fixed monthly correction added to the wind stress the ocean receives brings it to 1.20 kelvin, inside the range. That tells us the problem is in the winds over the tropical Pacific. It does not fix the emulator, because the correction is the same every year whatever the atmosphere does.
-->

---

# The emulator's trade winds are too strong

<div class="cm-cols">
<div>

<img src="/coupling/wind_stress.png" class="cm-fig-col" alt="Stress change per wind change against mean easterly wind; ensemble members on a line, coupled runs further along it" />

</div>
<div>

<div class="cm-right">

- Mean easterly winds near the surface are 5.7 m s⁻¹ in the coupled emulator, against 4.9 m s⁻¹ in CESM.
- Stress grows with the square of the wind, so stronger mean winds make the stress respond more to each wind change.
- The CESM2 runs follow one line; the coupled runs sit on its extension.

</div>

<div class="cm-src">Central equatorial Pacific (5°S–5°N, 160°E–150°W), 1981–2014; ± 1 s.d. over years. Coupler stress formula applied offline to every six-hour state.</div>

</div>
</div>

<!--
To find out why, we ran the coupler's stress formula offline on every six-hour state of the emulator and of the physical model. The emulator's mean trade winds near the surface are too strong, 5.7 metres per second against 4.9. Because stress grows with the square of the wind, a stronger mean wind makes the stress respond more to each change in wind. The physical runs show the same relation among themselves, and the coupled runs sit further along it. The fix belongs in the emulator's winds, not in the stress formula.
-->

---

# The emulator uses CO₂ as a clock

<img src="/coupling/co2_maps_mjja.png" class="cm-fig-wide" alt="Maps of the six-hour land surface temperature change per CO2 doubling for CAM6, CAMulator and DCN6, May to August" />

In one training simulation CO₂ and temperature rise together, so a network can use CO₂ to tell the year. Raising only CO₂ warms land by 0.17 K in CESM, 0.12 K in CAMulator with the wrong pattern, and 0.69 K in a smaller emulator.

<div class="cm-src">First six hours after CO₂ alone is raised, May–August, per CO₂ doubling. Emulators: 16 held-out states; CESM atmosphere: 10 starts. DCN6: a 173 M-parameter emulator in development.</div>

<!--
The second problem comes from training on a single history. In the training simulation, carbon dioxide and temperature both rise from 1980 to 2012, so a network can learn that more carbon dioxide means a later, warmer year, without learning the radiative physics. We test this by raising carbon dioxide alone and looking at the first six hours. The physical model warms the land a little. CAMulator gets roughly the right average but the wrong pattern, with cooling over East Asia. A smaller emulator we are developing warms about four times too much everywhere. In a coupled run, that error would feed straight into the ocean.
-->

---

# Next: training targets from the physical model

<div class="cm-cols">
<div>

<div class="cm-couple cm-couple-big">
  <div class="box">CESM physics (Fortran)<br /><small>radiation code, coupler flux formulas</small></div>
  <div class="arrows"><span>↓ responses to CO₂, sea temperature and wind</span></div>
  <div class="box gpu">Training targets (PyTorch)<br /><small>a checked copy of the Fortran flux code</small></div>
  <div class="arrows"><span>↓ train CAMulator</span></div>
  <div class="box">Coupled test<br /><small>inside the range of 50 CESM2 runs?</small></div>
  <div class="arrows"><span>↺ coupled failures become new targets</span></div>
</div>

</div>
<div>

<div class="cm-right">

- Train with CO₂ varied on its own, with the expected response from the radiation code.
- Compute surface-flux targets with a PyTorch copy of the coupler's Fortran flux code.
- Add targets found in the coupled runs: the tropical winds and their response to the ocean.
- Accept a model only when its coupled climate falls inside the range of the 50 CESM2 runs.

</div>

</div>
</div>

<!--
Where the group is going follows from these results. The emulator learned the physical model's trajectory, not its responses, so we now train the responses directly. For carbon dioxide we vary it on its own during training and take the expected change from the radiation code. For the surface we use a PyTorch copy of the coupler's flux code, checked against the Fortran, so the emulator is trained on the same physics the ocean will feel. The coupled runs add their own targets, starting with the tropical winds. A model is accepted only when its coupled climate sits inside the range of the fifty physical runs.
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
To summarise: a neural-network atmosphere can drive the CESM ocean and sea ice for decades, with a mean climate close to the physical model and warming that follows the forcing beyond the training years. Most of the early failures were in the interface between Python and Fortran. The remaining ones, a weak El Niño and the response to carbon dioxide, come from responses the emulator learned from a single simulation, and the next round trains those responses against the physical model directly. I am happy to take questions.
-->

