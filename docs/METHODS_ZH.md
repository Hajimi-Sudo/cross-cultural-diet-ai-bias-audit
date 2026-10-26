# 材料与方法（中文完整对应稿）

膳食评估框架将跨文化视觉不确定性转化为严格的多层级审计协议。该流程通过受热力学常量营养素守恒定律约束的深度卷积网络，将单视角餐食照片映射为多目标营养向量。所得预测在严格的数据域隔离下跨三个饮食文化群体进行审计，以量化方向性系统偏差、临床一致性与代谢安全性。机制性误差分解进一步将物理体积估算偏差与内部营养密度盲区解耦，为极低样本的就地校准协议提供理论依据。这一运作流程确保了特征表征、生理正则化与临床评估的每个阶段均具备完全的可溯源性与可复现性。

## 2.1 多队列研究人群与数据标准化协议

为在无领域混杂的前提下评估跨文化泛化性，本研究整合了三个真实世界食物基准数据集，涵盖北美、南亚和东亚饮食传统及差异化的金标准标注方法。

西方基准队列（Nutrition5k）由谷歌研究院在北美企业食堂餐饮设施中采集。真值通过在餐食组装前后对各成分进行工业级精密电子秤称重确定，并映射至美国农业部膳食研究食品与营养数据库（USDA SR28）。基线训练集包含 2,749 份餐食，官方俯视测试集包含 506 份在受控食堂光照下由天顶 RGB 传感器拍摄的测试餐食。

南亚基准队列（FoodBD）由 Ahmed 等人在孟加拉国达卡的真实家庭与餐馆场景中采集。共评估了 1,833 张包含完整营养标注的餐食图像。金标准营养量由持有执业资质的注册营养师使用标准化区域家用器具（如 katori 碗、传统匙、水杯）进行视觉份量估算，并映射至孟加拉国食物成分表。餐食具有复杂的混合菜肴特征，包括大量香料烹制的肉类与鱼类咖喱、bhunas、shak 以及与白米饭或扁面包主食搭配的扁豆浓汤。

东亚基准队列（ECUSTFD）由华东理工大学 Liang 与 Li 采集。该库包含 2,978 张高分辨率食物图像。为匹配 Nutrition5k 与 FoodBD 的天顶拍摄视角，提取了全部 1,484 张顶视图像。食物质量（克）与体积边界通过精密数字天平及物理圆形校准硬币测定，营养数值通过中国食物成分表关联。数据主要涵盖离散菜品、包子馒头、水果与点心小吃。

为确保异质标注源之间的完全互操作性，三个队列均纳入统一数据契约，严格执行十三个不变字段：`sample_id`、`dataset_name`、`cultural_domain`、`image_filename`、`dish_name`、`mass_g`、`energy_kcal`、`protein_g`、`fat_g`、`carb_g`、`provenance_type`、`fct_source` 和 `composite_type`。

## 2.2 问题形式化与多任务网络架构

设 $\mathbf{X} \in \mathbb{R}^{3 \times H \times W}$ 表示输入 RGB 餐食照片，空间尺寸为 $H = W = 224$ 像素。膳食计算机视觉的目标是学习映射 $f: \mathbf{X} \mapsto \hat{\mathbf{y}}$，其中 $\hat{\mathbf{y}}$ 是涵盖五个关键营养量的连续向量：
\begin{equation}
    \label{eq:output_vector}
    \hat{\mathbf{y}} = \left[ \hat{M}, \hat{E}, \hat{P}, \hat{F}, \hat{C} \right]^T \in \mathbb{R}_{\ge 0}^5
\end{equation}
在式 (1) 中，$\hat{M}$ 表示预测的餐食总质量（克），$\hat{E}$ 表示预测的膳食能量（千卡），$\hat{P}$ 表示预测的蛋白质质量（克），$\hat{F}$ 对应预测的总脂肪质量（克），$\hat{C}$ 表示预测的碳水化合物质量（克）。

