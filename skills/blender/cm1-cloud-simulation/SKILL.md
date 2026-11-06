---
name: cm1-cloud-simulation
description: Use when building or running NCAR CM1 on the Macs to simulate supercells, squall lines or cumulus LES (BOMEX, towering Cu) for rendering in Blender — setup, namelists, memory, monitoring and known failures.
---

# Running CM1 to make clouds

Clouds for the Blender scenes come from our own CM1 runs (supercell, cumulus LES). Converting output to VDB and rendering is in `cm1-clouds-to-blender`; lightning in `blender-cloud-lightning`.

## Machines
- **M3 Max MacBook** (14 cores, 30-core GPU, 36 GB, disk tight): `~/Documents/blender/farm_amf2/cm1/`, env `cm1/env/`. Lid closed = CM1 paused (resumes on wake).
- **Mac Studio M1 Ultra** (20 cores, 64 GB): env `cm1/env_studio/`. Use it fully but leave ~15 % for Scott; no new renders while CM1 runs.
- **MacBook Air** (M4, 24 GB): renders only; project root is `~/blender/farm_amf2/`.

## Build
- conda/mamba env (conda-forge): gfortran, netcdf-fortran, make, git, python 3.12, numpy, netCDF4 (no scipy).
- `git clone --depth 1` NCAR CM1 into `cm1/CM1/` (if the clone fails on lock files, clone elsewhere and copy).
- conda's `cpp` is clang and treats `.F` as Fortran — override:
  `make CPP="cpp -x c -C -P -traditional -Wno-invalid-pp-token -ffreestanding" FC=gfortran USE_OPENMP=true USE_NETCDF=true NETCDFBASE=<env>` (serial, ~4 min). Wrapped in `cm1/build.sh`.
- Custom source edits (e.g. nudging position in `init3d.F`) require a rebuild per run; keep build logs `build_<run>.log`.

## Running
- `run_cm1.sh <rundir> [threads]`: OMP_NUM_THREADS, `OMP_STACKSIZE=512M`, `ulimit -s 65532`, `GFORTRAN_UNBUFFERED_PRECONNECTED=y` (live log), `caffeinate -i nice -n 10` → `cm1.log`, ending `CM1_EXIT <code>`.
- Progress: `grep -a ' min ' cm1.log | tail -1`; `cm1out_stats.nc` has per-minute thpmin, wmax, qctop, dt.
- `watchdog_cm1.sh`: SIGSTOP cm1.exe below ~12–15 % free, SIGCONT above 25–30 %.
- **Memory:** keep CM1 ≤ ~26–30 GB on the Studio. A 768²×152 domain (~44 GB) drove macOS into compression (~2 model-min/h). `memory_pressure` is misleading — watch `vm_stat` compressor pages and cm1.exe RSS.
- CM1 at nice 10 yields to CPU Blender renders (3–5× slower); GPU renders coexist fine.
- macOS has no `timeout`; bash is 3.2 (no associative arrays).
- Wrap launch + watchdog in `go_<run>.sh`; chain conversion after `CM1_EXIT`.

## Supercell recipe (current best: Studio run E)
Base: `config_files/supercell` (Morrison 2-moment + hail, WENO-5, TKE, netCDF one file per time `output_format=2 output_filetype=2`, `adapt_dt=1`).
- Sounding: Weisman–Klemp `isnd=5` (θ_sfc 300 K, PBL qv 14 g/kg, tropopause 12 km; SBCAPE ~1.9–2.4 kJ/kg). Hodograph `iwnd=2` quarter circle, 0–6 km shear 32 m/s.
- Initiation: updraft nudging `iinit=12` (Naylor & Gilmore 2012: w → 10 m/s at 1.5 km, radius 10 km, off at 20 min), `irandp=1`. Set `xc_wnudge`/`yc` in `init3d.F` (domain centre for a stretched grid).
- Box motion: Bunkers right mover `umove/vmove = 13.4/−1.4` (compute with MetPy from the sounding). With a near-left-mover drift the right mover walks out of the box.
- Grid: dz 30 → 150 m stretched over 0–7.2 km (`stretch_z`, `dz_bot 30`, `dz_top 150`, `str_top 7200`), top 18 km. **Horizontal stretching** `stretch_x/y=1, dx_inner 100, dx_outer 1000, nos_len 36000, tot_len 150400` → 104+360+104 = 568 points, 150 km, 36 km inner at 100 m. CM1 requires tot = dx_in·ni2 + 2·ni1·(dx_in+dx_out)/2 exactly; check the log's 104/360/104.
- Free-slip lower boundary, no surface fluxes. `dtl 1.0` (adaptive dt is capped at 2×dtl, so set dtl ≈ half the dt you expect).
- Output every minute (`tapfrq 60`) for timelapses: ~80–90 GB for 90 min; lean variables (th, prs, qv, q, dbz, w). Restarts every 15–30 min.
- Cost: ~9 h wall on 16 threads, RSS ~25 GB, ~9–14 model-min/h.

### Why this recipe (lessons)
- Uniform 100 m in a 48–58 km box: the anvil hits the walls by 40 min and renders as flat box-edge walls. The stretched 150 km domain fixes it ("we need a larger domain" — Scott).
- Resolution: 500 m = soft blobs; 250 m = right macro shapes, pillowy; 100 m = sharp cauliflower turrets, flanking-line lip, ~1.5× peak graupel/rain. 250 m (100×100 km, 90 min, ~8.6 CPU-h, 7 GB) is the cheap all-rounder.
- Storms split; the "core" from a max search jumps between movers — track both.
- Coffer et al. (arXiv 2210.03715) style 80 m / NSSL 2-moment is out of memory budget here.

## Cumulus LES recipes
Common: `cm1setup=1`, `sgsmodel=1` (TKE), `ipbl=0`, advection order 5, `advwenos=2`, `weno_order=5`, `idiff=0`, `irandp=1`, periodic laterals, lean output.
- **BOMEX** (`les_ShallowCu`, testcase 3): works. `bomex50` = 50 m / 25 m, 128²×120 (6.4 km, 3 km top), Morrison, 6 h, output 20 min → shallow trade Cu, ~13 % cover, bases ~600 m, tops to ~1.9 km.
- **Towering Cu `tcu100`**: testcase 0, `sfcmodel=1`, constant fluxes `set_flx=1 cnst_shflx=0.12 cnst_lhflx=1.3e-4 set_ust=1` (0.3 m/s), custom `input_sounding` (SGP-like PBL, weak cap at 2.5 km, moist mid-levels, CAPE ~840), 100 m, 128²×130 (12.8 km, top 14 km), Morrison no hail, 8 h, 12 threads ~2.5 h. Shallow Cu from 80 min, breaks through at ~5 h, tops 7–8 km with snow/graupel/rain shafts by 7–8 h.
- **ARM SGP land case (testcase 14, `les_ShallowCuLand`) blows up** at cloud onset (~3.8 h: lowest-level cloud domain-wide, thpmin → −300 K, exit 143) regardless of microphysics, resolution or threads. Suspect the testcase 14 / `sfcmodel=5` surface path. Use the tcu100 approach instead.
- Thompson is `ptype=3` (not 28); Morrison 5; Rotunno–Emanuel 6. `shcond`, `itarget`, `itrans` are not CM1 options.

## After the run
Record in a project doc: namelist differences, sounding stats, core positions and cloud extents per time, wall time, RSS, disk, verdicts on the renders. Copy converted VDBs to Drive `My Drive/blends/farm_amf2/cm1/runs/<run>/` from a Popen'd script (never `ls`/`du` Drive inside a Blender MCP call — it hangs).
