"""Annual global means of tas, rsdt, rsut, rlut for CESM2 abrupt-4xCO2 and piControl (CMIP6, r1i1p1f1).

Writes cesm2_global_annual.csv with columns: experiment, year, tas, rsdt, rsut, rlut, N.
N = rsdt - rsut - rlut (net downward TOA flux, W m-2).
"""
import glob, sys
import numpy as np, pandas as pd, xarray as xr

ROOT = "/glade/collections/cmip/CMIP6/CMIP/NCAR/CESM2/{exp}/r1i1p1f1/Amon/{var}/gn/latest/*.nc"
VARS = ["tas", "rsdt", "rsut", "rlut"]
# days per month for the noleap calendar, used for annual means
DPM = np.array([31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31], float)

def annual_global(exp, var):
    out = []
    for f in sorted(glob.glob(ROOT.format(exp=exp, var=var))):
        ds = xr.open_dataset(f, use_cftime=True)
        w = np.cos(np.deg2rad(ds.lat))
        gm = ds[var].weighted(w).mean(("lat", "lon")).values
        yrs = np.array([t.year for t in ds.time.values])
        for y in np.unique(yrs):
            m = yrs == y
            if m.sum() == 12:
                out.append((y, np.sum(gm[m] * DPM) / DPM.sum()))
        print(exp, var, f.split("_")[-1], flush=True)
    return pd.Series(dict(out), name=var)

frames = []
for exp in ["abrupt-4xCO2", "piControl"]:
    df = pd.concat([annual_global(exp, v) for v in VARS], axis=1)
    df.index.name = "year"
    df["N"] = df.rsdt - df.rsut - df.rlut
    df["experiment"] = exp
    frames.append(df.reset_index())
pd.concat(frames).to_csv(sys.argv[1], index=False)
