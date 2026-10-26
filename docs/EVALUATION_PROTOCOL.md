# Cross-Cultural Dietary Assessment Evaluation Protocol

This protocol establishes the standardized metrics, mathematical definitions, and validation matrices for auditing cross-dataset generalizability and systematic bias in image-based dietary assessment.

---

## 1. Mathematical Metric Definitions

Let $y_i$ denote the ground-truth value (energy in kcal, or macronutrient mass in grams) for meal $i \in \{1, \dots, N\}$, and let $\hat{y}_i$ denote the model's predicted value.

### 1.1 Conventional Performance Metrics
- **Mean Absolute Error (MAE)**:
  $$\text{MAE} = \frac{1}{N} \sum_{i=1}^N |\hat{y}_i - y_i|$$
- **Root Mean Squared Error (RMSE)**:
  $$\text{RMSE} = \sqrt{\frac{1}{N} \sum_{i=1}^N (\hat{y}_i - y_i)^2}$$
- **Mean Absolute Percentage Error (MAPE)**:
  $$\text{MAPE} = \frac{1}{N} \sum_{i=1}^N \left| \frac{\hat{y}_i - y_i}{y_i} \right| \times 100\%$$

### 1.2 Directional Systematic Bias Metrics
- **Mean Signed Error (MSE / Absolute Bias)**:
  $$\text{Bias} = \frac{1}{N} \sum_{i=1}^N (\hat{y}_i - y_i)$$
  *Interpretation*: Positive value indicates systematic overestimation; negative value indicates systematic underestimation.
- **Mean Percentage Error (MPE / Relative Directional Bias)**:
  $$\text{MPE} = \frac{1}{N} \sum_{i=1}^N \left( \frac{\hat{y}_i - y_i}{y_i} \right) \times 100\%$$

### 1.3 Medical Agreement & Concordance Metrics
- **Bland-Altman 95% Limits of Agreement (LoA)**:
  For difference $d_i = \hat{y}_i - y_i$, with sample mean $\bar{d}$ and standard deviation $s_d$:
  $$\text{LoA} = \left[ \bar{d} - 1.96 \cdot s_d, \;\; \bar{d} + 1.96 \cdot s_d \right]$$
  A proportional bias test is conducted via linear regression: $d_i = \beta_0 + \beta_1 \cdot \frac{\hat{y}_i + y_i}{2} + \epsilon_i$. A significant slope ($\beta_1 \ne 0$, $p < 0.05$) indicates magnitude-dependent systematic bias.
- **Lin's Concordance Correlation Coefficient (CCC)**:
  Combines precision (Pearson correlation $r$) and accuracy (distance from the $45^\circ$ line):
  $$\rho_c = \frac{2 r \sigma_y \sigma_{\hat{y}}}{\sigma_y^2 + \sigma_{\hat{y}}^2 + (\mu_y - \mu_{\hat{y}})^2}$$

### 1.4 Clinical Safety & Metabolic Thresholds
Following American Diabetes Association (ADA) and clinical carbohydrate counting standards for type 1 and type 2 diabetes management:
- **$\text{Comp}_{\le 15\text{g}}$ (Absolute Carbohydrate Safety Rate)**:
  $$\text{Comp}_{\le 15\text{g}} = \frac{1}{N} \sum_{i=1}^N \mathbb{I}(|\hat{y}_{i, \text{carb}} - y_{i, \text{carb}}| \le 15\text{g}) \times 100\%$$
- **$\text{Comp}_{\le 20\%}$ (Relative Carbohydrate Safety Rate)**:
  $$\text{Comp}_{\le 20\%} = \frac{1}{N} \sum_{i=1}^N \mathbb{I}\left(\left| \frac{\hat{y}_{i, \text{carb}} - y_{i, \text{carb}}}{y_{i, \text{carb}}} \right| \le 0.20\right) \times 100\%$$

---

## 2. Cross-Dataset Evaluation Matrix

To prevent data leakage and evaluate real-world cultural domain transfer, experiments must execute the following evaluation matrix:

| Training Domain ($D_{train}$) | Target Evaluation Domain ($D_{test}$) | Experimental Role |
| :--- | :--- | :--- |
| **Nutrition5k (Western)** | **Nutrition5k Test Split** | In-domain performance upper bound (weighed gold standard). |
| **Nutrition5k (Western)** | **FoodBD (South Asian)** | **Zero-shot Cross-Cultural Transfer**: Measures Western model bias on South Asian mixed dishes. |
| **Nutrition5k (Western)** | **3rd Cohort (East Asian / ECUSTFD)** | **Zero-shot Cross-Cultural Transfer**: Measures Western model bias on East Asian stir-fry / composite dishes. |
| **FoodBD (South Asian)** | **FoodBD Test Split** | In-domain performance upper bound on South Asian cuisine. |
| **FoodBD (South Asian)** | **Nutrition5k Test Split** | **Reverse Cross-Cultural Transfer**: Tests whether South Asian model overestimates simple Western dishes. |
| **Foundation VLMs (Zero-Shot)** | **Nutrition5k / FoodBD / 3rd Cohort** | Benchmark of state-of-the-art multimodal LLMs (GPT-4o, Claude 3.5, Qwen2-VL) under identical zero-shot prompts. |
| **Few-Shot Adaptation (10%, 20%)** | **Target Domain** | Quantifies parameter-efficient adaptation cost to eliminate directional bias in low-resource diets. |

---

## 3. Orthogonal Error Decomposition Framework

The total estimation error is decomposed into three sequential, clinically interpretable stages:
$$\Delta_{\text{total}} = \mathcal{F}(\Delta_{\text{recognition}}, \Delta_{\text{portion/volume}}, \Delta_{\text{FCT/density}})$$

1. **Stage 1: Food Recognition / Taxonomy Error**: Did the vision model fail to recognize culturally specific food items (e.g., mistaking *dal* for lentil soup, or *roti* for pita)?
2. **Stage 2: Portion / Volume Estimation Error**: Holding the food category constant, did the model fail to account for container geometry (katori vs. plate) and packing density?
3. **Stage 3: Nutrient Density / FCT Discrepancy**: Holding food volume and category constant, how much error is driven by recipe variation (ghee, palm oil, hidden carbohydrates) vs. standard composition tables?
