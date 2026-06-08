# 技能生态管理系统架构设计

## 系统架构概览

```
┌─────────────────────────────────────────────────────────┐
│                  技能生态图书管理系统                       │
├─────────────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  │
│  │ 热气层  │  │ 常驻层  │  │ 种子库  │  │ 隔离层  │  │
│  │  (Hot)  │  │(Normal) │  │ (Seed)  │  │(Isolate)│  │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘  │
│       │            │            │            │          │
│       └────────────┴────────────┴────────────┘          │
│                         │                                │
│                    ┌────┴────┐                           │
│                    │ 评估引擎 │                           │
│                    └────┬────┘                           │
│                         │                                │
│       ┌─────────────────┼─────────────────┐             │
│       │                 │                 │             │
│  ┌────┴────┐      ┌────┴────┐      ┌────┴────┐       │
│  │六维评分 │      │反熵保护 │      │人类审批 │       │
│  └─────────┘      └─────────┘      └─────────┘       │
└─────────────────────────────────────────────────────────┘
```

## 核心组件

### 1. 四层分类引擎

#### 热气层（Hot Layer）
```python
# 判定条件
def is_hot_layer(skill):
    return (
        skill.last_used_days <= 7 and
        skill.use_count >= 10 and
        skill.success_rate >= 0.9
    )
```

**特点**：
- 最近7天内被调用
- 使用频率高（≥10次）
- 执行成功率高（≥90%）

#### 常驻层（Normal Layer）
```python
# 判定条件
def is_normal_layer(skill):
    return (
        skill.last_used_days <= 30 and
        skill.use_count >= 3 and
        skill.success_rate >= 0.7
    )
```

**特点**：
- 30天内被调用
- 使用频率中等（≥3次）
- 执行成功率良好（≥70%）

#### 种子库（Seed Bank）
```python
# 判定条件
def is_seed_bank(skill):
    return (
        skill.potential_value >= 0.7 or  # 有潜在价值
        skill.uniqueness_score >= 0.8 or  # 高独特性
        skill.last_used_days > 30  # 低频但保留
    )
```

**特点**：
- 有潜在价值
- 高独特性
- 低频使用但保留

#### 隔离层（Isolation Layer）
```python
# 判定条件
def is_isolation_layer(skill):
    return (
        skill.has_errors or  # 有错误
        skill.is_duplicate or  # 重复
        skill.is_outdated or  # 过时
        skill.needs_review  # 待审核
    )
```

**特点**：
- 有错误或问题
- 重复技能
- 过时内容
- 需要人工审核

### 2. 六维评分系统

#### 评分维度

| 维度 | 权重 | 计算方式 | 说明 |
|------|------|----------|------|
| **活跃度** | 25% | 调用频率 × 时间衰减 | 最近使用情况 |
| **关系度** | 20% | 引用图分析 | 被其他技能依赖程度 |
| **完整度** | 15% | 文档字段完整性 | 文档质量 |
| **稳健度** | 20% | 执行成功率 | 可靠性 |
| **适应度** | 10% | 环境兼容性 | 跨平台能力 |
| **独特性** | 10% | 不可替代性 | 独特价值 |

#### 评分算法
```python
def calculate_score(skill):
    score = 0
    
    # 活跃度 (25%)
    activity = calculate_activity_score(skill)
    score += activity * 0.25
    
    # 关系度 (20%)
    relationship = calculate_relationship_score(skill)
    score += relationship * 0.20
    
    # 完整度 (15%)
    completeness = calculate_completeness_score(skill)
    score += completeness * 0.15
    
    # 稳健度 (20%)
    robustness = calculate_robustness_score(skill)
    score += robustness * 0.20
    
    # 适应度 (10%)
    adaptability = calculate_adaptability_score(skill)
    score += adaptability * 0.10
    
    # 独特性 (10%)
    uniqueness = calculate_uniqueness_score(skill)
    score += uniqueness * 0.10
    
    return score
```

### 3. 反熵保护机制

#### 保护策略
```python
def apply_anti_entropy_protection(skills):
    # 找出所有低分技能
    low_score_skills = [s for s in skills if s.score < 50]
    
    # 随机保护5-10%
    protection_rate = random.uniform(0.05, 0.10)
    protected_count = max(3, int(len(low_score_skills) * protection_rate))
    
    # 优先保护有潜在价值的
    protected = []
    for skill in low_score_skills:
        if (skill.potential_value >= 0.7 or
            skill.uniqueness_score >= 0.8 or
            skill.has_user_dependency):
            protected.append(skill)
    
    # 补充随机保护
    remaining = [s for s in low_score_skills if s not in protected]
    protected.extend(random.sample(remaining, min(protected_count, len(remaining))))
    
    return protected
```

