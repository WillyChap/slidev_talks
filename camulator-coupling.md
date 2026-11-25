---
theme: cu-boulder
title: "An ML atmosphere in a coupled climate model"
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
      - { label: Motivation, start: 2, end: 7 }
      - { label: The emulator, start: 8, end: 10 }
      - { label: Coupling, start: 11, end: 16 }
      - { label: Coupled climate, start: 17, end: 22 }
      - { label: Next, start: 23, end: 24 }
    hideOnCover: true
---

# An ML atmosphere in a coupled climate model

## 'CAMulator' coupled to the CESM ocean and sea ice

<!--
Thank you for having me. This talk is about one project in my group: replacing the atmosphere of NCAR's climate model with a neural network and running it together with the model's physical ocean and sea ice. The question running through the talk is whether a network trained on one simulation can stand in for the atmosphere when a real ocean responds to it. I will show where the answer is yes, where it is not yet, and what we are changing as a result.
-->

---

# Chapman Research Group, Atmospheric and Oceanic Sciences

<div class="cm-team">
  <div><img src="/camulator/team_li.jpg" alt="Yuanpu Li" /><b>Yuanpu Li</b><span>Postdoctoral scholar</span><em>Coupling to ocean and sea ice</em></div>
  <div><img src="/camulator/team_heslin.png" alt="Sean Heslin" /><b>Sean Heslin</b><span>Graduate student</span><em>Atmospheric river representation and genesis in emulators</em></div>
  <div><img src="/camulator/team_becker.jpg" alt="Charlie Becker" /><b>Charlie Becker</b><span>Graduate student; NCAR ML scientist</span><em>Training losses; stochastics; high-frequency information </em></div>
  <div><img src="/camulator/team_pape.png" alt="Aiden Pape" /><b>Aiden Pape</b><span>Graduate student</span><em>structural error discovery in differentiable models </em></div>
  <div><img src="/camulator/team_melvin.png" alt="Ona Melvin" /><b>Ona Melvin</b><span>Graduate student</span><em>Kona Low <-> Atmospheric River connection </em></div>
  <div><img src="/camulator/team_gosnell.jpg" alt="Eric Gosnell" /><b>Eric Gosnell</b><span>CS master's student</span><em>Sattelite Snow Retrieval </em></div>
  <div><img src="/camulator/team_voeller.jpg" alt="Tate Voeller" /><b>Tate Voeller</b><span>Undergraduate student</span><em>Sea-ice Representation in Coupled Emulation </em></div>
</div>

<!--
The coupled system was built by Yuanpu Li, a postdoc in the group, and most of the coupled results today are his runs or come from diagnosing them. The emulator is trained in CREDIT, the machine-learning framework of the NCAR MILES group, and the ocean and sea-ice models are the standard CESM components. The other students work on extremes, training losses and the cost of the models.
-->

---

# ML weather models now 'match' physics models

<div class="cm-cols cm-wx">
<div>

<img src="/coupling/wb2_z500.png" class="cm-fig-col" alt="500-hPa height error against lead time for IFS HRES, the IFS ensemble mean and four machine-learning weather models, 2020" />

</div>
<div>

<div class="cm-right">

- At day 5, GraphCast's 500-hPa height error is 28 m and GenCast's ensemble mean 27 m, against 31 m for ECMWF's high-resolution forecast.
- ECMWF has run a machine-learning model (AIFS) operationally since 2025.
- A 10-day global forecast takes about a minute on one gpu
- AI models will be part of weather forecasting in some way, shape, or form

</div>

<div class="cm-src">Global root-mean-square error against ERA5, 2020, 1.5° grid. Data: WeatherBench 2 (Rasp et al. 2024).</div>

</div>
</div>

