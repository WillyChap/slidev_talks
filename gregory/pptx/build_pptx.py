"""Editable PowerPoint version of the Gregory diagram lecture, in the CU Boulder style of the Slidev deck.

Run from anywhere:
    /glade/u/apps/opt/conda/envs/npl-2024b/bin/python -I gregory/pptx/build_pptx.py
Reads  gregory/analysis/cesm2_global_annual.csv (from global_means.py) and the speaker notes in
       gregory-lecture.md, so edits to the notes there carry over.
Writes gregory/pptx/figures/*.png and gregory-lecture-editable.pptx in the project root.

Layout comes from the scientific-slides Deck helper; CUSlides adds the CU Boulder chrome
(gold rule under titles, black footer with logo and department, black cover).
"""
import os, re, sys
import numpy as np, pandas as pd

sys.path.insert(0, "/glade/u/home/wchapman/.claude/skills/scientific-slides/scripts")
import figstyle
import deck as D
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
FIG = os.path.join(HERE, "figures"); os.makedirs(FIG, exist_ok=True)
LOGO = os.path.join(ROOT, "node_modules", "slidev-theme-cu-boulder", "public", "cu-logo-rev.png")
DEPT = "Department of Atmospheric & Oceanic Sciences"

# ---------------------------------------------------------------- data
df = pd.read_csv(os.path.join(ROOT, "gregory", "analysis", "cesm2_global_annual.csv"))
a = df[df.experiment == "abrupt-4xCO2"].set_index("year").sort_index()
c = df[df.experiment == "piControl"].set_index("year").sort_index().loc[502:]
yr = a.index.values
dT = (a.tas - c.tas.mean()).values
N = (a.N - c.N.mean()).values

def fit(y0, y1):
    m = (yr >= y0) & (yr <= y1)
    s, F = np.polyfit(dT[m], N[m], 1)
    return F, -s, F / -s

F150, B150, T150 = fit(1, 150)
F20, B20, T20 = fit(1, 20)
F21, B21, T21 = fit(21, 150)
late = yr > yr.max() - 50
TL, NL = dT[late].mean(), N[late].mean()

# ---------------------------------------------------------------- figures
figstyle.use()
INK, ACC, BLUE, GREY = figstyle.INK, figstyle.ACCENT, figstyle.ACCENT2, figstyle.GREY
m150 = yr <= 150

def tag(ax, s):
    ax.text(0.01, 0.98, s, transform=ax.transAxes, va="top", fontsize=16)

# time series, full width
fig, (ax1, ax2) = figstyle.figure("full", 1, 2)
fig.set_size_inches(12.1, 3.05)
for ax, v, lab in [(ax1, dT, "ΔT (K)"), (ax2, N, "N (W m⁻²)")]:
    ax.plot(yr[m150], v[m150], color=INK, lw=1.8)
    for y, col in [(1, BLUE), (50, ACC)]:
        ax.plot(y, v[y - 1], "o", ms=10, color=col, zorder=3)
        ax.annotate(f"year {y}", (y, v[y - 1]), textcoords="offset points",
                    xytext=((12, 2) if y == 1 else (10, -18)) if ax is ax1 else (6, 22), color=col, fontsize=14)
    ax.set_xlabel("Year after CO₂ quadrupling"); ax.set_ylabel(lab); ax.set_xlim(0, 150)
ax2.axhline(0, color=GREY, lw=1.2, ls="--"); ax1.set_ylim(0, 8.5); ax2.set_ylim(-0.5, 9)
tag(ax1, "  (a)"); ax2.text(0.92, 0.98, "(b)", transform=ax2.transAxes, va="top", fontsize=16)
figstyle.save(fig, os.path.join(FIG, "timeseries.png"))

# board example, square-ish beside text
fig, ax = figstyle.figure("tall")
x = np.linspace(0, 4, 50)
ax.plot(x, 8 - 2 * x, color=ACC, label="N = 8 − 2ΔT")
ax.axhline(0, color=GREY, lw=1.2, ls="--")
ax.plot([1, 3], [6, 2], "o", ms=11, color=INK, zorder=3)
ax.annotate("year 1", (1, 6), xytext=(10, 6), textcoords="offset points", fontsize=14)
ax.annotate("year 50", (3, 2), xytext=(10, 6), textcoords="offset points", fontsize=14)
ax.plot(0, 8, "o", ms=11, mfc="none", mec=ACC, mew=2.5); ax.plot(4, 0, "o", ms=11, mfc="none", mec=ACC, mew=2.5)
ax.annotate("forcing\n8 W m⁻²", (0, 8), xytext=(14, 0), textcoords="offset points", fontsize=14, color=ACC)
ax.annotate("equilibrium\n4 K", (4, 0), xytext=(10, 12), textcoords="offset points", fontsize=14, color=ACC)
ax.set_xlim(-0.1, 5.4); ax.set_ylim(-1, 9)
ax.set_xlabel("Surface warming ΔT (K)"); ax.set_ylabel("TOA imbalance N (W m⁻²)")
figstyle.save(fig, os.path.join(FIG, "board.png"))

