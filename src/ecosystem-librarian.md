# Hermes 技能生态图书管理员

> 图书管理员不烧书，园丁不灭种，审计员不执刑。

## 系统概述

Hermes Skill Ecosystem Librarian 是技能生态系统的高级管理模块，建立在园丁系统之上，提供四层架构的分类管理能力。

## 核心理念

### 三不原则
1. **图书管理员不烧书** - 保留所有技能，分类管理
2. **园丁不灭种** - 保护低频但有价值的技能
3. **审计员不执刑** - 只建议，不删除

### 管理哲学
- **分类优于删除** - 通过分类组织管理，而非简单删除
- **保护多样性** - 维护生态系统的丰富性
- **渐进式优化** - 逐步改进，不激进变革

## 四层架构

### 架构图
```
┌─────────────────────────────────────────────────────────┐
│                  技能生态图书管理系统                       │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌─────────────────────────────────────────────────┐   │
│  │                  热气层 (Hot)                     │   │
│  │  • 最近7天使用  • 高频调用  • 核心功能            │   │
│  └─────────────────────────────────────────────────┘   │
│                                                          │
│  ┌─────────────────────────────────────────────────┐   │
│  │                  常驻层 (Normal)                  │   │
│  │  • 30天内使用  • 稳定调用  • 功能完整            │   │
│  └─────────────────────────────────────────────────┘   │
│                                                          │
│  ┌─────────────────────────────────────────────────┐   │
│  │                  种子库 (Seed Bank)               │   │
│  │  • 潜在价值  • 独特功能  • 低频但保留            │   │
│  └─────────────────────────────────────────────────┘   │
│                                                          │
│  ┌─────────────────────────────────────────────────┐   │
│  │                  隔离层 (Isolation)               │   │
│  │  • 待评估  • 有问题  • 重复或过时                │   │
│  └─────────────────────────────────────────────────┘   │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## 层级管理器

```python
class LayerManager:
    """层级管理器"""
    
    def __init__(self):
        self.layers = {
            "hot": HotLayer(),
            "normal": NormalLayer(),
            "seed": SeedBank(),
            "isolation": IsolationLayer(),
        }
    
    def get_layer(self, layer_name):
        """获取指定层级"""
        return self.layers.get(layer_name)
    
    def list_all_layers(self):
        """列出所有层级"""
        return {name: layer.get_info() for name, layer in self.layers.items()}
    
    def move_skill(self, skill, from_layer, to_layer):
        """移动技能到指定层级"""
        source = self.layers.get(from_layer)
        target = self.layers.get(to_layer)
        
        if source and target:
            source.remove_skill(skill)
            target.add_skill(skill)
            return True
        return False


class HotLayer:
    """热气层管理"""
    
    def __init__(self):
        self.skills = []
        self.criteria = {
            "max_days_since_used": 7,
            "min_use_count": 10,
            "min_success_rate": 0.9,
        }
    
    def add_skill(self, skill):
        """添加技能到热气层"""
        if self.meets_criteria(skill):
            self.skills.append(skill)
            return True
        return False
    
    def remove_skill(self, skill):
        """从热气层移除技能"""
        if skill in self.skills:
            self.skills.remove(skill)
            return True
        return False
    
    def meets_criteria(self, skill):
        """检查是否满足热气层标准"""
        return (
            skill.get("days_since_used", 999) <= self.criteria["max_days_since_used"] and
            skill.get("use_count", 0) >= self.criteria["min_use_count"] and
            skill.get("success_rate", 0) >= self.criteria["min_success_rate"]
        )
    
    def get_info(self):
        """获取层级信息"""
        return {
            "name": "hot",
            "display_name": "热气层",
            "skill_count": len(self.skills),
            "criteria": self.criteria,
            "skills": [s.get("name") for s in self.skills],
        }