<!--
Weather is where machine learning has already arrived. This is the WeatherBench 2 comparison, the community benchmark: the error of the 500-hectopascal height, the standard measure of the large-scale weather pattern, as a function of forecast lead time. The black line is ECMWF's flagship physics forecast. The coloured lines are machine-learning models trained on reanalysis. They match or beat it at every lead time, and an ensemble model, GenCast, matches ECMWF's physics ensemble. ECMWF now runs its own machine-learning model operationally. These models will be part of weather forecasting from here on.
-->

---

# <span class="cm-tswap"><b v-click.hide="1">How a coupled climate model works</b><b v-click="1">Swap the atmosphere for a neural network</b></span>

<div class="cm-cols">
<div>

<div class="cm-swap">
<img src="/camulator/cesm_components.png" alt="Components of the Community Earth System Model connected through a coupler" />
<div class="erase" v-click="1"></div>
<div class="camu" v-click="1"><b>CAMulator</b><span>neural network, 1 GPU</span></div>
</div>

<div class="cm-src">Community Earth System Model, version 3 (CESM3).</div>

</div>
<div>

<div class="cm-right">

<div class="cm-stack">
<div v-click.hide="1">

- **Represent Earth on a grid.** Physical equations evolve the atmosphere, ocean, land and sea ice through time, at roughly 100 km resolution here.
- **Connect the components.** They exchange heat, water and momentum: winds drive ocean currents, while ocean temperatures affect the atmosphere.

</div>
<div v-click="1">

- **Learn the atmosphere.** A neural network trained on CESM output replaces the atmosphere's equations and steps it forward six hours at a time on one GPU.
- **Keep the same connections.** It still exchanges heat, water and momentum with the physical ocean, land and sea ice through the coupler.

</div>
</div>

- **Let climate emerge.** Repeated interactions produce weather, variability and the response to changing greenhouse gases.

<div class="cm-grid">
<GridGlobe />
<div class="cap"><span v-click.hide="1">Each cell holds the state in a column of stacked levels.</span><span v-click="1">CAMulator works on the physical atmosphere's grid: 192 × 288 cells, 32 levels.</span></div>
</div>

</div>

</div>
</div>

---

# Cost and energy of a coupled ensemble

<div class="cm-cost">

<div class="cm-lead">Per simulated year: CESM2 uses 3,750 core-hours; coupled CAMulator uses 122 core-hours and 0.4 GPU-hours, about 30× fewer core-hours.</div>

<CarbonCalc />

<div class="cm-src">Defaults: Derecho CPU node (2 × AMD EPYC 7763) ≈ 6 W per core under load (estimate); H100 GPU 700 W; NWSC data-centre overhead 1.13 (CISL annual report FY2025); grid 0.47 kg CO₂e kWh⁻¹ (EPA eGRID 2023, RMPA subregion).</div>

</div>

<!--
Here is what the speed buys. Coupled to the CESM ocean and sea-ice models, the emulator runs 55 to 60 simulated years per day without any optimisation, about ten times faster than CESM2, and it uses about thirty times fewer core-hours. Most of the remaining time is spent in the ocean and sea ice, so the atmosphere is no longer the expensive part. The panel converts core-hours into energy and carbon for an ensemble the size of the CESM2 Large Ensemble. The defaults are Derecho's: about 6 watts per CPU core under load, the measured data-centre overhead of 1.13 at the Wyoming centre, and the regional grid's 0.47 kilograms of CO₂ per kilowatt-hour. Each is a slider, because each is an assumption.
-->

---

# What a climate model is and needs to do

<div class="cm-cap">
  <div class="card"><div class="yr">1960s</div><b>Warm by the right amount when CO₂ rises</b><span>climate sensitivity, set mostly by clouds</span><div class="chip part">ML: warms with CO₂, reason not yet shown</div></div>
  <div class="card"><div class="yr">1970s–90s</div><b>Exchange heat with a dynamic ocean</b><span>how fast warming happens; El Niño</span><div class="chip part">ML: this talk</div></div>
  <div class="card"><div class="yr">1990s</div><b>Account for warming that aerosols mask</b><span>a cooling forcing that acts through clouds</span><div class="chip no">ML: aerosols usually not an input</div></div>
  <div class="card"><div class="yr">2000s</div><b>Take up carbon on land and in the ocean</b><span>how much emitted CO₂ stays in the air</span><div class="chip no">ML: not included</div></div>