# energy balance model, one layer and two layer, against CESM2
def ebm(F, B, C, gamma, CD=100.0, years=150, dt=0.05):
    T = TD = 0.0; out = [(0, 0.0)]
    for k in range(1, int(years / dt) + 1):
        up = gamma * (T - TD)
        T += dt * (F - B * T - up) / C; TD += dt * up / CD
        if k % int(1 / dt) == 0: out.append((k * dt, T))
    t, T = np.array(out).T
    return t, T, F - B * T

Cml = 1025 * 3990 * 75 / 3.156e7          # 75 m mixed layer, W yr m-2 K-1
GAMMA = 0.7
t1, T1, N1 = ebm(F150, B150, Cml, 0.0)
t2, T2, N2 = ebm(F150, B150, Cml, GAMMA)
fig, (ax1, ax2) = figstyle.figure("full", 1, 2)
fig.set_size_inches(12.1, 4.1)
ax1.plot(yr[m150] - 0.5, dT[m150], "o", ms=3.5, color=GREY, label="CESM2")
ax1.plot(t1, T1, color=ACC, label="one layer, γ = 0")
ax1.plot(t2, T2, color=BLUE, label=f"two layer, γ = {GAMMA}")
ax1.set_xlabel("Year after CO₂ quadrupling"); ax1.set_ylabel("ΔT (K)"); ax1.set_xlim(0, 150); ax1.set_ylim(0, 11)
ax1.legend(loc="lower right")
ax2.plot(dT[m150], N[m150], "o", ms=3.5, color=GREY)
ax2.plot(T1, N1, color=ACC); ax2.plot(T2, N2, color=BLUE, ls="--")
ax2.axhline(0, color=GREY, lw=1.2, ls="--")
ax2.set_xlabel("ΔT (K)"); ax2.set_ylabel("N (W m⁻²)"); ax2.set_xlim(0, 11); ax2.set_ylim(-0.5, 9)
tag(ax1, "  (a)"); ax2.text(0.92, 0.98, "(b)", transform=ax2.transAxes, va="top", fontsize=16)
figstyle.save(fig, os.path.join(FIG, "ebm.png"))

# CESM2 Gregory diagram with three fits
fig, ax = figstyle.figure("left")
e = yr <= 20; l = (yr > 20) & m150
ax.plot(dT[e], N[e], "o", ms=5, color=BLUE, alpha=0.8)
ax.plot(dT[l], N[l], "o", ms=4, color=GREY, alpha=0.8)
for (F, B, T), col, ls, lab in [((F20, B20, T20), BLUE, "--", "years 1–20"),
                                ((F21, B21, T21), INK, "--", "years 21–150"),
                                ((F150, B150, T150), ACC, "-", "years 1–150")]:
    xx = np.array([0, T]); ax.plot(xx, F - B * xx, color=col, ls=ls, label=lab)
ax.axhline(0, color=GREY, lw=1.2, ls=":")
ax.set_xlim(0, 13); ax.set_ylim(-0.5, 10)
ax.set_xlabel("Surface warming ΔT (K)"); ax.set_ylabel("TOA imbalance N (W m⁻²)")
ax.legend(loc="upper right")
figstyle.save(fig, os.path.join(FIG, "gregory_fits.png"))

