"""
Nutritional Assessment Evaluation Suite:
Calculates standard regression metrics, directional systematic bias,
Bland-Altman statistics, Lin's Concordance Correlation Coefficient (CCC),
and clinical diabetic carbohydrate counting tolerances.
"""

import numpy as np
import pandas as pd
from scipy import stats


def calculate_cv_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict:
    """Standard computer vision regression metrics."""
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    diff = y_pred - y_true

    mae = np.mean(np.abs(diff))
    rmse = np.sqrt(np.mean(diff ** 2))
    
    # Avoid zero division in MAPE
    mask = y_true > 1e-4
    mape = np.mean(np.abs(diff[mask] / y_true[mask])) * 100.0 if np.any(mask) else np.nan

    # Coefficient of determination R^2
    ss_res = np.sum(diff ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    r2 = 1.0 - (ss_res / ss_tot) if ss_tot > 1e-8 else np.nan

    return {
        "MAE": float(mae),
        "RMSE": float(rmse),
        "MAPE (%)": float(mape),
        "R2": float(r2),
    }


def calculate_directional_bias(y_true: np.ndarray, y_pred: np.ndarray) -> dict:
    """Calculates directional systematic bias (Mean Signed Error and MPE)."""
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    diff = y_pred - y_true

    mse_bias = np.mean(diff)  # Mean Signed Error
    
    mask = y_true > 1e-4
    mpe_bias = np.mean(diff[mask] / y_true[mask]) * 100.0 if np.any(mask) else np.nan

    # Wilcoxon signed-rank test or paired t-test for bias significance != 0
    t_stat, p_val = stats.ttest_rel(y_pred, y_true)

    return {
        "Mean Signed Bias": float(mse_bias),
        "Mean Percentage Error (MPE %)": float(mpe_bias),
        "Bias p-value": float(p_val),
    }


def calculate_bland_altman_stats(y_true: np.ndarray, y_pred: np.ndarray) -> dict:
    """Bland-Altman analysis for medical agreement."""
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    
    diff = y_pred - y_true
    means = (y_pred + y_true) / 2.0
    
    mean_diff = np.mean(diff)
    sd_diff = np.std(diff, ddof=1)
    
    loa_lower = mean_diff - 1.96 * sd_diff
    loa_upper = mean_diff + 1.96 * sd_diff

    # Test for proportional bias via OLS regression: diff = beta_0 + beta_1 * means
    slope, intercept, r_val, p_val, std_err = stats.linregress(means, diff)

    return {
        "BA Mean Bias": float(mean_diff),
        "BA SD Diff": float(sd_diff),
        "BA 95% LoA Lower": float(loa_lower),
        "BA 95% LoA Upper": float(loa_upper),
        "Proportional Bias Slope": float(slope),
        "Proportional Bias p-value": float(p_val),
    }


def calculate_concordance_cc(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Lin's Concordance Correlation Coefficient (CCC)."""
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)

    mean_t = np.mean(y_true)
    mean_p = np.mean(y_pred)
    var_t = np.var(y_true, ddof=1)
    var_p = np.var(y_pred, ddof=1)
    
    cov = np.cov(y_true, y_pred)[0, 1]
    
    numerator = 2.0 * cov
    denominator = var_t + var_p + (mean_t - mean_p) ** 2
    
    if denominator < 1e-8:
        return np.nan
    return float(numerator / denominator)


def calculate_clinical_safety(y_true_carb: np.ndarray, y_pred_carb: np.ndarray) -> dict:
    """
    Evaluates clinical compliance with carbohydrate counting tolerance standards
    for diabetes and postprandial insulin management.
    """
    y_true_carb = np.asarray(y_true_carb, dtype=float)
    y_pred_carb = np.asarray(y_pred_carb, dtype=float)
    
    abs_err = np.abs(y_pred_carb - y_true_carb)
    n = len(y_true_carb)
    if n == 0:
        return {}

    pct_within_10g = (np.sum(abs_err <= 10.0) / n) * 100.0
    pct_within_15g = (np.sum(abs_err <= 15.0) / n) * 100.0
    pct_within_20g = (np.sum(abs_err <= 20.0) / n) * 100.0

    mask = y_true_carb > 1e-4
    rel_err = np.abs(abs_err[mask] / y_true_carb[mask])
    pct_within_15pct = (np.sum(rel_err <= 0.15) / len(rel_err)) * 100.0 if len(rel_err) > 0 else np.nan
    pct_within_20pct = (np.sum(rel_err <= 0.20) / len(rel_err)) * 100.0 if len(rel_err) > 0 else np.nan

    return {
        "Carb Within ±10g (%)": float(pct_within_10g),
        "Carb Within ±15g (%) [ADA Target]": float(pct_within_15g),
        "Carb Within ±20g (%)": float(pct_within_20g),
        "Carb Within ±15% (%)": float(pct_within_15pct),
        "Carb Within ±20% (%) [Clinical Safe]": float(pct_within_20pct),
    }


def evaluate_nutrient_predictions(df_results: pd.DataFrame, target_col: str, pred_col: str) -> dict:
    """Runs a complete evaluation suite for a single nutrient endpoint."""
    y_true = df_results[target_col].values
    y_pred = df_results[pred_col].values

    res = {}
    res.update(calculate_cv_metrics(y_true, y_pred))
    res.update(calculate_directional_bias(y_true, y_pred))
    res.update(calculate_bland_altman_stats(y_true, y_pred))
    res["Lin CCC"] = calculate_concordance_cc(y_true, y_pred)
    
    if "carb" in target_col.lower():
        res.update(calculate_clinical_safety(y_true, y_pred))

    return res
