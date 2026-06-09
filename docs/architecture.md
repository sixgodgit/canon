# 技能生态管理系统架构设计 v4.0

## 系统架构概览

```
┌──────────────────────────────────────────────────────────────────┐
│                    技能生态图书管理系统 v4.0                         │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    柔性标签系统                            │   │
│  │  hot · warm · cold · dormant · unique · core · healthy   │   │
│  └──────────────────────┬───────────────────────────────────┘   │
│                         │                                        │
│  ┌──────────┬───────────┼───────────┬──────────┐               │
│  │          │           │           │          │               │
│  ▼          ▼           ▼           ▼          ▼               │
│ ┌────┐  ┌────┐    ┌────────┐   ┌────┐   ┌────────┐           │
│ │Hot │  │Warm│    │  Seed  │   │Arch│   │Isolate │           │
│ │    │  │    │    │  Bank  │   │ive │   │        │           │
│ └────┘  └────┘    └────────┘   └────┘   └────────┘           │
│  ▲          ▲           ▲           ▲          ▲               │
│  │          │           │           │          │               │
│  └──────────┴───────────┼───────────┴──────────┘               │
│                         │                                        │
│  ┌──────────────────────┴───────────────────────────────────┐   │
│  │                    动态评分引擎                            │   │
│  │  tool | creative | research | infrastructure (类型权重)    │   │
│  │  expansion | stability | consolidation (生态上下文)        │   │
│  └──────────────────────┬───────────────────────────────────┘   │
│                         │                                        │
│  ┌──────────┬───────────┼───────────┬──────────┐               │
│  │          │           │           │          │               │
│  ▼          ▼           ▼           ▼          ▼               │
│ ┌────┐  ┌────┐    ┌────────┐   ┌────┐   ┌────────┐           │
│ │Reviv│  │Comm│    │Defense │   │Anti│   │Report │           │
│ │al   │  │unit│    │Gen     │   │Ent.│   │Engine │           │
│ └────┘  └────┘    └────────┘   └────┘   └────────┘           │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

## 核心组件

### 1. 柔性标签系统

取代硬性四层分类，每个技能可拥有多个标签：

```python
# 标签类型
ACTIVE_TAGS = ["hot", "warm", "cold", "dormant"]      # 活跃度
VALUE_TAGS = ["unique", "potential", "core"]           # 价值
STATUS_TAGS = ["healthy", "degraded", "broken", "review"]  # 状态
LIFECYCLE_TAGS = ["incubating", "mature", "legacy"]    # 生命周期
DOMAIN_TAGS = ["creative", "devops", "research", "productivity", "gaming"]
```

**vs v3.0 硬性分层：**
- v3.0：技能只能属于一个层（hot/normal/seed/isolation）
- v4.0：技能可同时拥有多个标签（如 `hot + unique + healthy + mature`）
- 优势：避免边界跳跃，支持多维度检索，更精细的管理

### 2. 动态评分引擎

```python
class DynamicScorer:
    # 类型权重模板
    TYPE_PROFILES = {
        "tool":          {"activity": 0.30, "robustness": 0.25, ...},
        "creative":      {"uniqueness": 0.30, "completeness": 0.20, ...},
        "research":      {"uniqueness": 0.25, "adaptability": 0.20, ...},
        "infrastructure": {"robustness": 0.30, "relationship": 0.20, ...},
    }

    # 生态上下文调整
    ECOSYSTEM_FACTORS = {
        "expansion":     {"uniqueness": 1.5, "activity": 0.8},
        "stability":     {"robustness": 1.3, "activity": 1.2},
        "consolidation": {"relationship": 1.4, "completeness": 1.3},
    }
```

**vs v3.0 固定权重：**
- v3.0：活跃度永远25%，独特性永远10%
- v4.0：创意型技能的独特性权重提升到30%，工具型的活跃度提升到30%
- 优势：避免马太效应，鼓励多样性

### 3. 归档深冻层

解决"僵尸技能"堆积问题：

```python
class ArchiveLayer:
    def freeze(self, skill, reason):
        """冻结：保存元数据，释放运行时资源"""

    def can_revive(self, skill_name):
        """检查：冷冻>30天 且 复活次数<3"""

    def attempt_revival(self, skill_name, test_context):
        """复活：在特定场景中测试"""
```

**vs v3.0 隔离层：**
- v3.0：隔离层无限堆积，无清理机制
- v4.0：超过90天未使用的技能自动归档，保留元数据但释放资源
- 优势：控制运行时开销，同时保留复活可能性

### 4. 复兴引擎

```python
class RevivalEngine:
    def discover_revival_candidates(self, all_skills, archive):
        """发现：高独特性但长期休眠的技能"""

    def schedule_revival_test(self, candidate, test_scenarios):
        """测试：在特定场景中验证技能价值"""
```

### 5. 社区共识治理

```python
class CommunityGovernance:
    def submit_proposal(self, type, skill, reason):
        """提交RFC提案"""

    def vote(self, proposal_id, voter, direction):
        """投票：3票通过"""
```

## 数据流 v4.0

```
扫描技能
    ↓
分配标签（柔性分类）
    ↓
动态评分（类型+上下文感知）
    ↓
柔性分层（标签组合+软阈值）
    ↓
归档检查（僵尸技能 → 归档深冻）
    ↓
复兴检查（休眠技能 → 复兴测试）
    ↓
生成辩护（隔离层技能）
    ↓
提交RFC（重大变更）
    ↓
输出报告
```

## vs v3.0 架构对比

| 维度 | v3.0 | v4.0 |
|------|------|------|
| 分类 | 硬性四层 | 柔性标签+软分层 |
| 评分 | 固定权重 | 动态权重（类型+上下文） |
| 保护 | 被动存储 | 主动活化+复兴测试 |
| 清理 | 无（无限堆积） | 归档深冻+元数据保存 |
| 治理 | 中心化审批 | 社区共识+RFC |
| 状态 | 单一状态 | 多标签并存 |

## 配置参数

```yaml
librarian:
  version: "4.0"
  ecosystem_context: "stability"

  tags:
    hot: { max_days: 7, min_uses: 10 }
    warm: { max_days: 30, min_uses: 3 }
    dormant: { min_days: 90 }
    unique: { min_score: 0.8 }
    potential: { min_score: 0.7 }
    core: { min_in_degree: 5 }

  archive:
    freeze_after_days: 90
    max_revival_attempts: 3

  revival:
    interval_days: 30
    max_per_cycle: 5
    min_uniqueness: 0.6

  governance:
    votes_to_pass: 3
```
