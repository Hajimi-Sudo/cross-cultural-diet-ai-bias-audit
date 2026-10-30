# 投稿投稿信 / Cover Letter for Initial Submission

---

## 1. 中文版本（Chinese Version）

**尊敬的 Frontiers in Nutrition 编辑部与主编:**

我们荣幸地向贵刊“Nutritional Methodology”（营养方法学）专栏提交题为《Directional Error Drift and Diagnostic Concordance in Computerized Dietary Tracking Across Global Food Cultures: A Tri-Cohort Safety Evaluation》（计算机辅助膳食监测在不同饮食文化下的方向性误差偏移与诊断一致性：一项三队列安全性评估）的原创研究（Original Research）论文手稿，诚挚期盼进入同行评审流程。

【研究背景与核心科学问题】准确量化膳食能量与常量营养素摄入是营养流行病学调查与糖尿病血糖精准管理的基础。近年来，智能手机餐食摄影与深度学习视觉算法被广泛寄予厚望以实现自动化的膳食摄入监测。然而，当前计算机视觉营养估算模型几乎完全建立在同质化的北美工作场所机构食堂配餐基准上。当这些算法跨越国界部署于非西方饮食文化时，其在真实世界复杂烹饪基质下的测量可靠度、方向性系统偏倚及其对代谢疾病患者用药安全的潜在危害，此前从未经过严谨的多队列跨文化实证审计。

【核心方法学突破与临床安全性发现】本研究严格遵循 STROBE-nut 营养流行病学报告指南与 TRIPOD-AI 人工智能诊断预测模型规范，构建了跨越三大饮食文化的标准化多队列审计基准（涵盖 3,823 个独立进餐实例）：西方食堂餐盘（Nutrition5k, N=506）、南亚复合咖喱与肉汁食谱（FoodBD, N=1,833）以及东亚离散独立菜品（ECUSTFD, N=1,484）。我们在模型中融入了受 Atwater 生理能量守恒约束的归纳偏置，并通过医学一致性界限（Bland-Altman）、Lin 一致性相关系数以及美国糖尿病协会（ADA）餐时胰岛素计算安全阈值（±15 g 或 ±20%）系统量化了零样本迁移性能。研究证实，在源域西方菜肴中表现无偏的深度模型直接推断南亚餐食时诱发了灾难性的负向碳水化合物严重少算（平均偏差 -18.18 g, p = 8.64 × 10^-206），导致临床胰岛素用药达标率骤降至 49.5%，半数以上餐食面临餐前胰岛素注射不足（漏打 1.2 至 1.8 单位速效胰岛素）与剧烈餐后高血糖（经常超过 180-250 mg/dL）的临床危机；而在东亚菜品上则出现显著的能量正向虚高（+134.7 kcal, p < 10^-300）。正交误差分解从数学上证实，不透明基质内部隐匿的营养密度盲区解释了超过 75% 的跨数据集方差，远超平面轮廓分割误差；而仅需 50 份区域餐食的就地校准即可使临床合规率恢复至 63.9% 并削减 39.6% 的热量误差。

【专栏契合度与投稿合规声明】本手稿与 Frontiers in Nutrition 的“Nutritional Methodology”专栏高度契合，为数字化营养监测系统的测量有效性评估、算法偏见消除与跨人群临床应用提供了首个标准化的审计蓝图。本手稿正文约 8,200 词，包含 3 幅高清矢量/位图插图与 5 个标准三线表，参考文献采用标准的 Frontiers Vancouver 顺序编码制。本研究为公开去标识化科研基准数据的二次计算评估，符合赫尔辛基宣言及国际伦理豁免准则；全体作者均深度参与研究并审阅通过手稿，郑重确认不存在任何商业利益冲突。完整的评估代码与数据接口已在 GitHub 开源（https://github.com/Hajimi-Sudo/cross-cultural-diet-ai-bias-audit）。我们深信该研究将为国际营养学界、数字医疗监管机构与临床内分泌专家带来坚实而切实的科学价值，诚挚期盼将本稿件送交同行评审。

