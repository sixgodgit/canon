# 技能评分体系详解

## 概述

Hermes 技能生态系统使用六维评分体系来评估技能质量，为分类和管理提供数据支撑。

## 六维评分模型

### 1. 活跃度（Activity Score）

**定义**：衡量技能最近的使用频率和时效性。

#### 计算公式
```
活跃度 = (调用频率 × 时间衰减) × 100
```

#### 时间衰减函数
```python
def time_decay(days_since_used):
    """指数衰减，半衰期7天"""
    return math.exp(-0.1 * days_since_used)
```

#### 调用频率分级
| 调用次数 | 得分 | 级别 |
|----------|------|------|
| ≥50次 | 100 | 极高 |
| 20-49次 | 80 | 高 |
| 10-19次 | 60 | 中高 |
| 3-9次 | 40 | 中等 |
| 1-2次 | 20 | 低 |
| 0次 | 0 | 无 |

#### 示例计算
```python
# 技能A：10天前使用，共调用15次
activity_a = 15 * time_decay(10)  # ≈ 15 × 0.37 = 5.55

# 技能B：2天前使用，共调用5次
activity_b = 5 * time_decay(2)    # ≈ 5 × 0.82 = 4.10

# 技能C：30天前使用，共调用30次
activity_c = 30 * time_decay(30)  # ≈ 30 × 0.05 = 1.50
```

### 2. 关系度（Relationship Score）

**定义**：衡量技能在引用图中的重要性。

#### 计算公式
```
关系度 = (入度 × 0.7 + 出度 × 0.3) × 归一化系数
```

#### 引用图分析
```python
def calculate_relationship_score(skill, dependency_graph):
    # 入度：被其他技能引用的次数
    in_degree = len(dependency_graph.get_dependents(skill))
    
    # 出度：引用其他技能的次数
    out_degree = len(dependency_graph.get_dependencies(skill))
    
    # 归一化
    max_degree = max(in_degree + out_degree for skill in all_skills)
    normalized = (in_degree * 0.7 + out_degree * 0.3) / max_degree
    
    return normalized * 100
```

#### 关系类型
| 类型 | 权重 | 说明 |
|------|------|------|
| **被依赖** | 0.7 | 被其他技能引用 |
| **依赖** | 0.3 | 引用其他技能 |

### 3. 完整度（Completeness Score）

**定义**：衡量技能文档的完整性和质量。

#### 检查字段
```python
required_fields = [
    "name",           # 技能名称
    "description",    # 描述
    "version",        # 版本
    "author",         # 作者
    "triggers",       # 触发条件
    "prerequisites",  # 前置条件
    "content",        # 核心内容
]

optional_fields = [
    "tags",           # 标签
    "related_skills", # 相关技能
    "examples",       # 示例
    "pitfalls",       # 注意事项
    "references",     # 参考资料
]
```

#### 计算公式
```
完整度 = (必填字段完整率 × 0.7 + 选填字段完整率 × 0.3) × 100
```

#### 示例
```python
# 技能A：7个必填字段完整，5个选填字段完整3个
completeness_a = (7/7 * 0.7 + 3/5 * 0.3) * 100  # ≈ 88

# 技能B：5个必填字段完整，5个选填字段完整1个
completeness_b = (5/7 * 0.7 + 1/5 * 0.3) * 100  # ≈ 56
```

### 4. 稳健度（Robustness Score）

**定义**：衡量技能执行的可靠性和错误率。

#### 计算公式
```
稳健度 = 成功率 × 100
```

#### 成功率计算
```python
def calculate_success_rate(skill):
    if skill.total_executions == 0:
        return 0.5  # 默认50%
    
    success_rate = skill.successful_executions / skill.total_executions
    
    # 考虑最近表现（加权）
    recent_rate = skill.recent_success_rate  # 最近10次
    
    # 综合评分（近期表现权重更高）
    return success_rate * 0.4 + recent_rate * 0.6
```

#### 稳健度分级
| 成功率 | 得分 | 级别 |
|--------|------|------|
| ≥95% | 100 | 极高 |
| 85-94% | 80 | 高 |
| 70-84% | 60 | 中等 |
| 50-69% | 40 | 低 |
| <50% | 20 | 极低 |

### 5. 适应度（Adaptability Score）

**定义**：衡量技能与当前环境的兼容性。

#### 评估维度
```python
adaptability_factors = {
    "platform_compatibility": 0.3,  # 平台兼容性
    "dependency_availability": 0.3,  # 依赖可用性
    "resource_requirements": 0.2,    # 资源需求
    "version_compatibility": 0.2,    # 版本兼容性
}
```

#### 计算公式
```
适应度 = Σ(因子得分 × 权重) × 100
```

