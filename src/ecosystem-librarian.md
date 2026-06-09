# Hermes 技能生态图书管理员 v4.0

> 图书管理员不烧书，园丁不灭种，审计员不执刑。

## 系统概述

Hermes Skill Ecosystem Librarian v4.0 是技能生态系统的高级管理模块。基于多模型深度分析（Claude/DeepSeek/Qwen/GPT 四模型哲学讨论），从 v3.0 的静态四层架构演进为**动态标签+柔性分层+主动活化**的韧性生态系统。

### v4.0 核心改进（vs v3.0）

| 维度 | v3.0 | v4.0 |
|------|------|------|
| 评分权重 | 固定权重 | **上下文感知动态权重** |
| 分类方式 | 硬性四层 | **柔性标签+软分层** |
| 保护机制 | 被动存储 | **主动活化+技能复兴** |
| 生命周期 | 无 | **孵化→成熟→遗产 三阶段** |
| 治理模式 | 中心化审批 | **社区共识+RFC 流程** |

## 核心理念

### 三不原则（继承）
1. **图书管理员不烧书** - 保留所有技能，分类管理
2. **园丁不灭种** - 保护低频但有价值的技能
3. **审计员不执刑** - 只建议，不删除

### v4.0 新增原则
4. **韧性优先** - 系统设计以生态韧性为核心，非效率最大化
5. **动态适应** - 评分权重和分类标准随生态状态自调整
6. **主动活化** - 定期尝试复活休眠技能，验证其潜在价值

## 柔性标签系统

取代硬性四层分类，每个技能可拥有多个标签：

```python
class SkillTag:
    """技能标签系统 — 柔性分类取代硬性分层"""

    # 活跃度标签
    HOT = "hot"           # 7天内使用，≥10次
    WARM = "warm"         # 30天内使用，≥3次
    COLD = "cold"         # 超过30天未使用
    DORMANT = "dormant"   # 超过90天未使用

    # 价值标签
    UNIQUE = "unique"           # 独特性 ≥ 0.8
    HIGH_POTENTIAL = "potential" # 潜在价值 ≥ 0.7
    CORE = "core"               # 被 ≥5 个其他技能依赖

    # 状态标签
    HEALTHY = "healthy"     # 成功率 ≥ 90%
    DEGRADED = "degraded"   # 成功率 70-90%
    BROKEN = "broken"       # 成功率 < 70% 或有错误
    REVIEW = "review"       # 待审核

    # 生命周期标签
    INCUBATING = "incubating"   # 孵化期（<30天）
    MATURE = "mature"           # 成熟期
    LEGACY = "legacy"           # 遗产期（>180天未更新）

    # 领域标签（自动推断）
    CREATIVE = "creative"
    DEVOPS = "devops"
    RESEARCH = "research"
    PRODUCTIVITY = "productivity"
    GAMING = "gaming"
```

标签分配规则：
```python
def assign_tags(skill):
    """根据多维度数据为技能分配标签"""
    tags = set()

    # 活跃度标签
    days = skill.get("days_since_used", 999)
    uses = skill.get("use_count", 0)
    if days <= 7 and uses >= 10:
        tags.add(SkillTag.HOT)
    elif days <= 30 and uses >= 3:
        tags.add(SkillTag.WARM)
    elif days <= 90:
        tags.add(SkillTag.COLD)
    else:
        tags.add(SkillTag.DORMANT)

    # 价值标签
    if skill.get("uniqueness_score", 0) >= 0.8:
        tags.add(SkillTag.UNIQUE)
    if skill.get("potential_value", 0) >= 0.7:
        tags.add(SkillTag.HIGH_POTENTIAL)
    if skill.get("in_degree", 0) >= 5:
        tags.add(SkillTag.CORE)

    # 状态标签
    rate = skill.get("success_rate", 0.5)
    if rate >= 0.9:
        tags.add(SkillTag.HEALTHY)
    elif rate >= 0.7:
        tags.add(SkillTag.DEGRADED)
    else:
        tags.add(SkillTag.BROKEN)

    # 生命周期
    age_days = skill.get("age_days", 0)
    if age_days < 30:
        tags.add(SkillTag.INCUBATING)
    elif age_days > 180 and days > 60:
        tags.add(SkillTag.LEGACY)
    else:
        tags.add(SkillTag.MATURE)

    return tags
```

## 动态权重评分系统

取代固定权重，根据技能类型和生态上下文自动调整：

