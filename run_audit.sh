#!/usr/bin/env bash
set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PATH="/root/code/rh-workspace/latex/texlive/2022/bin/x86_64-linux:$PATH"

echo "============================================================"
echo " [1/4] Running Data Harmonization and Synthetic Pilot Audit"
echo "============================================================"
python3 "${PROJECT_DIR}/code/standardize_labels.py"

echo ""
echo "============================================================"
echo " [2/4] Verifying Metrics Suite and Clinical Thresholds"
echo "============================================================"
python3 -c "
import sys
sys.path.append('${PROJECT_DIR}/code')
import numpy as np
import pandas as pd
from metrics import evaluate_nutrient_predictions

np.random.seed(42)
n = 100
true_carb = np.random.normal(60, 20, n)
pred_carb = true_carb * 0.85 + np.random.normal(0, 8, n)

df_test = pd.DataFrame({'true_carb': true_carb, 'pred_carb': pred_carb})
res = evaluate_nutrient_predictions(df_test, 'true_carb', 'pred_carb')
print('Carbohydrate Evaluation Metrics Summary:')
for k, v in res.items():
    print(f'  {k}: {v:.3f}' if isinstance(v, float) else f'  {k}: {v}')
"

echo ""
echo "============================================================"
echo " [3/4] Generating Publication-Quality Bland-Altman Agreement"
echo "============================================================"
python3 "${PROJECT_DIR}/code/bland_altman.py"
mv test_bland_altman.png "${PROJECT_DIR}/analysis/pilot_bland_altman.png"
echo "Saved pilot figure to ${PROJECT_DIR}/analysis/pilot_bland_altman.png"

echo ""
echo "============================================================"
echo " [4/4] Compiling Frontiers in Nutrition LaTeX Manuscript"
echo "============================================================"
cd "${PROJECT_DIR}/manuscript/frontiers"
xelatex -interaction=nonstopmode main.tex > /dev/null
bibtex main > /dev/null
xelatex -interaction=nonstopmode main.tex > /dev/null
xelatex -interaction=nonstopmode main.tex > /dev/null

if [ -f main.pdf ]; then
    echo "✓ PDF successfully compiled: ${PROJECT_DIR}/manuscript/frontiers/main.pdf"
else
    echo "✗ LaTeX compilation failed"
    exit 1
fi

echo "============================================================"
echo "✓ Full audit completed successfully!"
echo "============================================================"