</div>
<div class="cm-cap-arrow"><div class="bar"></div><svg viewBox="0 0 14 14"><polygon points="0,0 14,7 0,14"/></svg></div>
<div class="cm-cap-lab">about 50 years of physical model development</div>

None of these can be learned from observations of the future; each had to be built in.

<div class="cm-src">Framing after T. Schneider. Manabe & Wetherald (1967); Manabe & Bryan (1969); Charney et al. (1979); Mitchell et al. (1995); Cox et al. (2000).</div>
<!--
What does a climate model need to be able to do, and how long did it take physical models to get there? This framing follows Tapio Schneider. In the 1960s, Manabe's radiative models first warmed by about the right amount when carbon dioxide rose. From the 1970s to the 1990s, models were coupled to dynamic oceans, which set how fast warming happens and produce El Niño. In the 1990s they learned that aerosols mask part of the greenhouse warming. Around 2000 they began to take up carbon on land and in the ocean. None of this could be learned from observations of the future; each piece was built in, over about fifty years. Machine-learning emulators warm with carbon dioxide but have not shown it is for the right reason, coupling to an ocean is this talk, and the last two are not there yet.
-->
---

# Where ML climate emulation stands

<div class="cm-cols">
<div>

<div class="cm-couple cm-couple-big cm-ladder">
  <div class="box gpu">Shown<br /><small>run stably for decades and follow a forced historical trajectory</small></div>
  <div class="arrows"><span>CAMulator (Chapman et al. 2025), ACE2 (Watt-Meyer et al. 2025)</span></div>
  <div class="box" v-click="1">Open<br /><small>whether they respond to CO₂ and the ocean through the right mechanisms</small></div>
  <div class="arrows" v-click="1"><span>in one training run, CO₂ and sea temperature rise together</span></div>
</div>

</div>
<div>

<div class="cm-unc">
  <div class="hd" v-click="2">Possible uses, by how uncertain they are</div>
  <div class="row" v-click="2"><span>Large ensembles within a trained scenario</span><div class="u" style="width: 22%"></div></div>
  <div class="row" v-click="3"><span>Long coupled runs, such as ocean spin-up</span><div class="u" style="width: 55%"></div></div>
  <div class="row" v-click="4"><span>New scenarios outside the training runs</span><div class="u" style="width: 100%"></div></div>
  <div class="ax" v-click="2"><span>smaller</span><span>uncertainty</span><span>larger</span></div>
  <div class="side" v-click="5"><b>Another significant purpose of clmate models is mechanistic discovery.</b> Learning something about the Earth system from a fast, differentiable model.</div>
</div>

</div>
</div>

<div class="cm-unc-end" v-click="6">

The field has a long way to go before climate emulation is where weather emulation is.

</div>

<div class="cm-src cm-unc-end" v-click="1">ACE2 reports that holding CO₂ fixed loses much of the near-surface warming trend (Watt-Meyer et al. 2025).</div>

<!--
So where does machine-learning climate emulation stand? Our emulator and others such as AI2's ACE2 can run for decades and follow the forced historical trajectory of the model they were trained on. [click] What is not shown is that they get there for the right reasons. In a single training simulation, carbon dioxide and ocean temperature rise together, so a network can lean on either one. [click] That makes some uses far more certain than others. Large ensembles within a scenario the model was trained on are the safest. [click] Long coupled runs, such as spinning up an ocean, are less certain. [click] New scenarios outside the training runs are much less certain still. [click] Alongside these there is a side quest: a fast, differentiable model may teach us something about the Earth system itself. [click] The field has a long way to go before climate is where weather is. The rest of the talk is one test of that: coupling the emulator to a physical ocean.
-->

