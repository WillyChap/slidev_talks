<script setup lang="ts">
// A coarse latitude-longitude grid on an orthographic globe, with one cell pulled out as a
// column of model levels. Schematic: the drawn grid is 15 degrees so the cells are visible.
const R = 88, CX = 98, CY = 104
const LAM0 = -25 * Math.PI / 180, PHI0 = 22 * Math.PI / 180
const d2r = Math.PI / 180

function proj(latDeg: number, lonDeg: number) {
  const p = latDeg * d2r, l = lonDeg * d2r - LAM0
  const cosc = Math.sin(PHI0) * Math.sin(p) + Math.cos(PHI0) * Math.cos(p) * Math.cos(l)
  const x = CX + R * Math.cos(p) * Math.sin(l)
  const y = CY - R * (Math.cos(PHI0) * Math.sin(p) - Math.sin(PHI0) * Math.cos(p) * Math.cos(l))
  return { x, y, vis: cosc > 0 }
}
// Polyline through visible samples, broken where the line goes behind the globe.
function curve(pts: { x: number, y: number, vis: boolean }[]) {
  let d = '', pen = false
  for (const q of pts) {
    if (!q.vis) { pen = false; continue }
    d += `${pen ? 'L' : 'M'}${q.x.toFixed(1)},${q.y.toFixed(1)}`; pen = true
  }
  return d
}
const STEP = 15
const lines: string[] = []
for (let lat = -75; lat <= 75; lat += STEP) {
  const pts = []; for (let lon = -180; lon <= 180; lon += 3) pts.push(proj(lat, lon)); lines.push(curve(pts))
}
for (let lon = -180; lon < 180; lon += STEP) {
  const pts = []; for (let lat = -90; lat <= 90; lat += 3) pts.push(proj(lat, lon)); lines.push(curve(pts))
}
// Highlighted cell: 30-45N, 0-15E
const cellPts: { x: number, y: number, vis: boolean }[] = []
for (let lon = 0; lon <= 15; lon += 3) cellPts.push(proj(30, lon))
for (let lat = 30; lat <= 45; lat += 3) cellPts.push(proj(lat, 15))
for (let lon = 15; lon >= 0; lon -= 3) cellPts.push(proj(45, lon))
for (let lat = 45; lat >= 30; lat -= 3) cellPts.push(proj(lat, 0))
const cell = curve(cellPts) + 'Z'
const cTR = proj(45, 15), cBR = proj(30, 15)

// Column: front face, right face and top face, split into layers
const X0 = 238, W = 44, DX = 16, DY = -10, TOP = 40, BOT = 168, N = 8
const layers = Array.from({ length: N - 1 }, (_, i) => TOP + (i + 1) * (BOT - TOP) / N)
</script>

<template>
  <svg class="gg" viewBox="0 6 370 190" role="img" aria-label="Globe divided into grid cells, with one cell pulled out as a column of stacked model levels">
    <circle :cx="CX" :cy="CY" :r="R" class="sea" />
    <path v-for="(d, i) in lines" :key="i" :d="d" class="grid" />
    <path :d="cell" class="cell" />
    <circle :cx="CX" :cy="CY" :r="R" class="rim" />
    <!-- leader lines from the cell to the column base -->
    <line :x1="cTR.x" :y1="cTR.y" :x2="X0" :y2="TOP" class="lead" />
    <line :x1="cBR.x" :y1="cBR.y" :x2="X0" :y2="BOT" class="lead" />
    <!-- column -->
    <polygon :points="`${X0},${TOP} ${X0 + W},${TOP} ${X0 + W + DX},${TOP + DY} ${X0 + DX},${TOP + DY}`" class="ctop" />
    <polygon :points="`${X0 + W},${TOP} ${X0 + W + DX},${TOP + DY} ${X0 + W + DX},${BOT + DY} ${X0 + W},${BOT}`" class="cside" />
    <rect :x="X0" :y="TOP" :width="W" :height="BOT - TOP" class="cfront" />
    <g v-for="y in layers" :key="y">
      <line :x1="X0" :x2="X0 + W" :y1="y" :y2="y" class="lyr" />
      <line :x1="X0 + W" :x2="X0 + W + DX" :y1="y" :y2="y + DY" class="lyr" />
    </g>
    <rect :x="X0" :y="BOT - (BOT - TOP) / N" :width="W" :height="(BOT - TOP) / N" class="sfc" />
    <!-- labels -->
    <path :d="`M${X0 + W + DX + 6},${TOP + DY} h4 V${BOT + DY} h-4`" class="brk" />
    <text :x="X0 + W + DX + 14" :y="(TOP + BOT) / 2 + DY + 4" class="lab">32 levels</text>
    <text :x="X0 + W / 2" :y="BOT + 16" text-anchor="middle" class="lab">~100 km</text>
    <text :x="X0 + W / 2" :y="TOP + DY - 8" text-anchor="middle" class="lab sm">top of model</text>
    <text :x="X0 + W / 2 + 2" :y="BOT - 4" text-anchor="middle" class="lab sm">surface</text>
  </svg>
</template>

<style scoped>
.gg { width: 100%; height: auto; display: block; }
.sea { fill: #E8EEF5; }
.grid { fill: none; stroke: #8FA6BF; stroke-width: 0.7; }
.rim { fill: none; stroke: #2E4A6B; stroke-width: 1.4; }
.cell { fill: var(--cu-gold); stroke: #000; stroke-width: 1.2; }
.lead { stroke: #555; stroke-width: 0.9; stroke-dasharray: 3 3; }
.cfront { fill: #FBF3DF; stroke: #000; stroke-width: 1.2; }
.cside { fill: #EBDDB5; stroke: #000; stroke-width: 1.2; }
.ctop { fill: #F5EAD0; stroke: #000; stroke-width: 1.2; }
.lyr { stroke: #B49A55; stroke-width: 0.8; }
.sfc { fill: var(--cu-gold); stroke: #000; stroke-width: 1.2; }
.brk { fill: none; stroke: #2E4A6B; stroke-width: 1.2; }
.lab { fill: var(--cu-text); font-size: 13px; font-weight: 600; }
.lab.sm { font-size: 10.5px; font-weight: 400; fill: var(--cu-text-muted); }
</style>