# 999-year check, full width
fig, (ax1, ax2) = figstyle.figure("full", 1, 2)
fig.set_size_inches(12.1, 4.2)
sc = ax1.scatter(dT, N, c=yr, s=9, cmap="cividis", zorder=2)
xx = np.array([0, T150]); ax1.plot(xx, F150 - B150 * xx, color=ACC, label="fit to years 1–150")
ax1.axhline(0, color=GREY, lw=1.2, ls="--")
ax1.set_xlabel("Surface warming ΔT (K)"); ax1.set_ylabel("N (W m⁻²)")
ax1.set_xlim(0, 13.5); ax1.set_ylim(-1, 10); ax1.legend(loc="upper right")
cb = fig.colorbar(sc, ax=ax1, pad=0.01); cb.set_label("Year"); cb.outline.set_visible(False)
ax2.plot(yr, dT, color=INK, lw=1.2)
ax2.axhline(T150, color=ACC, ls="--", label=f"years 1–150 estimate, {T150:.1f} K")
ax2.axvline(150, color=GREY, lw=1.2, ls=":")
ax2.set_xlabel("Year after CO₂ quadrupling"); ax2.set_ylabel("ΔT (K)")
ax2.set_xlim(0, yr.max()); ax2.set_ylim(0, 13); ax2.legend(loc="lower right")
tag(ax1, "  (a)"); tag(ax2, "  (b)")
figstyle.save(fig, os.path.join(FIG, "check999.png"))

# ---------------------------------------------------------------- notes from the Slidev deck
md = open(os.path.join(ROOT, "gregory-lecture.md")).read()
NOTES = [re.sub(r"\s+", " ", n).strip() for n in re.findall(r"<!--(.*?)-->", md, flags=re.S)]
assert len(NOTES) == 12, len(NOTES)
NOTES[0] = ("Lecture plan, about 50 minutes, with two discussion pauses (slides 3 and 6) and one board exercise "
            "(slide 6). This is the editable PowerPoint version of the Slidev deck. Slides 8 and 10 are static "
            "versions of the interactive slides; to run the sliders, present those two from the browser with "
            "npm run gregory. Figures are rebuilt from the CMIP6 archive by gregory/pptx/build_pptx.py.")
NOTES[7] = (f"Both curves use the CESM2 forcing and slope from the years 1-150 fit, {F150:.1f} W m-2 and "
            f"{B150:.2f} W m-2 K-1, with a 75 m mixed layer. The one-layer model reaches equilibrium within a few "
            f"decades, with a timescale C/B of about {Cml / B150:.0f} years. Adding deep-ocean uptake with gamma = "
            f"{GAMMA} gives a fast and a slow part, as in CESM2, but the Gregory line stays straight because N still "
            "equals dF - B dT. The CESM2 points curve on the right panel, which neither model reproduces. That "
            "curvature is the subject of the last part. The live version of this slide has sliders for each parameter.")
NOTES[9] = (f"The fit for years 1-150 gives {F150:.1f} W m-2, B = {B150:.2f} W m-2 K-1 and an equilibrium warming "
            f"of {T150:.1f} K, so ECS of about {T150 / 2:.1f} K. This matches the 5.2 K that Zelinka et al. (2020) "
            f"report for CESM2 with the same method. The early years give a steeper slope (B = {B20:.2f}) and the "
            f"later years a shallower one (B = {B21:.2f}), which crosses N = 0 at {T21:.1f} K. The crossing is only an "
            "estimate because the geographic pattern of surface warming changes, so the global radiative response "
            "per kelvin can change as well. He et al. (2026), Figure 2, shows the same comparison.")

# ---------------------------------------------------------------- CU Boulder chrome on the Deck helper
D.BODY_PT, D.CAPTION_PT, D.TITLE_PT = 17, 13, 30
D.TITLE_RGB = RGBColor(0, 0, 0)
D.C_TOP, D.C_BOT = 1.6, 6.5
D.FOOT_Y = 7.07                       # slide number sits inside the footer bar
D.FOOT_RGB = RGBColor(0xCF, 0xB8, 0x7C)
D.TEXT_W.update(left=4.3, right=5.0, tall=5.6)
D.SLOT_W["right"] = 6.6
GOLD = RGBColor(0xCF, 0xB8, 0x7C); BLACK = RGBColor(0, 0, 0)
MUTED = RGBColor(0x56, 0x5A, 0x5C)
SRC_Y = 6.6


