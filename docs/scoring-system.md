# 技能评分体系详解 v4.0

## 概述

v4.0 评分体系从固定权重演进为**上下文感知动态权重**，解决了 v3.0 的马太效应和同质化偏向问题。

## 动态评分模型

### 核心变化

| 维度 | v3.0 权重 | v4.0 工具型 | v4.0 创意型 | v4.0 研究型 |
|------|-----------|------------|------------|------------|
| 活跃度 | 25% | **30%** | 15% | 10% |
| 关系度 | 20% | 15% | 10% | 15% |
| 完整度 | 15% | 15% | **20%** | 15% |
| 稳健度 | 20% | **25%** | 15% | 15% |
| 适应度 | 10% | 10% | 10% | **20%** |
| 独特性 | 10% | 5% | **30%** | **25%** |

### 设计理由

**v3.0 的问题（四模型共识）：**
- 活跃度25%最高权重 → 用"流行度"衡量"重要性" → 马太效应
- 独特性仅10% → 天然偏向同质化 → 与"不灭种"哲学矛盾
- 固定权重无法适应不同技能类型的需求

**v4.0 的解决方案：**
- 工具型（如 devops 类）：重视活跃度和稳健度，因为可靠性最重要
- 创意型（如 pixel-art 类）：重视独特性和完整度，因为创新最重要
- 研究型（如 dspy 类）：重视独特性和适应度，因为前沿探索最重要
- 基础设施型（如 linux-server-health-check）：重视稳健度和关系度，因为系统稳定最重要

### 生态上下文调整

权重还会根据生态整体状态动态微调：

```python
ECOSYSTEM_FACTORS = {
    "expansion": {      # 扩张期：新技能涌入
        "uniqueness": 1.5,   # 鼓励多样性
        "activity": 0.8,     # 降低活跃度权重
    },
    "stability": {      # 稳定期：正常运行
        "robustness": 1.3,   # 重视可靠性
        "activity": 1.2,     # 适度重视使用
    },
    "consolidation": {  # 整合期：技能合并
        "relationship": 1.4, # 重视关联性
        "completeness": 1.3, # 重视文档质量
    },
}
```

## 六维评分详解

### 1. 活跃度（Activity Score）

计算方式不变，但权重随类型变化：

```python
# 半衰期7天的指数衰减
time_decay = math.exp(-0.1 * days_since_used)

# 调用频率分级
if use_count >= 50: frequency_score = 100
elif use_count >= 20: frequency_score = 80
elif use_count >= 10: frequency_score = 60
elif use_count >= 3: frequency_score = 40
elif use_count >= 1: frequency_score = 20
else: frequency_score = 0

activity = frequency_score * time_decay
```

### 2. 关系度（Relationship Score）

```python
# 归一化（最大度数20）
in_degree * 0.7 + out_degree * 0.3 → 0-100
```

### 3. 完整度（Completeness Score）

```python
# 必填字段 × 0.7 + 选填字段 × 0.3
required = ["name", "description", "version", "author",
            "triggers", "prerequisites", "content"]
optional = ["tags", "related_skills", "examples",
            "pitfalls", "references"]
```

### 4. 稳健度（Robustness Score）

```python
# 历史成功率 × 0.4 + 近期成功率 × 0.6
if total_executions == 0: return 50  # 默认50%
```

### 5. 适应度（Adaptability Score）

```python
factors = {
    "platform_compatibility": 0.3,
    "dependency_availability": 0.3,
    "resource_requirements": 0.2,
    "version_compatibility": 0.2,
}
```

### 6. 独特性（Uniqueness Score）

```python
# 功能独特性 × 0.6 + 实现独特性 × 0.4
functional_uniqueness = 1 - functional_similarity
implementation_uniqueness = 1 - implementation_similarity
```

## 评分示例

```python
# 创意型技能：pixel-art
# v3.0: activity(25%) + ... + uniqueness(10%) = 中等分数
# v4.0: uniqueness(30%) 权重大幅提升 → 更公平的评分

scorer = DynamicScorer("stability")
score, dims, weights = scorer.score(pixel_art_skill, "creative")
# weights = {"activity": 0.15, "uniqueness": 0.30, ...}
# uniqueness 的贡献从 10% 提升到 30%
```

## 评分阈值（继承 v3.0）

| 评分区间 | 标签 | 说明 |
|----------|------|------|
| 80-100 | hot | 高频优质 |
| 60-79 | warm | 稳定使用 |
| 40-59 | cold | 低频但保留 |
| 20-39 | dormant | 休眠观察 |
| 0-19 | archive | 归档深冻 |

## 特殊规则

### 反熵保护（v4.0 增强）

```python
def apply_anti_entropy(skills):
    # 1. 标签保护：UNIQUE 或 HIGH_POTENTIAL 标签的技能自动保护
    # 2. 随机保护：额外随机保护 5-10% 低分技能
    # 3. 归档保护：已归档技能保留元数据，可复活
```

### 边界弹性（v4.0 新增）

```python
# v3.0: 29天使用2次 → 常驻层，31天使用2次 → 隔离层（硬切）
# v4.0: 标签可叠加，边界有缓冲区
# 例如：days=31 但 uniqueness=0.85 → 标签 [cold, unique] → 种子库
```

## v3.0 vs v4.0 评分对比

| 场景 | v3.0 结果 | v4.0 结果 |
|------|-----------|-----------|
| 高独特性创意技能（低频） | 种子库（35分） | 种子库（65分，uniqueness权重30%） |
| 高频工具技能 | 热气层（85分） | 热气层（90分，activity权重30%） |
| 休眠但高价值技能 | 隔离层（30分） | 种子库（55分，标签保护） |
| 新孵化技能 | 不确定（无生命周期） | 孵化期标签，宽松评估 |

## 参考资料

- `docs/architecture.md` - 架构设计
- `src/ecosystem-librarian.md` - 核心代码实现
- `src/skill-curation.md` - v2.0 园丁系统（历史参考）