网络架构将卷积特征提取器与多阶段非线性投影头耦合。特征提取由在 ImageNet 上预训练的深度残差网络 (ResNet-50) 执行。对于输入照片 $\mathbf{X}$，来自最终残差块的空间特征图通过全局平均池化层进行聚合，生成紧凑的视觉潜在嵌入 $\mathbf{h} = f_\theta(\mathbf{X}) \in \mathbb{R}^{2048}$。

为了将高维视觉嵌入 $\mathbf{h}$ 映射为相互关联的营养目标，构建了带有两个连续全连接变换块的专用回归头 $g_\phi$。第一级中间投影通过式 (2) 将 $\mathbf{h}$ 转换为 512 维隐状态：
\begin{equation}
    \label{eq:projection_head_one}
    \mathbf{h}_1 = \text{Dropout}_{0.2}\left( \text{SiLU}\left( \text{BatchNorm}\left( \mathbf{W}_1 \mathbf{h} + \mathbf{b}_1 \right) \right) \right)
\end{equation}
其中 $\mathbf{W}_1 \in \mathbb{R}^{512 \times 2048}$ 表示权重矩阵，$\mathbf{b}_1 \in \mathbb{R}^{512}$ 为偏置向量，$\text{BatchNorm}(\cdot)$ 稳定异质营养尺度下的中间梯度分布，$\text{SiLU}(u) = u \cdot \sigma(u)$ 提供连续非线性激活，$\text{Dropout}_{0.2}(\cdot)$ 应用 20% 的丢弃率以防止训练期间的特征共适应。

第二级投影块通过式 (3) 将 $\mathbf{h}_1$ 压缩为 128 维潜在表征：
\begin{equation}
    \label{eq:projection_head_two}
    \mathbf{h}_2 = \text{Dropout}_{0.2}\left( \text{SiLU}\left( \text{BatchNorm}\left( \mathbf{W}_2 \mathbf{h}_1 + \mathbf{b}_2 \right) \right) \right)
\end{equation}
权重矩阵为 $\mathbf{W}_2 \in \mathbb{R}^{128 \times 512}$，偏置为 $\mathbf{b}_2 \in \mathbb{R}^{128}$。最终，终端输出向量在式 (4) 中通过受非负激活约束的线性投影生成：
\begin{equation}
    \label{eq:terminal_output}
    \hat{\mathbf{y}} = \text{ReLU}\left( \mathbf{W}_3 \mathbf{h}_2 + \mathbf{b}_3 \right)
\end{equation}
其中 $\mathbf{W}_3 \in \mathbb{R}^{5 \times 128}$，$\mathbf{b}_3 \in \mathbb{R}^5$。终端线性整流单元 $\text{ReLU}(u) = \max(0, u)$ 保证所有估计的营养质量与能量数值严格非负，杜绝了生理上不可能出现的负值估计。

## 2.3 生理正则化与复合训练目标

标准的无约束回归网络经常生成违背基本热力学原理的预测，例如在常量营养素质量接近零的情况下预测出高热量值。为消除非生理性预测，引入了基于 Atwater 建立的燃烧热系数的归纳偏置。对于任何餐食，理论膳食能量受常量营养素组成的物理约束：
\begin{equation}
    \label{eq:atwater_consistency}
    \hat{E}_{\text{Atwater}} = 4.0 \hat{P} + 9.0 \hat{F} + 4.0 \hat{C}
\end{equation}
在式 (5) 中，$4.0$\,kcal/g 作为蛋白质与碳水化合物的能量当量，而 $9.0$\,kcal/g 对应膳食脂质。

生理一致性损失通过式 (6) 在每个批次大小为 $B$ 的小批量上惩罚直接预测能量 $\hat{E}$ 与 Atwater 当量 $\hat{E}_{\text{Atwater}}$ 之间的差异：
\begin{equation}
    \label{eq:atwater_loss}
    \mathcal{L}_{\text{Atwater}} = \frac{1}{B} \sum_{i=1}^B \ell_\delta \left( \hat{E}_i - \left( 4.0 \hat{P}_i + 9.0 \hat{F}_i + 4.0 \hat{C}_i \right) \right)