---

# CAMulator ($F\theta$) - UNET crossformer

<img src="/camulator/rollout_diagram.png" class="cm-roll" alt="The same network F applied repeatedly: x at t to x at t plus one to x at t plus two" />

<div class="cm-stats">
  <div><span class="big">6 h</span><b>per step</b><em>the whole atmosphere: winds, temperature, moisture on 32 levels, 192 × 288 grid</em></div>
  <div><span class="big">146,000</span><b>steps per century</b><em>each prediction is fed back in as the next input</em></div>
  <div><span class="big">48,000</span><b>training samples</b><em>six-hourly output of one CESM2 run, 1980–2012</em></div>
  <div><span class="big">0.3 s</span><b>per step on one GPU</b><em>874 M parameters</em></div>
</div>

<div class="cm-given"><b>Prescribed:</b> ocean temperature, sea ice, sunlight and CO₂ enter as inputs. In training/inference they come from the CESM2 run</div>

<!--
CAMulator takes the state of the atmosphere, winds, temperature and moisture on thirty-two levels plus surface pressure, and predicts the state six hours later. The prediction becomes the next input, and the model is applied again, so a century is about 146,000 steps. It was trained on six-hourly output of one CESM2 run, about 48,000 samples from a single history. The ocean temperature, sea ice, sunlight and carbon dioxide are inputs. That design is what makes coupling possible: if the ocean is an input, a real ocean model can supply it.
-->

---

# Training for stability over long runs

<div class="cm-trswap">
<div v-click.hide="1">
<img src="/camulator/three_step_loss.png" alt="Three-step rollout: the network applied three times, with a squared error against CESM at each step" />
<div class="cm-src">The loss sums the squared error over three consecutive six-hour steps, with gradients through all three.</div>
</div>
<div v-click="1">

<div class="cm-pb">
  <div class="io"><i>x</i><sub>t</sub><small>+ forcing</small></div>
  <div class="ar"></div>
  <div class="net"><span><i>F</i><sub>θ</sub>: CAMulator</span><small>874 M weights</small></div>
  <div class="ar"></div>
  <div class="post">
    <div class="brk">post-blocks: global conservation, differentiable</div>
    <div class="row">
      <div class="pb">tracers ≥ 0<small>clip</small></div><div class="ar s"></div>
      <div class="pb">dry-air mass<small>rescale <i>p</i><sub>s</sub></small></div><div class="ar s"></div>
      <div class="pb">water<small>rescale rain</small></div><div class="ar s"></div>
      <div class="pb">energy<small>rescale <i>T</i></small></div>
    </div>
  </div>
  <div class="ar"></div>
  <div class="io"><i>x̂</i><sub>t+Δt</sub><small>147 + 17 maps</small></div>
  <div class="grad"><span>∂ℒ/∂θ</span></div>
</div>

$$
\mathcal{L} = \tfrac{1}{3}\sum_{k=1}^{3} \big\lVert \hat{x}_{t+k\Delta t} - x_{t+k\Delta t} \big\rVert_w^2 \quad \text{on the delivered state, gradient through the post-blocks}
$$

<div class="cm-src">Final layers rescale the output so that global dry-air mass, water and energy are conserved; they are trained with the network.</div>

</div>
</div>

<!--
Two choices in training matter for climate. First, the loss is not computed on one step. The network makes three six-hour steps from its own output, and the error at each step is summed, so training sees the errors the network feeds itself. [click] Second, the last layers enforce physics. Small blocks rescale the global dry-air mass, the water budget and the energy budget so that they balance, and the network is trained through them. Without these constraints, runs of more than a few years drift and eventually fail.
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
layout: section
---

# Coupling CAMulator to the ocean and sea ice

Can a network trained on one simulation stand in for the atmosphere when a real ocean responds to it?

