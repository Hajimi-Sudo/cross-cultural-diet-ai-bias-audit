"""
Dataset loader and image transformations for cross-cultural dietary nutrition AI.
Handles multi-cohort images and regression targets:
[mass_g, energy_kcal, protein_g, fat_g, carb_g].
"""

import os
from typing import Optional, List, Tuple
import pandas as pd
import torch
from torch.utils.data import Dataset
from PIL import Image
import torchvision.transforms as T

DEFAULT_TARGET_COLS = ["mass_g", "energy_kcal", "protein_g", "fat_g", "carb_g"]


def get_transforms(is_train: bool = False, image_size: int = 224) -> T.Compose:
    """Returns standard torchvision preprocessing pipelines."""
    normalize = T.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
    if is_train:
        return T.Compose([
            T.Resize((image_size, image_size)),
            T.RandomHorizontalFlip(p=0.5),
            T.RandomRotation(degrees=15),
            T.ColorJitter(brightness=0.1, contrast=0.1, saturation=0.1),
            T.ToTensor(),
            normalize,
        ])
    else:
        return T.Compose([
            T.Resize((image_size, image_size)),
            T.ToTensor(),
            normalize,
        ])


class DietaryNutrientDataset(Dataset):
    """
    PyTorch Dataset for multi-cohort dietary assessment.
    Returns:
        image: torch.Tensor of shape (3, H, W)
        targets: torch.Tensor of shape (5,) containing [mass_g, energy_kcal, protein_g, fat_g, carb_g]
        sample_id: str identifier of the dish/sample
    """
    def __init__(
        self,
        df: pd.DataFrame,
        image_dir: str,
        transform: Optional[T.Compose] = None,
        target_cols: Optional[List[str]] = None
    ):
        self.df = df.reset_index(drop=True)
        self.image_dir = image_dir
        self.transform = transform if transform is not None else get_transforms(is_train=False)
        self.target_cols = target_cols if target_cols is not None else DEFAULT_TARGET_COLS

    def __len__(self) -> int:
        return len(self.df)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor, str]:
        row = self.df.iloc[idx]
        img_name = str(row["image_filename"])
        img_path = os.path.join(self.image_dir, img_name)

        if os.path.exists(img_path):
            image = Image.open(img_path).convert("RGB")
        else:
            # Fallback placeholder image (neutral gray) if image file is not present locally
            image = Image.new("RGB", (224, 224), color=(128, 128, 128))

        if self.transform:
            image = self.transform(image)

        targets_vals = row[self.target_cols].values.astype(float)
        targets = torch.tensor(targets_vals, dtype=torch.float32)
        sample_id = str(row.get("sample_id", f"sample_{idx}"))

        return image, targets, sample_id
