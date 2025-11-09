import numpy as np
import pandas as pd
from scipy.optimize import minimize
import matplotlib.pyplot as plt

CSV_PATH = "xy_data.csv"  # path to your CSV with columns x,y (no t column)

def curve(t, theta, M, X):
    exp_term = np.exp(M * np.abs(t)) * np.sin(0.3 * t)
    c, s = np.cos(theta), np.sin(theta)
    x = t * c - exp_term * s + X
    y = 42 + t * s + exp_term * c
    return x, y

def main():
    df = pd.read_csv(CSV_PATH)
    x_obs = df['x'].to_numpy(dtype=float)
    y_obs = df['y'].to_numpy(dtype=float)
    n = len(df)
    t = np.linspace(6, 60, n)

    def loss(params):
        theta, M, X = params
        x_pred, y_pred = curve(t, theta, M, X)
        return np.sum(np.abs(x_obs - x_pred) + np.abs(y_obs - y_pred))

    bounds = [(np.deg2rad(0), np.deg2rad(50)), (-0.05, 0.05), (0, 100)]

    best = (np.inf, None)
    rng = np.random.default_rng(0)
    starts = [[np.deg2rad(25), 0.0, 50.0]]
    for _ in range(40):
        starts.append([
            rng.uniform(np.deg2rad(0), np.deg2rad(50)),
            rng.uniform(-0.05, 0.05),
            rng.uniform(0, 100)
        ])

    for s0 in starts:
        res = minimize(loss, s0, bounds=bounds, method='L-BFGS-B')
        if res.fun < best[0]:
            best = (res.fun, res.x)

    best_loss, (theta_opt, M_opt, X_opt) = best
    print("Theta (rad):", theta_opt, "| Theta (deg):", np.rad2deg(theta_opt))
    print("M:", M_opt)
    print("X:", X_opt)
    print("L1 loss:", best_loss)

    x_fit, y_fit = curve(t, theta_opt, M_opt, X_opt)
    plt.figure(figsize=(7,6))
    plt.plot(x_obs, y_obs, '.', markersize=2, label='Observed')
    plt.plot(x_fit, y_fit, '-', linewidth=2, label='Fitted')
    plt.legend(); plt.xlabel('x'); plt.ylabel('y'); plt.title('Parametric Curve Fit')
    plt.tight_layout(); plt.savefig("fit_plot.png", dpi=160)

    # Submission strings
    latex = ("\\left(t\\cos({:.6f}) - e^{{{:.6f}\\lvert t\\rvert}}"
             "\\sin(0.3t)\\sin({:.6f}) + {:.6f},\\; "
             "42 + t\\sin({:.6f}) + e^{{{:.6f}\\lvert t\\rvert}}"
             "\\sin(0.3t)\\cos({:.6f})\\right)".format(theta_opt, M_opt, theta_opt, X_opt, theta_opt, M_opt, theta_opt))
    desmos = ("(t*cos({:.6f}) - e^({:.6f}*abs(t))*sin(0.3*t)*sin({:.6f}) + {:.6f}, "
              "42 + t*sin({:.6f}) + e^({:.6f}*abs(t))*sin(0.3*t)*cos({:.6f}))".format(theta_opt, M_opt, theta_opt, X_opt, theta_opt, M_opt, theta_opt))
    print("\nLaTeX:\n", latex)
    print("\nDesmos:\n", desmos)

if __name__ == "__main__":
    main()