<!--
That brings us to the main question. In training, the ocean was a fixed record. In the coupled system, the ocean reacts to whatever the emulator does, and the emulator then sees the ocean it helped create. The next part is how the two codes talk, what physics sits between them, and what went wrong the first time.
-->

---

# The Ocean and Sea-ice: slow manifold variability

<div class="cm-cols cm-loops-cols">
<div class="cm-loops">
<div>
<div class="hd">Ocean: El Niño</div>
<div class="cm-couple cm-couple-big">
  <div class="box">Trade winds weaken</div>
  <div class="arrows"><span>↓</span></div>
  <div class="box">Warm water spreads east across the Pacific</div>
  <div class="arrows"><span>↓</span></div>
  <div class="box">Rainfall and heating move east with it</div>
  <div class="arrows"><span>↺ winds weaken further</span></div>
</div>
</div>
<div>
<div class="hd ice">Sea ice: ice–albedo</div>
<div class="cm-couple cm-couple-big cm-ice">
  <div class="box">The Arctic warms</div>
  <div class="arrows"><span>↓</span></div>
  <div class="box">Sea ice melts, exposing dark ocean</div>
  <div class="arrows"><span>↓</span></div>
  <div class="box">The ocean absorbs more sunlight</div>
  <div class="arrows"><span>↺ more warming, more melt</span></div>
</div>
</div>
</div>
<div>

<div class="cm-right">

- The ocean stores most of the climate system's heat and changes slowly.
- El Niño, the largest year-to-year swing in climate, exists only because winds and ocean push on each other.
- Sea ice reflects sunlight and insulates the ocean from cold winter air. Losing it amplifies warming, and the Arctic has warmed about four times faster than the globe since 1979.
- Over a prescribed ocean and sea ice, an atmosphere model never has to get these loops right; coupled, it must.

</div>

<div class="cm-src">Arctic amplification: Rantanen et al. (2022).</div>

</div>
</div>

<!--
The ocean and sea ice matter for the same reason: they are slow, and they talk back. The ocean holds most of the heat in the climate system, so it is the system's memory. And the largest year-to-year swing in climate, El Niño, is a conversation between the atmosphere and the ocean. When the trade winds over the Pacific weaken, warm water spreads east, rainfall and heating follow it, and the winds weaken further. Sea ice has its own loop. Ice is bright and reflects most of the sunlight that reaches it; open ocean is dark and absorbs most of it. So when the Arctic warms and ice melts, the ocean absorbs more sunlight and warms further, which is a large part of why the Arctic has warmed about four times faster than the globe. Ice also acts as a lid, keeping the ocean's heat from the cold winter air. For both loops, the atmosphere has to hand the right winds, heat and sunlight to the surface. With a prescribed ocean and ice, the atmosphere model never has to get these loops right. Coupled, it does, so coupling is a real test of an atmosphere model, not a formality.
-->

---

# Fortran and Python exchange files

<div class="cm-cols cm-cols-hs">
<div>

<div class="cm-hs">
  <div class="side fortran">
    <div class="hdr">CESM (Fortran)<small>CPU nodes</small></div>
    <div class="cbox">Ocean (POP2)</div>
    <div class="cbox">Sea ice (CICE5)</div>
    <div class="cbox">Coupler: surface fluxes</div>
    <div class="cbox da">Data atmosphere (modified)</div>
    <div class="t">≈ 1.1 s per exchange</div>
  </div>
  <div class="mid">
    <div class="msg">
      <div class="lbl"><b>①</b> <code>camulator_sst_in.nc</code> + <code>go.flag</code></div>
      <div class="line"><div class="bar"></div><svg class="tri" viewBox="0 0 14 14"><polygon points="0,0 14,7 0,14"/></svg></div>
      <div class="what">sea-surface temperature, sea-ice fraction</div>
    </div>
    <div class="msg">
      <div class="lbl"><b>②</b> <code>camulator_cam_out.nc</code> + <code>done.flag</code></div>
      <div class="line"><svg class="tri" viewBox="0 0 14 14"><polygon points="14,0 0,7 14,14"/></svg><div class="bar"></div></div>
      <div class="what">wind, temperature, humidity, radiation, rain</div>
    </div>
    <div class="every">every 6 model hours</div>
  </div>
  <div class="side python">
    <div class="hdr">CAMulator (Python)<small>1 GPU</small></div>
    <div class="cbox gpu">Read the ocean state</div>
    <div class="cbox gpu">One six-hour network step</div>
    <div class="cbox gpu">Write the atmosphere state</div>
    <div class="t">≈ 0.3 s per step</div>
  </div>
