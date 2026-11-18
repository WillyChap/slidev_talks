<script setup lang="ts">
// 0D energy balance model (slab ocean) under abrupt forcing, as in Lecture 3.
//   C dT/dt = N = F - B T   (N: net downward TOA flux)
// C is set from a mixed-layer depth h.
import { computed, ref } from 'vue'
import data from '../gregory/data/cesm2_gregory.json'

const F = ref(8.0)       // W m-2
const B = ref(1.0)       // W m-2 K-1
const h = ref(75)        // m
const showCesm = ref(false)

const RHO_CP = 1025 * 3990          // J m-3 K-1, sea water
const SEC_YR = 3.156e7
const C = computed(() => RHO_CP * h.value / SEC_YR)   // W yr m-2 K-1
const YEARS = 150

const run = computed(() => {
  const dt = 0.05
  let T = 0
  const out: { t: number, T: number, N: number }[] = [{ t: 0, T: 0, N: F.value }]
  for (let k = 1; k <= YEARS / dt; k++) {
    T += dt * (F.value - B.value * T) / C.value
    if (k % Math.round(1 / dt) === 0) out.push({ t: Math.round(k * dt), T, N: F.value - B.value * T })
  }
  return out
})
const tau = computed(() => C.value / B.value)
const Teq = computed(() => F.value / B.value)
const cesm = data.year.map((y: number, i: number) => ({ t: y - 0.5, T: data.dT[i], N: data.N[i] }))
  .filter(p => p.t <= YEARS)

// two panels
const W = 330, H = 290, m = { l: 52, r: 18, t: 10, b: 48 }
const TMAX = 12, NMAX = 10
const px = (v: number, max: number) => m.l + (v / max) * (W - m.l - m.r)
const py = (v: number, max: number) => H - m.b - (v / max) * (H - m.t - m.b)
const path = (pts: { x: number, y: number }[]) =>
  pts.map((p, i) => `${i ? 'L' : 'M'}${p.x.toFixed(1)},${p.y.toFixed(1)}`).join('')
const pathT = computed(() => path(run.value.map(p => ({ x: px(p.t, YEARS), y: py(Math.min(p.T, TMAX), TMAX) }))))
const pathG = computed(() => path(run.value.map(p => ({ x: px(Math.min(p.T, TMAX), TMAX), y: py(Math.max(p.N, 0), NMAX) }))))
</script>

