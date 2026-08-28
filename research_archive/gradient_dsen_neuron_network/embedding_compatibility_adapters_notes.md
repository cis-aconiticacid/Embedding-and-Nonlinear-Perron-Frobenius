# Embedding Compatibility Adapters —— 阅读笔记

**仓库**:<https://github.com/hanxiao/embedding-compatibility-adapters>

**Report PDF**:<https://github.com/hanxiao/embedding-compatibility-adapters/blob/main/report.pdf>

---

## 一、原始来源:Han Xiao 的推文

> Saw a poster at ICLR showing contrastive learning (InfoNCE included!) ≈ a closed-form spectral decomposition in RKHS. Got curious whether a map could adapt embedding spaces across model families, while preserving NDCG retrieval perf. Did some experiments on my flights back to sf. Video shows diff maps on simple swiss roll data.
>
> Then I tested different adapters on all jina embedding models and turned out models sharing training data & recipes (v5-nano/v5-small) have near-identical geometry regardless their model architectures (eurobert/qwen3), the spaces differ mainly by rotation. Procrustes alignment finds the optimal orthogonal matrix W from calibration pairs in one shot. This means v5-nano vectors in 768d can be used to search v5-small vectors in 1024d at nano performance! This is kind of surprising to me.
>
> This thing can be useful when your embedding provider deprecated their model (not jina!). You have billions of documents embedded with the old one. Re-embedding costs thousands of dollars and days of compute. A Procrustes adapter can save a lot of time and almost instant (one SVD, one matprod, closed-form solution). Anyway I put code here for ref:

---

## 二、项目本身在干什么(第一轮解释)

### 它解决的问题

想象你是一家公司,用某个 embedding model(比如 OpenAI 的 `text-embedding-ada-002`)把几十亿份文档全都编码成向量,存进了向量数据库,做检索用。然后某天供应商说:"我们这个模型 deprecated 了,请换新模型。"

问题是新旧模型的 embedding 空间是**不兼容**的——你不能拿旧空间的 doc embedding 和新空间的 query embedding 算 cosine similarity,几何意义完全不对。常规做法是把所有文档**重新编码一遍**,但这可能要花掉几千美金 + 几天的算力。

### 它的解法:Procrustes 对齐

核心 insight 是:**两个在相似数据上训练的 embedding model,学到的几何结构其实差不多,主要差别只是一个旋转**。所以可以找一个正交矩阵 $W$ 把旧空间映射到新空间。

具体做法是经典的 **正交 Procrustes 问题**:

$$\min_W \|X_{\text{source}} W - X_{\text{target}}\|_F \quad \text{s.t.} \quad W^\top W = I$$

解法是对 $M = X_{\text{source}}^\top X_{\text{target}}$ 做 SVD,然后 $W = UV^\top$。一次 SVD 搞定,没有梯度下降,没有神经网络,没有 GPU。

只需要大约 5000 个 calibration pairs(同样的文本分别用新旧模型 embed),就能算出这个 $W$。推理时旧的 query embedding 乘一下 $W$ 就到新空间了,正交矩阵保 norm 保 angle,cosine similarity 直接就对了。

### 实验结果

在 NanoBEIR 上测了 12 对模型组合:

- **同家族同代**(比如 jina v5-nano ↔ v5-small):retention 99% 左右,几乎无损
- **跨代**(v3 → v4):retention 70-85%
- **跨厂商**(Jina ↔ Qwen3):有时甚至超过 100%(因为目标模型本身性能就差一些)

他们用 **CKA(Centered Kernel Alignment)** 作为 predictor:CKA > 0.9 基本无损,CKA < 0.8 就别硬适配了,老老实实重新 embed 吧。

### 为什么这个 idea 比较优雅

它本质上是在说:embedding model 的 representation space 在抽象意义上有一种 **isometry-up-to-rotation** 的稳定性,那么 alignment 就是个**线性问题**,而且是 orthogonal group $O(d)$ 上的优化。作者也对比了 MLP adapter,结论是 MLP 一直最差,印证了"这是线性问题不要过度参数化"的直觉。

跟 LP duality / spectral theory 那套语言其实很合拍——约束在 Stiefel manifold($W^\top W = I$)上的 Frobenius norm 最小化,有 closed-form 解,而且 sample complexity 极低(参数只有 $d \times d$,完全没法过拟合)。

### 一句话总结

**当 embedding 供应商弃用旧模型,与其花大钱重新编码所有文档,不如用 5000 个样本算一个 SVD,得到一个正交矩阵把旧空间"旋转"到新空间——前提是两个模型几何上足够相似(CKA > 0.9)。**

---

## 三、为什么这件事冲击力很大(第二轮拆解)

这里面其实有几层独立的"惊喜"叠在一起。

### 第一层:contrastive learning ≈ RKHS 里的 spectral decomposition

ICLR poster 顺着挖一下值得看。背景是这几年有一系列工作(HaoChen et al. 2021 spectral contrastive loss、Johnson et al. 关于 InfoNCE 的 kernel PCA 视角、Balestriero & LeCun 2022 把 SimCLR/VICReg/BarlowTwins 全都还原成 spectral methods 的统一框架)在论证:**contrastive learning 本质上是在做一个隐式的算子的特征分解**。

具体说,你定义一个 augmentation graph(或者 positive pair distribution),它诱导出一个 RKHS 上的算子;contrastive loss 的最优解就是这个算子的 top-k eigenfunction。InfoNCE 是其中一个特例——它对应的是某个归一化算子。

这一下就把一大堆看起来 ad hoc 的 self-supervised 方法和 **spectral theory / kernel methods / Perron-Frobenius 那套谱论** 放到了同一个语言里。这条线跟非线性 PF / Hilbert metric 那套是一脉的——都是"非线性优化问题的最优解其实是某个算子的谱"。