</div>

</div>
<div>

<div class="cm-right">

- CESM's data atmosphere normally reads observed weather from files; ours reads the emulator's file.
- Each side writes a file, sets a flag, and waits for the other's flag.
- The Python server never calls Fortran, and CESM never imports PyTorch.
- The ocean and sea ice now take most of the time.

</div>

</div>
</div>

<div class="cm-src">CESM2.1.5 with POP2 and CICE5; flags polled every 50 ms. Timing on one H100 GPU and two Derecho CPU nodes. Server and handshake: Yuanpu Li and Will Chapman.</div>

<!--
The two halves never share memory. CESM has a component called the data atmosphere, normally used to drive the ocean with observed weather read from files. We modified it so that every six model hours it writes the sea-surface temperature and ice fraction to a file and sets a flag. The Python server sees the flag, reads the ocean state, runs one six-hour step on the GPU, writes the atmospheric fields to a second file and sets its own flag. The Fortran side reads that file and hands the fields to the coupler, which computes the fluxes for the ocean and sea ice. A network step takes about 0.3 seconds; the ocean and sea ice take about a second, so the Fortran side now sets the pace.
-->

---

# The ocean/ice are given the emulator's lowest model level + fluxes

<div class="cm-flow">
  <div class="cam">CAMulator<small>one six-hour step</small></div>
  <div class="lane la">
    <div class="tag">CAMulator emulated Fluxes<small>stress, rad., t. fluxes, E, P</small></div>
    <div class="ar"></div>
    <div class="end">
      <div class="unused" v-click="1">✕ not used over the ocean</div>
    </div>
    <div class="dim" v-click="1"></div>
  </div>
  <div class="lane lb">
    <div class="tag">Lowest model-level state, ~60 m<small>temperature, humidity, wind</small></div>
    <div class="ar"></div>
    <div class="cpl">Coupler<small>bulk formulas</small></div>
    <div class="ar both"><span class="up">SST</span><span class="dn">stress, rad., t. fluxes, E, P</span></div>
    <div class="ocn">Ocean (POP2)<small>surface temperature </small></div>
  </div>
</div>

<div class="cm-given"><b>Stress grows roughly as wind squared.</b> A 10% error in near-surface wind becomes about a 20% error in the stress that drives the ocean.</div>

<!--
This is the main physical point of the coupling. The neural network predicts surface heat fluxes and wind stress, because the physical atmosphere had them in its output and the network was trained on everything. [click] In the coupled system those predictions are never used over the ocean. The coupler takes the emulator's air temperature, humidity and wind at the lowest level, about sixty metres up, combines them with the ocean's surface temperature and currents, and computes the fluxes itself with bulk formulas: wind stress tau = rho C_D |V| (u_air - u_ocean), and heat flux H = rho c_p C_H |V| (T_sea - theta_air). Because the stress has the wind speed in it twice, a ten percent error in the near-surface wind becomes roughly a twenty percent error in the stress. So an emulator can have good flux outputs and still drive the ocean wrongly, if the air near the surface is wrong. Keep the winds in mind; they come back when we look at El Niño.
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

