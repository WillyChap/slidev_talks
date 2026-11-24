<script setup lang="ts">
// Compute, energy and carbon for an ensemble experiment with CESM against coupled CAMulator.
// Cost per simulated year (core-hours) from the AI2 workshop deck (Nov 2026), Derecho:
//   CESM3 25,643; CESM2.1.5 fully coupled 3,750; CAMulator + POP2/CICE 122 core-h + 0.4 GPU-h.
// Energy and carbon need assumptions (power per core, per GPU, data-centre overhead, grid intensity);
// they are sliders so the audience can see what the estimate depends on.
import { computed, ref } from 'vue'

const members = ref(100)
const years = ref(250)
const wCore = ref(6)        // W per CPU core: Derecho node 2x EPYC 7763 (280 W TDP each) + memory/NIC ~700-800 W / 128 cores (estimate)
const wGpu = ref(700)       // W per GPU: H100 SXM board power (the GPU our coupled runs used; Derecho A100 = 400 W)
const pue = ref(1.13)       // NWSC PUE, CISL annual report FY2025 (design value 1.08)
const ci = ref(0.47)        // kg CO2e per kWh: EPA eGRID2023 RMPA subregion (Cheyenne, WY), 1042.5 lb/MWh

const models = [
  { name: 'CESM3', core: 25643, gpu: 0, cls: 'cc-m3' },
  { name: 'CESM2', core: 3750, gpu: 0, cls: 'cc-m2' },
  { name: 'CAMulator + POP2/CICE', core: 122, gpu: 0.4, cls: 'cc-cm' },
]
const simYears = computed(() => members.value * years.value)
const rows = computed(() => models.map(m => {
  const coreH = m.core * simYears.value
  const gpuH = m.gpu * simYears.value
  const mwh = (coreH * wCore.value + gpuH * wGpu.value) * pue.value / 1e6
  return { ...m, coreH, mwh, t: mwh * ci.value }
}))
// Fixed log axis so the bars move with the sliders (normalising to the largest bar kept every ratio constant).
const LO = -2, HI = 5   // 0.01 t to 100,000 t CO2e
const width = (t: number) => Math.min(100, Math.max(0.6, 100 * (Math.log10(Math.max(t, 1e-6)) - LO) / (HI - LO)))
const ticks = [0.01, 1, 100, 10000]
const fmt = (v: number) => v >= 100 ? Math.round(v).toLocaleString() : v >= 10 ? v.toFixed(0) : v.toFixed(1)
const fmtM = (v: number) => (v / 1e6 >= 10 ? (v / 1e6).toFixed(0) : (v / 1e6).toFixed(1)) + ' M'
</script>

<template>
  <div class="cc">
    <div class="ctrl">
      <label>Ensemble members <b>{{ members }}</b><input type="range" min="1" max="100" v-model.number="members" /></label>
      <label>Years per member <b>{{ years }}</b><input type="range" min="10" max="500" step="10" v-model.number="years" /></label>
      <div class="assume">Assumptions</div>
      <label>Power per CPU core <b>{{ wCore }} W</b><input type="range" min="3" max="9" step="0.5" v-model.number="wCore" /></label>
      <label>Power per GPU <b>{{ wGpu }} W</b><input type="range" min="300" max="1000" step="50" v-model.number="wGpu" /></label>
      <label>Data-centre overhead (PUE) <b>{{ pue.toFixed(2) }}</b><input type="range" min="1" max="1.6" step="0.01" v-model.number="pue" /></label>
      <label>Grid intensity <b>{{ ci.toFixed(2) }} kg CO₂e kWh⁻¹</b><input type="range" min="0" max="1" step="0.01" v-model.number="ci" /></label>
    </div>
    <div class="out">
      <div class="total">{{ simYears.toLocaleString() }} simulated years</div>
      <div v-for="r in rows" :key="r.name" class="row">
        <div class="lab">{{ r.name }}</div>
        <div class="bar-wrap"><div class="bar" :class="r.cls" :style="{ width: width(r.t) + '%' }" /></div>
        <div class="num"><b>{{ fmt(r.t) }} t CO₂e</b><br /><span>{{ fmt(r.mwh) }} MWh · {{ fmtM(r.coreH) }} core-h</span></div>
      </div>
      <div class="axis"><span v-for="v in ticks" :key="v" :style="{ left: (100 * (Math.log10(v) - LO) / (HI - LO)) + '%' }">{{ v.toLocaleString() }}</span></div>
      <div class="axis-lab">t CO₂e (log scale)</div>
      <div class="ratio">CESM2 ÷ CAMulator coupled: <b>{{ (rows[1].t / rows[2].t).toFixed(0) }}×</b> the energy</div>
    </div>
  </div>
</template>

<style scoped>
.cc { display: grid; grid-template-columns: 1fr 1.25fr; gap: 1.4rem; align-items: start; font-size: 0.68rem; }
.ctrl { display: grid; grid-template-columns: 1fr 1fr; gap: 0.35rem 0.9rem; }
.ctrl label { display: flex; flex-direction: column; gap: 0.05rem; }
.ctrl input[type=range] { width: 100%; accent-color: var(--cu-gold); }
.assume { grid-column: 1 / -1; margin-top: 0.2rem; font-weight: 700; color: var(--cu-text-muted); border-top: 1px solid var(--cu-border); padding-top: 0.3rem; }
.total { font-weight: 700; margin-bottom: 0.4rem; }
.row { display: grid; grid-template-columns: 7.5rem 1fr 9rem; gap: 0.6rem; align-items: center; margin: 0.45rem 0; }
.lab { font-weight: 600; line-height: 1.15; }
.bar-wrap { background: var(--cu-surface); height: 1.3rem; border-radius: 2px; }
.bar { height: 100%; border-radius: 2px; transition: width 0.2s; }
.bar.cc-m3 { background: var(--cu-dark-gray); }
.bar.cc-m2 { background: var(--cu-light-gray); }
.bar.cc-cm { background: var(--cu-gold); }
.num { line-height: 1.2; font-variant-numeric: tabular-nums; }
.num span { color: var(--cu-text-muted); font-size: 0.9em; }
.axis { position: relative; height: 1rem; margin-left: 8.1rem; margin-right: 9.6rem; font-size: 0.85em; color: var(--cu-text-muted); }
.axis span { position: absolute; transform: translateX(-50%); }
.axis-lab { text-align: center; font-size: 0.85em; color: var(--cu-text-muted); margin-right: 1.5rem; }
.ratio { margin-top: 0.6rem; border-top: 1px solid var(--cu-border); padding-top: 0.4rem; }
</style>
