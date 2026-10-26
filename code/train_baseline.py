import os
import sys
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import pandas as pd
import numpy as np

from dataset import DietaryNutrientDataset, get_transforms
from models import NutrientRegressionModel, AtwaterConsistencyLoss
from metrics import evaluate_nutrient_predictions

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.getenv("DIET_BIAS_BASE_DIR", os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
DATA_DIR = os.path.join(BASE_DIR, "data/nutrition5k")
IMAGE_DIR = os.path.join(DATA_DIR, "images")
CKPT_DIR = os.path.join(BASE_DIR, "checkpoints")
RESULTS_DIR = os.path.join(BASE_DIR, "results")

os.makedirs(CKPT_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

def load_nutrition5k_metadata():
    """Parses dish metadata from cafe1 and cafe2."""
    meta_files = [
        os.path.join(DATA_DIR, "metadata/dish_metadata_cafe1.csv"),
        os.path.join(DATA_DIR, "metadata/dish_metadata_cafe2.csv")
    ]
    records = []
    for mf in meta_files:
        if not os.path.exists(mf):
            continue
        with open(mf, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) >= 6:
                    did = parts[0].strip()
                    try:
                        cal = float(parts[1])
                        mass = float(parts[2])
                        fat = float(parts[3])
                        carb = float(parts[4])
                        prot = float(parts[5])
                        records.append({
                            "sample_id": did,
                            "dataset_name": "Nutrition5k",
                            "cultural_domain": "Western",
                            "image_filename": f"{did}.png",
                            "mass_g": mass,
                            "energy_kcal": cal,
                            "protein_g": prot,
                            "fat_g": fat,
                            "carb_g": carb,
                            "provenance_type": "physical_scale_weighed",
                        })
                    except ValueError:
                        continue

    df = pd.DataFrame(records)
    avail_imgs = set(os.listdir(IMAGE_DIR))
    df = df[df["image_filename"].isin(avail_imgs)].copy()
    return df

def train_epoch(model, loader, optimizer, criterion, target_means, target_stds):
    model.train()
    total_loss = 0.0
    for images, targets, _ in loader:
        images = images.to(DEVICE)
        targets = targets.to(DEVICE)

        norm_targets = (targets - target_means) / target_stds

        optimizer.zero_grad()
        preds = model(images)
        loss = criterion(preds, norm_targets)
        loss.backward()
        optimizer.step()

        total_loss += loss.item() * len(images)

    return total_loss / len(loader.dataset)

@torch.no_grad()
def evaluate(model, loader, target_means, target_stds):
    model.eval()
    all_preds = []
    all_targets = []
    all_ids = []

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
    df_eval = pd.DataFrame(all_targets, columns=[f"true_{c}" for c in cols])
    for idx, c in enumerate(cols):
        df_eval[f"pred_{c}"] = all_preds[:, idx]
    df_eval["sample_id"] = all_ids

    eval_energy = evaluate_nutrient_predictions(df_eval, "true_energy_kcal", "pred_energy_kcal")
    eval_carb = evaluate_nutrient_predictions(df_eval, "true_carb_g", "pred_carb_g")

    return df_eval, eval_energy, eval_carb

def main(epochs: int = 20, batch_size: int = 32, lr: float = 1e-4):
    print("=" * 60)
    print("Training Nutrition Regression Baseline on Nutrition5k (Western)")
    print(f"Device: {DEVICE} ({torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'})")
    print("=" * 60)

    df_all = load_nutrition5k_metadata()
    print(f"Total available dishes with verified images: {len(df_all)}")

    splits_dir = os.path.join(DATA_DIR, "dish_ids/splits")
    with open(os.path.join(splits_dir, "overhead_test_ids.txt")) as f:
        test_ids = set(l.strip() for l in f if l.strip())

    df_test = df_all[df_all["sample_id"].isin(test_ids)].copy()
    df_train = df_all[~df_all["sample_id"].isin(test_ids)].copy()

    print(f"Train samples: {len(df_train)} | Test samples: {len(df_test)}")

    raw_train_targets = df_train[["mass_g", "energy_kcal", "protein_g", "fat_g", "carb_g"]].values
    target_means = torch.tensor(raw_train_targets.mean(axis=0), dtype=torch.float32).to(DEVICE)
    target_stds = torch.tensor(raw_train_targets.std(axis=0) + 1e-6, dtype=torch.float32).to(DEVICE)

    train_ds = DietaryNutrientDataset(df_train, IMAGE_DIR, transform=get_transforms(is_train=True))
    test_ds = DietaryNutrientDataset(df_test, IMAGE_DIR, transform=get_transforms(is_train=False))

    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True, num_workers=4, pin_memory=True)
    test_loader = DataLoader(test_ds, batch_size=batch_size, shuffle=False, num_workers=4, pin_memory=True)

    model = NutrientRegressionModel(pretrained=True).to(DEVICE)
    criterion = AtwaterConsistencyLoss(lambda_atwater=0.05)
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-2)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)

    best_mae = float("inf")
    best_ckpt = os.path.join(CKPT_DIR, "nutrition5k_resnet50_best.pth")

    for epoch in range(1, epochs + 1):
        loss = train_epoch(model, train_loader, optimizer, criterion, target_means, target_stds)
        scheduler.step()

        if epoch % 2 == 0 or epoch == epochs:
            df_eval, res_energy, res_carb = evaluate(model, test_loader, target_means, target_stds)
            print(f"Epoch {epoch:02d}/{epochs:02d} | Train Loss: {loss:.4f} | "
                  f"Energy MAE: {res_energy['MAE']:.1f} kcal, MAPE: {res_energy['MAPE (%)']:.1f}% | "
                  f"Carb MAE: {res_carb['MAE']:.1f}g, Target Safe: {res_carb['Carb Within ±15g (%) [ADA Target]']:.1f}%", flush=True)

            if res_energy["MAE"] < best_mae:
                best_mae = res_energy["MAE"]
                torch.save({
                    "epoch": epoch,
                    "model_state": model.state_dict(),
                    "target_means": target_means.cpu(),
                    "target_stds": target_stds.cpu(),
                    "best_energy_mae": best_mae,
                }, best_ckpt)
                df_eval.to_csv(os.path.join(RESULTS_DIR, "in_domain_nutrition5k_test_preds.csv"), index=False)

    print("=" * 60)
    print(f"Training finished! Best Energy MAE: {best_mae:.2f} kcal")
    print(f"Best checkpoint saved to: {best_ckpt}")
    print("=" * 60)

if __name__ == "__main__":
    main()