\end{equation}
在式 (6) 中，$\ell_\delta(\cdot)$ 表示式 (7) 中定义的 Smooth $L_1$ Huber 损失函数：
\begin{equation}
    \label{eq:huber_loss}
    \ell_\delta(u) = \begin{cases} 
    \frac{1}{2} u^2 & \text{若 } |u| < \delta \\ 
    \delta \left( |u| - \frac{1}{2} \delta \right) & \text{其他} 
    \end{cases}
\end{equation}
在式 (7) 中，阈值参数设为 $\delta = 1.0$。该公式对微小偏差提供二次惩罚，同时限制对极端异常值的梯度幅度。

由于各目标终点跨越完全不同的物理尺度（总质量与能量达到数百单位，而脂肪与蛋白质仅数十单位），原始目标损失会不成比例地偏向质量而忽视常量营养素。为平衡所有五个终点的梯度贡献，真值与预测向量通过 z-score 标准化进行归一化：
\begin{equation}
    \label{eq:target_norm}
    z_{i,j} = \frac{y_{i,j} - \mu_j^{\text{train}}}{\sigma_j^{\text{train}}}, \quad \hat{z}_{i,j} = \frac{\hat{y}_{i,j} - \mu_j^{\text{train}}}{\sigma_j^{\text{train}}}
\end{equation}
在式 (8) 中，$j \in \{1, \dots, 5\}$ 索引五个营养目标，$\mu_j^{\text{train}}$ 与 $\sigma_j^{\text{train}}$ 代表严格在训练集上计算的样本均值与标准差。利用式 (8) 的归一化表示，主要监督回归损失在式 (9) 中定义为：
\begin{equation}
    \label{eq:reg_loss}
    \mathcal{L}_{\text{reg}} = \frac{1}{B} \sum_{i=1}^B \sum_{j=1}^5 \ell_\delta \left( \hat{z}_{i,j} - z_{i,j} \right)
\end{equation}
复合训练目标通过式 (10) 将式 (9) 的标准化回归损失与式 (6) 的 Atwater 生理惩罚相结合：
\begin{equation}
    \label{eq:total_loss}
    \mathcal{L}_{\text{total}} = \mathcal{L}_{\text{reg}} + \lambda_{\text{Atwater}} \mathcal{L}_{\text{Atwater}}
\end{equation}
其中 $\lambda_{\text{Atwater}} = 0.05$ 控制生理约束的权重。

基线模型专门在西方 Nutrition5k 训练队列（$N=2,749$ 份餐食）上训练 20 个轮次，在单张 NVIDIA RTX 2080 Ti GPU（11\,GB 显存）上使用 Adam 优化器，初始学习率为 $10^{-4}$，权重衰减为 $10^{-4}$，批大小为 32。模型检查点选择取决于官方 Nutrition5k 验证集上的最低损失。

## 2.4 跨文化零样本迁移与信息隔离

为在杜绝人为数据泄漏的前提下审计跨文化泛化性，执行了严格的非混合协议。各数据集绝不跨文化边界混合、重排或随机划分。在临床部署中，在集中式高收入国家数据集上训练的消费级健康应用无需经过本地重新训练即可在全球下载。混洗数据集会掩盖特定文化的失效模式，并产生虚假乐观的性能估计。

因此，西方训练的模型在零样本迁移模式下跨三个独立的文化测试集进行评估。西方域内审计利用全部 $N=506$ 份 Nutrition5k 官方顶视测试餐食确立性能上限基准。南亚迁移审计评估全部 $N=1,833$ 份 FoodBD 测试餐食，以刻画在复杂复合肉汁烹饪准备上的迁移表现。东亚迁移审计评估全部 $N=1,484$ 张 ECUSTFD 顶视图像，以审计模型在离散单品食物与区域点心上的行为表现。

在跨文化评估期间，网络参数 $\theta, \phi$ 与批归一化运行统计量完全保持冻结。特征提取与预测过程中无法访问任何目标图像、标签或目标域统计矩。