#### 因子评估
```python
def evaluate_platform_compatibility(skill):
    """评估平台兼容性"""
    supported_platforms = skill.platforms
    current_platform = get_current_platform()
    
    if current_platform in supported_platforms:
        return 1.0
    elif "linux" in supported_platforms and current_platform == "linux":
        return 0.9
    else:
        return 0.5

def evaluate_dependency_availability(skill):
    """评估依赖可用性"""
    required_deps = skill.required_commands
    available_deps = check_commands_availability(required_deps)
    
    return len(available_deps) / len(required_deps)
```

### 6. 独特性（Uniqueness Score）

**定义**：衡量技能的不可替代性和独特价值。

#### 计算公式
```
独特性 = (功能独特性 × 0.6 + 实现独特性 × 0.4) × 100
```

#### 独特性评估
```python
def calculate_uniqueness_score(skill, all_skills):
    # 功能独特性：功能描述的相似度
    functional_similarity = calculate_functional_similarity(skill, all_skills)
    functional_uniqueness = 1 - functional_similarity
    
    # 实现独特性：实现方式的相似度
    implementation_similarity = calculate_implementation_similarity(skill, all_skills)
    implementation_uniqueness = 1 - implementation_similarity
    
    return (functional_uniqueness * 0.6 + implementation_uniqueness * 0.4) * 100
```

#### 独特性分级
| 独特性 | 得分 | 说明 |
|--------|------|------|
| ≥90% | 100 | 完全独特 |
| 70-89% | 80 | 高度独特 |
| 50-69% | 60 | 中等独特 |
| 30-49% | 40 | 部分独特 |
| <30% | 20 | 高度相似 |

## 综合评分

### 计算公式
```
综合评分 = 活跃度 × 0.25 + 关系度 × 0.20 + 完整度 × 0.15 + 
           稳健度 × 0.20 + 适应度 × 0.10 + 独特性 × 0.10
```

### 权重说明
| 维度 | 权重 | 说明 |
|------|------|------|
| **活跃度** | 25% | 使用频率最重要 |
| **稳健度** | 20% | 可靠性次之 |
| **关系度** | 20% | 生态位置重要 |
| **完整度** | 15% | 文档质量 |
| **适应度** | 10% | 兼容性 |
| **独特性** | 10% | 不可替代性 |

### 评分示例
```python
# 技能评分示例
skill_scores = {
    "activity": 75,
    "relationship": 60,
    "completeness": 85,
    "robustness": 90,
    "adaptability": 80,
    "uniqueness": 70,
}

# 综合评分
total_score = (
    75 * 0.25 +   # 18.75
    60 * 0.20 +   # 12.00
    85 * 0.15 +   # 12.75
    90 * 0.20 +   # 18.00
    80 * 0.10 +   # 8.00
    70 * 0.10     # 7.00
)  # = 76.5

print(f"综合评分: {total_score:.1f}")
```

## 评分阈值

### 层级判定
| 评分区间 | 层级 | 说明 |
|----------|------|------|
| 80-100 | 热气层 | 高频优质 |
| 60-79 | 常驻层 | 稳定使用 |
| 40-59 | 种子库 | 潜在价值 |
| 20-39 | 隔离层 | 待评估 |
| 0-19 | 删除候选 | 建议删除 |

### 特殊规则
1. **反熵保护**：随机保护5-10%低分技能
2. **人类审批**：所有删除需人工确认
3. **对抗性辩护**：为拟删除技能辩护

## 评分优化

### 动态权重调整
```python
def adjust_weights_based_on_context(context):
    """根据上下文调整权重"""
    if context == "maintenance":
        # 维护模式：更重视稳健度和完整度
        return {
            "activity": 0.15,
            "relationship": 0.15,
            "completeness": 0.25,
            "robustness": 0.25,
            "adaptability": 0.10,
            "uniqueness": 0.10,
        }
    elif context == "discovery":
        # 发现模式：更重视独特性和潜力
        return {
            "activity": 0.10,
            "relationship": 0.15,
            "completeness": 0.15,
            "robustness": 0.15,
            "adaptability": 0.15,
            "uniqueness": 0.30,
        }
    else:
        # 默认权重
        return default_weights
```

### 评分校准
```python
def calibrate_scores(skills):
    """校准评分，确保分布合理"""
    scores = [skill.total_score for skill in skills]
    
    # 计算均值和标准差
    mean_score = sum(scores) / len(scores)
    std_score = (sum((s - mean_score) ** 2 for s in scores) / len(scores)) ** 0.5
    
    # Z-score 标准化
    for skill in skills:
        z_score = (skill.total_score - mean_score) / std_score
        skill.calibrated_score = 50 + z_score * 15  # 转换到0-100范围
    
    return skills
```

## 最佳实践

1. **定期评分** - 每月执行一次完整评分
2. **动态调整** - 根据使用情况调整权重
3. **人工校准** - 定期人工审核评分结果
4. **文档记录** - 记录评分变化原因
5. **反馈循环** - 收集用户反馈优化评分

## 参考资料

- `references/evaluation-example.json` - 完整评估示例
- `docs/architecture.md` - 架构设计文档
- `src/skill-curation.md` - 评分实现代码
