# Hermes 技能生态园丁系统

> 不是刽子手，是园丁。

## 系统概述

Hermes Skill Curation 是技能生态系统的核心管理模块，负责评估、分类和维护技能库。

## 核心原则

1. **你不是刽子手，是园丁** - 目标是维护生态健康，不是最小化技能数
2. **保护多样性** - 随机保留5-10%低分技能
3. **对抗性辩护** - 对每个拟删除技能生成辩护理由
4. **人类审批** - 所有删除需用户批准

## 六维评分体系

```python
class SkillScorer:
    """技能评分器"""
    
    def __init__(self):
        self.weights = {
            "activity": 0.25,
            "relationship": 0.20,
            "completeness": 0.15,
            "robustness": 0.20,
            "adaptability": 0.10,
            "uniqueness": 0.10,
        }
    
    def calculate_score(self, skill, context=None):
        """计算综合评分"""
        scores = {
            "activity": self.activity_score(skill),
            "relationship": self.relationship_score(skill),
            "completeness": self.completeness_score(skill),
            "robustness": self.robustness_score(skill),
            "adaptability": self.adaptability_score(skill),
            "uniqueness": self.uniqueness_score(skill),
        }
        
        # 根据上下文调整权重
        weights = self.adjust_weights(context)
        
        # 计算加权平均
        total = sum(scores[dim] * weights[dim] for dim in scores)
        
        return total, scores
    
    def activity_score(self, skill):
        """活跃度评分"""
        import math
        
        days_since_used = skill.get("days_since_used", 365)
        use_count = skill.get("use_count", 0)
        
        # 时间衰减（半衰期7天）
        time_decay = math.exp(-0.1 * days_since_used)
        
        # 调用频率分级
        if use_count >= 50:
            frequency_score = 100
        elif use_count >= 20:
            frequency_score = 80
        elif use_count >= 10:
            frequency_score = 60
        elif use_count >= 3:
            frequency_score = 40
        elif use_count >= 1:
            frequency_score = 20
        else:
            frequency_score = 0
        
        return frequency_score * time_decay
    
    def relationship_score(self, skill):
        """关系度评分"""
        in_degree = skill.get("in_degree", 0)
        out_degree = skill.get("out_degree", 0)
        
        # 归一化（假设最大度数为20）
        max_degree = 20
        normalized = (in_degree * 0.7 + out_degree * 0.3) / max_degree
        
        return min(normalized * 100, 100)
    
    def completeness_score(self, skill):
        """完整度评分"""
        required_fields = ["name", "description", "version", "author", 
                          "triggers", "prerequisites", "content"]
        optional_fields = ["tags", "related_skills", "examples", 
                          "pitfalls", "references"]
        
        # 计算必填字段完整率
        required_complete = sum(1 for f in required_fields if skill.get(f))
        required_rate = required_complete / len(required_fields)
        
        # 计算选填字段完整率
        optional_complete = sum(1 for f in optional_fields if skill.get(f))
        optional_rate = optional_complete / len(optional_fields)
        
        return (required_rate * 0.7 + optional_rate * 0.3) * 100
    
    def robustness_score(self, skill):
        """稳健度评分"""
        total_executions = skill.get("total_executions", 0)
        successful_executions = skill.get("successful_executions", 0)
        
        if total_executions == 0:
            return 50  # 默认50%
        
        success_rate = successful_executions / total_executions
        
        # 考虑最近表现
        recent_success_rate = skill.get("recent_success_rate", success_rate)
        
        # 综合评分
        return (success_rate * 0.4 + recent_success_rate * 0.6) * 100
    
    def adaptability_score(self, skill):
        """适应度评分"""
        factors = {
            "platform_compatibility": 0.3,
            "dependency_availability": 0.3,
            "resource_requirements": 0.2,
            "version_compatibility": 0.2,
        }
        
        scores = {}
        for factor, weight in factors.items():
            scores[factor] = skill.get(f"{factor}_score", 0.5) * weight
        
        return sum(scores.values()) * 100
    
    def uniqueness_score(self, skill):
        """独特性评分"""
        functional_uniqueness = skill.get("functional_uniqueness", 0.5)
        implementation_uniqueness = skill.get("implementation_uniqueness", 0.5)
        
        return (functional_uniqueness * 0.6 + implementation_uniqueness * 0.4) * 100
    
    def adjust_weights(self, context):
        """根据上下文调整权重"""
        if context == "maintenance":
            return {
                "activity": 0.15,
                "relationship": 0.15,
                "completeness": 0.25,
                "robustness": 0.25,
                "adaptability": 0.10,
                "uniqueness": 0.10,
            }
        elif context == "discovery":
            return {
                "activity": 0.10,
                "relationship": 0.15,
                "completeness": 0.15,
                "robustness": 0.15,
                "adaptability": 0.15,
                "uniqueness": 0.30,
            }
        else:
            return self.weights
```

## 四层分类系统