#### 保护优先级
1. **创意/媒体类** - 技术+艺术交汇，不可替代的美学表达
2. **游戏/教育类** - 教育和社会协作的天然入口
3. **ML/研究类** - 前沿方向，有GPU后价值立现
4. **生产力类** - 特定场景的独特方案
5. **智能家居类** - 有硬件后价值立现

### 4. 对抗性辩护系统

#### 辩护框架
```python
def generate_defense_notes(skill):
    defense = {
        "scenario_usage": "这个技能在什么场景下可能有用？",
        "future复活": "如果三五年后环境变了，这个技能会复活吗？",
        "unique_value": "这个技能代表了什么独特的价值取向或方法论？",
        "user_dependency": "有没有用户可能依赖它？（即使频率很低）",
        "irreversible_loss": "删除后有什么不可逆的损失？"
    }
    
    # 生成具体辩护理由
    defense["notes"] = generate_specific_defense(skill, defense)
    
    return defense
```

## 数据流

### 评估流程
```
1. 扫描所有技能
   ↓
2. 加载技能元数据
   ↓
3. 六维评分计算
   ↓
4. 四层分类判定
   ↓
5. 反熵保护应用
   ↓
6. 重复检测
   ↓
7. 输出评估报告
   ↓
8. 等待人类审批
```

### 分类流转
```
新技能 → 隔离层 → 评估 → 常驻层/种子库
                              ↓
热气层 ← 高频使用 ← 常驻层
  ↓
种子库 ← 低频使用
  ↓
隔离层 ← 问题技能
```

## 配置参数

### 评估参数
```yaml
evaluation:
  # 层级阈值
  hot_layer_threshold: 7  # 天
  normal_layer_threshold: 30  # 天
  
  # 评分权重
  weights:
    activity: 0.25
    relationship: 0.20
    completeness: 0.15
    robustness: 0.20
    adaptability: 0.10
    uniqueness: 0.10
  
  # 保护参数
  anti_entropy:
    min_protection_rate: 0.05
    max_protection_rate: 0.10
    min_protected_count: 3
```

### 分类参数
```yaml
classification:
  # 热气层条件
  hot_layer:
    max_days_since_used: 7
    min_use_count: 10
    min_success_rate: 0.9
  
  # 常驻层条件
  normal_layer:
    max_days_since_used: 30
    min_use_count: 3
    min_success_rate: 0.7
  
  # 种子库条件
  seed_bank:
    min_potential_value: 0.7
    min_uniqueness_score: 0.8
```

## 扩展点

### 1. 自定义评分维度
```python
# 添加新维度
custom_dimensions = {
    "community_support": 0.05,  # 社区支持度
    "documentation_quality": 0.05,  # 文档质量
    "test_coverage": 0.05,  # 测试覆盖率
}
```

### 2. 自定义分类规则
```python
# 添加新层级
custom_layers = {
    "experimental": {  # 实验层
        "conditions": ["is_experimental", "has_risk"],
        "actions": ["isolate", "monitor"]
    }
}
```

### 3. 自定义保护策略
```python
# 添加保护优先级
custom_protection_priorities = [
    "mission_critical",  # 任务关键
    "user_favorite",  # 用户喜爱
    "future_potential",  # 未来潜力
]
```

## 监控指标

### 生态健康度
- **技能总数**：当前技能数量
- **层级分布**：各层技能比例
- **平均评分**：整体质量
- **更新频率**：维护活跃度

### 风险指标
- **重复率**：重复技能比例
- **过时率**：过时技能比例
- **错误率**：有问题技能比例
- **依赖度**：被依赖程度

## 最佳实践

1. **定期评估** - 每月执行一次完整评估
2. **渐进式优化** - 逐步改进，不激进删除
3. **用户反馈** - 收集用户使用反馈
4. **文档维护** - 保持文档更新
5. **版本控制** - 使用Git管理技能版本

## 参考实现

- `src/skill-curation.md` - 园丁系统实现
- `src/ecosystem-librarian.md` - 图书管理员实现
- `references/evaluation-example.json` - 评估示例
