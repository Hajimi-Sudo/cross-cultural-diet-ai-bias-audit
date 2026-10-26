# Cross-Cultural Generalizability & Systematic Bias in Dietary Nutrition AI

## Working Title

**Cross-Cultural Generalizability and Systematic Bias in Image-Based Dietary Energy and Macronutrient Estimation: A Multi-Dataset Evaluation Protocol**

## Scope

- **Discipline**: Medicine / Nutritional Epidemiology / Digital Health / AI Dietary Assessment
- **Study Type**: Multi-cohort cross-cultural evaluation, algorithmic fairness audit, and clinical safety validation
- **Target Journal**: *Frontiers in Nutrition* (Section: Nutritional Methodology or Nutritional Epidemiology)
- **Primary Clinical Endpoints**:
  1. Directional systematic bias (Mean Percentage Error / Bland-Altman mean bias) in energy (kcal) and macronutrient (carbohydrate, protein, fat in grams) estimation when transferring models across diverse cultural cuisines.
  2. Clinical tolerance violation rate in dietary carbohydrate estimation (proportion of meals exceeding $\pm 15\text{g}$ or $\pm 20\%$ error, the clinical safety threshold for postprandial glycemic control and insulin dosing in diabetic management).
  3. Disentanglement of error components: Visual food category recognition failure vs. portion/mass estimation discrepancy vs. regional food composition table (FCT) nutrient density divergence.
- **Reference Guidelines**:
  - STROBE-nut (Strengthening the Reporting of Observational Studies in Epidemiology - Nutritional Epidemiology)
  - EQUATOR Network TRIPOD / STARD-AI reporting standards for AI diagnostic evaluation
  - American Diabetes Association (ADA) and International Diabetes Federation (IDF) standards of medical care in carbohydrate counting

## Datasets

- **Primary Western Benchmark**: **Nutrition5k** (Google Research, CVPR 2021)
  - ~5,000 unique real-world cafeteria dishes, RGB-D imagery.
  - Ground truth: Physical weighing on precision scale + USDA SR28 nutrient composition database.
  - Cultural archetype: Discrete, plated, Western dishes with visible boundaries.
- **Primary South Asian Benchmark**: **FoodBD** (BMC Research Notes 2025)
  - 3,523 smartphone meal images (1,837 with dietitian-annotated nutritional metadata).
  - Ground truth: Registered dietitian portion estimation using traditional household utensils (e.g., katori/bati) + Bangladesh Food Composition Tables.
  - Cultural archetype: Composite, mixed dishes, gravies, curries, and high-starch staples.
- **Candidate East Asian Benchmark / External Validation 2**: **ECUSTFD** (East China University of Science and Technology Food Dataset) / **NutriImage** (Japanese dishes with dietitian gold standards) / candidate 3rd cohort (e.g. verifying user-specified ACETADA or Chinese complex composite dishes).

## Frozen Boundaries

- **Do not frame this as a pure computer science / CVPR benchmark paper**:
  - The core innovation is NOT inventing an arbitrary neural network architecture or loss function.
  - The manuscript must remain firmly grounded in nutritional science, measurement validity, public health risks of AI bias in non-Western populations, and algorithmic fairness.
- **Strictly prohibit random pooling and shuffling across datasets**:
  - Datasets must NOT be concatenated and randomly split into 70/15/15 train/val/test sets. That obscures cultural distribution shifts and introduces severe data leakage and domain confounding.
  - Evaluation must strictly follow a **Zero-Shot Cross-Dataset Transfer Matrix** and **Few-Shot Domain Adaptation** protocol.
- **Address Label Provenance as an Explicit Scientific Dimension**:
  - Nutrition5k utilizes scale-weighed physical mass; FoodBD utilizes expert visual portion estimation.
  - Explicitly model and discuss how much discrepancy stems from:
    (a) cross-cultural visual domain shifts,
    (b) human visual portion estimation error,
    (c) local Food Composition Table (FCT) preparation/recipe variations (e.g., hidden cooking oil and ghee in curries).
- **Report Medical and Clinical Utility Metrics**:
  - Beyond standard computer vision metrics (MAE, RMSE, MAPE), mandatory reporting includes:
    1. Mean Signed Error (MSE / Directional Bias: indicating systematic over- or under-estimation).
    2. Bland-Altman 95% Limits of Agreement (LoA) with proportional bias regression.
    3. Lin's Concordance Correlation Coefficient (CCC).
    4. Clinical Carbohydrate Safety Tolerances: % of predictions within $\pm 10\text{g}$, $\pm 15\text{g}$, and $\pm 20\%$.

## Fatal Flaws to Avoid

1. Randomly mixing images from different datasets during training, which creates artificial data leakage and destroys cultural boundary analysis.
2. Reporting only aggregate $R^2$ or MAE while concealing directional bias (e.g., a model that constantly underestimates calories in South Asian curries by 40% might have a moderate MAE, but is clinically hazardous).
3. Ignoring the difference between "weighed food record" labels and "dietitian visual estimation" labels.
4. Failing to connect carbohydrate estimation errors to practical clinical endpoints (such as insulin dosing risks in diabetic patients).

## Local LaTeX Environment

Always compile with the local TeX Live 2022 binaries per workspace instructions:
`PATH=/root/code/rh-workspace/latex/texlive/2022/bin/x86_64-linux:$PATH`
Helper script: `/root/code/rh-workspace/latex/use-texlive2022.sh`
Target template: `FrontiersinVancouver.cls` with `Frontiers-Vancouver.bst`
