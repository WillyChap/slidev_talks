<script setup lang="ts">
// Interactive Gregory diagram for CESM2 abrupt-4xCO2.
// Pick a range of years; an ordinary least-squares line N = F - B*dT is fitted to those years
// and extended to N = 0. Data: gregory/data/cesm2_gregory.json (see gregory/analysis/).
import { computed, ref } from 'vue'
import data from '../gregory/data/cesm2_gregory.json'

const props = withDefaults(defineProps<{ start?: number, end?: number, maxYear?: number }>(), {
  start: 1, end: 150, maxYear: 150,
})

const years: number[] = data.year
const dT: number[] = data.dT
const N: number[] = data.N
const lastYear = years[years.length - 1]

const y0 = ref(props.start)
const y1 = ref(props.end)
const shown = ref(props.maxYear)

const presets = [
  { label: '1–20', a: 1, b: 20 },
  { label: '21–150', a: 21, b: 150 },
  { label: '1–150', a: 1, b: 150 },
  { label: `151–${lastYear}`, a: 151, b: lastYear },
]
function setRange(a: number, b: number) {
  y0.value = a; y1.value = b
  if (b > shown.value) shown.value = lastYear
}
function onStart() { if (y0.value > y1.value - 5) y0.value = y1.value - 5 }
function onEnd() {
  if (y1.value < y0.value + 5) y1.value = y0.value + 5
  if (y1.value > shown.value) shown.value = lastYear
}

const fit = computed(() => {
  let n = 0, sx = 0, sy = 0, sxx = 0, sxy = 0
  for (let i = 0; i < years.length; i++) {
    if (years[i] < y0.value || years[i] > y1.value) continue
    n++; sx += dT[i]; sy += N[i]; sxx += dT[i] * dT[i]; sxy += dT[i] * N[i]
  }
  const slope = (n * sxy - sx * sy) / (n * sxx - sx * sx)
  const F = (sy - slope * sx) / n
  const B = -slope
  return { n, F, B, Teq: F / B, ecs: F / B / 2 }
})

// plot geometry
const W = 600, H = 380, m = { l: 62, r: 18, t: 14, b: 52 }
const xmax = computed(() => (shown.value > 150 ? 14 : 11))
const ymin = -1, ymax = 10
const sx = (x: number) => m.l + (x / xmax.value) * (W - m.l - m.r)
const sy = (y: number) => H - m.b - ((y - ymin) / (ymax - ymin)) * (H - m.t - m.b)
const xticks = computed(() => Array.from({ length: Math.floor(xmax.value / 2) + 1 }, (_, i) => 2 * i))
const yticks = [0, 2, 4, 6, 8, 10]

const pts = computed(() => years
  .map((y, i) => ({ y, x: dT[i], n: N[i] }))
  .filter(p => p.y <= shown.value))

const line = computed(() => {
  const { F, B, Teq } = fit.value
  const xEnd = Math.min(Math.max(Teq, 0), xmax.value)
  return { x1: sx(0), y1: sy(F), x2: sx(xEnd), y2: sy(F - B * xEnd) }
})
const fmt = (v: number, d = 1) => (Number.isFinite(v) ? v.toFixed(d) : '—')
</script>