class CUSlides(D.Deck):
    def __init__(self):
        super().__init__(font="Arial")

    def _rect(self, s, x, y, w, h, rgb):
        r = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
        r.fill.solid(); r.fill.fore_color.rgb = rgb; r.line.fill.background(); r.shadow.inherit = False
        return r

    def _footer(self, s, cover=False):
        self._rect(s, 0, 6.95, D.W, 0.55, BLACK)
        s.shapes.add_picture(LOGO, Inches(0.3), Inches(7.04), height=Inches(0.36))
        if not cover:
            self._box(s, DEPT, 3.5, 7.07, D.W - 7.0, 0.3, 11, color=GOLD, align=PP_ALIGN.CENTER)

    def title_slide(self, title, subtitle, author, notes=""):
        s = self.p.slides.add_slide(self.p.slide_layouts[6]); self.n += 1
        s.background.fill.solid(); s.background.fill.fore_color.rgb = BLACK
        self._box(s, title, 0.9, 2.0, D.W - 1.8, 1.0, 44, bold=True, color=GOLD, anchor=MSO_ANCHOR.BOTTOM)
        self._rect(s, 0.9, 3.12, D.W - 1.8, 0.03, GOLD)
        self._box(s, subtitle, 0.9, 3.35, D.W - 1.8, 0.6, 24, color=RGBColor(255, 255, 255))
        self._box(s, author, 0.9, 4.15, D.W - 1.8, 0.4, 16, color=RGBColor(0xA2, 0xA4, 0xA3))
        self._footer(s, cover=True)
        if notes: s.notes_slide.notes_text_frame.text = notes
        return s

    def slide(self, title, notes=""):
        s = super().slide(title, notes)
        self._rect(s, 0, 0, D.W, 0.06, GOLD)
        self._rect(s, D.M, D.TITLE_Y + D.TITLE_H + 0.08, D.W - 2 * D.M, 0.045, GOLD)
        return s

    def prose(self, s, paras, top=None, pt=None, width=None, x=None):
        """Several paragraphs on a text-led lecture slide, drawn immediately. Each item is a string,
        or a list of (text, bold) runs. Returns the text box."""
        x = D.M if x is None else x
        tb = s.shapes.add_textbox(Inches(x), Inches(top or D.C_TOP), Inches(width or D.W - 2 * D.M), Inches(D.C_BOT - (top or D.C_TOP)))
        tf = tb.text_frame; tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = Inches(0)
        for i, para in enumerate(paras):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.space_after = Pt(10)
            kind = "p"
            if isinstance(para, tuple) and para[0] in ("eq", "bullet", "context"):
                kind, para = para
            runs = para if isinstance(para, list) else [(para, False)]
            if kind == "eq": p.alignment = PP_ALIGN.CENTER
            if kind == "bullet":
                pPr = p._p.get_or_add_pPr(); pPr.set("marL", str(int(0.28 * 914400))); pPr.set("indent", str(-int(0.28 * 914400)))
                from lxml import etree; from pptx.oxml.ns import qn
                etree.SubElement(pPr, qn("a:buFont")).set("typeface", "Arial"); etree.SubElement(pPr, qn("a:buChar")).set("char", "•")
            for text, bold in runs:
                r = p.add_run(); r.text = text; r.font.name = "Arial"; r.font.bold = bold
                r.font.size = Pt((pt or D.BODY_PT) + (4 if kind == "eq" else 0) - (2 if kind == "context" else 0))
                r.font.color.rgb = MUTED if kind == "context" else D.INK
        return tb

    def _place(self, s):
        src = s._spec.pop("source", None); s._spec["source"] = None
        self._footer(s)               # draw the bar first so the slide number sits on top of it
        super()._place(s)
        if src: self._box(s, src, D.M, SRC_Y, D.W - 2 * D.M, 0.3, 11, color=RGBColor(0x7A, 0x7A, 0x7A))


d = CUSlides()
B = lambda t: (t, True)
R = lambda t: (t, False)

# 1
d.title_slide("Gregory Diagrams", "Estimating equilibrium warming from an unfinished simulation",
              "Will Chapman   Fall 2026", notes=NOTES[0])

# 2
s = d.slide("How much warming is still to come?", NOTES[1])
d.prose(s, [
    "Suppose we abruptly increase CO₂ in a coupled climate model and then hold it fixed. The model continues to warm for decades as the ocean takes up heat.",
    "After 150 years, the run tells us how much warming has occurred so far. How can we estimate the warming that would occur if we kept running the model?",
    ("context", [B("Why not just keep running it? "), R("The deep ocean adjusts over centuries to millennia. A coupled model would need thousands of simulated years to reach equilibrium, so most CMIP abrupt-4×CO₂ runs stop at 150 years.")]),
    ("context", [R("The warming at equilibrium for "), B("doubled"), R(" CO₂ is the "), B("equilibrium climate sensitivity (ECS)"), R(", the most widely quoted number about any climate model.")]),
], top=1.9, pt=20)

