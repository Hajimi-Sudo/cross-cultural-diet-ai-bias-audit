# Dataset Characteristics and Label Provenance Audit

This document profiles the benchmark datasets, their acquisition modalities, cultural cuisines, and nutritional label provenances.

---

## 1. Comparative Dataset Landscape

| Dimension | **Nutrition5k** (Google Research, 2021) | **FoodBD** (Ahmed et al., BMC Res Notes 2025) | **Candidate 3rd Cohort: ECUSTFD / NutriImage** |
| :--- | :--- | :--- | :--- |
| **Origin / Region** | United States / Western | Dhaka, Bangladesh / South Asia | East Asia (China / Japan) |
| **Culinary Archetype** | Cafeteria dishes, plated meals, discrete items | Home-cooked and restaurant meals, curries, lentils (*dal*), flatbreads (*ruti*), high-starch rice | Complex stir-fries, mixed hotpots, bento meals, noodles |
| **Sample Size** | ~5,000 unique plates (video & overhead RGB-D) | 3,523 images (1,837 with nutritional metadata) | 1,000+ paired images/volumes (ECUSTFD) |
| **Visual Boundaries** | Discrete, largely separable ingredients | Highly composite, overlapping ingredients, gravies | Mixed ingredients, stir-fried glazes, broths |
| **Acquisition Device** | Controlled multi-camera overhead scanning rig | Smartphone cameras under variable ambient lighting | Smartphone cameras / calibrated markers |
| **Ground-Truth Mass** | High-precision physical weighing scale (grams) | Dietitian visual portion estimation via local household utensils | Scale weighing (grams) / 3D volumetric calibration |
| **Nutrient Composition** | USDA Food and Nutrient Database (SR28) | Food Composition Table for Bangladesh (Shaheen et al.) | National Food Composition Tables (China/Japan) |
| **Target Nutrients** | Total calories (kcal), mass (g), fat, carb, protein | Total calories (kcal), mass (g), fat, carb, protein | Mass (g), volume ($cm^3$), calories, macronutrients |

---

## 2. In-Depth Dataset Profiles

### 2.1 Nutrition5k
- **Citation**: Thames et al., *"Nutrition5k: Towards Automatic Nutritional Understanding of Generic Food"*, IEEE/CVF CVPR 2021.
- **Strengths**: Gold-standard physical weighing of individual ingredients as they are placed on the plate; overhead and multi-angle RGB-D images; high fidelity USDA SR28 nutrient mapping.
- **Limitations**: Restricted to North American cafeteria menus; heavy over-representation of Western salads, grilled meats, and clear grain portions; lack of mixed, stewed, or fried multi-ingredient curries.

### 2.2 FoodBD
- **Citation**: Ahmed et al., *"FoodBD: a polygon-annotated meal image dataset of Bangladeshi cuisines with visual and nutritional labels"*, *BMC Research Notes*, 2025.
- **Strengths**: Authentic real-world South Asian cuisine captured on smartphones; polygon annotations for 67 food classes; enriched with nutritional annotations for 1,837 meals specifically targeted at diabetic dietary assessment.
- **Limitations & Provenance Details**: Nutritional values are derived from expert dietitian estimation rather than direct scale weighing. Serving sizes follow indigenous Bangladeshi household utensils (e.g., standard bowls, cups, spoons). Glycemic load and carbohydrate estimations reflect local preparation methods.

### 2.3 The 3rd Cohort & Note on "ACETADA"
- **Status of ACETADA**: A comprehensive search across PubMed, PMC, CrossRef, and OpenAlex reveals no standard, indexed academic food image dataset titled "ACETADA". If this refers to a private, institutional, or newly proposed cohort, it can be integrated directly via the standardized schema below.
- **Recommended East Asian Counterparts**:
  - **ECUSTFD** (Liang & Li, *Sensors* 2017): East China University of Science and Technology Food Dataset. Contains calibrated volume, mass, and nutritional calculations for complex Asian foods.
  - **NutriImage**: Japanese cafeteria dishes with registered dietitian reference values.

---

## 3. Label Provenance & The "Ground-Truth Gap"

A vital conceptual contribution of this audit is addressing **Label Provenance Discrepancy**:
1. **Physical Scale vs. Dietitian Estimation**: A model trained on Nutrition5k learns physical density distributions. When evaluated against FoodBD, some discrepancy reflects the known human inter-rater error of dietitian visual estimation ($\approx 10\text{--}20\%$).
2. **Food Composition Table (FCT) Variations**: Different FCTs (USDA vs. Bangladesh FCT) account for local agriculture and cooking traditions. For instance, chicken curry prepared in South Asia incorporates substantially more oil/ghee per gram than a Western grilled chicken breast cataloged in USDA SR28.
