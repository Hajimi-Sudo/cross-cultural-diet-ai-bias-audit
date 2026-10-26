# 摘要与关键词（中英双语同步对应）

## 1. 英文摘要与关键词

### Abstract
Computer vision dietary intake assessment holds transformative potential for nutritional epidemiology and diabetic glycemic management, yet current algorithms are developed predominantly on Western cafeteria benchmarks with uncharacterized cross-cultural generalizability. To assess directional bias and metabolic risks across diverse culinary traditions, we established an audit protocol across 3,823 meal photographs from three cohorts: Nutrition5k (Western baseline, $N=506$), FoodBD (South Asian composite meals, $N=1,833$), and ECUSTFD (East Asian discrete dishes, $N=1,484$). An Atwater-regularized deep neural network was evaluated under zero-shot transfer for directional systematic bias (Mean Signed Error, paired $t$-test), Bland-Altman agreement, Lin concordance correlation, and American Diabetes Association carbohydrate safety thresholds ($\pm 15$\,g and $\pm 20\%$). In-domain Western assessment demonstrated unbiased carbohydrate estimation (Mean Signed Bias $+0.94$\,g, $p = 0.176$, $63.8\%$ safety compliant). In contrast, zero-shot transfer to South Asian meals provoked catastrophic negative carbohydrate bias (Mean Signed Bias $-18.18$\,g, $p = 8.64 \times 10^{-206}$), collapsing clinical compliance to $49.5\%$ and placing over half of meals in the hazardous insulin bolusing zone. On East Asian dishes, Western cafeteria priors induced positive energy bias ($+134.7$\,kcal, $p < 10^{-300}$). Mechanistic error decomposition revealed that over $75\%$ of cross-cultural estimation error arose from internal nutrient density collapse rather than surface segmentation deviation. Localized calibration on 50 target meals restored clinical safety compliance to $63.9\%$ and attenuated energy error by $39.6\%$. These results demonstrate that vision-based models inherit culturally bound compositional priors that cause severe estimation bias, highlighting multi-cohort auditing and localized recalibration as essential requirements for clinical safety and algorithmic equity in global digital health.

### Keywords
dietary intake assessment, cross-cultural generalizability, systematic estimation bias, deep learning, carbohydrate counting, algorithmic fairness, type 2 diabetes mellitus

---

## 2. 中文摘要与关键词

### 摘要
基于计算机视觉的膳食评估在营养流行病学与糖尿病管理中具有重大应用价值，但现有算法几乎全部在西方食堂数据上训练，其跨饮食文化的估算偏差方向尚未得到验证。为了评估模型跨文化迁移时的系统偏差与代谢安全风险，本研究建立了涵盖 3,823 张图像的标准审计协议，纳入西方基准（Nutrition5k，$N=506$）、南亚复合餐食（FoodBD，$N=1,833$）与东亚离散食品（ECUSTFD，$N=1,484$）三组队列。我们在西方菜肴上训练了受 Atwater 生理能量守恒约束的多任务神经网络，并在零样本迁移下系统评估平均带符号误差、Bland-Altman 一致性与美国糖尿病协会碳水化合物安全阈值（$\pm 15$\,g 和 $\pm 20\%$）。实验表明，该模型在西方域内估算无偏（碳水化合物平均偏差 $+0.94$\,g，安全合规率 $63.8\%$）。迁移至南亚餐食时诱发了严重的负向低估（碳水化合物偏差 $-18.18$\,g，$p = 8.64 \times 10^{-206}$），使安全合规率骤降至 $49.5\%$ 并显著增加胰岛素误给风险。东亚菜肴则表现出能量正向高估（$+134.7$\,kcal）。误差分解表明超过 $75\%$ 的跨文化误差源于内部营养密度盲区而非轮廓分割，而 50 份餐食的就地校准即可将安全合规率恢复至 $63.9\%$ 并降低 $39.6\%$ 的能量误差。本研究证实视觉模型会继承特定文化先验并诱发危及患者安全的方向性偏差，确立了多队列审计与就地重校准作为保障全球数字营养系统测量可靠性与算法公平性的必要路径。

### 关键词
膳食摄入评估, 跨文化泛化性, 系统性估算偏差, 深度学习, 碳水化合物计算, 算法公平性, 2型糖尿病

---

## 3. 关键词中英对照表

| 序号 | 英文关键词 | 中文关键词 | 概念层级 |
| :--- | :--- | :--- | :--- |
| 1 | dietary intake assessment | 膳食摄入评估 | 核心应用领域 |
| 2 | cross-cultural generalizability | 跨文化泛化性 | 研究核心问题 |
| 3 | systematic estimation bias | 系统性估算偏差 | 核心评估终点 |
| 4 | deep learning | 深度学习 | 方法技术类型 |
| 5 | carbohydrate counting | 碳水化合物计算 | 临床专科任务 |
| 6 | algorithmic fairness | 算法公平性 | 医学伦理与公平性 |
| 7 | type 2 diabetes mellitus | 2型糖尿病 | 目标临床人群 |