<template>
  <div class="ebm">
    <div class="panels">
      <svg :viewBox="`0 0 ${W} ${H}`" role="img" aria-label="Model surface warming against year">
        <line :x1="m.l" :x2="m.l" :y1="m.t" :y2="H - m.b" class="axis" />
        <line :x1="m.l" :x2="W - m.r" :y1="H - m.b" :y2="H - m.b" class="axis" />
        <line v-if="Teq <= TMAX" :x1="m.l" :x2="W - m.r" :y1="py(Teq, TMAX)" :y2="py(Teq, TMAX)" class="ref" />
        <g v-for="t in [0, 50, 100, 150]" :key="'a' + t">
          <text :x="px(t, YEARS)" :y="H - m.b + 19" text-anchor="middle" class="tick">{{ t }}</text></g>
        <g v-for="t in [0, 3, 6, 9, 12]" :key="'b' + t">
          <text :x="m.l - 8" :y="py(t, TMAX) + 5" text-anchor="end" class="tick">{{ t }}</text></g>
        <template v-if="showCesm">
          <circle v-for="p in cesm" :key="'c' + p.t" :cx="px(p.t, YEARS)" :cy="py(p.T, TMAX)" r="2.2" class="obs" /></template>
        <path :d="pathT" class="model" />
        <text :x="(m.l + W) / 2" :y="H - 8" text-anchor="middle" class="lab">Year</text>
        <text x="14" :y="(H - m.b) / 2" text-anchor="middle" class="lab" :transform="`rotate(-90 14 ${(H - m.b) / 2})`">ΔT (K)</text>
      </svg>
      <svg :viewBox="`0 0 ${W} ${H}`" role="img" aria-label="Model Gregory diagram">
        <line :x1="m.l" :x2="m.l" :y1="m.t" :y2="H - m.b" class="axis" />
        <line :x1="m.l" :x2="W - m.r" :y1="H - m.b" :y2="H - m.b" class="axis" />
        <g v-for="t in [0, 3, 6, 9, 12]" :key="'c' + t">
          <text :x="px(t, TMAX)" :y="H - m.b + 19" text-anchor="middle" class="tick">{{ t }}</text></g>
        <g v-for="t in [0, 2, 4, 6, 8, 10]" :key="'e' + t">
          <text :x="m.l - 8" :y="py(t, NMAX) + 5" text-anchor="end" class="tick">{{ t }}</text></g>
        <template v-if="showCesm">
          <circle v-for="p in cesm" :key="'g' + p.t" :cx="px(p.T, TMAX)" :cy="py(Math.max(p.N, 0), NMAX)" r="2.2" class="obs" /></template>
        <path :d="pathG" class="model" />
        <circle v-for="p in run.filter(q => q.t > 0 && q.t % 10 === 0)" :key="'d' + p.t"
          :cx="px(Math.min(p.T, TMAX), TMAX)" :cy="py(Math.max(p.N, 0), NMAX)" r="3" class="dot" />
        <text :x="(m.l + W) / 2" :y="H - 8" text-anchor="middle" class="lab">ΔT (K)</text>
        <text x="14" :y="(H - m.b) / 2" text-anchor="middle" class="lab" :transform="`rotate(-90 14 ${(H - m.b) / 2})`">N (W m⁻²)</text>
      </svg>
    </div>
    <div class="ctrl">
      <label>Forcing ΔF <b>{{ F.toFixed(1) }} W m⁻²</b><input type="range" min="1" max="10" step="0.1" v-model.number="F" /></label>
      <label>Restoring B <b>{{ B.toFixed(2) }} W m⁻² K⁻¹</b><input type="range" min="0.4" max="3" step="0.05" v-model.number="B" /></label>
      <label>Mixed layer <b>{{ h }} m</b><input type="range" min="20" max="300" step="5" v-model.number="h" /></label>
      <label class="chk"><input type="checkbox" v-model="showCesm" /> Overlay CESM2 years 1–150</label>
      <div class="read">Equilibrium ΔT = ΔF/B = <b>{{ Teq.toFixed(1) }} K</b><br />
        Timescale C/B = <b>{{ tau.toFixed(0) }} yr</b></div>
    </div>
  </div>
</template>

<style scoped>
.ebm { display: grid; grid-template-columns: 2fr 1fr; gap: 1rem; align-items: start; }
.panels { display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; }
svg { width: 100%; height: auto; }
.axis { stroke: var(--cu-text); stroke-width: 1.2; }
.ref { stroke: var(--cu-light-gray); stroke-width: 1.2; stroke-dasharray: 5 4; }
.tick { fill: var(--cu-text); font-size: 14px; }
.lab { fill: var(--cu-text); font-size: 16px; }
.model { fill: none; stroke: #B5473A; stroke-width: 3; }
.dot { fill: #B5473A; }
.obs { fill: var(--cu-sky-blue); opacity: 0.5; }
:global(.dark) .obs { fill: var(--cu-gold); }
.ctrl { font-size: 0.78rem; display: flex; flex-direction: column; gap: 0.5rem; }
.ctrl label { display: flex; flex-direction: column; gap: 0.1rem; }
.ctrl label.chk { flex-direction: row; align-items: center; gap: 0.4rem; }
.ctrl input[type=range] { width: 100%; accent-color: var(--cu-gold); }
.read { border-top: 1px solid var(--cu-border); padding-top: 0.4rem; line-height: 1.5; }
</style>
