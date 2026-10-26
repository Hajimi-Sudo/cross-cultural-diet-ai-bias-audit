import os
import sys
import torch
import pandas as pd
import numpy as np
from torch.utils.data import DataLoader

from dataset import DietaryNutrientDataset, get_transforms
from models import NutrientRegressionModel
from metrics import evaluate_nutrient_predictions
from bland_altman import plot_bland_altman

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.getenv("DIET_BIAS_BASE_DIR", os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
CKPT_DIR = os.path.join(BASE_DIR, "checkpoints")
RESULTS_DIR = os.path.join(BASE_DIR, "results")
ANALYSIS_DIR = os.path.join(BASE_DIR, "analysis")

os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(ANALYSIS_DIR, exist_ok=True)

def run_cross_cultural_audit(ckpt_path: str, datasets_dict: dict):
    print("=" * 70)
    print("Running Cross-Cultural Generalizability & Systematic Bias Audit")
    print(f"Loading checkpoint: {ckpt_path}")
    print("=" * 70)

    checkpoint = torch.load(ckpt_path, map_location=DEVICE)
    model = NutrientRegressionModel(pretrained=False).to(DEVICE)
    model.load_state_dict(checkpoint["model_state"])
    model.eval()

    target_means = checkpoint["target_means"].to(DEVICE)
    target_stds = checkpoint["target_stds"].to(DEVICE)

    summary_rows = []

    for domain_name, (df_meta, image_dir) in datasets_dict.items():
        print(f"\nEvaluating Domain: [{domain_name}] ({len(df_meta)} samples)")
        ds = DietaryNutrientDataset(df_meta, image_dir, transform=get_transforms(is_train=False))
        loader = DataLoader(ds, batch_size=32, shuffle=False, num_workers=2)

        all_preds = []
        all_targets = []
        all_ids = []

        with torch.no_grad():
            for images, targets, s_ids in loader:
                images = images.to(DEVICE)
                preds = model(images)
                unnorm_preds = preds * target_stds + target_means
                unnorm_preds = torch.clamp(unnorm_preds, min=0.0)

                all_preds.append(unnorm_preds.cpu().numpy())
                all_targets.append(targets.numpy())
                all_ids.extend(s_ids)

        all_preds = np.vstack(all_preds)
        all_targets = np.vstack(all_targets)

        cols = ["mass_g", "energy_kcal", "protein_g", "fat_g", "carb_g"]
        df_domain = pd.DataFrame(all_targets, columns=[f"true_{c}" for c in cols])
        for idx, c in enumerate(cols):
            df_domain[f"pred_{c}"] = all_preds[:, idx]
        df_domain["sample_id"] = all_ids
        df_domain.to_csv(os.path.join(RESULTS_DIR, f"preds_{domain_name}.csv"), index=False)

        # Generate Bland-Altman plots for Energy and Carb
        plot_bland_altman(
            y_true=df_domain["true_energy_kcal"].values,
            y_pred=df_domain["pred_energy_kcal"].values,
            endpoint_name="Energy (kcal)",
            culture_label=domain_name,
            output_path=os.path.join(ANALYSIS_DIR, f"bland_altman_{domain_name}_energy.png")
        )
        plot_bland_altman(
            y_true=df_domain["true_carb_g"].values,
            y_pred=df_domain["pred_carb_g"].values,
            endpoint_name="Carbohydrate (g)",
            culture_label=domain_name,
            output_path=os.path.join(ANALYSIS_DIR, f"bland_altman_{domain_name}_carb.png")
        )

        for col in cols:
            eval_res = evaluate_nutrient_predictions(df_domain, f"true_{col}", f"pred_{col}")
            summary_rows.append({
                "Domain": domain_name,
                "Nutrient": col,
                "MAE": eval_res["MAE"],
                "RMSE": eval_res["RMSE"],
                "MAPE (%)": eval_res["MAPE (%)"],
                "Mean Signed Bias": eval_res["Mean Signed Bias"],
                "Mean Pct Error (%)": eval_res["Mean Percentage Error (MPE %)"],
                "Bias p-val": eval_res["Bias p-value"],
                "Lin CCC": eval_res["Lin CCC"],
                "Carb ±15g Safe (%)": eval_res.get("Carb Within ±15g (%) [ADA Target]", np.nan),
                "Carb ±20% Safe (%)": eval_res.get("Carb Within ±20% (%) [Clinical Safe]", np.nan),
            })

    df_summary = pd.DataFrame(summary_rows)
    df_summary.to_csv(os.path.join(RESULTS_DIR, "cross_cultural_evaluation_matrix.csv"), index=False)

    print("\n" + "=" * 70)
    print("Cross-Cultural Evaluation Summary Matrix:")
    print("=" * 70)
    print(df_summary.to_string(index=False))

    return df_summary

if __name__ == "__main__":
    print("Evaluation module loaded successfully.")