class NormalLayer:
    """常驻层管理"""
    
    def __init__(self):
        self.skills = []
        self.criteria = {
            "max_days_since_used": 30,
            "min_use_count": 3,
            "min_success_rate": 0.7,
        }
    
    def add_skill(self, skill):
        """添加技能到常驻层"""
        if self.meets_criteria(skill):
            self.skills.append(skill)
            return True
        return False
    
    def remove_skill(self, skill):
        """从常驻层移除技能"""
        if skill in self.skills:
            self.skills.remove(skill)
            return True
        return False
    
    def meets_criteria(self, skill):
        """检查是否满足常驻层标准"""
        return (
            skill.get("days_since_used", 999) <= self.criteria["max_days_since_used"] and
            skill.get("use_count", 0) >= self.criteria["min_use_count"] and
            skill.get("success_rate", 0) >= self.criteria["min_success_rate"]
        )
    
    def get_info(self):
        """获取层级信息"""
        return {
            "name": "normal",
            "display_name": "常驻层",
            "skill_count": len(self.skills),
            "criteria": self.criteria,
            "skills": [s.get("name") for s in self.skills],
        }


class SeedBank:
    """种子库管理"""
    
    def __init__(self):
        self.skills = []
        self.criteria = {
            "min_potential_value": 0.7,
            "min_uniqueness_score": 0.8,
        }
    
    def add_skill(self, skill):
        """添加技能到种子库"""
        if self.meets_criteria(skill):
            self.skills.append(skill)
            return True
        return False
    
    def remove_skill(self, skill):
        """从种子库移除技能"""
        if skill in self.skills:
            self.skills.remove(skill)
            return True
        return False
    
    def meets_criteria(self, skill):
        """检查是否满足种子库标准"""
        return (
            skill.get("potential_value", 0) >= self.criteria["min_potential_value"] or
            skill.get("uniqueness_score", 0) >= self.criteria["min_uniqueness_score"]
        )
    
    def get_info(self):
        """获取层级信息"""
        return {
            "name": "seed",
            "display_name": "种子库",
            "skill_count": len(self.skills),
            "criteria": self.criteria,
            "skills": [s.get("name") for s in self.skills],
        }


class IsolationLayer:
    """隔离层管理"""
    
    def __init__(self):
        self.skills = []
        self.reasons = {}
    
    def add_skill(self, skill, reason="待评估"):
        """添加技能到隔离层"""
        self.skills.append(skill)
        self.reasons[skill.get("name")] = reason
        return True
    
    def remove_skill(self, skill):
        """从隔离层移除技能"""
        if skill in self.skills:
            self.skills.remove(skill)
            skill_name = skill.get("name")
            if skill_name in self.reasons:
                del self.reasons[skill_name]
            return True
        return False
    
    def get_reason(self, skill):
        """获取隔离原因"""
        return self.reasons.get(skill.get("name"), "未知")
    
    def get_info(self):
        """获取层级信息"""
        return {
            "name": "isolation",
            "display_name": "隔离层",
            "skill_count": len(self.skills),
            "skills": [
                {"name": s.get("name"), "reason": self.get_reason(s)}
                for s in self.skills
            ],
        }
```

## 技能流转引擎

```python
class SkillFlowEngine:
    """技能流转引擎"""
    
    def __init__(self, layer_manager):
        self.layer_manager = layer_manager
    
    def evaluate_and_flow(self, skill):
        """评估并流转技能"""
        # 计算评分
        scorer = SkillScorer()
        total_score, dimension_scores = scorer.calculate_score(skill)
        
        # 确定目标层级
        target_layer = self.determine_target_layer(skill, total_score)
        
        # 获取当前层级
        current_layer = skill.get("current_layer")
        
        # 如果需要流转
        if current_layer != target_layer:
            self.flow_skill(skill, current_layer, target_layer)
        
        return {
            "skill_name": skill.get("name"),
            "total_score": total_score,
            "current_layer": current_layer,
            "target_layer": target_layer,
            "flowed": current_layer != target_layer,
        }
    
    def determine_target_layer(self, skill, total_score):
        """确定目标层级"""
        classifier = SkillClassifier()
        return classifier.classify(skill, total_score)
    
    def flow_skill(self, skill, from_layer, to_layer):
        """流转技能"""
        if from_layer:
            self.layer_manager.move_skill(skill, from_layer, to_layer)
        else:
            # 新技能，直接添加到目标层级
            target = self.layer_manager.get_layer(to_layer)
            if target:
                target.add_skill(skill)
        
        # 更新技能的当前层级
        skill["current_layer"] = to_layer
    
    def batch_flow(self, skills):
        """批量流转技能"""
        results = []
        for skill in skills:
            result = self.evaluate_and_flow(skill)
            results.append(result)
        return results