```python
class DynamicScorer:
    """上下文感知的动态评分器"""

    # 基础权重
    BASE_WEIGHTS = {
        "activity": 0.25,
        "relationship": 0.20,
        "completeness": 0.15,
        "robustness": 0.20,
        "adaptability": 0.10,
        "uniqueness": 0.10,
    }

    # 按技能类型的权重模板
    TYPE_PROFILES = {
        "tool": {  # 工具型：重视活跃度和稳健度
            "activity": 0.30,
            "relationship": 0.15,
            "completeness": 0.15,
            "robustness": 0.25,
            "adaptability": 0.10,
            "uniqueness": 0.05,
        },
        "creative": {  # 创意型：重视独特性和完整度
            "activity": 0.15,
            "relationship": 0.10,
            "completeness": 0.20,
            "robustness": 0.15,
            "adaptability": 0.10,
            "uniqueness": 0.30,
        },
        "research": {  # 研究型：重视独特性和适应度
            "activity": 0.10,
            "relationship": 0.15,
            "completeness": 0.15,
            "robustness": 0.15,
            "adaptability": 0.20,
            "uniqueness": 0.25,
        },
        "infrastructure": {  # 基础设施型：重视稳健度和适应度
            "activity": 0.20,
            "relationship": 0.20,
            "completeness": 0.15,
            "robustness": 0.30,
            "adaptability": 0.10,
            "uniqueness": 0.05,
        },
    }

    # 生态上下文调整因子
    ECOSYSTEM_FACTORS = {
        "expansion": {"uniqueness": 1.5, "activity": 0.8},   # 扩张期：鼓励多样性
        "stability": {"robustness": 1.3, "activity": 1.2},   # 稳定期：重视可靠性
        "consolidation": {"relationship": 1.4, "completeness": 1.3},  # 整合期：重视关联
    }

    def __init__(self, ecosystem_context="stability"):
        self.context = ecosystem_context

    def get_weights(self, skill_type="tool"):
        """获取动态权重"""
        # 基础权重
        weights = dict(self.TYPE_PROFILES.get(skill_type, self.BASE_WEIGHTS))

        # 应用生态上下文调整
        factors = self.ECOSYSTEM_FACTORS.get(self.context, {})
        for dim, factor in factors.items():
            if dim in weights:
                weights[dim] *= factor

        # 归一化
        total = sum(weights.values())
        return {k: v / total for k, v in weights.items()}

    def score(self, skill, skill_type="tool"):
        """计算动态评分"""
        weights = self.get_weights(skill_type)
        dimensions = {}
        dimensions["activity"] = self._activity_score(skill)
        dimensions["relationship"] = self._relationship_score(skill)
        dimensions["completeness"] = self._completeness_score(skill)
        dimensions["robustness"] = self._robustness_score(skill)
        dimensions["adaptability"] = self._adaptability_score(skill)
        dimensions["uniqueness"] = self._uniqueness_score(skill)

        total = sum(dimensions[d] * weights[d] for d in dimensions)
        return total, dimensions, weights

    def _activity_score(self, skill):
        import math
        days = skill.get("days_since_used", 365)
        uses = skill.get("use_count", 0)
        decay = math.exp(-0.1 * days)
        if uses >= 50: freq = 100
        elif uses >= 20: freq = 80
        elif uses >= 10: freq = 60
        elif uses >= 3: freq = 40
        elif uses >= 1: freq = 20
        else: freq = 0
        return freq * decay

    def _relationship_score(self, skill):
        in_d = skill.get("in_degree", 0)
        out_d = skill.get("out_degree", 0)
        return min((in_d * 0.7 + out_d * 0.3) / 20 * 100, 100)

    def _completeness_score(self, skill):
        required = ["name", "description", "version", "author",
                     "triggers", "prerequisites", "content"]
        optional = ["tags", "related_skills", "examples",
                     "pitfalls", "references"]
        r = sum(1 for f in required if skill.get(f)) / len(required)
        o = sum(1 for f in optional if skill.get(f)) / len(optional)
        return (r * 0.7 + o * 0.3) * 100

    def _robustness_score(self, skill):
        total = skill.get("total_executions", 0)
        success = skill.get("successful_executions", 0)
        if total == 0: return 50
        rate = success / total
        recent = skill.get("recent_success_rate", rate)
        return (rate * 0.4 + recent * 0.6) * 100

    def _adaptability_score(self, skill):
        factors = {"platform_compatibility": 0.3, "dependency_availability": 0.3,
                    "resource_requirements": 0.2, "version_compatibility": 0.2}
        return sum(skill.get(f"{k}_score", 0.5) * v for k, v in factors.items()) * 100

    def _uniqueness_score(self, skill):
        fu = skill.get("functional_uniqueness", 0.5)
        iu = skill.get("implementation_uniqueness", 0.5)
        return (fu * 0.6 + iu * 0.4) * 100
```

## 柔性分类引擎