<template>
  <div class="gx">
    <svg :viewBox="`0 0 ${W} ${H}`" class="gx-plot" role="img"
      aria-label="Gregory diagram of CESM2 abrupt-4xCO2 annual means with a fitted line">
      <!-- axes -->
      <line :x1="m.l" :x2="W - m.r" :y1="sy(0)" :y2="sy(0)" class="zero" />
      <line :x1="m.l" :x2="m.l" :y1="m.t" :y2="H - m.b" class="axis" />
      <line :x1="m.l" :x2="W - m.r" :y1="H - m.b" :y2="H - m.b" class="axis" />
      <g v-for="t in xticks" :key="'x' + t">
        <line :x1="sx(t)" :x2="sx(t)" :y1="H - m.b" :y2="H - m.b + 5" class="axis" />
        <text :x="sx(t)" :y="H - m.b + 20" text-anchor="middle" class="tick">{{ t }}</text>
      </g>
      <g v-for="t in yticks" :key="'y' + t">
        <line :x1="m.l - 5" :x2="m.l" :y1="sy(t)" :y2="sy(t)" class="axis" />
        <text :x="m.l - 9" :y="sy(t) + 5" text-anchor="end" class="tick">{{ t }}</text>
      </g>
      <text :x="(m.l + W - m.r) / 2" :y="H - 8" text-anchor="middle" class="lab">Surface warming ΔT (K)</text>
      <text :x="16" :y="(m.t + H - m.b) / 2" text-anchor="middle" class="lab"
        :transform="`rotate(-90 16 ${(m.t + H - m.b) / 2})`">TOA imbalance N (W m⁻²)</text>

      <!-- points -->
      <circle v-for="p in pts" :key="p.y" :cx="sx(p.x)" :cy="sy(p.n)" r="3.2"
        :class="p.y >= y0 && p.y <= y1 ? 'pt in' : 'pt out'" />

      <!-- fit -->
      <line v-bind="line" class="fit" />
      <circle :cx="line.x1" :cy="line.y1" r="6" class="mark" />
      <circle v-if="fit.Teq <= xmax" :cx="sx(fit.Teq)" :cy="sy(0)" r="6" class="mark" />
    </svg>

    <div class="gx-ctrl">
      <div class="presets">
        <button v-for="p in presets" :key="p.label" @click="setRange(p.a, p.b)"
          :class="{ on: y0 === p.a && y1 === p.b }">{{ p.label }}</button>
      </div>
      <label>First year <b>{{ y0 }}</b>
        <input type="range" min="1" :max="lastYear - 5" v-model.number="y0" @input="onStart" />
      </label>
      <label>Last year <b>{{ y1 }}</b>
        <input type="range" min="6" :max="lastYear" v-model.number="y1" @input="onEnd" />
      </label>
      <label class="chk"><input type="checkbox" :checked="shown > 150"
          @change="shown = ($event.target as HTMLInputElement).checked ? lastYear : 150" />
        Show years 151–{{ lastYear }}</label>
      <table>
        <tbody>
          <tr><td>Intercept F</td><td>{{ fmt(fit.F) }} W m⁻²</td></tr>
          <tr><td>Slope −B</td><td>{{ fmt(-fit.B, 2) }} W m⁻² K⁻¹</td></tr>
          <tr><td>ΔT where N = 0</td><td>{{ fmt(fit.Teq) }} K</td></tr>
          <tr><td>ECS ≈ ΔT / 2</td><td>{{ fmt(fit.ecs) }} K</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.gx { display: grid; grid-template-columns: 1.55fr 1fr; gap: 1.2rem; align-items: start; }
.gx-plot { width: 100%; height: auto; }
.axis { stroke: var(--cu-text); stroke-width: 1.2; }
.zero { stroke: var(--cu-light-gray); stroke-width: 1.2; stroke-dasharray: 5 4; }
.tick { fill: var(--cu-text); font-size: 14px; }
.lab { fill: var(--cu-text); font-size: 16px; }
.pt.in { fill: var(--cu-sky-blue); opacity: 0.75; }
.pt.out { fill: var(--cu-light-gray); opacity: 0.45; }
:global(.dark) .pt.in { fill: var(--cu-gold); }
.fit { stroke: #B5473A; stroke-width: 3; }
.mark { fill: none; stroke: #B5473A; stroke-width: 2.5; }
.gx-ctrl { font-size: 0.8rem; display: flex; flex-direction: column; gap: 0.55rem; }
.gx-ctrl label { display: flex; flex-direction: column; gap: 0.15rem; }
.gx-ctrl label.chk { flex-direction: row; align-items: center; gap: 0.4rem; }
.gx-ctrl input[type=range] { width: 100%; accent-color: var(--cu-gold); }
.presets { display: flex; flex-wrap: wrap; gap: 0.35rem; }
.presets button { border: 1px solid var(--cu-border); border-radius: 3px; padding: 0.1rem 0.5rem; font-size: 0.75rem; }
.presets button.on { background: var(--cu-gold); color: var(--cu-on-gold, #000); border-color: var(--cu-gold); }
table { font-size: 0.8rem; margin: 0; border-collapse: collapse; }
td { padding: 0.15rem 0.4rem 0.15rem 0; border: none; }
td:last-child { text-align: right; font-variant-numeric: tabular-nums; }
tr { border-top: 1px solid var(--cu-border); }
</style>