```python
class SkillClassifier:
    """技能分类器"""
    
    def __init__(self):
        self.layers = {
            "hot": {"max_days": 7, "min_uses": 10, "min_success_rate": 0.9},
            "normal": {"max_days": 30, "min_uses": 3, "min_success_rate": 0.7},
            "seed": {"min_potential": 0.7, "min_uniqueness": 0.8},
            "isolation": {},  # 特殊条件
        }
    
    def classify(self, skill, total_score):
        """分类技能到对应层级"""
        
        # 检查是否需要隔离
        if self.needs_isolation(skill):
            return "isolation"
        
        # 检查是否为热气层
        if self.is_hot_layer(skill):
            return "hot"
        
        # 检查是否为常驻层
        if self.is_normal_layer(skill):
            return "normal"
        
        # 检查是否为种子库
        if self.is_seed_bank(skill):
            return "seed"
        
        # 默认到隔离层
        return "isolation"
    
    def needs_isolation(self, skill):
        """检查是否需要隔离"""
        return (
            skill.get("has_errors", False) or
            skill.get("is_duplicate", False) or
            skill.get("is_outdated", False) or
            skill.get("needs_review", False)
        )
    
    def is_hot_layer(self, skill):
        """检查是否为热气层"""
        return (
            skill.get("days_since_used", 999) <= self.layers["hot"]["max_days"] and
            skill.get("use_count", 0) >= self.layers["hot"]["min_uses"] and
            skill.get("success_rate", 0) >= self.layers["hot"]["min_success_rate"]
        )
    
    def is_normal_layer(self, skill):
        """检查是否为常驻层"""
        return (
            skill.get("days_since_used", 999) <= self.layers["normal"]["max_days"] and
            skill.get("use_count", 0) >= self.layers["normal"]["min_uses"] and
            skill.get("success_rate", 0) >= self.layers["normal"]["min_success_rate"]
        )
    
    def is_seed_bank(self, skill):
        """检查是否为种子库"""
        return (
            skill.get("potential_value", 0) >= self.layers["seed"]["min_potential"] or
            skill.get("uniqueness_score", 0) >= self.layers["seed"]["min_uniqueness"]
        )
```

## 反熵保护机制

```python
class AntiEntropyProtector:
    """反熵保护器"""
    
    def __init__(self):
        self.protection_rate = (0.05, 0.10)  # 5-10%
        self.min_protected = 3
    
    def protect(self, skills):
        """应用反熵保护"""
        # 找出所有低分技能（评分<50）
        low_score_skills = [s for s in skills if s.get("total_score", 0) < 50]
        
        if not low_score_skills:
            return []
        
        # 计算保护数量
        import random
        protection_rate = random.uniform(*self.protection_rate)
        protected_count = max(self.min_protected, 
                            int(len(low_score_skills) * protection_rate))
        
        # 优先保护有潜在价值的
        protected = []
        for skill in low_score_skills:
            if (skill.get("potential_value", 0) >= 0.7 or
                skill.get("uniqueness_score", 0) >= 0.8 or
                skill.get("has_user_dependency", False)):
                protected.append(skill)
        
        # 补充随机保护
        remaining = [s for s in low_score_skills if s not in protected]
        if len(protected) < protected_count and remaining:
            additional = random.sample(remaining, 
                                     min(protected_count - len(protected), 
                                         len(remaining)))
            protected.extend(additional)
        
        return protected
```

## 对抗性辩护系统