# 3
s = d.slide("Is the climate still gaining energy?", NOTES[2])
d.prose(s, [
    "At the top of the atmosphere, Earth absorbs shortwave radiation and emits longwave radiation. The difference is the net energy flux into the climate system.",
    ("eq", "R_TOA = ASR − OLR"),
    ("bullet", [B("ASR"), R(" is absorbed shortwave radiation, about 240 W m⁻² in the global mean.")]),
    ("bullet", [B("OLR"), R(" is outgoing longwave radiation, also about 240 W m⁻².")]),
    [R("All fluxes are global means in W m⁻². A positive R_TOA means the climate system is gaining energy. At equilibrium, incoming and outgoing energy balance on average. Today the observed imbalance is about "), B("+1 W m⁻²"), R(", less than 1% of either term.")],
    [B("Discussion. "), R("Where does most of the extra energy go while the climate warms?")],
], top=1.75, pt=19)

# 4
s = d.slide("Forcing and the response to warming", NOTES[3])
d.table(s, ["Feedback", "Effect on B (W m⁻² K⁻¹)"],
        [["Planck (hotter emits more)", "about +3.2, stabilising"], ["Water vapour", "reduces B"],
         ["Lapse rate", "increases B"], ["Surface albedo (snow, ice)", "reduces B"],
         ["Clouds", "reduces B in most models"]], side="right", pt=15, row_h=0.46)
d.caption(s, "CMIP6 models give a net B of roughly 0.5 to 1.8 W m⁻² K⁻¹, so feedbacks cancel much of the Planck response.")
d.prose(s, [
    [B("CO₂ changes the energy budget. "), R("Immediately after CO₂ increases, less longwave radiation escapes to space. The planet starts gaining energy before the surface has warmed appreciably.")],
    [B("Warming changes the energy budget again. "), R("A warmer planet tends to emit more longwave radiation. Changes in clouds and surface reflectivity also affect the net flux.")],
    "As warming proceeds, the net radiative response can offset more of the original forcing. The TOA imbalance then decreases even though CO₂ remains fixed.",
], top=1.75, pt=16, width=5.4)
d.source(s, "Feedback ranges from Zelinka et al. (2020), CMIP6.")

# 5
s = d.slide("An abrupt CO₂ experiment", NOTES[4])
d.figure(s, os.path.join(FIG, "timeseries.png"), side="full")
d.caption(s, "Annual global means from CESM2 abrupt-4×CO₂ minus the piControl mean. Year 1 and year 50 are marked in both panels.")
d.text(s, "Start a control run at preindustrial CO₂ and an abrupt-4×CO₂ run from the same state, with CO₂ quadrupled and held fixed. "
          "Each year, ΔT is the change in global surface air temperature (K) and N the change in net downward TOA radiation (W m⁻²), relative to the control.")
d.source(s, "CESM2 abrupt-4×CO₂ and piControl, r1i1p1f1, CMIP6.")

# 6
s = d.slide("From two time series to one Gregory diagram", NOTES[5])
d.table(s, ["Illustrative year", "ΔT (K)", "N (W m⁻²)"], [["Year 1", "1", "6"], ["Year 50", "3", "2"]],
        side="left", pt=18, row_h=0.55)
d.text(s, bullets=["Each dot pairs ΔT and N from the same year.",
                   "Put ΔT on the horizontal axis and N on the vertical axis.",
                   "Which way does the model move as it warms?",
                   "Has it reached energy balance by year 50?"])
d.caption(s, f"Numbers rounded for the board. CESM2 gives year 1 at ({dT[0]:.1f} K, {N[0]:.1f} W m⁻²) "
             f"and year 50 at ({dT[49]:.1f} K, {N[49]:.1f} W m⁻²).")

# 7
s = d.slide("Why fit a straight line?", NOTES[6])
d.prose(s, [
    "Recall the 0D energy balance model from Lecture 3.",
    ("eq", "C dΔT/dt = N = ΔF − BΔT"),
    "ΔF is the imposed radiative forcing in W m⁻². The restoring coefficient B is the decrease in net downward radiation per kelvin of warming, in W m⁻² K⁻¹. C is the heat capacity per unit area, in J m⁻² K⁻¹.",
    "With fixed forcing and constant B, plotting N against ΔT gives a straight line with slope −B. In a coupled model, we fit that line to the annual points and use the slope to estimate the net radiative response to warming.",
    ("context", [B("Two limits fix the line. "), R("At the start, ΔT = 0 so N = ΔF. At equilibrium, N = 0 so ΔT_eq = ΔF/B. The heat capacity C sets how fast the model moves along the line, not where the line is.")]),
], top=1.75, pt=18)