### 第二层:既然是谱分解,那不同模型学到的是"同一个东西"的不同坐标

这是 Han Xiao 的逻辑跳跃,而且很合理:

如果两个 embedding model 在**相似的数据 + 相似的 augmentation/positive pair 分布**下用 contrastive loss 训练,那它们其实都在逼近**同一个底层算子的 top-k 特征空间**。

特征子空间是 intrinsic 的,但**特征基不是**——任何正交变换 $W \in O(d)$ 都能把一组特征基换成另一组同样合法的特征基。所以两个模型学出来的 embedding,在理想情况下应该是 **同一个子空间的两组不同正交基**。

那它们之间的关系自然就是一个**正交矩阵**。

这就解释了实验结果里最 striking 的那一条:**v5-nano (768d) 和 v5-small (1024d) 架构都不一样(EuroBERT vs Qwen3),但只要训练数据和 recipe 一样,几何就近乎同构**。架构是 expressive enough 的载体,真正决定几何的是 contrastive objective 隐式定义的那个算子。

### 第三层:既然只差一个旋转,Procrustes 直接给闭式解

到这里就是经典的正交 Procrustes 了。值得多说一句的是这件事的 **sample complexity**:

- 参数量 $d \times d$,但被约束在 Stiefel manifold $V_d(\mathbb{R}^d)$ 上,有效自由度 $\frac{d(d-1)}{2}$
- 5000 个 calibration pair 远远超过需要量,基本不可能过拟合
- closed-form,没有优化的不稳定性

对比 MLP adapter 一直最差——这非常 telling。MLP 给你的是 $\mathbb{R}^{d \times d'}$ 整个空间,但真实的 ground truth 就活在 $O(d)$ 这个低维流形上。**过参数化会让你 fit 到 calibration set 的噪声方向,而不是 fit 到真正的旋转**。这就是 inductive bias 的胜利——选对约束比选对架构重要。

### 为什么"维度不同还能对齐"不矛盾

768 → 1024 这条结果可能稍微卡一下:正交矩阵不是要求方阵吗?

实际上你做的是 **rectangular Procrustes**:在 768 维子空间和 1024 维空间之间找一个 $W \in \mathbb{R}^{768 \times 1024}$,满足 $W W^\top = I_{768}$(行正交)。这等价于把 768 维的源空间**等距嵌入**到 1024 维目标空间的某个 768 维子空间里。

几何意义:1024 维 model 学到的有效信息可能本来就主要集中在一个 ~768 维的子空间里(目标空间冗余),或者 nano 模型只能 capture 到 small 模型信息的一个子集——后者更符合 nano 性能略低于 small 的事实。所以 retention 是 99.3% 而不是 100%。

---

## 四、可以继续挖的方向

1. **CKA 作为 predictor 本身就是一个谱量**。CKA 衡量的是两个 Gram matrix 的相似度,本质上是比较两个核诱导的算子的谱。CKA > 0.9 → adapter lossless 这条经验规律,理论上应该可以用算子谱距离推出来。

2. **non-orthogonal 的情形**。如果两个模型训练数据**不同**,那它们逼近的是不同的算子,谱不一样,Procrustes 就不够了。这时候需要的是 **Gromov-Wasserstein** 风格的对齐——它不要求两个空间嵌在同一个外部空间里,而是直接对齐距离结构。这个方向跟 optimal transport 和 metric geometry 强相关。

3. **跟非线性 PF 的连接**。spectral contrastive 那套用的是线性算子的谱;如果换成 **non-expansive map under Hilbert projective metric** 那套,可以问:non-contrastive self-supervised(BYOL, DINO 那种没有 negative sample 的)是不是对应一个非线性 PF 算子的不动点?framework 上是 natural 的。

4. **Report PDF 值得读一下**。仓库里那个 `report.pdf` 应该会把实验细节和理论 framing 都写得更清楚。

---

## 五、关键数字速查

### Native baselines (NanoBEIR, nDCG@10)

| Model | nDCG@10 |
| --- | --- |
| jina-embeddings-v5-nano | 0.667 |
| jina-embeddings-v5-small | 0.671 |
| jina-embeddings-v3 | 0.634 |
| jina-embeddings-v4 | 0.647 |
| Qwen3-Embedding-0.6B | 0.584 |

### Same-family adaptation (5000 calibration samples)

| Source → Target | Adapted | Native Target | Retention |
| --- | --- | --- | --- |
| v5-nano → v5-small | 0.666 | 0.671 | 99.3% |
| v5-small → v5-nano | 0.660 | 0.667 | 98.9% |
| v3 → v5-small | 0.548 | 0.671 | 81.7% |
| v4 → v5-small | 0.586 | 0.671 | 87.3% |
| v3 → v4 | 0.540 | 0.647 | 83.5% |
| v4 → v3 | 0.434 | 0.634 | 68.5% |

### Cross-vendor adaptation

| Source → Target | Adapted | Native Target | Retention |
| --- | --- | --- | --- |
| v5-nano → Qwen3 | 0.613 | 0.584 | 105.0% |
| v5-small → Qwen3 | 0.614 | 0.584 | 105.1% |
| v3 → Qwen3 | 0.535 | 0.584 | 91.6% |
| v4 → Qwen3 | 0.516 | 0.584 | 88.4% |
| Qwen3 → v5-nano | 0.563 | 0.667 | 84.4% |
| Qwen3 → v3 | 0.455 | 0.634 | 71.8% |

### 经验规律

- **CKA > 0.9** → 适配近乎无损
- **CKA < 0.8** → 别硬适配,重新 embed
- 同 recipe + 不同架构 ≈ 同 geometry(架构只要 expressive enough 就够)