```python
class DefenseGenerator:
    """辩护理由生成器"""
    
    def generate_defense(self, skill):
        """生成辩护理由"""
        defense = {
            "scenario_usage": self.analyze_scenario_usage(skill),
            "future_potential": self.analyze_future_potential(skill),
            "unique_value": self.analyze_unique_value(skill),
            "user_dependency": self.analyze_user_dependency(skill),
            "irreversible_loss": self.analyze_irreversible_loss(skill),
        }
        
        # 生成总结
        defense["summary"] = self.generate_summary(defense)
        
        return defense
    
    def analyze_scenario_usage(self, skill):
        """分析使用场景"""
        scenarios = []
        
        # 基于技能内容分析可能的使用场景
        content = skill.get("content", "").lower()
        
        if "test" in content or "debug" in content:
            scenarios.append("测试和调试场景")
        if "deploy" in content or "install" in content:
            scenarios.append("部署和安装场景")
        if "monitor" in content or "check" in content:
            scenarios.append("监控和检查场景")
        
        return scenarios if scenarios else ["未知场景"]
    
    def analyze_future_potential(self, skill):
        """分析未来潜力"""
        potential_indicators = []
        
        # 基于标签分析
        tags = skill.get("tags", [])
        if any(tag in ["ai", "machine-learning", "deep-learning"] for tag in tags):
            potential_indicators.append("AI/ML相关，技术发展中")
        if any(tag in ["cloud", "kubernetes", "docker"] for tag in tags):
            potential_indicators.append("云原生相关，持续重要")
        
        return potential_indicators if potential_indicators else ["潜力未知"]
    
    def analyze_unique_value(self, skill):
        """分析独特价值"""
        uniqueness = skill.get("uniqueness_score", 0)
        
        if uniqueness >= 80:
            return "高度独特，难以替代"
        elif uniqueness >= 60:
            return "中等独特，有一定替代方案"
        else:
            return "高度可替代"
    
    def analyze_user_dependency(self, skill):
        """分析用户依赖"""
        dependency_count = skill.get("dependency_count", 0)
        
        if dependency_count >= 10:
            return f"被{dependency_count}个用户依赖，删除影响大"
        elif dependency_count >= 3:
            return f"被{dependency_count}个用户依赖，删除有影响"
        elif dependency_count >= 1:
            return f"被{dependency_count}个用户依赖，删除有轻微影响"
        else:
            return "无用户依赖"
    
    def analyze_irreversible_loss(self, skill):
        """分析不可逆损失"""
        loss_factors = []
        
        if skill.get("is_unique", False):
            loss_factors.append("独特功能永久丢失")
        if skill.get("has_custom_data", False):
            loss_factors.append("自定义数据丢失")
        if skill.get("integration_dependencies", []):
            loss_factors.append("集成关系断裂")
        
        return loss_factors if loss_factors else ["无可逆损失"]
    
    def generate_summary(self, defense):
        """生成辩护总结"""
        positive_factors = []
        
        if defense["scenario_usage"] != ["未知场景"]:
            positive_factors.append("有明确使用场景")
        if defense["future_potential"] != ["潜力未知"]:
            positive_factors.append("有未来潜力")
        if defense["unique_value"] in ["高度独特，难以替代", "中等独特，有一定替代方案"]:
            positive_factors.append("具有一定独特性")
        if "影响大" in defense["user_dependency"] or "影响" in defense["user_dependency"]:
            positive_factors.append("有用户依赖")
        
        if positive_factors:
            return f"建议保留：{', '.join(positive_factors)}"
        else:
            return "建议删除：无明显保留价值"
```

## 评估流程

```python
class SkillEvaluator:
    """技能评估器"""
    
    def __init__(self):
        self.scorer = SkillScorer()
        self.classifier = SkillClassifier()
        self.protector = AntiEntropyProtector()
        self.defense_generator = DefenseGenerator()
    
    def evaluate(self, skills):
        """评估所有技能"""
        results = []
        
        for skill in skills:
            # 评分
            total_score, dimension_scores = self.scorer.calculate_score(skill)
            
            # 分类
            layer = self.classifier.classify(skill, total_score)
            
            # 生成辩护（如果需要）
            defense = None
            if layer == "isolation" and total_score < 50:
                defense = self.defense_generator.generate_defense(skill)
            
            results.append({
                "skill_name": skill.get("name"),
                "total_score": total_score,
                "dimension_scores": dimension_scores,
                "layer": layer,
                "defense": defense,
                "recommended_action": self.get_recommended_action(layer, total_score),
            })
        
        # 应用反熵保护
        protected = self.protector.protect(results)
        for skill_result in protected:
            skill_result["anti_entropy_protected"] = True
        
        return results
    
    def get_recommended_action(self, layer, score):
        """获取建议操作"""
        if layer == "hot":
            return "keep"
        elif layer == "normal":
            return "keep"
        elif layer == "seed":
            return "keep"
        elif layer == "isolation":
            if score < 20:
                return "delete_candidate"
            elif score < 40:
                return "probation"
            else:
                return "review"
        else:
            return "unknown"
```

## 使用示例

```python
# 初始化评估器
evaluator = SkillEvaluator()

# 加载技能数据
skills = load_skills_from_directory("~/.hermes/skills/")

# 执行评估
results = evaluator.evaluate(skills)

# 输出报告
for result in results:
    print(f"技能: {result['skill_name']}")
    print(f"评分: {result['total_score']:.1f}")
    print(f"层级: {result['layer']}")
    print(f"建议: {result['recommended_action']}")
    if result.get('defense'):
        print(f"辩护: {result['defense']['summary']}")
    print("---")
```

## 配置参数

```yaml
curation:
  # 评分权重
  scoring_weights:
    activity: 0.25
    relationship: 0.20
    completeness: 0.15
    robustness: 0.20
    adaptability: 0.10
    uniqueness: 0.10
  
  # 层级阈值
  layer_thresholds:
    hot_layer:
      max_days: 7
      min_uses: 10
      min_success_rate: 0.9
    normal_layer:
      max_days: 30
      min_uses: 3
      min_success_rate: 0.7
    seed_bank:
      min_potential: 0.7
      min_uniqueness: 0.8
  
  # 反熵保护
  anti_entropy:
    min_protection_rate: 0.05
    max_protection_rate: 0.10
    min_protected_count: 3
  
  # 辩护配置
  defense:
    enable_scenario_analysis: true
    enable_future_analysis: true
    enable_dependency_analysis: true
```

## 参考资料

- `docs/architecture.md` - 架构设计文档
- `docs/scoring-system.md` - 评分体系详解
- `references/evaluation-example.json` - 评估示例
