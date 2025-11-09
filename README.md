# R&D / AI Assignment — Parametric Curve Parameter Estimation

**Final parameters (from `xy_data.csv`):**
- θ (radians): **0.490759**
- θ (degrees): **28.118422°**
- M: **0.021389**
- X: **54.901924**
- L1 loss: **37865.093839**

## Submission
**LaTeX:**  
\left(t\cos(0.490759) - e^{0.021389\lvert t\rvert}\sin(0.3t)\sin(0.490759) + 54.901924,\; 42 + t\sin(0.490759) + e^{0.021389\lvert t\rvert}\sin(0.3t)\cos(0.490759)\right)

**Desmos (parametric):**  
(t*cos(0.490759) - e^(0.021389*abs(t))*sin(0.3*t)*sin(0.490759) + 54.901924, 42 + t*sin(0.490759) + e^(0.021389*abs(t))*sin(0.3*t)*cos(0.490759))

*(Domain for t: 6 ≤ t ≤ 60)*

---

## Method (Short)
- Used the given model:
  - x = t·cos(θ) − e^(M|t|)·sin(0.3t)·sin(θ) + X
  - y = 42 + t·sin(θ) + e^(M|t|)·sin(0.3t)·cos(θ)
- CSV contained only (x, y). As specified, points lie on the curve for 6 < t < 60, so t was assigned as a uniform grid over [6, 60] in row order.
- Optimized (θ, M, X) by minimizing L1 distance Σ|x_obs − x| + |y_obs − y| with bounds:
  - 0° ≤ θ ≤ 50°,  −0.05 < M < 0.05,  0 ≤ X ≤ 100
- Multi-start L-BFGS-B ensured robustness; best solution chosen by minimal loss.

## How to Reproduce
```bash
pip install -r requirements.txt
python fit_curve.py            # expects xy_data.csv in the same folder
```

## Result Visualization
The script also saves a comparison plot to **fit_plot.png**.