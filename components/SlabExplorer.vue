<script setup lang="ts">
// Slab-ocean CO2-doubling experiment with weather noise, laid out like HW5 Part 1:
// time series of ΔT, time series of N, and the Gregory diagram, 60 annual means.
//   C dT/dt = F - B T + xi(t),   N = F - B T + xi(t)
// xi is white noise stepped monthly, scaled so that its annual mean has standard deviation `noise`.
// In a slab model the slab is the only heat reservoir, so the TOA imbalance N is what warms it.
import { computed, ref } from 'vue'

const F = ref(3.7)        // W m-2, roughly CO2 doubling
const B = ref(1.0)        // W m-2 K-1
const h = ref(50)         // m, slab depth
const noise = ref(0.6)    // W m-2, std of annual-mean noise
const seed = ref(1)
const showFit = ref(false)

const RHO_CP = 1025 * 3990, SEC_YR = 3.156e7
const C = computed(() => RHO_CP * h.value / SEC_YR)   // W yr m-2 K-1
const YEARS = 60, SUB = 12

function rng(a: number) {                     // mulberry32 + Box-Muller, so a run is reproducible
  return () => {
    let u = 0, v = 0
    const r = () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a)
      t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296 }
    while (u === 0) u = r(); v = r()
    return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v)
  }
}

const years = computed(() => {
  const g = rng(seed.value * 7919)
  const dt = 1 / SUB, s = noise.value * Math.sqrt(SUB)
  let T = 0
  const out: { y: number, T: number, N: number }[] = []
  for (let y = 1; y <= YEARS; y++) {
    let sT = 0, sN = 0
    for (let m = 0; m < SUB; m++) {
      const N = F.value - B.value * T + s * g()
      T += dt * N / C.value
      sT += T; sN += N
    }
    out.push({ y, T: sT / SUB, N: sN / SUB })
  }
  return out
})

const fit = computed(() => {                 // least squares N = a + b T over all years
  const p = years.value, n = p.length
  const mx = p.reduce((s, q) => s + q.T, 0) / n, my = p.reduce((s, q) => s + q.N, 0) / n
  let sxy = 0, sxx = 0
  for (const q of p) { sxy += (q.T - mx) * (q.N - my); sxx += (q.T - mx) ** 2 }
  const b = sxy / sxx, a = my - b * mx
  return { F: a, B: -b, Teq: -a / b }
})
const Teq = computed(() => F.value / B.value)

// panels
const W = 300, H = 230, m = { l: 46, r: 12, t: 10, b: 42 }
const TMAX = 8, NMIN = -2, NMAX = 6
const sx = (v: number, lo: number, hi: number) => m.l + (v - lo) / (hi - lo) * (W - m.l - m.r)
const sy = (v: number, lo: number, hi: number) => H - m.b - (Math.min(Math.max(v, lo), hi) - lo) / (hi - lo) * (H - m.t - m.b)
const line = (pts: [number, number][]) => pts.map((p, i) => `${i ? 'L' : 'M'}${p[0].toFixed(1)},${p[1].toFixed(1)}`).join('')
const pathT = computed(() => line(years.value.map(p => [sx(p.y, 0, YEARS), sy(p.T, 0, TMAX)])))
const pathN = computed(() => line(years.value.map(p => [sx(p.y, 0, YEARS), sy(p.N, NMIN, NMAX)])))
const fitLine = computed(() => {
  const f = fit.value, x1 = Math.min(TMAX, Math.max(f.Teq, 0.5))
  return line([[sx(0, 0, TMAX), sy(f.F, NMIN, NMAX)], [sx(x1, 0, TMAX), sy(f.F - f.B * x1, NMIN, NMAX)]])
})
const tYear = [0, 20, 40, 60], tT = [0, 2, 4, 6, 8], tN = [-2, 0, 2, 4, 6]
</script>