```

## 图书管理员主类

```python
class SkillEcosystemLibrarian:
    """技能生态图书管理员"""
    
    def __init__(self):
        self.layer_manager = LayerManager()
        self.flow_engine = SkillFlowEngine(self.layer_manager)
        self.defense_generator = DefenseGenerator()
        self.anti_entropy_protector = AntiEntropyProtector()
    
    def organize(self, skills):
        """组织技能到四层架构"""
        results = []
        
        for skill in skills:
            # 评估并流转
            flow_result = self.flow_engine.evaluate_and_flow(skill)
            
            # 生成辩护（如果需要）
            defense = None
            if flow_result["target_layer"] == "isolation":
                defense = self.defense_generator.generate_defense(skill)
            
            results.append({
                **flow_result,
                "defense": defense,
            })
        
        return results
    
    def get_ecosystem_status(self):
        """获取生态系统状态"""
        layers = self.layer_manager.list_all_layers()
        
        total_skills = sum(layer["skill_count"] for layer in layers.values())
        
        return {
            "total_skills": total_skills,
            "layers": layers,
            "distribution": {
                name: {
                    "count": layer["skill_count"],
                    "percentage": (layer["skill_count"] / total_skills * 100) 
                                 if total_skills > 0 else 0,
                }
                for name, layer in layers.items()
            },
        }
    
    def generate_report(self, skills):
        """生成评估报告"""
        # 组织技能
        organization_results = self.organize(skills)
        
        # 获取状态
        status = self.get_ecosystem_status()
        
        # 生成报告
        report = {
            "summary": {
                "total_skills": status["total_skills"],
                "organization_results": len(organization_results),
                "layer_distribution": status["distribution"],
            },
            "details": organization_results,
            "recommendations": self.generate_recommendations(organization_results),
        }
        
        return report
    
    def generate_recommendations(self, results):
        """生成建议"""
        recommendations = []
        
        # 分析组织结果
        for result in results:
            if result["flowed"]:
                recommendations.append({
                    "type": "flow",
                    "skill": result["skill_name"],
                    "from": result["current_layer"],
                    "to": result["target_layer"],
                    "reason": f"评分 {result['total_score']:.1f}，符合 {result['target_layer']} 层标准",
                })
            
            if result.get("defense"):
                recommendations.append({
                    "type": "defense",
                    "skill": result["skill_name"],
                    "summary": result["defense"]["summary"],
                })
        
        return recommendations
```

## 使用示例

```python
# 初始化图书管理员
librarian = SkillEcosystemLibrarian()

# 加载技能
skills = load_skills_from_directory("~/.hermes/skills/")

# 组织技能
report = librarian.generate_report(skills)

# 输出报告
print("=== 技能生态系统报告 ===")
print(f"总技能数: {report['summary']['total_skills']}")
print()
print("层级分布:")
for layer, info in report['summary']['layer_distribution'].items():
    print(f"  {layer}: {info['count']} ({info['percentage']:.1f}%)")
print()
print("建议:")
for rec in report['recommendations']:
    print(f"  - {rec['type']}: {rec['skill']}")
    if 'reason' in rec:
        print(f"    原因: {rec['reason']}")
    if 'summary' in rec:
        print(f"    辩护: {rec['summary']}")
```

## 配置参数

```yaml
librarian:
  # 层级配置
  layers:
    hot:
      max_days_since_used: 7
      min_use_count: 10
      min_success_rate: 0.9
    normal:
      max_days_since_used: 30
      min_use_count: 3
      min_success_rate: 0.7
    seed:
      min_potential_value: 0.7
      min_uniqueness_score: 0.8
    isolation:
      enable_defense: true
  
  # 流转配置
  flow:
    enable_auto_flow: true
    flow_threshold: 0.1  # 分数变化超过10%才流转
  
  # 报告配置
  report:
    include_defense: true
    include_recommendations: true
    format: "json"  # json 或 markdown
```

## 最佳实践

1. **定期组织** - 每月执行一次完整组织
2. **监控流转** - 跟踪技能层级变化
3. **人工审核** - 定期审核隔离层技能
4. **文档更新** - 保持文档与代码同步
5. **反馈循环** - 收集用户反馈优化组织策略

## 参考资料

- `docs/architecture.md` - 架构设计文档
- `docs/evolution.md` - 演进历史
- `src/skill-curation.md` - 园丁系统实现
- `references/evaluation-example.json` - 评估示例