## 2.5 方向性系统偏差与统计一致性指标

在临床膳食评估中，非方向性误差指标（如 MAE 和 RMSE）无法揭示算法是在持续低估还是高估营养摄入。为揭示方向性失真，通过平均带符号误差 (MSE) 在式 (11) 中形式化方向性系统偏差：
\begin{equation}
    \label{eq:mean_signed_bias}
    \text{Bias} = \frac{1}{N} \sum_{i=1}^N \left( \hat{y}_i - y_i \right)
\end{equation}
在式 (11) 中，$y_i$ 代表真实营养量，$\hat{y}_i$ 为第 $i$ 份餐食的预测值。正偏差代表系统性高估，而负偏差表示系统性低估。

为评估相对于餐食分量的相对方向失真，计算了平均百分比误差 (MPE)：
\begin{equation}
    \label{eq:mpe}
    \text{MPE} = \frac{1}{N} \sum_{i=1}^N \left( \frac{\hat{y}_i - y_i}{y_i} \right) \times 100\%
\end{equation}
在餐食水平的差值序列 $d_i = \hat{y}_i - y_i$ 上进行了双尾配对 Student's $t$ 检验，以评估无系统偏差的零假设 ($H_0: \mu_d = 0$)。

医学测量一致性使用 Bland-Altman 方法进行分析。设 $\bar{d} = \frac{1}{N}\sum_{i=1}^N d_i$ 为平均差值，$s_d = \sqrt{\frac{1}{N-1}\sum_{i=1}^N (d_i - \bar{d})^2}$ 为样本标准差。95% 一致性界限 (LoA) 在式 (13) 中定义为：
\begin{equation}
    \label{eq:loa}
    \text{LoA} = \left[ \bar{d} - 1.96 s_d, \quad \bar{d} + 1.96 s_d \right]
\end{equation}
为确定偏差是否随餐食大小发生系统性变化，在式 (14) 中通过测量差值对配对均值的普通最小二乘回归审计了比例偏差：
\begin{equation}
    \label{eq:ols_proportional_bias}
    d_i = \beta_0 + \beta_1 \left( \frac{\hat{y}_i + y_i}{2} \right) + \epsilon_i
\end{equation}
具有统计学意义的斜率 ($\beta_1 \ne 0, p < 0.05$) 表明存在比例偏差，说明估算差异随份量增加而扩大。

预测值与参考值之间的一致性通过 Lin 氏一致性相关系数 (CCC) 进行评估：
\begin{equation}
    \label{eq:lin_ccc}
    \rho_c = \frac{2 \sigma_{y\hat{y}}}{\sigma_y^2 + \sigma_{\hat{y}}^2 + \left( \mu_y - \mu_{\hat{y}} \right)^2}
\end{equation}
在式 (15) 中，$\mu_y$ 与 $\mu_{\hat{y}}$ 为均值，$\sigma_y^2$ 与 $\sigma_{\hat{y}}^2$ 为方差，$\sigma_{y\hat{y}}$ 为样本协方差。Lin CCC 同时衡量精确度（相关性）与准确度（偏离 45 度等值线的距离），提供范围在 $-1.0$ 至 $+1.0$ 之间的综合指数。

## 2.6 糖尿病碳水化合物计数的临床安全标准

对于接受餐时胰岛素治疗的糖尿病患者，精确的碳水化合物计数对于胰岛素剂量调整至关重要。美国糖尿病协会 (ADA) 的临床指南和临床大剂量算法采用胰岛素与碳水化合物比例（通常每 10 至 15 克碳水化合物对应 1 个单位速效胰岛素）。超过 $\pm 15$\,g 碳水化合物的估算差异会直接转化为 $1.0$ 至 $1.5$ 个单位的胰岛素推注剂量误差，造成餐后低血糖或持续高血糖的严重风险。