**通讯作者：梁伟军（Weijun Liang），刘翠翠（Cuicui Liu）**  
**邮箱：2018050548@usc.edu.cn, liucuicui@csmu.edu.cn**

---

## 2. 英文版本（English Version）

**Subject: Submission of Original Research Manuscript to Frontiers in Nutrition**

**Dear Specialty Chief Editors and Editorial Board of Frontiers in Nutrition,**

We are pleased to submit our original research manuscript entitled "Directional Error Drift and Diagnostic Concordance in Computerized Dietary Tracking Across Global Food Cultures: A Tri-Cohort Safety Evaluation" for consideration for publication in Frontiers in Nutrition, specifically within the Nutritional Methodology specialty section.

Automated mobile meal photography and deep learning regression represent a rapidly expanding frontier in digital health, offering objective dietary intake tracking for nutritional epidemiology and outpatient cardiometabolic care. However, existing dietary vision models are developed almost exclusively on discrete, planar North American institutional cafeteria benchmarks. When transported across international borders into diverse cultural food traditions, these algorithms encounter uncharacterized compositional shifts and opacity challenges whose measurement reliability, systematic bias directionality, and direct clinical hazards for patient care have never been rigorously audited.

In this investigation, we established a standardized multi-cohort audit benchmark spanning 3,823 eating instances across three distinct cultural traditions: Western institutional plates (Nutrition5k, N=506), South Asian composite curries (FoodBD, N=1,833), and East Asian dishes (ECUSTFD, N=1,484). We evaluated an Atwater energy-constrained multi-task convolutional network using Bland-Altman limits of agreement, Lin concordance correlation, and American Diabetes Association (ADA) prandial carbohydrate bolusing safety thresholds (±15 g or ±20%). While the network demonstrated unbiased carbohydrate estimation in-domain (+0.94 g, p = 0.176), direct transfer to South Asian preparations elicited a profound negative carbohydrate undercounting of -18.18 g (p = 8.64 * 10^-206), depressing clinical dosing compliance from 63.8% to 49.5% and leaving more than half of meal instances vulnerable to prandial insulin under-dosing (1.2 to 1.8 units of missed rapid-acting insulin) and acute postprandial glucose excursions exceeding 180 to 250 mg/dL. In East Asian dishes, cafeteria priors induced significant positive energy inflation (+134.7 kcal, p < 10^-300), posing contrasting hazards of hypoglycemia or over-restriction. Orthogonal error decomposition proved that unobserved nutrient density variations beneath opaque gravies accounted for over 75% of cross-cultural variance, while localized few-shot recalibration with only 50 regional samples recovered clinical compliance to 63.9% and suppressed energy error by 39.6%.

This manuscript aligns directly with the scope of the Nutritional Methodology section of Frontiers in Nutrition, which prioritizes the rigorous validation of dietary assessment tools, measurement error characterization, and the safe integration of digital health technologies into clinical practice. The study adheres strictly to the STROBE-nut and TRIPOD-AI reporting guidelines. The text contains approximately 8,200 words, 3 high-resolution figures, and 5 standard tables formatted in compliance with the Frontiers Vancouver citation style.

All authors have made substantial intellectual contributions to this work, approved the final manuscript, and declared no competing financial interests. This secondary computational investigation analyzed publicly available, fully anonymized benchmark datasets and is exempt from formal institutional review board approval. To support full reproducibility and open science, the complete evaluation suite, data contracts, and calibration routines are publicly accessible at https://github.com/Hajimi-Sudo/cross-cultural-diet-ai-bias-audit.

Given the pressing global need to ensure clinical safety, measurement accuracy, and algorithmic equity in dietary artificial intelligence, we believe our findings will be of substantial interest to the readers, clinical nutritionists, and editorial leadership of Frontiers in Nutrition. Thank you very much for your time and consideration of our submission.

**Sincerely,**  
**Corresponding Authors: Weijun Liang (2018050548@usc.edu.cn), Cuicui Liu (liucuicui@csmu.edu.cn)**