<template>
  <div class="slab">
    <div class="panels">
      <svg :viewBox="`0 0 ${W} ${H}`">
        <line :x1="m.l" :x2="m.l" :y1="m.t" :y2="H - m.b" class="axis" />
        <line :x1="m.l" :x2="W - m.r" :y1="H - m.b" :y2="H - m.b" class="axis" />
        <line v-if="Teq <= TMAX" :x1="m.l" :x2="W - m.r" :y1="sy(Teq, 0, TMAX)" :y2="sy(Teq, 0, TMAX)" class="ref" />
        <g v-for="t in tYear" :key="'a' + t"><text :x="sx(t, 0, YEARS)" :y="H - m.b + 17" text-anchor="middle" class="tick">{{ t }}</text></g>
        <g v-for="t in tT" :key="'b' + t"><text :x="m.l - 7" :y="sy(t, 0, TMAX) + 4" text-anchor="end" class="tick">{{ t }}</text></g>
        <path :d="pathT" class="model" />
        <text :x="(m.l + W) / 2" :y="H - 6" text-anchor="middle" class="lab">Year</text>
        <text x="13" :y="(H - m.b) / 2" text-anchor="middle" class="lab" :transform="`rotate(-90 13 ${(H - m.b) / 2})`">ΔT (K)</text>
      </svg>
      <svg :viewBox="`0 0 ${W} ${H}`">
        <line :x1="m.l" :x2="m.l" :y1="m.t" :y2="H - m.b" class="axis" />
        <line :x1="m.l" :x2="W - m.r" :y1="sy(0, NMIN, NMAX)" :y2="sy(0, NMIN, NMAX)" class="zero" />
        <line :x1="m.l" :x2="W - m.r" :y1="H - m.b" :y2="H - m.b" class="axis" />
        <g v-for="t in tYear" :key="'c' + t"><text :x="sx(t, 0, YEARS)" :y="H - m.b + 17" text-anchor="middle" class="tick">{{ t }}</text></g>
        <g v-for="t in tN" :key="'d' + t"><text :x="m.l - 7" :y="sy(t, NMIN, NMAX) + 4" text-anchor="end" class="tick">{{ t }}</text></g>
        <path :d="pathN" class="model" />
        <text :x="(m.l + W) / 2" :y="H - 6" text-anchor="middle" class="lab">Year</text>
        <text x="13" :y="(H - m.b) / 2" text-anchor="middle" class="lab" :transform="`rotate(-90 13 ${(H - m.b) / 2})`">N (W m⁻²)</text>
      </svg>
      <svg :viewBox="`0 0 ${W} ${H}`">
        <line :x1="m.l" :x2="m.l" :y1="m.t" :y2="H - m.b" class="axis" />
        <line :x1="m.l" :x2="W - m.r" :y1="sy(0, NMIN, NMAX)" :y2="sy(0, NMIN, NMAX)" class="zero" />
        <line :x1="m.l" :x2="W - m.r" :y1="H - m.b" :y2="H - m.b" class="axis" />
        <g v-for="t in tT" :key="'e' + t"><text :x="sx(t, 0, TMAX)" :y="H - m.b + 17" text-anchor="middle" class="tick">{{ t }}</text></g>
        <g v-for="t in tN" :key="'f' + t"><text :x="m.l - 7" :y="sy(t, NMIN, NMAX) + 4" text-anchor="end" class="tick">{{ t }}</text></g>
        <circle v-for="p in years" :key="p.y" :cx="sx(Math.min(p.T, TMAX), 0, TMAX)" :cy="sy(p.N, NMIN, NMAX)" r="3" class="dot" :style="{ opacity: 0.35 + 0.65 * p.y / YEARS }" />
        <path v-if="showFit" :d="fitLine" class="fit" />
        <text :x="(m.l + W) / 2" :y="H - 6" text-anchor="middle" class="lab">ΔT (K)</text>
        <text x="13" :y="(H - m.b) / 2" text-anchor="middle" class="lab" :transform="`rotate(-90 13 ${(H - m.b) / 2})`">N (W m⁻²)</text>
      </svg>
    </div>
    <div class="ctrl">
      <label>Forcing ΔF <b>{{ F.toFixed(1) }} W m⁻²</b><input type="range" min="1" max="5" step="0.1" v-model.number="F" /></label>
      <label>Restoring B <b>{{ B.toFixed(2) }} W m⁻² K⁻¹</b><input type="range" min="0.6" max="2.5" step="0.05" v-model.number="B" /></label>
      <label>Slab depth <b>{{ h }} m</b><input type="range" min="10" max="200" step="5" v-model.number="h" /></label>
      <label>Weather noise <b>{{ noise.toFixed(1) }} W m⁻²</b><input type="range" min="0" max="1.5" step="0.1" v-model.number="noise" /></label>
      <div class="btns">
        <button @click="seed++">New run</button>
        <label class="chk"><input type="checkbox" v-model="showFit" /> Fit all 60 years</label>
      </div>
      <div class="read">
        True: ΔF/B = <b>{{ Teq.toFixed(1) }} K</b>, timescale C/B = <b>{{ (C / B).toFixed(0) }} yr</b>
        <template v-if="showFit"><br />Fit: ΔF ≈ <b>{{ fit.F.toFixed(1) }}</b>, B ≈ <b>{{ fit.B.toFixed(2) }}</b>, ΔT<sub>eq</sub> ≈ <b>{{ fit.Teq.toFixed(1) }} K</b></template>
      </div>
    </div>
  </div>
</template>

<style scoped>
.slab { display: flex; flex-direction: column; gap: 0.5rem; }
.panels { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.6rem; }
svg { width: 100%; height: auto; }
.axis { stroke: var(--cu-text); stroke-width: 1.2; }
.zero { stroke: var(--cu-light-gray); stroke-width: 1; }
.ref { stroke: var(--cu-light-gray); stroke-width: 1.2; stroke-dasharray: 5 4; }
.tick { fill: var(--cu-text); font-size: 13px; }
.lab { fill: var(--cu-text); font-size: 15px; }
.model { fill: none; stroke: #B5473A; stroke-width: 2; }
.dot { fill: #B5473A; }
.fit { stroke: var(--cu-text); stroke-width: 2; stroke-dasharray: 6 4; }
.ctrl { font-size: 0.72rem; display: grid; grid-template-columns: repeat(4, 1fr) 1.1fr; gap: 0.3rem 1rem; align-items: end; }
.ctrl > label { display: flex; flex-direction: column; gap: 0.1rem; }
.ctrl input[type=range] { width: 100%; accent-color: var(--cu-gold); }
.btns { display: flex; flex-direction: column; gap: 0.25rem; }
.btns button { border: 1px solid var(--cu-gold); border-radius: 3px; padding: 0.1rem 0.5rem; background: transparent; color: inherit; cursor: pointer; font: inherit; }
.chk { display: flex; align-items: center; gap: 0.3rem; }
.read { grid-column: 1 / -1; border-top: 1px solid var(--cu-border); padding-top: 0.3rem; line-height: 1.5; }
</style>