- The coupled system has run from 1981 to 2040 without failing or drifting.
- El Niño events, storms and the seasonal ice edge emerge from the coupled system.
- No flux correction is applied.
- It runs 55 to 60 simulated years per day, about 10× faster than CESM2. The ocean and sea ice now take most of the time.
- The first runs drifted cold because of bugs in the exchange code, not in the network.

</div>

</div>
</div>

<!--
The first coupled runs drifted cold, and the cause turned out to be bugs in the exchange code, such as a temperature passed from the wrong level, not the network. With those fixed, the coupled system runs. It has gone from 1981 to 2040 without blowing up, which was not guaranteed: an emulator trained over a prescribed ocean has never seen its own errors fed back through an ocean. The movie shows one year of the coupled run, with sea-surface temperature anomalies, sea ice in white and rain in cyan. El Niño events develop and decay, storms cross the oceans, and the ice edge moves with the seasons. And it is fast: 55 to 60 simulated years per day, about ten times faster than CESM2, with most of the remaining time spent in the ocean and sea ice rather than the atmosphere.
-->

---

# Coupled sea ice in the Arctic

<div class="cm-cols">
<div>

<video src="/camulator/coupled_arctic_seaice_2028.mp4" class="cm-video" autoplay loop muted playsinline></video>

<div class="cm-src">Coupled run, 2028: sea-ice thickness, sea-surface temperature anomaly and precipitation over the Arctic.</div>

</div>
<div>

<img src="/coupling/ice_series.png" class="cm-fig-col cm-fig-ice" alt="Arctic sea-ice area in March and September, 1981 to 2040, coupled CAMulator against 10 CESM2 runs" />

<div class="cm-src">Arctic sea-ice area, 1981–2039. Grey: 5–95 % of 100 CESM2 runs (higher-emissions scenario after 2015).</div>

</div>
</div>

The seasonal cycle and decline follow CESM2; the run has 5 % more ice in March and 26 % more in September (1981–2014).

<!--
The sea-ice model is fully physical and responds only to the fluxes the coupler computes from the emulator's state. The movie shows one year of the coupled Arctic: the ice thins through the summer, open water appears along the coasts, and the pack refreezes in autumn. The time series shows that this holds over decades. The winter maximum and the summer minimum both follow the range of a hundred CESM2 runs and decline at about the same rate. The coupled run has somewhat too much ice, 5 percent in March and 26 percent in September over 1981 to 2014, with the September excess largest in the 2000s.
-->

---
layout: section
---

# The coupled climate

Mean state and warming are close to CESM2; El Niño and the response to CO₂ still need some work.

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

<div class="cm-cols cm-fill">
<div>

<img src="/coupling/enso_hist.png" class="cm-fig-col" alt="Histogram of tropical Pacific SST variability across 50 CESM2 runs, with lines for the coupled run and the corrected run" />

</div>
<div>

<div class="cm-right">

- Tropical Pacific variability is 0.97 K, below all 50 CESM2 runs (1.33 ± 0.14 K).
- A fixed correction to the wind stress the ocean receives raises it to 1.20 K, inside their range.
- The correction is the same every year; it shows where the problem is but does not fix the emulator.

</div>

<div class="cm-src">Standard deviation of monthly Niño-3.4 SST anomalies, 1981–2014. Grey: 50 CESM2 runs that differ only in their initial state.</div>

</div>
</div>

<!--
The main failure is El Niño. The grey histogram is fifty CESM2 runs that differ only in tiny changes to their starting state, so their spread is the natural chance variation of El Niño. In the coupled emulator the tropical Pacific varies about three quarters as much as in the physical model, 0.97 kelvin, below every one of the fifty Large Ensemble runs. A fixed monthly correction added to the wind stress the ocean receives brings it to 1.20 kelvin, inside the range. That tells us the problem is in the winds over the tropical Pacific. It does not fix the emulator, because the correction is the same every year whatever the atmosphere does.
-->

---

