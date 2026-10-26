"""
Bland-Altman Agreement Visualization:
Generates publication-quality agreement plots with mean bias lines,
95% Limits of Agreement (LoA), and proportional bias regression overlays.
"""

import matplotlib.pyplot as plt
import numpy as np
import os
from scipy import stats


def plot_bland_altman(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    endpoint_name: str = "Energy (kcal)",
    culture_label: str = "Cross-Cultural Transfer",
    output_path: str = "bland_altman.png"
):
    """
    Renders and saves a standardized medical Bland-Altman agreement plot.
    """
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)

    means = (y_pred + y_true) / 2.0
    diffs = y_pred - y_true

    mean_diff = np.mean(diffs)
    sd_diff = np.std(diffs, ddof=1)
    loa_upper = mean_diff + 1.96 * sd_diff
    loa_lower = mean_diff - 1.96 * sd_diff

    # Proportional bias regression
    slope, intercept, r_val, p_val, _ = stats.linregress(means, diffs)
    x_vals = np.linspace(np.min(means), np.max(means), 100)
    reg_line = intercept + slope * x_vals

    plt.figure(figsize=(8, 6), dpi=300)
    plt.scatter(means, diffs, alpha=0.55, edgecolors="none", c="#1f77b4", s=30, label="Meal Predictions")
    
    # Zero line (perfect agreement)
    plt.axhline(0, color="gray", linestyle=":", linewidth=1.2, label="Zero Bias Line")

    # Mean bias line
    plt.axhline(mean_diff, color="#d62728", linestyle="-", linewidth=1.8,
                label=f"Mean Bias: {mean_diff:+.1f}")

    # 95% Limits of Agreement
    plt.axhline(loa_upper, color="#2ca02c", linestyle="--", linewidth=1.4,
                label=f"+1.96 SD: {loa_upper:+.1f}")
    plt.axhline(loa_lower, color="#2ca02c", linestyle="--", linewidth=1.4,
                label=f"-1.96 SD: {loa_lower:+.1f}")

    # Proportional bias trendline if p < 0.05
    if p_val < 0.05:
        plt.plot(x_vals, reg_line, color="purple", linestyle="-.", linewidth=1.4,
                 label=f"Prop. Bias Trend (p={p_val:.3f})")

    plt.title(f"Bland-Altman Agreement: {endpoint_name}\n[{culture_label}]", fontsize=12, pad=12)
    plt.xlabel(f"Mean of True and Predicted {endpoint_name}", fontsize=11)
    plt.ylabel(f"Difference (Predicted - True) [{endpoint_name}]", fontsize=11)
    plt.legend(loc="upper left", bbox_to_anchor=(1.02, 1), fontsize=9, frameon=True)
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()

    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()
    print(f"Bland-Altman plot saved to {output_path}")


if __name__ == "__main__":
    np.random.seed(42)
    # Simulate Nutrition5k model evaluated on South Asian meals:
    # True calories ~550 kcal, model systematically underpredicts by 22% due to hidden oils/curries
    y_true_sim = np.random.normal(550, 120, 200)
    y_pred_sim = y_true_sim * 0.78 + np.random.normal(0, 45, 200)

    plot_bland_altman(
        y_true=y_true_sim,
        y_pred=y_pred_sim,
        endpoint_name="Dietary Energy (kcal)",
        culture_label="Nutrition5k Trained Model -> FoodBD Test",
        output_path="test_bland_altman.png"
    )
