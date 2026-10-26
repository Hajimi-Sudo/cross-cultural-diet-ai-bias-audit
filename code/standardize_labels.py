"""
Data Harmonization Suite:
Standardizes metadata schemas across Nutrition5k, FoodBD, and candidate datasets.
Enforces common columns, unit representations, and provenance tracking.
"""

import pandas as pd
import numpy as np

STANDARDIZED_COLUMNS = [
    "sample_id",           # Unique meal identifier
    "dataset_name",        # Nutrition5k, FoodBD, ECUSTFD, etc.
    "cultural_domain",     # Western, South_Asian, East_Asian
    "image_filename",      # Local relative path to overhead image
    "dish_name",           # Descriptive title / food category
    "mass_g",              # Total meal weight in grams
    "energy_kcal",         # Total energy in kilocalories
    "protein_g",           # Protein in grams
    "fat_g",               # Total fat in grams
    "carb_g",              # Carbohydrate in grams
    "provenance_type",     # 'physical_scale_weighed' vs 'dietitian_visual_estimated'
    "fct_source",          # 'USDA_SR28', 'Bangladesh_FCT', etc.
    "composite_type",      # 'discrete_plated', 'mixed_curry_gravy', 'stir_fry', etc.
]


def validate_schema(df: pd.DataFrame) -> bool:
    """Verifies that a dataframe adheres to the standardized dietary schema."""
    missing = [c for c in STANDARDIZED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Schema violation: Missing required columns: {missing}")

    # Check for non-negative nutritional values
    nutrients = ["mass_g", "energy_kcal", "protein_g", "fat_g", "carb_g"]
    for n in nutrients:
        if (df[n] < 0).any():
            raise ValueError(f"Data integrity error: Negative values detected in {n}")

    # Check physiological consistency: 4*protein + 9*fat + 4*carb ~ energy
    est_energy = 4.0 * df["protein_g"] + 9.0 * df["fat_g"] + 4.0 * df["carb_g"]
    ratio = df["energy_kcal"] / np.maximum(est_energy, 1.0)
    abnormal = ((ratio < 0.5) | (ratio > 1.8)) & (df["energy_kcal"] > 50)
    if abnormal.sum() > 0:
        print(f"Warning: {abnormal.sum()} records exhibit >50% discrepancy between Atwater estimate and energy_kcal.")

    print(f"Schema validation passed: {len(df)} records verified successfully.")
    return True


def generate_synthetic_pilot_benchmark(n_samples: int = 150) -> pd.DataFrame:
    """
    Generates a calibrated synthetic pilot benchmark matching empirical distributions
    of Nutrition5k (Western) and FoodBD (South Asian) for protocol testing and pipeline auditing.
    """
    np.random.seed(42)
    records = []

    # 1. Nutrition5k-like (Western, discrete, scale-weighed)
    n_west = n_samples // 2
    for i in range(n_west):
        mass = np.random.normal(380, 110)
        protein = np.random.normal(32, 12)
        fat = np.random.normal(20, 8)
        carb = np.random.normal(45, 18)
        mass = max(80.0, mass)
        protein = max(5.0, protein)
        fat = max(2.0, fat)
        carb = max(5.0, carb)
        energy = 4.0 * protein + 9.0 * fat + 4.0 * carb + np.random.normal(0, 15)

        records.append({
            "sample_id": f"nutri5k_{i:04d}",
            "dataset_name": "Nutrition5k",
            "cultural_domain": "Western",
            "image_filename": f"images/nutri5k_{i:04d}.jpg",
            "dish_name": np.random.choice(["Grilled Chicken Salad", "Steak with Mash", "Turkey Sandwich", "Salmon with Rice"]),
            "mass_g": round(mass, 1),
            "energy_kcal": round(max(50.0, energy), 1),
            "protein_g": round(protein, 1),
            "fat_g": round(fat, 1),
            "carb_g": round(carb, 1),
            "provenance_type": "physical_scale_weighed",
            "fct_source": "USDA_SR28",
            "composite_type": "discrete_plated",
        })

    # 2. FoodBD-like (South Asian, mixed gravies, dietitian-estimated)
    n_sa = n_samples - n_west
    for i in range(n_sa):
        mass = np.random.normal(450, 140)
        # Higher carbs (rice/roti staples), higher hidden fats (ghee/mustard oil in gravies)
        protein = np.random.normal(22, 9)
        fat = np.random.normal(28, 12)
        carb = np.random.normal(82, 28)
        mass = max(100.0, mass)
        protein = max(4.0, protein)
        fat = max(5.0, fat)
        carb = max(15.0, carb)
        energy = 4.0 * protein + 9.0 * fat + 4.0 * carb + np.random.normal(0, 20)

        records.append({
            "sample_id": f"foodbd_{i:04d}",
            "dataset_name": "FoodBD",
            "cultural_domain": "South_Asian",
            "image_filename": f"images/foodbd_{i:04d}.jpg",
            "dish_name": np.random.choice(["Beef Bhuna with Rice", "Chicken Curry & Ruti", "Egg Curry with Dal", "Fish Gravy with Rice"]),
            "mass_g": round(mass, 1),
            "energy_kcal": round(max(50.0, energy), 1),
            "protein_g": round(protein, 1),
            "fat_g": round(fat, 1),
            "carb_g": round(carb, 1),
            "provenance_type": "dietitian_visual_estimated",
            "fct_source": "Bangladesh_FCT",
            "composite_type": "mixed_curry_gravy",
        })

    df = pd.DataFrame(records)
    validate_schema(df)
    return df


if __name__ == "__main__":
    df = generate_synthetic_pilot_benchmark()
    print("\nSummary by Cultural Domain:")
    print(df.groupby("cultural_domain")[["mass_g", "energy_kcal", "carb_g", "fat_g", "protein_g"]].mean())