# The emulator's trade winds are too strong

<div class="cm-cols cm-fill">
<div>

<img src="/coupling/wind_stress.png" class="cm-fig-col" alt="Stress change per wind change against mean easterly wind; ensemble members on a line, coupled runs further along it" />

</div>
<div>

<div class="cm-right">

- Mean easterly winds near the surface are 5.7&nbsp;m&nbsp;s⁻¹ in the coupled emulator, against 4.9&nbsp;m&nbsp;s⁻¹ in CESM.
- Stress grows with the square of the wind, so the ocean gets a larger push for each change in wind.
- Across 30 CESM2 runs the same relation holds; the coupled runs sit on its extension.
- The fix is the emulator's mean wind, which is a training target.

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

In one training simulation CO₂ and temperature rise together, so a network can use CO₂ to tell the year. Raised alone, CO₂ warms land by 0.17 K in CESM, 0.12 K in CAMulator (wrong pattern) and 0.69 K in DCN6.

<div class="cm-src">First six hours after CO₂ alone is raised, May–August, per CO₂ doubling. Emulators: 16 held-out states; CESM atmosphere: 10 starts. DCN6: a 173 M-parameter emulator in development.</div>

<!--
The second problem comes from training on a single history. In the training simulation, carbon dioxide and temperature both rise from 1980 to 2012, so a network can learn that more carbon dioxide means a later, warmer year, without learning the radiative physics. We test this by raising carbon dioxide alone and looking at the first six hours. The physical model warms the land a little. CAMulator gets roughly the right average but the wrong pattern, with cooling over East Asia. A smaller emulator we are developing warms about four times too much everywhere. In a coupled run, that error would feed straight into the ocean.
-->

---

# Next: training targets from the physical model

<div class="cm-cols cm-fill">
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

---

# Backup: the response to El Niño, ocean prescribed

<img src="/camulator/enso_teleconnections.png" class="cm-fig-wide" alt="Composite 500 hPa height and precipitation differences for warm minus cold tropical Pacific winters, CAM6 and CAMulator" />

Pattern correlation with the physical model: 0.95 for tropical rainfall and 0.82 for the North Pacific pressure pattern.

<div class="cm-src">Ten warmest minus ten coldest tropical Pacific winters of 34, ocean prescribed. Top: pressure pattern near 5 km. Bottom: precipitation. Left: CESM atmosphere. Right: CAMulator.</div>

<!--
With the ocean prescribed, we can ask whether the emulator responds to El Niño correctly. During warm Pacific winters tropical rainfall shifts east, and a chain of high and low pressure arches over the North Pacific and North America. The emulator reproduces the rainfall shift with a pattern correlation of 0.95 against the physical model and the pressure pattern with 0.82. So the emulator responds to the ocean in the right places. Whether it responds with the right strength is a question only a coupled run can answer.
-->

---

# Backup: one model, many possible histories

<img src="/coupling/le_nino34_three.png" class="cm-fig-wide" alt="Tropical Pacific SST anomaly from 1981 to 2014 in three CESM2 runs that differ only in their initial state" />

Three CESM2 runs with identical physics and forcing, started from slightly different states, produce different El Niño histories.

<div class="cm-src">Red: El Niño (warm); blue: La Niña (cold). Tropical Pacific (Niño-3.4) SST anomaly, 3-month mean. The CESM2 Large Ensemble has 50 such runs over 1981–2014.</div>

<!--
One more idea is needed to read the results. Weather is chaotic, so the same climate model started from two almost identical states produces different histories. These are three runs of CESM2 with the same physics and the same greenhouse gases. Their El Niño events come in different years. The CESM2 Large Ensemble has fifty such runs. Their spread tells us how much any statistic varies by chance, and that is the yardstick for the emulator: we ask whether it falls inside the range of the physical model, not whether it matches any one history.
-->

---

# Backup: the first coupled runs failed at the interface

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