为了将计算机视觉精度转化为临床安全终点，在式 (16) 中定义了绝对碳水化合物安全达标率：
\begin{equation}
    \label{eq:clinical_compliance_abs}
    \text{Comp}_{\le \theta} = \frac{1}{N} \sum_{i=1}^N \mathbb{I}\left( |\hat{C}_i - C_i| \le \theta \right) \times 100\%
\end{equation}
在式 (16) 中，$\mathbb{I}(\cdot)$ 为示性函数，$\theta \in \{10, 15, 20\}$\,g 代表临床容忍阈值。主要安全终点规定为 $\theta = 15$\,g，其中 $\theta = 10$\,g 代表严格的高敏感胰岛素控制，$\theta = 20$\,g 代表宽松边界。

为考虑不同餐食大小，在式 (17) 中评估了相对百分比达标率：
\begin{equation}
    \label{eq:clinical_compliance_rel}
    \text{Comp}_{\le \eta\%} = \frac{1}{N} \sum_{i=1}^N \mathbb{I}\left( \frac{|\hat{C}_i - C_i|}{C_i} \le \eta \right) \times 100\%
\end{equation}
在式 (17) 中，$\eta \in \{0.15, 0.20\}$ 表示 $\pm 15\%$ 和 $\pm 20\%$ 的相对误差范围。

## 2.7 机制性误差分解形式化

跨文化估算误差可能源自不准确的份量体积估算（几何分割误差），或源自单位食物质量的不准确营养密度估算（生物化学成分盲区）。为隔离这些机制，构建了膳食碳水化合物的正交误差分解公式。

真实碳水化合物质量 $C$ 是总餐食质量 $M$ 与碳水化合物密度 $D = C / M$ 的乘积，如式 (18) 所示：
\begin{equation}
    \label{eq:carb_product}
    C = M \cdot D
\end{equation}
类似地，预测碳水化合物质量 $\hat{C}$ 等于预测质量 $\hat{M}$ 乘以预测密度 $\hat{D} = \hat{C} / \hat{M}$。从预测摄入量中减去式 (18) 中的参考摄入量，得到式 (19) 的误差分解：
\begin{equation}
    \label{eq:error_decomposition}
    \hat{C} - C = \underbrace{(\hat{M} - M) D}_{\Delta_{\text{mass}}} + \underbrace{M (\hat{D} - D)}_{\Delta_{\text{density}}} + \underbrace{(\hat{M} - M)(\hat{D} - D)}_{\Delta_{\text{interaction}}}
\end{equation}
在式 (19) 中，$\Delta_{\text{mass}}$ 隔离了在保持真实密度不变时因餐食质量偏差引起的误差，$\Delta_{\text{density}}$ 量化了在保持真实质量不变时内部营养密度误判引起的误差，$\Delta_{\text{interaction}}$ 捕捉了质量与密度误差之间的二阶耦合项。该数学归因隔离了跨文化失效究竟是由表面分割边界引起，还是源自内部化学组成盲区。

## 2.8 少样本就地校准协议

为评估是否可以在不重新训练深层视觉主干的情况下修复跨文化系统偏差，构建了仿射重新校准协议。通过实验室称重收集大规模营养数据集成本高昂，而由区域医疗机构收集 $K \in \{20, 50, 100\}$ 份餐食的小规模本地校准集具有临床可行性。

对于每个营养终点 $y \in \{M, E, P, F, C\}$，在保持视觉参数 $\theta, \phi$ 冻结的同时，在校准样本库上学习仿射校准映射：
\begin{equation}
    \label{eq:few_shot_calibration}
    \hat{y}_{\text{cal}} = \alpha \hat{y} + \beta
\end{equation}
在式 (20) 中，缩放参数 $\alpha \in \mathbb{R}$ 和截距 $\beta \in \mathbb{R}$ 通过对 $K$ 个校准对 $(y_k, \hat{y}_k)_{k=1}^K$ 进行普通最小二乘回归估计。然后在独立的保留目标测试集（$N=180$）上评估校准后的预测，以衡量偏差衰减与临床安全达标率的恢复情况。