# 8
s = d.slide("The 0D model under abrupt forcing", NOTES[7])
d.figure(s, os.path.join(FIG, "ebm.png"), side="full")
d.caption(s, f"C dΔT/dt = ΔF − BΔT − γ(ΔT − ΔT_D), with ΔF = {F150:.1f} W m⁻², B = {B150:.2f} W m⁻² K⁻¹ "
             f"and a 75 m mixed layer, against CESM2 years 1–150 (grey).")
d.source(s, "Two-layer model of Held et al. (2010) with a deep-ocean heat capacity of 100 W yr m⁻² K⁻¹.")

# 9
s = d.slide("Reading the Gregory diagram", NOTES[8])
d.figure(s, os.path.join(FIG, "board.png"), side="tall")
d.text(s, bullets=["The vertical intercept at ΔT = 0 estimates the effective radiative forcing.",
                   "The slope −B is the change in N per kelvin of warming.",
                   "The horizontal intercept at N = 0 estimates the equilibrium warming.",
                   "Prediction: with the same forcing and a shallower slope, where does the line cross N = 0?"])
d.caption(s, "The board points give N = 8 − 2ΔT, which reaches N = 0 at 4 K, so 1 K more after year 50.")

# 10
s = d.slide("A Gregory diagram from CESM2", NOTES[9])
d.figure(s, os.path.join(FIG, "gregory_fits.png"), side="left")
d.text(s, bullets=[f"Years 1–150 give B = {B150:.2f} W m⁻² K⁻¹ and cross N = 0 at {T150:.1f} K.",
                   f"Years 1–20 give B = {B20:.2f} W m⁻² K⁻¹ and cross at {T20:.1f} K.",
                   f"Years 21–150 give B = {B21:.2f} W m⁻² K⁻¹ and cross at {T21:.1f} K.",
                   f"Half the years 1–150 crossing gives ECS ≈ {T150 / 2:.1f} K."])
d.caption(s, "Each point is one year of CESM2 abrupt-4×CO₂; lines are least-squares fits.")
d.source(s, "CESM2 abrupt-4×CO₂, r1i1p1f1, CMIP6; He et al. (2026), Figure 2.")

# 11
s = d.slide("The 150-year estimate against 999 years", NOTES[10])
d.figure(s, os.path.join(FIG, "check999.png"), side="full")
d.caption(s, f"By years {yr[late][0]}–{yr[late][-1]} CESM2 has warmed {TL:.1f} K and still gains {NL:.1f} W m⁻², "
             f"above the {T150:.1f} K given by the fit to years 1–150.")
d.source(s, "CESM2 abrupt-4×CO₂, r1i1p1f1, years 1–999, CMIP6.")

# 12
s = d.slide("References", NOTES[11])
refs = [
    "Gregory, J. M., et al. (2004). A new method for diagnosing radiative forcing and climate sensitivity. Geophys. Res. Lett., 31, L03205. doi:10.1029/2003GL018747",
    "He, et al. (2026). CESM2 time series and Gregory diagram, Figures 1 and 2. J. Geophys. Res. Atmos. doi:10.1029/2026JD046855",
    "Held, I. M., et al. (2010). Probing the fast and slow components of global warming by returning abruptly to preindustrial forcing. J. Climate, 23, 2418–2427.",
    "Gettelman, A., et al. (2019). High climate sensitivity in the Community Earth System Model version 2 (CESM2). Geophys. Res. Lett., 46, 8329–8337.",
    "Rugenstein, M., et al. (2020). Equilibrium climate sensitivity estimated by equilibrating climate models. Geophys. Res. Lett., 47, e2019GL083898.",
    "Zelinka, M. D., et al. (2020). Causes of higher climate sensitivity in CMIP6 models. Geophys. Res. Lett., 47, e2019GL085782.",
    "Data: CESM2 abrupt-4×CO₂ and piControl, r1i1p1f1, CMIP6 archive (Danabasoglu, 2019).",
]
d.prose(s, [("bullet", r) for r in refs], top=1.75, pt=15)

# text-led slides have no Deck visual; give them the footer through _place
out = d.save(os.path.join(ROOT, "gregory-lecture-editable.pptx"))
print("wrote", out)