取代硬性四层，基于标签组合+软阈值：

```python
class FlexibleClassifier:
    """柔性分类器 — 标签组合取代硬性分层"""

    def classify(self, skill, total_score, tags):
        """基于标签组合和评分的柔性分类"""
        # 硬性规则：有明确问题的直接隔离
        if SkillTag.BROKEN in tags or SkillTag.REVIEW in tags:
            return "isolation"

        # 软性规则：基于标签组合
        if SkillTag.HOT in tags and SkillTag.CORE in tags:
            return "hot"
        if SkillTag.WARM in tags and total_score >= 60:
            return "normal"
        if SkillTag.UNIQUE in tags or SkillTag.HIGH_POTENTIAL in tags:
            return "seed"
        if SkillTag.DORMANT in tags and total_score < 40:
            return "archive"  # 新增：归档深冻层

        # 默认：基于评分
        if total_score >= 80: return "hot"
        if total_score >= 60: return "normal"
        if total_score >= 40: return "seed"
        return "isolation"
```

## 归档深冻层（新增）

解决"僵尸技能"堆积问题：

```python
class ArchiveLayer:
    """归档深冻层 — 长期未使用技能的元数据保存"""

    def __init__(self):
        self.archived = {}  # name -> {metadata, code_hash, archived_at}

    def freeze(self, skill, reason="long_term_dormant"):
        """冻结技能：保存元数据，标记为归档"""
        self.archived[skill["name"]] = {
            "metadata": {k: v for k, v in skill.items() if k != "content"},
            "code_hash": skill.get("code_hash", ""),
            "archived_at": time.time(),
            "reason": reason,
            "revival_count": 0,
        }

    def can_revive(self, skill_name):
        """检查是否可以复活"""
        info = self.archived.get(skill_name)
        if not info: return False
        # 冷冻超过30天且复活次数<3 才可以尝试
        frozen_days = (time.time() - info["archived_at"]) / 86400
        return frozen_days > 30 and info["revival_count"] < 3

    def attempt_revival(self, skill_name, test_context):
        """尝试复活：在特定场景中测试技能"""
        info = self.archived.get(skill_name)
        if not info: return None
        info["revival_count"] += 1
        # 返回技能元数据供测试
        return info["metadata"]
```

## 主动活化引擎（新增）

定期尝试复活休眠技能：

```python
class RevivalEngine:
    """技能复兴引擎 — 主动验证休眠技能的潜在价值"""

    def __init__(self, revival_interval_days=30):
        self.interval = revival_interval_days
        self.revival_log = []

    def discover_revival_candidates(self, all_skills, archive):
        """发现可复活候选"""
        candidates = []
        for skill in all_skills:
            tags = assign_tags(skill)
            if SkillTag.DORMANT in tags and skill.get("uniqueness_score", 0) >= 0.6:
                if archive.can_revive(skill["name"]):
                    candidates.append({
                        "name": skill["name"],
                        "reason": "高独特性但长期休眠",
                        "uniqueness": skill.get("uniqueness_score", 0),
                        "last_used": skill.get("days_since_used", 999),
                    })
        return sorted(candidates, key=lambda x: -x["uniqueness"])

    def schedule_revival_test(self, candidate, test_scenarios):
        """安排复兴测试"""
        return {
            "skill": candidate["name"],
            "scenarios": test_scenarios,
            "expected_duration": "7天",
            "success_criteria": "在至少1个场景中成功执行",
        }
```

## 社区共识机制（新增）

取代纯中心化审批：

```python
class CommunityGovernance:
    """社区共识治理 — RFC 流程式的技能审核"""

    def __init__(self):
        self.proposals = []  # 提案列表
        self.votes = {}      # 技能名 -> {approve: N, reject: N, comments: []}

    def submit_proposal(self, proposal_type, skill_name, reason, proposer="system"):
        """提交提案"""
        proposal = {
            "id": len(self.proposals) + 1,
            "type": proposal_type,  # merge / archive / revive / delete
            "skill": skill_name,
            "reason": reason,
            "proposer": proposer,
            "status": "open",
            "created_at": time.time(),
            "votes": {"approve": 0, "reject": 0},
            "comments": [],
        }
        self.proposals.append(proposal)
        return proposal

    def vote(self, proposal_id, voter, direction, comment=""):
        """投票"""
        proposal = self.proposals[proposal_id - 1]
        if proposal["status"] != "open":
            return False
        proposal["votes"][direction] += 1
        if comment:
            proposal["comments"].append({"voter": voter, "comment": comment})
        # 3票通过
        if proposal["votes"]["approve"] >= 3:
            proposal["status"] = "approved"
        elif proposal["votes"]["reject"] >= 3:
            proposal["status"] = "rejected"
        return True
```

