import torch
import torch.nn as nn
import torchvision.models as models

class AtwaterConsistencyLoss(nn.Module):
    """
    Physiological Loss:
    Enforces Atwater energy balance: Energy ~ 4 * Protein + 9 * Fat + 4 * Carb
    """
    def __init__(self, lambda_atwater: float = 0.05):
        super().__init__()
        self.smooth_l1 = nn.SmoothL1Loss(reduction="mean")
        self.lambda_atwater = lambda_atwater

    def forward(self, pred: torch.Tensor, target: torch.Tensor):
        base_loss = self.smooth_l1(pred, target)

        pred_energy = pred[:, 1]
        pred_protein = torch.clamp(pred[:, 2], min=0.0)
        pred_fat = torch.clamp(pred[:, 3], min=0.0)
        pred_carb = torch.clamp(pred[:, 4], min=0.0)

        calc_energy = 4.0 * pred_protein + 9.0 * pred_fat + 4.0 * pred_carb
        atwater_loss = self.smooth_l1(pred_energy, calc_energy)

        return base_loss + self.lambda_atwater * atwater_loss


class NutrientRegressionModel(nn.Module):
    """
    Multi-task visual nutrition estimation model using torchvision ResNet-50.
    Predicts 5 continuous endpoints:
    [0: mass_g, 1: energy_kcal, 2: protein_g, 3: fat_g, 4: carb_g]
    """
    def __init__(self, pretrained: bool = True, dropout: float = 0.2):
        super().__init__()
        weights = models.ResNet50_Weights.DEFAULT if pretrained else None
        base = models.resnet50(weights=weights)
        self.features = nn.Sequential(*list(base.children())[:-1])
        num_features = 2048

        self.regressor = nn.Sequential(
            nn.Flatten(),
            nn.Linear(num_features, 512),
            nn.BatchNorm1d(512),
            nn.SiLU(),
            nn.Dropout(dropout),
            nn.Linear(512, 128),
            nn.BatchNorm1d(128),
            nn.SiLU(),
            nn.Dropout(dropout),
            nn.Linear(128, 5),
            nn.ReLU(),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        feat = self.features(x)
        return self.regressor(feat)


if __name__ == "__main__":
    model = NutrientRegressionModel(pretrained=True)
    x = torch.randn(4, 3, 224, 224)
    y = model(x)
    print("Model output shape:", y.shape)
    crit = AtwaterConsistencyLoss()
    target = torch.randn(4, 5).abs()
    loss = crit(y, target)
    print("Atwater-regularized loss:", loss.item())