## 图书管理员主类 v4.0

```python
class SkillEcosystemLibrarianV4:
    """技能生态图书管理员 v4.0 — 韧性生态系统"""

    def __init__(self, ecosystem_context="stability"):
        self.scorer = DynamicScorer(ecosystem_context)
        self.classifier = FlexibleClassifier()
        self.archive = ArchiveLayer()
        self.revival = RevivalEngine()
        self.governance = CommunityGovernance()
        self.defense_gen = DefenseGenerator()

    def organize(self, skills, skill_types=None):
        """组织技能到柔性分类"""
        results = []
        for skill in skills:
            stype = (skill_types or {}).get(skill["name"], "tool")
            tags = assign_tags(skill)
            total_score, dimensions, weights = self.scorer.score(skill, stype)
            layer = self.classifier.classify(skill, total_score, tags)

            # 归档深冻
            if layer == "archive":
                self.archive.freeze(skill)
                continue

            # 生成辩护（隔离层）
            defense = None
            if layer == "isolation":
                defense = self.defense_gen.generate_defense(skill)

            results.append({
                "name": skill["name"],
                "total_score": total_score,
                "dimensions": dimensions,
                "weights_used": weights,
                "tags": list(tags),
                "layer": layer,
                "skill_type": stype,
                "defense": defense,
            })
        return results

    def run_revival_cycle(self, skills):
        """运行一轮复兴测试"""
        candidates = self.revival.discover_revival_candidates(skills, self.archive)
        revival_tests = []
        for c in candidates[:5]:  # 每轮最多5个
            test = self.revival.schedule_revival_test(c, ["auto_test"])
            revival_tests.append(test)
            # 自动提交RFC提案
            self.governance.submit_proposal(
                "revive", c["name"],
                f"高独特性({c['uniqueness']:.2f})但休眠{c['last_used']}天，建议复兴测试"
            )
        return revival_tests

    def generate_report(self, skills, skill_types=None):
        """生成完整评估报告"""
        results = self.organize(skills, skill_types)
        revival_tests = self.run_revival_cycle(skills)

        # 统计
        layer_counts = {}
        tag_counts = {}
        for r in results:
            layer_counts[r["layer"]] = layer_counts.get(r["layer"], 0) + 1
            for t in r["tags"]:
                tag_counts[t] = tag_counts.get(t, 0) + 1

        return {
            "version": "4.0",
            "total_skills": len(results),
            "layer_distribution": layer_counts,
            "tag_distribution": tag_counts,
            "archived_count": len(self.archive.archived),
            "revival_candidates": len(revival_tests),
            "open_proposals": len([p for p in self.governance.proposals if p["status"] == "open"]),
            "details": results,
            "revival_tests": revival_tests,
        }
```

## 配置参数 v4.0

```yaml
librarian:
  version: "4.0"
  ecosystem_context: "stability"  # expansion | stability | consolidation

  # 柔性标签阈值
  tags:
    hot:
      max_days: 7
      min_uses: 10
    warm:
      max_days: 30
      min_uses: 3
    dormant:
      min_days: 90
    unique:
      min_score: 0.8
    potential:
      min_score: 0.7
    core:
      min_in_degree: 5

  # 归档深冻
  archive:
    freeze_after_days: 90
    max_revival_attempts: 3
    min_frozen_days: 30

  # 复兴引擎
  revival:
    interval_days: 30
    max_per_cycle: 5
    min_uniqueness: 0.6

  # 社区治理
  governance:
    votes_to_pass: 3
    auto_propose: true

  # 评分上下文
  scoring:
    default_type: "tool"
    type_profiles:
      tool: { activity: 0.30, robustness: 0.25 }
      creative: { uniqueness: 0.30, completeness: 0.20 }
      research: { uniqueness: 0.25, adaptability: 0.20 }
      infrastructure: { robustness: 0.30, relationship: 0.20 }
```

## 最佳实践 v4.0

1. **定期组织** - 每月执行一次完整组织，每季度运行复兴测试
2. **标签审计** - 检查标签分布是否健康（避免过度集中）
3. **RFC 审核** - 重大变更（合并/归档）走社区共识流程
4. **复兴日志** - 跟踪复兴测试结果，优化复兴策略
5. **生态健康度** - 监控标签分布的多样性指数（Shannon Index）

## 参考资料

- `docs/architecture.md` - 架构设计文档
- `docs/evolution.md` - 演进历史（v1.0→v4.0）
- `docs/scoring-system.md` - 评分体系详解
- `src/skill-curation.md` - 园丁系统实现（v2.0）
- `references/evaluation-example.json` - 评估示例
